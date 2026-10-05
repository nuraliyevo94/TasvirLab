import base64
import urllib.parse
import datetime
import secrets
import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.config import Config
from backend.database import get_db
from backend.models import User, CreditTransaction, PaymentOrder
from backend.auth import get_current_user

logger = logging.getLogger("tasvirlab.billing")

router = APIRouter(prefix="/api/billing", tags=["To'lovlar va Balans"])

PRICING_PACKAGES = [
    {
        "id": "pack_starter",
        "name": "Boshlang'ich To'plam",
        "credits": 5,
        "price_uzs": 15000,
        "price_per_video_uzs": 3000,
        "discount_percent": 0,
        "popular": False,
        "icon": "🌱",
        "description": "Kichik oilalar va dastlabki video darslar uchun qulay to'plam."
    },
    {
        "id": "pack_popular",
        "name": "Oila To'plami (Ommabop)",
        "credits": 20,
        "price_uzs": 45000,
        "price_per_video_uzs": 2250,
        "discount_percent": 25,
        "popular": True,
        "icon": "⭐",
        "description": "Eng ko'p tanlanadigan xalqchil to'plam! 20 ta video dars — bor-yo'g'i 45 000 so'm."
    },
    {
        "id": "pack_pro",
        "name": "O'qituvchilar & Bog'cha",
        "credits": 50,
        "price_uzs": 89000,
        "price_per_video_uzs": 1780,
        "discount_percent": 40,
        "popular": False,
        "icon": "🚀",
        "description": "Bog'cha tarbiyachilari, repetitorlar va faol ota-onalar uchun eng tejamkor paket."
    },
    {
        "id": "pack_vip",
        "name": "Maktab & VIP Ta'lim",
        "credits": 150,
        "price_uzs": 199000,
        "price_per_video_uzs": 1320,
        "discount_percent": 55,
        "popular": False,
        "icon": "👑",
        "description": "O'quv markazlari va katta ta'limiy loyihalar uchun maksimal ulgurji chegirma."
    }
]

# ==================== SCHEMAS ====================

class CreateCheckoutRequest(BaseModel):
    package_id: str = Field(..., example="pack_popular", description="Paket IDsi")
    payment_provider: str = Field(default="payme", example="payme", description="payme, click yoki uzum")
    return_url: Optional[str] = Field(None, description="To'lovdan keyin qaytish manzili")

class TopUpRequest(BaseModel):
    package_id: Optional[str] = Field(None, example="pack_popular")
    custom_credits: Optional[int] = Field(None, ge=1, le=1000)
    payment_method: str = Field(default="demo", example="payme")
    reference_id: Optional[str] = Field(default=None)

# ==================== YORDAMCHI FUNKSIYALAR ====================

def activate_paid_order(order: PaymentOrder, db: Session, provider_tx_id: Optional[str] = None) -> bool:
    """To'langan buyurtmani tasdiqlash, foydalanuvchiga kreditlarni yozish."""
    if order.status == "paid":
        return True  # Allaqachon tasdiqlangan

    order.status = "paid"
    order.paid_at = datetime.datetime.utcnow()
    if provider_tx_id:
        order.provider_transaction_id = str(provider_tx_id)

    # Foydalanuvchi balansini oshirish
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        return False

    user.credits_balance += order.credits_amount

    # Tranzaksiya yozuvi yaratish
    tx = CreditTransaction(
        user_id=user.id,
        amount=order.credits_amount,
        balance_after=user.credits_balance,
        transaction_type="purchase",
        description=f"{order.package_name} ({order.credits_amount} ta video, {order.amount_uzs:,} so'm)",
        payment_method=order.payment_provider,
        reference_id=order.order_id
    )
    db.add(tx)
    db.commit()
    logger.info(f"To'lov muvaffaqiyatli: Order {order.order_id}, User #{user.id}, +{order.credits_amount} kredit")
    return True

def generate_payme_url(merchant_id: str, order_id: str, amount_uzs: int, user_id: int, return_url: str) -> str:
    amount_tiyin = amount_uzs * 100
    if not merchant_id:
        # Sinov / test rejim havolasi
        return f"https://checkout.paycom.uz/demo?order_id={order_id}&amount={amount_tiyin}&user_id={user_id}"
    
    # Payme rasmiy base64 checkout parametri
    raw_params = f"m={merchant_id};ac.order_id={order_id};ac.user_id={user_id};a={amount_tiyin};c={return_url}"
    b64_params = base64.b64encode(raw_params.encode("utf-8")).decode("utf-8")
    return f"https://checkout.paycom.uz/{b64_params}"

def generate_click_url(service_id: str, merchant_id: str, order_id: str, amount_uzs: int, return_url: str) -> str:
    s_id = service_id or "demo_service"
    m_id = merchant_id or "demo_merchant"
    ret = urllib.parse.quote(return_url)
    return f"https://my.click.uz/services/pay?service_id={s_id}&merchant_id={m_id}&amount={amount_uzs}&transaction_param={order_id}&return_url={ret}"

def generate_uzum_url(service_id: str, order_id: str, amount_uzs: int) -> str:
    s_id = service_id or "demo_uzum"
    return f"https://www.uzumbank.uz/open-service?service_id={s_id}&amount={amount_uzs}&order_id={order_id}"

def generate_paynet_url(service_id: str, order_id: str, amount_uzs: int, return_url: str) -> str:
    s_id = service_id or "demo_paynet"
    ret = urllib.parse.quote(return_url)
    return f"https://paynet.uz/checkout?service_id={s_id}&order_id={order_id}&amount={amount_uzs}&return_url={ret}"

# ==================== ENDPOINTS ====================

@router.get("/packages", summary="Mavjud to'lov tariflari ro'yxati")
async def get_packages():
    return {
        "currency": "UZS",
        "packages": PRICING_PACKAGES
    }

@router.post("/create-checkout", summary="Tanlangan to'plam uchun Payme / Click / Uzum / Paynet to'lov havolasini yaratish")
async def create_checkout(
    req: CreateCheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    selected_pkg = next((p for p in PRICING_PACKAGES if p["id"] == req.package_id), None)
    if not selected_pkg:
        raise HTTPException(status_code=400, detail="Tanlangan paket topilmadi.")

    prov = req.payment_provider.lower().strip()
    if prov not in ["payme", "click", "uzum", "paynet"]:
        prov = "payme"

    order_id = f"TL-{int(datetime.datetime.utcnow().timestamp())}-{secrets.randbelow(9000) + 1000}"
    base_url = Config.APP_BASE_URL.rstrip("/")
    return_url = req.return_url or f"{base_url}/?payment=completed&order={order_id}"

    # Buyurtma yaratamiz
    order = PaymentOrder(
        order_id=order_id,
        user_id=current_user.id,
        package_id=selected_pkg["id"],
        package_name=selected_pkg["name"],
        credits_amount=selected_pkg["credits"],
        amount_uzs=selected_pkg["price_uzs"],
        payment_provider=prov,
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Havola shakllantiramiz
    is_live = False
    if prov == "payme":
        checkout_url = generate_payme_url(Config.PAYME_MERCHANT_ID, order_id, selected_pkg["price_uzs"], current_user.id, return_url)
        is_live = bool(Config.PAYME_MERCHANT_ID)
    elif prov == "click":
        checkout_url = generate_click_url(Config.CLICK_SERVICE_ID, Config.CLICK_MERCHANT_ID, order_id, selected_pkg["price_uzs"], return_url)
        is_live = bool(Config.CLICK_SERVICE_ID)
    elif prov == "uzum":
        checkout_url = generate_uzum_url(Config.UZUM_MERCHANT_ID, order_id, selected_pkg["price_uzs"])
        is_live = bool(Config.UZUM_MERCHANT_ID)
    else:
        checkout_url = generate_paynet_url(Config.PAYNET_SERVICE_ID, order_id, selected_pkg["price_uzs"], return_url)
        is_live = bool(Config.PAYNET_SERVICE_ID)

    return {
        "status": "success",
        "order_id": order_id,
        "package_name": selected_pkg["name"],
        "credits": selected_pkg["credits"],
        "amount_uzs": selected_pkg["price_uzs"],
        "provider": prov,
        "checkout_url": checkout_url,
        "is_live_merchant": is_live,
        "message": f"{selected_pkg['name']} uchun {prov.upper()} to'lov havolasi yaratildi."
    }

@router.get("/orders/{order_id}", summary="Buyurtma holatini tekshirish")
async def check_order_status(order_id: str, db: Session = Depends(get_db)):
    order = db.query(PaymentOrder).filter(PaymentOrder.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi.")

    return {
        "order_id": order.order_id,
        "status": order.status,
        "is_paid": order.status == "paid",
        "package_name": order.package_name,
        "credits_amount": order.credits_amount,
        "amount_uzs": order.amount_uzs,
        "payment_provider": order.payment_provider,
        "paid_at": order.paid_at.isoformat() if order.paid_at else None
    }

@router.post("/simulate-paid/{order_id}", include_in_schema=False)
async def simulate_paid_order(order_id: str):
    """Sinov to'lovlari o'chirilgan."""
    raise HTTPException(
        status_code=403,
        detail="Sinov to'lovlari o'chirilgan. To'lov faqat rasmiy to'lov ilovalari (Payme, Click, Uzum, Paynet) orqali amalga oshiriladi."
    )

# ==================== PAYME MERCHANT WEBHOOK ====================

@router.post("/payme/webhook", summary="Payme Merchant API Webhook (JSON-RPC 2.0)")
async def payme_merchant_webhook(req_body: Dict[str, Any], db: Session = Depends(get_db)):
    """Payme to'lov tizimining to'liq standart JSON-RPC 2.0 protokoli."""
    method = req_body.get("method")
    params = req_body.get("params", {})
    req_id = req_body.get("id")

    def json_rpc_error(code: int, message_ru: str, message_uz: str):
        return {
            "error": {
                "code": code,
                "message": {"ru": message_ru, "uz": message_uz}
            },
            "id": req_id
        }

    account = params.get("account", {})
    order_id = account.get("order_id")

    if method == "CheckPerformTransaction":
        if not order_id:
            return json_rpc_error(-31050, "Не указан заказ", "Buyurtma ko'rsatilmagan")
        order = db.query(PaymentOrder).filter(PaymentOrder.order_id == order_id).first()
        if not order:
            return json_rpc_error(-31050, "Заказ не найден", "Buyurtma topilmadi")
        amount = params.get("amount", 0)
        if amount != order.amount_uzs * 100:
            return json_rpc_error(-31001, "Неверная сумма", "Noto'g'ri summa")
        if order.status == "paid":
            return json_rpc_error(-31051, "Заказ уже оплачен", "Buyurtma allaqachon to'langan")
        return {"result": {"allow": True}, "id": req_id}

    elif method == "CreateTransaction":
        order = db.query(PaymentOrder).filter(PaymentOrder.order_id == order_id).first()
        if not order:
            return json_rpc_error(-31050, "Заказ не найден", "Buyurtma topilmadi")
        now_ts = int(datetime.datetime.utcnow().timestamp() * 1000)
        payme_tx_id = params.get("id")
        order.provider_transaction_id = payme_tx_id
        db.commit()
        return {
            "result": {
                "create_time": now_ts,
                "transaction": str(order.id),
                "state": 1
            },
            "id": req_id
        }

    elif method == "PerformTransaction":
        payme_tx_id = params.get("id")
        order = db.query(PaymentOrder).filter(
            (PaymentOrder.provider_transaction_id == payme_tx_id) | (PaymentOrder.order_id == order_id)
        ).first()
        if not order:
            return json_rpc_error(-31003, "Транзакция не найдена", "Tranzaksiya topilmadi")

        now_ts = int(datetime.datetime.utcnow().timestamp() * 1000)
        if order.status != "paid":
            activate_paid_order(order, db, provider_tx_id=payme_tx_id)

        return {
            "result": {
                "transaction": str(order.id),
                "perform_time": now_ts,
                "state": 2
            },
            "id": req_id
        }

    elif method == "CheckTransaction":
        payme_tx_id = params.get("id")
        order = db.query(PaymentOrder).filter(
            (PaymentOrder.provider_transaction_id == payme_tx_id) | (PaymentOrder.order_id == order_id)
        ).first()
        if not order:
            return json_rpc_error(-31003, "Транзакция не найдена", "Tranzaksiya topilmadi")
        
        create_ts = int(order.created_at.timestamp() * 1000) if order.created_at else 0
        perform_ts = int(order.paid_at.timestamp() * 1000) if order.paid_at else 0
        state = 2 if order.status == "paid" else 1

        return {
            "result": {
                "create_time": create_ts,
                "perform_time": perform_ts,
                "cancel_time": 0,
                "transaction": str(order.id),
                "state": state,
                "reason": None
            },
            "id": req_id
        }

    elif method == "CancelTransaction":
        payme_tx_id = params.get("id")
        order = db.query(PaymentOrder).filter(PaymentOrder.provider_transaction_id == payme_tx_id).first()
        if order:
            order.status = "cancelled"
            db.commit()
        return {
            "result": {
                "transaction": str(order.id) if order else "0",
                "cancel_time": int(datetime.datetime.utcnow().timestamp() * 1000),
                "state": -1
            },
            "id": req_id
        }

    return json_rpc_error(-32601, "Метод не найден", "Metod topilmadi")

# ==================== CLICK WEBHOOK ====================

@router.post("/click/webhook", summary="Click to'lov tizimi Webhook (Prepare va Complete)")
async def click_merchant_webhook(request: Request, db: Session = Depends(get_db)):
    """Click protokolining Prepare (action=0) va Complete (action=1) qadami."""
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8", errors="ignore")
    data = {}
    try:
        import json
        data = json.loads(body_str)
    except Exception:
        parsed = urllib.parse.parse_qs(body_str)
        data = {k: v[0] for k, v in parsed.items()}

    action = str(data.get("action", "0"))
    order_id = data.get("merchant_trans_id")
    click_trans_id = data.get("click_trans_id")
    try:
        amount = float(data.get("amount", 0))
    except Exception:
        amount = 0.0

    order = db.query(PaymentOrder).filter(PaymentOrder.order_id == order_id).first()
    if not order:
        return {"error": -5, "error_note": "Order does not exist"}

    if float(order.amount_uzs) != amount:
        return {"error": -2, "error_note": "Incorrect amount"}

    if action == "0":
        # Prepare qadami
        return {
            "error": 0,
            "error_note": "Success",
            "click_trans_id": click_trans_id,
            "merchant_trans_id": order_id,
            "merchant_prepare_id": order.id
        }
    elif action == "1":
        # Complete qadami
        if order.status != "paid":
            activate_paid_order(order, db, provider_tx_id=str(click_trans_id))
        return {
            "error": 0,
            "error_note": "Success",
            "click_trans_id": click_trans_id,
            "merchant_trans_id": order_id,
            "merchant_confirm_id": order.id
        }

    return {"error": -3, "error_note": "Action not supported"}

# ==================== UZUM PAY WEBHOOK ====================

@router.post("/uzum/webhook", summary="Uzum Bank / Uzum Pay to'lov Webhook")
async def uzum_merchant_webhook(req_body: Dict[str, Any], db: Session = Depends(get_db)):
    order_id = req_body.get("order_id")
    status_field = req_body.get("status", "").upper()
    uzum_tx_id = req_body.get("trans_id")

    if not order_id:
        raise HTTPException(status_code=400, detail="Order ID kiritilmagan.")

    order = db.query(PaymentOrder).filter(PaymentOrder.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order topilmadi.")

    if status_field in ["CONFIRMED", "SUCCESS", "PAID"]:
        if order.status != "paid":
            activate_paid_order(order, db, provider_tx_id=str(uzum_tx_id))
        return {"status": "success", "message": "Uzum to'lovi tasdiqlandi"}

    return {"status": "ignored", "message": f"Holat: {status_field}"}

# ==================== PAYNET MERCHANT WEBHOOK ====================

@router.post("/paynet/webhook", summary="Paynet Webhook (Callback)")
async def paynet_merchant_webhook(req_body: Dict[str, Any], db: Session = Depends(get_db)):
    """Paynet to'lov tizimidan kelgan so'rovlarni qabul qilish va tasdiqlash."""
    order_id = req_body.get("order_id") or req_body.get("transaction_param") or req_body.get("orderId")
    if not order_id:
        return {"status": "error", "message": "order_id topilmadi"}

    order = db.query(PaymentOrder).filter(PaymentOrder.order_id == str(order_id)).first()
    if not order:
        return {"status": "error", "message": "Buyurtma topilmadi"}

    tx_id = req_body.get("paynet_tx_id") or req_body.get("transactionId") or f"paynet_{secrets.token_hex(4)}"
    if order.status != "paid":
        activate_paid_order(order, db, provider_tx_id=str(tx_id))
    return {"status": "success", "message": "Paynet to'lovi tasdiqlandi", "order_id": order.order_id}

# ==================== TRANSACTION HISTORY ====================

@router.get("/transactions", summary="Foydalanuvchining hisob-kitoblar tarixi")
async def get_transaction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transactions = db.query(CreditTransaction)\
        .filter(CreditTransaction.user_id == current_user.id)\
        .order_by(CreditTransaction.created_at.desc())\
        .all()
    
    orders = db.query(PaymentOrder)\
        .filter(PaymentOrder.user_id == current_user.id)\
        .order_by(PaymentOrder.created_at.desc())\
        .limit(20)\
        .all()

    return {
        "current_balance": current_user.credits_balance,
        "transactions": [tx.to_dict() for tx in transactions],
        "orders": [o.to_dict() for o in orders]
    }
