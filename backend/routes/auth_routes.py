import re
import datetime
import hashlib
import hmac
import secrets
import logging
from typing import Optional, Dict, Any
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.config import Config
from backend.database import get_db
from backend.models import User, OTPCode, TelegramAuthSession, CreditTransaction
from backend.auth import hash_password, verify_password, create_access_token, get_current_user
from backend.sms_service import SMSService

logger = logging.getLogger("tasvirlab.auth")

router = APIRouter(prefix="/api/auth", tags=["Autentifikatsiya"])

@router.get("/config", summary="Ommaviy autentifikatsiya sozlamalari")
async def get_auth_public_config():
    """Frontend uchun Google Client ID va Telegram bot nomini qaytaradi."""
    return {
        "google_client_id": Config.GOOGLE_CLIENT_ID or "",
        "telegram_bot_username": (Config.TELEGRAM_BOT_USERNAME or "").replace("@", "")
    }

def normalize_phone(phone: str) -> str:
    """Telefon raqamni toza xalqaro formatga keltiradi (masalan: +998901234567)."""
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("998") and len(digits) == 12:
        return f"+{digits}"
    elif len(digits) == 9:
        return f"+998{digits}"
    elif len(digits) >= 9:
        return f"+{digits}"
    return phone.strip()

# ==================== REQUEST SCHEMAS ====================

class SendOTPRequest(BaseModel):
    phone_number: str = Field(..., example="+998901234567", description="Tasdiqlash kodi yuboriladigan telefon raqami")
    purpose: Optional[str] = Field("login", description="Kod maqsadi: login, register, reset")

class VerifyOTPRequest(BaseModel):
    phone_number: str = Field(..., example="+998901234567")
    code: str = Field(..., example="123456", description="6 xonali SMS kod")
    full_name: Optional[str] = Field(None, example="Alisher Navoiy")
    device_id: Optional[str] = Field(None, description="Mobil qurilma unikal IDsi (anti-fraud)")

class SocialLoginRequest(BaseModel):
    provider: str = Field(..., example="google", description="google yoki apple")
    id_token: str = Field(..., description="Google/Apple tomonidan berilgan autentifikatsiya tokeni")
    email: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    device_id: Optional[str] = None

class FCMTokenRequest(BaseModel):
    fcm_token: str = Field(..., description="Firebase Cloud Messaging push bildirishnoma tokeni")

class TelegramWidgetAuthRequest(BaseModel):
    id: int = Field(..., description="Telegram foydalanuvchi unikal IDsi")
    first_name: str
    last_name: Optional[str] = ""
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str
    device_id: Optional[str] = None

class TelegramSessionRequest(BaseModel):
    device_id: Optional[str] = None

class TelegramSimulateConfirmRequest(BaseModel):
    auth_token: str
    telegram_id: str = "12345678"
    first_name: str = "Telegram Ota-ona"
    username: Optional[str] = "otaona_tg"
    phone_number: Optional[str] = "+998901112233"

class RegisterRequest(BaseModel):
    phone_number: str = Field(..., example="+998901234567", description="O'zbekiston yoki xalqaro telefon raqami")
    password: str = Field(..., min_length=6, description="Eng kamida 6 belgidan iborat parol")
    full_name: Optional[str] = Field(default="", example="Alisher Navoiy", description="Foydalanuvchi ismi")
    device_id: Optional[str] = Field(default="", description="Mobil qurilma unikal identifikatori")

class LoginRequest(BaseModel):
    phone_number: str = Field(..., example="+998901234567")
    password: str = Field(...)

class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

# ==================== OTP ENDPOINTS ====================

@router.post("/send-otp", summary="Telefon raqamga SMS tasdiqlash kodini yuborish")
async def send_otp(req: SendOTPRequest, db: Session = Depends(get_db)):
    clean_phone = normalize_phone(req.phone_number)
    if len(clean_phone) < 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telefon raqami noto'g'ri kiritildi."
        )

    # Avvalgi ishlatilmagan va muddati o'tmagan kodlarni bekor qilamiz
    db.query(OTPCode).filter(
        OTPCode.phone_number == clean_phone,
        OTPCode.is_used == False
    ).update({"is_used": True})

    # Yangi 6 xonali kod hosil qilamiz
    otp_code = SMSService.generate_otp_code(6)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=Config.OTP_EXPIRE_MINUTES)

    db_otp = OTPCode(
        phone_number=clean_phone,
        code=otp_code,
        purpose=req.purpose or "login",
        expires_at=expires_at,
        is_used=False
    )
    db.add(db_otp)
    db.commit()

    # SMS yuborish
    sms_text = f"TasvirLab: Tasdiqlash kodingiz - {otp_code}. Uni hech kimga bermang!"
    sms_res = await SMSService.send_sms(clean_phone, sms_text)

    response_payload = {
        "status": "success",
        "message": "Tasdiqlash kodi telefoningizga yuborildi.",
        "phone_number": clean_phone,
        "expires_in_minutes": Config.OTP_EXPIRE_MINUTES
    }
    
    return response_payload

@router.post("/verify-otp", summary="SMS kodni tekshirish va tizimga kirish (Avtomatik ro'yxatdan o'tish)")
async def verify_otp(req: VerifyOTPRequest, db: Session = Depends(get_db)):
    clean_phone = normalize_phone(req.phone_number)
    # Oxirgi faol OTP kodni tekshiramiz
    now = datetime.datetime.utcnow()
    db_otp = db.query(OTPCode).filter(
        OTPCode.phone_number == clean_phone,
        OTPCode.is_used == False,
        OTPCode.expires_at >= now
    ).order_by(OTPCode.created_at.desc()).first()

    if not db_otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tasdiqlash kodi topilmadi yoki muddati o'tgan. Qayta kod so'rang."
        )

    db_otp.attempts += 1
    if db_otp.attempts > 5:
        db_otp.is_used = True
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Urinishlar soni oshib ketdi. Yangi kod so'rang."
        )

    if db_otp.code != req.code.strip():
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tasdiqlash kodi xato kiritildi."
        )

    # Kod to'g'ri bo'lsa, uni ishlatilgan deb belgilaymiz
    db_otp.is_used = True

    # Foydalanuvchini qidiramiz yoki yangi yaratamiz
    user = db.query(User).filter(User.phone_number == clean_phone).first()
    is_new_user = False

    if not user:
        is_new_user = True
        free_credits = Config.INITIAL_FREE_CREDITS
        
        # Anti-fraud tekshiruvi: bitta qurilmadan ko'p marotaba ro'yxatdan o'tishni cheklash
        if req.device_id:
            existing_devices = db.query(User).filter(User.device_id == req.device_id).count()
            if existing_devices >= 2:
                free_credits = 0

        user = User(
            phone_number=clean_phone,
            full_name=req.full_name or "Foydalanuvchi",
            hashed_password=hash_password(secrets.token_urlsafe(32)),
            auth_provider="phone",
            credits_balance=free_credits,
            is_active=True,
            is_verified=True,
            device_id=req.device_id
        )
        db.add(user)
        db.flush()

        if free_credits > 0:
            welcome_tx = CreditTransaction(
                user_id=user.id,
                amount=free_credits,
                balance_after=free_credits,
                transaction_type="welcome_bonus",
                description=f"Xush kelibsiz bonusi: {free_credits} ta bepul video",
                payment_method="system_bonus"
            )
            db.add(welcome_tx)
    else:
        user.is_verified = True
        if req.full_name and (not user.full_name or user.full_name == "Foydalanuvchi"):
            user.full_name = req.full_name
        if req.device_id:
            user.device_id = req.device_id

    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": str(user.id), "phone": user.phone_number})

    return {
        "status": "success",
        "is_new_user": is_new_user,
        "message": "Xush kelibsiz!" if not is_new_user else "Muvaffaqiyatli ro'yxatdan o'tdingiz! 🎉",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }

@router.post("/demo-login", include_in_schema=False)
async def demo_login():
    """Demo kirish o'chirilgan."""
    raise HTTPException(
        status_code=403,
        detail="Demo kirish rejimi o'chirilgan. Iltimos, telefon raqam, Google yoki Telegram orqali tizimga kiring."
    )

# ==================== SOCIAL LOGIN ====================

@router.post("/social-login", summary="Google yoki Apple ID orqali kirish")
async def social_login(req: SocialLoginRequest, db: Session = Depends(get_db)):
    if req.provider not in ["google", "apple"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Qo'llab-quvvatlanmaydigan provayder."
        )

    # Haqiqiy Google token bo'lsa, Google API orqali tekshirish
    social_user_id = f"{req.provider}_{req.id_token[:24]}"
    
    if req.provider == "google" and req.id_token and len(req.id_token) > 30 and not req.id_token.startswith("google_token_"):
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                g_res = await client.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={req.id_token}")
                if g_res.status_code == 200:
                    g_data = g_res.json()
                    g_sub = g_data.get("sub")
                    if g_sub:
                        social_user_id = f"google_{g_sub}"
                    if g_data.get("email"):
                        req.email = g_data.get("email")
                    if g_data.get("name"):
                        req.full_name = g_data.get("name")
                    if g_data.get("picture"):
                        req.avatar_url = g_data.get("picture")
                    logger.info(f"Google OAuth tekshirildi: email={req.email}, sub={g_sub}")
        except Exception as e:
            logger.warning(f"Google tokeninfo xatolik: {e}")
    
    # Avval shu provider ID bo'yicha yoki email bo'yicha qidiramiz
    user = None
    if req.provider == "google":
        user = db.query(User).filter(User.google_id == social_user_id).first()
    elif req.provider == "apple":
        user = db.query(User).filter(User.apple_id == social_user_id).first()
        
    if not user and req.email:
        user = db.query(User).filter(User.email == req.email).first()

    is_new_user = False
    if not user:
        is_new_user = True
        free_credits = Config.INITIAL_FREE_CREDITS
        if req.device_id:
            if db.query(User).filter(User.device_id == req.device_id).count() >= 2:
                free_credits = 0

        user = User(
            phone_number=f"{req.provider}_{social_user_id}",
            email=req.email,
            full_name=req.full_name or "Foydalanuvchi",
            hashed_password=hash_password(secrets.token_urlsafe(32)),
            avatar_url=req.avatar_url,
            google_id=social_user_id if req.provider == "google" else None,
            apple_id=social_user_id if req.provider == "apple" else None,
            auth_provider=req.provider,
            credits_balance=free_credits,
            is_active=True,
            is_verified=True,
            device_id=req.device_id
        )
        db.add(user)
        db.flush()

        if free_credits > 0:
            welcome_tx = CreditTransaction(
                user_id=user.id,
                amount=free_credits,
                balance_after=free_credits,
                transaction_type="welcome_bonus",
                description=f"Xush kelibsiz bonusi: {free_credits} ta bepul video",
                payment_method="system_bonus"
            )
            db.add(welcome_tx)
    else:
        # Mavjud foydalanuvchining provider ID sini yangilaymiz
        if req.provider == "google" and not user.google_id:
            user.google_id = social_user_id
        elif req.provider == "apple" and not user.apple_id:
            user.apple_id = social_user_id
        if req.avatar_url:
            user.avatar_url = req.avatar_url

    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": str(user.id), "phone": user.phone_number or ""})

    return {
        "status": "success",
        "is_new_user": is_new_user,
        "message": f"{req.provider.capitalize()} orqali muvaffaqiyatli kirdingiz!",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }


# ==================== TELEGRAM AUTHENTICATION ====================

def verify_telegram_data(auth_dict: dict, bot_token: str) -> bool:
    """Telegram Login Widget yoki WebApp ma'lumotlarining haqiqiyligini HMAC-SHA256 orqali tekshirish."""
    if not bot_token:
        # Bot tokeni hali kiritilmagan bo'lsa, DEV rejimida sinov uchun ruxsat beramiz
        return Config.DEV_MODE

    received_hash = auth_dict.get("hash")
    if not received_hash:
        return False

    check_pairs = []
    for k in sorted(auth_dict.keys()):
        if k != "hash" and auth_dict[k] is not None:
            check_pairs.append(f"{k}={auth_dict[k]}")
    data_check_string = "\n".join(check_pairs)

    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()
    return calculated_hash == received_hash

@router.post("/telegram/widget-login", summary="Telegram Login Widget orqali darhol kirish")
async def telegram_widget_login(req: TelegramWidgetAuthRequest, db: Session = Depends(get_db)):
    auth_dict = req.dict(exclude={"device_id"})
    
    if not verify_telegram_data(auth_dict, Config.TELEGRAM_BOT_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telegram ma'lumotlari haqiqiy emas yoki ruxsatsiz o'zgartirilgan."
        )

    tg_id_str = str(req.id)
    user = db.query(User).filter(User.telegram_id == tg_id_str).first()
    is_new_user = False

    full_name = f"{req.first_name} {req.last_name or ''}".strip()

    if not user:
        is_new_user = True
        free_credits = Config.INITIAL_FREE_CREDITS
        if req.device_id:
            if db.query(User).filter(User.device_id == req.device_id).count() >= 2:
                free_credits = 0

        user = User(
            phone_number=f"tg_{tg_id_str}",
            telegram_id=tg_id_str,
            telegram_username=req.username,
            full_name=full_name or "Telegram Foydalanuvchi",
            hashed_password=hash_password(secrets.token_urlsafe(32)),
            avatar_url=req.photo_url,
            auth_provider="telegram",
            credits_balance=free_credits,
            is_active=True,
            is_verified=True,
            device_id=req.device_id
        )
        db.add(user)
        db.flush()

        if free_credits > 0:
            welcome_tx = CreditTransaction(
                user_id=user.id,
                amount=free_credits,
                balance_after=free_credits,
                transaction_type="welcome_bonus",
                description=f"Xush kelibsiz bonusi: {free_credits} ta bepul video",
                payment_method="system_bonus"
            )
            db.add(welcome_tx)
    else:
        user.telegram_username = req.username or user.telegram_username
        if req.photo_url:
            user.avatar_url = req.photo_url
        if full_name:
            user.full_name = full_name

    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": str(user.id), "phone": user.phone_number or ""})

    return {
        "status": "success",
        "is_new_user": is_new_user,
        "message": f"Telegram orqali xush kelibsiz, {user.full_name}! 🎉",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }

@router.post("/telegram/request-session", summary="Telegram Bot orqali 1-bosishda kirish sessiyasini yaratish (Deep Link)")
async def telegram_request_session(req: TelegramSessionRequest, db: Session = Depends(get_db)):
    auth_token = f"tg_auth_{secrets.token_urlsafe(16)}"
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    session_rec = TelegramAuthSession(
        auth_token=auth_token,
        status="pending",
        expires_at=expires_at
    )
    db.add(session_rec)
    db.commit()

    bot_username = Config.TELEGRAM_BOT_USERNAME.replace("@", "")
    deep_link = f"https://t.me/{bot_username}?start={auth_token}"

    return {
        "status": "success",
        "auth_token": auth_token,
        "deep_link": deep_link,
        "bot_username": bot_username,
        "expires_in_minutes": 10
    }

@router.get("/telegram/check-session/{auth_token}", summary="Telegram bot orqali kirish holatini tekshirish (Polling)")
async def telegram_check_session(auth_token: str, db: Session = Depends(get_db)):
    now = datetime.datetime.utcnow()
    session_rec = db.query(TelegramAuthSession).filter(
        TelegramAuthSession.auth_token == auth_token
    ).first()

    if not session_rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kirish sessiyasi topilmadi."
        )

    if session_rec.expires_at < now:
        session_rec.status = "expired"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kirish sessiyasining muddati tugagan. Qaytadan urinib ko'ring."
        )

    if session_rec.status == "pending":
        return {
            "status": "pending",
            "message": "Foydalanuvchi Telegram botda tasdiqlashi kutilmoqda..."
        }

    if session_rec.status == "confirmed" and session_rec.user_id:
        user = db.query(User).filter(User.id == session_rec.user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Foydalanuvchi faol emas."
            )

        access_token = create_access_token(data={"sub": str(user.id), "phone": user.phone_number or ""})

        return {
            "status": "confirmed",
            "message": f"Telegram orqali xush kelibsiz, {user.full_name}!",
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.to_dict()
        }

    return {"status": session_rec.status}

@router.post("/telegram/webhook", summary="Telegram Bot Webhook (Botdan /start qabul qilish)")
async def telegram_bot_webhook(update: Dict[str, Any], db: Session = Depends(get_db)):
    message = update.get("message") or {}
    text = message.get("text", "")
    from_user = message.get("from") or {}
    
    if text.startswith("/start tg_auth_"):
        auth_token = text.split()[1].strip()
        now = datetime.datetime.utcnow()
        session_rec = db.query(TelegramAuthSession).filter(
            TelegramAuthSession.auth_token == auth_token,
            TelegramAuthSession.status == "pending",
            TelegramAuthSession.expires_at >= now
        ).first()

        if session_rec:
            tg_id = str(from_user.get("id"))
            tg_username = from_user.get("username")
            full_name = f"{from_user.get('first_name', '')} {from_user.get('last_name', '')}".strip()

            user = db.query(User).filter(User.telegram_id == tg_id).first()
            if not user:
                free_credits = Config.INITIAL_FREE_CREDITS
                user = User(
                    phone_number=f"tg_{tg_id}",
                    telegram_id=tg_id,
                    telegram_username=tg_username,
                    full_name=full_name or "Telegram Foydalanuvchi",
                    hashed_password=hash_password(secrets.token_urlsafe(32)),
                    auth_provider="telegram",
                    credits_balance=free_credits,
                    is_active=True,
                    is_verified=True
                )
                db.add(user)
                db.flush()

                if free_credits > 0:
                    welcome_tx = CreditTransaction(
                        user_id=user.id,
                        amount=free_credits,
                        balance_after=free_credits,
                        transaction_type="welcome_bonus",
                        description=f"Xush kelibsiz bonusi: {free_credits} ta bepul video",
                        payment_method="system_bonus"
                    )
                    db.add(welcome_tx)
            else:
                if full_name and (not user.full_name or user.full_name == "Foydalanuvchi"):
                    user.full_name = full_name
                user.telegram_username = tg_username or user.telegram_username

            session_rec.status = "confirmed"
            session_rec.telegram_id = tg_id
            session_rec.telegram_username = tg_username
            session_rec.user_id = user.id
            db.commit()

            return {"ok": True, "message": "Tasdiqlandi"}

    return {"ok": True}

@router.post("/telegram/simulate-bot-confirm", include_in_schema=False)
async def telegram_simulate_confirm():
    """Telegram simulyatsiyasi o'chirilgan."""
    raise HTTPException(
        status_code=403,
        detail="Telegram simulyatsiyasi o'chirilgan. Faqat haqiqiy Telegram bot orqali tasdiqlash amal qiladi."
    )

# ==================== FCM PUSH NOTIFICATION ====================

@router.post("/update-fcm-token", summary="Mobil ilova push-bildirishnoma tokenini saqlash")
async def update_fcm_token(
    req: FCMTokenRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.fcm_token = req.fcm_token.strip()
    db.commit()
    return {"status": "success", "message": "FCM token yangilandi"}

# ==================== CLASSIC PASSWORD ENDPOINTS (BACKWARD COMPATIBILITY) ====================

@router.post("/register", summary="Yangi foydalanuvchini ro'yxatdan o'tkazish (Parol bilan)")
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    clean_phone = normalize_phone(req.phone_number)
    
    if len(clean_phone) < 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telefon raqami noto'g'ri kiritildi."
        )

    existing_user = db.query(User).filter(User.phone_number == clean_phone).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ushbu telefon raqami allaqachon ro'yxatdan o'tgan. Iltimos, tizimga kiring."
        )

    free_credits = Config.INITIAL_FREE_CREDITS
    if req.device_id:
        existing_devices_count = db.query(User).filter(User.device_id == req.device_id).count()
        if existing_devices_count >= 2:
            free_credits = 0

    new_user = User(
        phone_number=clean_phone,
        full_name=req.full_name or "Foydalanuvchi",
        hashed_password=hash_password(req.password),
        credits_balance=free_credits,
        device_id=req.device_id or None,
        auth_provider="phone",
        is_active=True
    )
    db.add(new_user)
    db.flush()

    if free_credits > 0:
        welcome_tx = CreditTransaction(
            user_id=new_user.id,
            amount=free_credits,
            balance_after=free_credits,
            transaction_type="welcome_bonus",
            description=f"Xush kelibsiz bonusi: {free_credits} ta bepul ta'limiy video",
            payment_method="system_bonus"
        )
        db.add(welcome_tx)

    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": str(new_user.id), "phone": new_user.phone_number})

    return {
        "status": "success",
        "message": f"Muvaffaqiyatli ro'yxatdan o'tdingiz! Sizga {free_credits} ta bepul video kredit taqdim etildi. 🎉",
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user.to_dict()
    }

@router.post("/login", summary="Tizimga kirish (Parol bilan yoki Admin)")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    raw_login = req.phone_number.strip()

    # 1. Administrator tekshiruvi: login 'admin' bo'lsa yoki admin paroli kiritilsa avtomatik admin ekani aniqlanadi
    if raw_login.lower() == Config.ADMIN_USERNAME.lower() and req.password == Config.ADMIN_PASSWORD:
        admin_phone = "+998900000001"
        admin_user = db.query(User).filter(
            (User.phone_number == admin_phone) | (User.is_admin == True)
        ).first()

        if not admin_user:
            admin_user = User(
                phone_number=admin_phone,
                email="admin@tasvirlab.uz",
                full_name="Boshqaruv Administratori",
                hashed_password=hash_password(Config.ADMIN_PASSWORD),
                auth_provider="admin",
                credits_balance=999,
                is_active=True,
                is_verified=True,
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        else:
            if not admin_user.is_admin:
                admin_user.is_admin = True
                db.commit()

        token = create_access_token(
            data={"sub": str(admin_user.id), "phone": admin_user.phone_number, "is_admin": True, "role": "admin"}
        )

        return {
            "status": "success",
            "is_admin": True,
            "message": "Administrator sifatida tizimga kirdingiz! 🛡️",
            "access_token": token,
            "token_type": "bearer",
            "user": admin_user.to_dict()
        }

    # 2. Oddiy foydalanuvchi tekshiruvi
    clean_phone = normalize_phone(raw_login)
    user = db.query(User).filter((User.phone_number == clean_phone) | (User.email == raw_login)).first()
    if not user or not user.hashed_password or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login/telefon raqam yoki parol noto'g'ri."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ushbu akkaunt bloklangan. Qo'llab-quvvatlash xizmatiga murojaat qiling."
        )

    token_data = {"sub": str(user.id), "phone": user.phone_number}
    if user.is_admin:
        token_data["is_admin"] = True
        token_data["role"] = "admin"

    access_token = create_access_token(data=token_data)

    return {
        "status": "success",
        "is_admin": bool(user.is_admin),
        "message": f"Xush kelibsiz, {user.full_name or 'do`stim'}!",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }

@router.get("/me", summary="Joriy foydalanuvchi ma'lumotlari va balansi")
async def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recent_transactions = [
        tx.to_dict() for tx in current_user.transactions[:5]
    ]
    videos_count = len(current_user.videos)
    
    return {
        "user": current_user.to_dict(),
        "total_videos_created": videos_count,
        "recent_transactions": recent_transactions
    }

@router.put("/profile", summary="Profil ma'lumotlarini yangilash")
async def update_profile(
    req: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if req.full_name is not None:
        current_user.full_name = req.full_name.strip()
    if req.avatar_url is not None:
        current_user.avatar_url = req.avatar_url.strip()
    db.commit()
    db.refresh(current_user)
    return {
        "status": "success",
        "message": "Profil yangilandi",
        "user": current_user.to_dict()
    }
