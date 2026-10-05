import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.config import Config
from backend.database import get_db
from backend.models import User, CreditTransaction, UserVideo, PaymentOrder
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_admin
)
from backend.topics_store import TopicsStore

router = APIRouter(prefix="/api/admin", tags=["Administrator Paneli"])

# ==================== SCHEMAS ====================

class AdminLoginRequest(BaseModel):
    username: str = Field(..., description="Administrator logini")
    password: str = Field(..., description="Administrator paroli")

class AdjustCreditsRequest(BaseModel):
    amount: int = Field(..., description="Qo'shiladigan yoki ayiriladigan kreditlar miqdori (masalan: +5 yoki -2)")
    reason: Optional[str] = Field("Admin tomonidan bonus", description="O'zgartirish sababi yoki tavsifi")

class TopicCreateRequest(BaseModel):
    title: str = Field(..., description="Mavzu nomi")
    age_group: str = Field(default="5-7", description="Yosh guruhi: 2-4, 5-7, 8-11, 12-16")
    prompt: Optional[str] = Field(default="", description="Mavzuning dastlabki yo'riqnomasi")

# ==================== AUTH ENDPOINTS ====================

@router.post("/login", summary="Administrator tizimiga kirish")
async def admin_login(req: AdminLoginRequest, db: Session = Depends(get_db)):
    is_valid_username = (req.username.strip() == Config.ADMIN_USERNAME.strip())
    is_valid_password = (req.password.strip() == Config.ADMIN_PASSWORD.strip())

    if not (is_valid_username and is_valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin login yoki parol noto'g'ri kiritildi."
        )

    # Ma'lumotlar bazasida admin yozuvini tekshiramiz yoki yaratamiz
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
        data={"sub": str(admin_user.id), "phone": admin_user.phone_number, "is_admin": True, "role": "admin"},
        expires_delta=datetime.timedelta(days=7)
    )

    return {
        "status": "success",
        "message": "Administrator paneliga xush kelibsiz!",
        "access_token": token,
        "token_type": "bearer",
        "admin": {
            "id": admin_user.id,
            "username": Config.ADMIN_USERNAME,
            "full_name": admin_user.full_name,
            "is_admin": True
        }
    }

# ==================== OVERVIEW & STATISTICS ====================

@router.get("/overview", summary="Tizim umumiy statistikasi va iqtisodiy tahlili")
async def get_overview(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    # 1. Foydalanuvchilar statistikasi
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    today_start = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    new_users_today = db.query(User).filter(User.created_at >= today_start).count()

    # Kirish usullari bo'yicha taqsimot
    providers_query = db.query(User.auth_provider, func.count(User.id)).group_by(User.auth_provider).all()
    providers_stat = {p[0] or "boshqa": p[1] for p in providers_query}

    # 2. Iqtisodiy ko'rsatkichlar
    transactions = db.query(CreditTransaction).all()
    
    total_credits_purchased = db.query(func.sum(CreditTransaction.amount))\
        .filter(CreditTransaction.amount > 0, CreditTransaction.transaction_type == "purchase")\
        .scalar() or 0

    total_credits_spent = db.query(func.sum(CreditTransaction.amount))\
        .filter(CreditTransaction.amount < 0)\
        .scalar() or 0
    total_credits_spent = abs(total_credits_spent)

    total_active_credits = db.query(func.sum(User.credits_balance)).scalar() or 0

    # Tushum hisobi (Xaridlar bo'yicha)
    purchases = db.query(CreditTransaction).filter(CreditTransaction.transaction_type == "purchase").all()
    # O'rtacha 1 kredit narxi ~1,200 so'm deb hisoblanadi
    total_revenue_uzs = sum([getattr(tx, "amount", 0) * 1200 for tx in purchases])

    # 3. Yaratilgan videolar statistikasi
    total_videos = db.query(UserVideo).count()
    videos_today = db.query(UserVideo).filter(UserVideo.created_at >= today_start).count()

    # So'nggi tranzaksiyalar
    recent_txs = db.query(CreditTransaction)\
        .order_by(CreditTransaction.created_at.desc())\
        .limit(8)\
        .all()

    # 4. Tizim va API holati
    system_health = {
        "gemini_api_configured": bool(Config.GEMINI_API_KEY),
        "mohirai_tts_configured": bool(Config.MOHIRAI_API_KEY),
        "telegram_bot_configured": bool(Config.TELEGRAM_BOT_TOKEN),
        "database_status": "Faol (SQLite)",
        "server_time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "new_today": new_users_today,
            "by_provider": providers_stat
        },
        "economics": {
            "total_revenue_uzs": total_revenue_uzs,
            "total_credits_purchased": total_credits_purchased,
            "total_credits_spent": total_credits_spent,
            "total_active_balance": total_active_credits,
            "total_transactions": len(transactions),
            "recent_transactions": [tx.to_dict() for tx in recent_txs]
        },
        "videos": {
            "total": total_videos,
            "today": videos_today
        },
        "system_health": system_health
    }

# ==================== USERS MANAGEMENT ====================

@router.get("/users", summary="Barcha foydalanuvchilar ro'yxati (Qidiruv va filter bilan)")
async def get_users_list(
    search: Optional[str] = Query(None, description="Telefon raqami yoki ism bo'yicha qidiruv"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    query = db.query(User)
    if search:
        s = f"%{search.strip()}%"
        query = query.filter((User.phone_number.ilike(s)) | (User.full_name.ilike(s)) | (User.email.ilike(s)))

    total_count = query.count()
    users = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()

    users_data = []
    for u in users:
        v_count = len(u.videos)
        u_dict = u.to_dict()
        u_dict["videos_count"] = v_count
        users_data.append(u_dict)

    return {
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "users": users_data
    }

@router.post("/users/{user_id}/adjust-credits", summary="Foydalanuvchi hisobiga kredit qo'shish yoki ayirish")
async def adjust_user_credits(
    user_id: int,
    req: AdjustCreditsRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi.")

    new_balance = max(0, target_user.credits_balance + req.amount)
    target_user.credits_balance = new_balance

    tx = CreditTransaction(
        user_id=target_user.id,
        amount=req.amount,
        balance_after=new_balance,
        transaction_type="admin_adjustment",
        description=req.reason or "Admin tomonidan o'zgartirildi",
        payment_method="admin_panel"
    )
    db.add(tx)
    db.commit()
    db.refresh(target_user)

    return {
        "status": "success",
        "message": f"Foydalanuvchi balansi muvaffaqiyatli o'zgartirildi. Yangi balans: {new_balance} ta video.",
        "user": target_user.to_dict()
    }

@router.post("/users/{user_id}/toggle-status", summary="Foydalanuvchini bloklash yoki faollashtirish")
async def toggle_user_status(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi.")

    target_user.is_active = not target_user.is_active
    db.commit()
    db.refresh(target_user)

    status_str = "faollashtirildi" if target_user.is_active else "bloklandi"
    return {
        "status": "success",
        "message": f"Foydalanuvchi hisobi muvaffaqiyatli {status_str}.",
        "is_active": target_user.is_active
    }

# ==================== RECOMMENDED TOPICS MANAGEMENT ====================

@router.get("/topics", summary="Tavsiya etilgan barcha namunaviy mavzular ro'yxati")
async def get_recommended_topics(admin: User = Depends(get_current_admin)):
    topics = TopicsStore.get_all_topics()
    return {
        "count": len(topics),
        "topics": topics
    }

@router.post("/topics", summary="Yangi tavsiya etilgan mavzu qo'shish")
async def add_recommended_topic(
    req: TopicCreateRequest,
    admin: User = Depends(get_current_admin)
):
    new_topic = {
        "title": req.title.strip(),
        "age": req.age_group,
        "age_group": req.age_group,
        "prompt": req.prompt.strip() or f"{req.title} mavzusida bolalar uchun ibratli darslik"
    }
    updated_topics = TopicsStore.add_topic(new_topic)
    return {
        "status": "success",
        "message": "Yangi tavsiyaviy mavzu qo'shildi va barcha foydalanuvchilarga ko'rinadi!",
        "count": len(updated_topics)
    }

@router.delete("/topics/{topic_id_or_title}", summary="Tavsiya etilgan mavzuni o'chirish")
async def delete_recommended_topic(
    topic_id_or_title: str,
    admin: User = Depends(get_current_admin)
):
    updated_topics = TopicsStore.delete_topic(topic_id_or_title)
    return {
        "status": "success",
        "message": "Mavzu muvaffaqiyatli o'chirildi.",
        "count": len(updated_topics)
    }

# ==================== VIDEOS MONITORING ====================

@router.get("/videos", summary="Barcha yaratilgan videolar ro'yxati")
async def get_all_videos(
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    total = db.query(UserVideo).count()
    videos = db.query(UserVideo).order_by(UserVideo.created_at.desc()).offset(offset).limit(limit).all()

    video_items = []
    for v in videos:
        v_dict = v.to_dict()
        user = db.query(User).filter(User.id == v.user_id).first()
        v_dict["user_phone"] = user.phone_number if user else "Noma'lum"
        v_dict["user_name"] = user.full_name if user else "Mehmon"
        video_items.append(v_dict)

    return {
        "total": total,
        "videos": video_items
    }

# ==================== INTEGRATIONS & SETTINGS ====================

class IntegrationsUpdateRequest(BaseModel):
    google_client_id: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    telegram_bot_username: Optional[str] = None
    admin_password: Optional[str] = None
    mohirai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    # To'lov tizimlari sozlamalari
    payme_merchant_id: Optional[str] = None
    payme_secret_key: Optional[str] = None
    click_service_id: Optional[str] = None
    click_merchant_id: Optional[str] = None
    click_secret_key: Optional[str] = None
    uzum_merchant_id: Optional[str] = None
    uzum_secret_key: Optional[str] = None
    paynet_service_id: Optional[str] = None
    paynet_secret_key: Optional[str] = None

@router.get("/integrations", summary="Google, Telegram, To'lovlar va API kalitlari holatini ko'rish")
async def get_integrations(admin: User = Depends(get_current_admin)):
    return {
        "google_client_id": Config.GOOGLE_CLIENT_ID,
        "telegram_bot_token": Config.TELEGRAM_BOT_TOKEN,
        "telegram_bot_username": Config.TELEGRAM_BOT_USERNAME,
        "admin_username": Config.ADMIN_USERNAME,
        "mohirai_configured": bool(Config.MOHIRAI_API_KEY),
        "gemini_configured": bool(Config.GEMINI_API_KEY),
        "mohirai_api_key": Config.MOHIRAI_API_KEY or "",
        "gemini_api_key": Config.GEMINI_API_KEY or "",
        "payme_merchant_id": Config.PAYME_MERCHANT_ID,
        "payme_secret_key": Config.PAYME_SECRET_KEY,
        "click_service_id": Config.CLICK_SERVICE_ID,
        "click_merchant_id": Config.CLICK_MERCHANT_ID,
        "click_secret_key": Config.CLICK_SECRET_KEY,
        "uzum_merchant_id": Config.UZUM_MERCHANT_ID,
        "uzum_secret_key": Config.UZUM_SECRET_KEY,
        "paynet_service_id": Config.PAYNET_SERVICE_ID,
        "paynet_secret_key": Config.PAYNET_SECRET_KEY
    }

@router.post("/integrations", summary="Barcha integratsiyalar va kalitlarni saqlash")
async def save_integrations(
    req: IntegrationsUpdateRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    from pathlib import Path
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"

    env_lines = {}
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_lines[k.strip()] = v.strip()

    if req.google_client_id is not None:
        Config.GOOGLE_CLIENT_ID = req.google_client_id.strip()
        env_lines["GOOGLE_CLIENT_ID"] = req.google_client_id.strip()

    if req.telegram_bot_token is not None:
        Config.TELEGRAM_BOT_TOKEN = req.telegram_bot_token.strip()
        env_lines["TELEGRAM_BOT_TOKEN"] = req.telegram_bot_token.strip()

    if req.telegram_bot_username is not None:
        clean_user = req.telegram_bot_username.strip().replace("@", "")
        Config.TELEGRAM_BOT_USERNAME = clean_user
        env_lines["TELEGRAM_BOT_USERNAME"] = clean_user

    if req.admin_password is not None and len(req.admin_password.strip()) >= 6:
        Config.ADMIN_PASSWORD = req.admin_password.strip()
        env_lines["ADMIN_PASSWORD"] = req.admin_password.strip()
        admin.hashed_password = hash_password(req.admin_password.strip())
        db.commit()

    if req.mohirai_api_key is not None:
        Config.MOHIRAI_API_KEY = req.mohirai_api_key.strip()
        env_lines["MOHIRAI_API_KEY"] = req.mohirai_api_key.strip()

    if req.gemini_api_key is not None:
        Config.GEMINI_API_KEY = req.gemini_api_key.strip()
        env_lines["GEMINI_API_KEY"] = req.gemini_api_key.strip()

    # To'lov kalitlari
    if req.payme_merchant_id is not None:
        Config.PAYME_MERCHANT_ID = req.payme_merchant_id.strip()
        env_lines["PAYME_MERCHANT_ID"] = req.payme_merchant_id.strip()

    if req.payme_secret_key is not None:
        Config.PAYME_SECRET_KEY = req.payme_secret_key.strip()
        env_lines["PAYME_SECRET_KEY"] = req.payme_secret_key.strip()

    if req.click_service_id is not None:
        Config.CLICK_SERVICE_ID = req.click_service_id.strip()
        env_lines["CLICK_SERVICE_ID"] = req.click_service_id.strip()

    if req.click_merchant_id is not None:
        Config.CLICK_MERCHANT_ID = req.click_merchant_id.strip()
        env_lines["CLICK_MERCHANT_ID"] = req.click_merchant_id.strip()

    if req.click_secret_key is not None:
        Config.CLICK_SECRET_KEY = req.click_secret_key.strip()
        env_lines["CLICK_SECRET_KEY"] = req.click_secret_key.strip()

    if req.uzum_merchant_id is not None:
        Config.UZUM_MERCHANT_ID = req.uzum_merchant_id.strip()
        env_lines["UZUM_MERCHANT_ID"] = req.uzum_merchant_id.strip()

    if req.uzum_secret_key is not None:
        Config.UZUM_SECRET_KEY = req.uzum_secret_key.strip()
        env_lines["UZUM_SECRET_KEY"] = req.uzum_secret_key.strip()

    if req.paynet_service_id is not None:
        Config.PAYNET_SERVICE_ID = req.paynet_service_id.strip()
        env_lines["PAYNET_SERVICE_ID"] = req.paynet_service_id.strip()

    if req.paynet_secret_key is not None:
        Config.PAYNET_SECRET_KEY = req.paynet_secret_key.strip()
        env_lines["PAYNET_SECRET_KEY"] = req.paynet_secret_key.strip()

    try:
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("# TasvirLab Environment Configuration\n")
            for k, v in env_lines.items():
                f.write(f"{k}={v}\n")
    except Exception as e:
        print(f"Error saving .env: {e}")

    return {
        "status": "success",
        "message": "Integratsiyalar va to'lov sozlamalari muvaffaqiyatli saqlandi!",
        "settings": {
            "google_client_id": Config.GOOGLE_CLIENT_ID,
            "telegram_bot_username": Config.TELEGRAM_BOT_USERNAME,
            "payme_configured": bool(Config.PAYME_MERCHANT_ID),
            "click_configured": bool(Config.CLICK_SERVICE_ID),
            "uzum_configured": bool(Config.UZUM_MERCHANT_ID),
            "paynet_configured": bool(Config.PAYNET_SERVICE_ID)
        }
    }
