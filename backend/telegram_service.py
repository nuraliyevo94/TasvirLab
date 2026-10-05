import asyncio
import datetime
import httpx
from typing import Optional
from backend.config import Config
from backend.database import SessionLocal
from backend.models import User, TelegramAuthSession, CreditTransaction
from backend.auth import hash_password

class TelegramBotWorker:
    """Telegram Bot bilan avtomatik bog'lanish va /start tg_auth_ orqali avtorizatsiya qilish xizmati."""
    _is_running = False
    _last_update_id = 0

    @classmethod
    async def start(cls):
        if cls._is_running:
            return
        cls._is_running = True
        asyncio.create_task(cls._poll_loop())

    @classmethod
    async def _poll_loop(cls):
        print("[TelegramBotWorker] Fon rejimi boshlandi...")
        async with httpx.AsyncClient(timeout=20.0) as client:
            while cls._is_running:
                token = Config.TELEGRAM_BOT_TOKEN
                if not token:
                    await asyncio.sleep(4)
                    continue

                try:
                    url = f"https://api.telegram.org/bot{token}/getUpdates"
                    params = {"timeout": 10}
                    if cls._last_update_id:
                        params["offset"] = cls._last_update_id + 1

                    resp = await client.get(url, params=params)
                    if resp.status_code == 200:
                        data = resp.json()
                        updates = data.get("result", [])
                        for update in updates:
                            cls._last_update_id = update["update_id"]
                            await cls._process_update(update, client, token)
                    elif resp.status_code == 409:
                        await asyncio.sleep(5)
                    else:
                        await asyncio.sleep(3)
                except Exception as e:
                    await asyncio.sleep(3)

    @classmethod
    async def _process_update(cls, update: dict, client: httpx.AsyncClient, token: str):
        message = update.get("message")
        if not message:
            return

        text = message.get("text", "")
        from_user = message.get("from", {})
        chat_id = message.get("chat", {}).get("id")

        if text.startswith("/start"):
            parts = text.split()
            auth_token = parts[1].strip() if len(parts) > 1 else None

            if auth_token and auth_token.startswith("tg_auth_"):
                db = SessionLocal()
                try:
                    now = datetime.datetime.utcnow()
                    session_rec = db.query(TelegramAuthSession).filter(
                        TelegramAuthSession.auth_token == auth_token,
                        TelegramAuthSession.status == "pending",
                        TelegramAuthSession.expires_at >= now
                    ).first()

                    if session_rec:
                        tg_id = str(from_user.get("id"))
                        tg_username = from_user.get("username")
                        full_name = f"{from_user.get('first_name', '')} {from_user.get('last_name', '')}".strip() or "Telegram Foydalanuvchi"

                        user = db.query(User).filter(User.telegram_id == tg_id).first()
                        if not user:
                            user = User(
                                phone_number=f"tg_{tg_id}",
                                telegram_id=tg_id,
                                telegram_username=tg_username,
                                full_name=full_name,
                                hashed_password=hash_password(auth_token),
                                auth_provider="telegram",
                                credits_balance=Config.INITIAL_FREE_CREDITS,
                                is_active=True,
                                is_verified=True
                            )
                            db.add(user)
                            db.flush()

                            tx = CreditTransaction(
                                user_id=user.id,
                                amount=Config.INITIAL_FREE_CREDITS,
                                balance_after=Config.INITIAL_FREE_CREDITS,
                                transaction_type="welcome_bonus",
                                description=f"Telegram orqali ro'yxatdan o'tish bonusi: {Config.INITIAL_FREE_CREDITS} ta bepul video",
                                payment_method="telegram"
                            )
                            db.add(tx)
                        else:
                            if tg_username:
                                user.telegram_username = tg_username
                            if full_name and user.full_name == "Telegram Foydalanuvchi":
                                user.full_name = full_name

                        session_rec.status = "confirmed"
                        session_rec.telegram_id = tg_id
                        session_rec.telegram_username = tg_username
                        session_rec.user_id = user.id
                        db.commit()

                        if chat_id:
                            reply_text = (
                                f"🎉 Assalomu alaykum, {from_user.get('first_name', 'qadrli do`stimiz')}!\n\n"
                                f"✅ TasvirLab platformasiga muvaffaqiyatli kirdingiz!\n"
                                f"🎁 Hisobingizda {user.credits_balance} ta video balansi mavjud.\n\n"
                                f"Saytga qaytib darslarni yaratishingiz mumkin! ✨"
                            )
                            await client.post(
                                f"https://api.telegram.org/bot{token}/sendMessage",
                                json={"chat_id": chat_id, "text": reply_text}
                            )
                        print(f"[TelegramBotWorker] Sessiya tasdiqlandi: {user.full_name} (tg: {tg_id})")
                finally:
                    db.close()
            else:
                if chat_id:
                    greeting = (
                        f"Assalomu alaykum, {from_user.get('first_name', 'do`stim')}! 🎈\n\n"
                        f"Bu TasvirLab platformasining rasmiy boti.\n"
                        f"Saytga tezkor kirish uchun saytdagi 'Telegram orqali kirish' tugmasini bosing!"
                    )
                    await client.post(
                        f"https://api.telegram.org/bot{token}/sendMessage",
                        json={"chat_id": chat_id, "text": greeting}
                    )
