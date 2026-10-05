import datetime
import json
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(32), unique=True, index=True, nullable=True)
    email = Column(String(128), unique=True, index=True, nullable=True)
    full_name = Column(String(128), nullable=True)
    hashed_password = Column(String(255), nullable=True)
    google_id = Column(String(128), unique=True, index=True, nullable=True)
    apple_id = Column(String(128), unique=True, index=True, nullable=True)
    telegram_id = Column(String(64), unique=True, index=True, nullable=True)
    telegram_username = Column(String(128), nullable=True)
    avatar_url = Column(String(512), nullable=True)
    auth_provider = Column(String(32), default="phone", nullable=False)  # phone, google, apple, telegram
    credits_balance = Column(Integer, default=3, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    device_id = Column(String(128), nullable=True, index=True)
    fcm_token = Column(String(255), nullable=True)  # Mobil push-bildirishnomalar uchun
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Aloqalar
    transactions = relationship("CreditTransaction", back_populates="user", cascade="all, delete-orphan", order_by="desc(CreditTransaction.created_at)")
    videos = relationship("UserVideo", back_populates="user", cascade="all, delete-orphan", order_by="desc(UserVideo.created_at)")

    def to_dict(self):
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "email": self.email,
            "telegram_id": self.telegram_id,
            "telegram_username": self.telegram_username,
            "full_name": self.full_name or "Foydalanuvchi",
            "avatar_url": self.avatar_url,
            "auth_provider": self.auth_provider,
            "credits_balance": self.credits_balance,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class TelegramAuthSession(Base):
    __tablename__ = "telegram_auth_sessions"

    id = Column(Integer, primary_key=True, index=True)
    auth_token = Column(String(64), unique=True, index=True, nullable=False)
    status = Column(String(32), default="pending", nullable=False)  # pending, confirmed, expired
    telegram_id = Column(String(64), nullable=True)
    telegram_username = Column(String(128), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def is_valid(self) -> bool:
        return self.status == "pending" and datetime.datetime.utcnow() <= self.expires_at

class OTPCode(Base):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(32), index=True, nullable=False)
    code = Column(String(8), nullable=False)
    purpose = Column(String(32), default="login", nullable=False)  # login, register, reset
    is_used = Column(Boolean, default=False, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def is_valid(self) -> bool:
        return not self.is_used and datetime.datetime.utcnow() <= self.expires_at

class CreditTransaction(Base):
    __tablename__ = "credit_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Integer, nullable=False)  # Masalan: +3, -1, +20
    balance_after = Column(Integer, nullable=False)
    transaction_type = Column(String(64), nullable=False)  # welcome_bonus, video_generation, purchase, refund
    description = Column(String(255), nullable=True)
    payment_method = Column(String(64), nullable=True)  # click, payme, uzum, apple_iap, google_iap, system_bonus
    reference_id = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="transactions")

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "balance_after": self.balance_after,
            "transaction_type": self.transaction_type,
            "description": self.description,
            "payment_method": self.payment_method,
            "reference_id": self.reference_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class UserVideo(Base):
    __tablename__ = "user_videos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = Column(String(255), nullable=False)
    age_group = Column(String(32), default="5-7")
    voice_id = Column(String(64), default="lola")
    visual_style_id = Column(String(64), default="pixar_3d")
    status = Column(String(32), default="completed")  # pending, processing, completed, failed
    render_progress = Column(Integer, default=100)  # 0 to 100%
    duration = Column(Float, default=0.0)
    credits_spent = Column(Integer, default=1)
    audio_url = Column(String(512), nullable=True)
    video_url = Column(String(512), nullable=True)
    thumbnail_url = Column(String(512), nullable=True)
    screenplay_json = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="videos")

    def to_dict(self):
        screenplay_data = None
        if self.screenplay_json:
            try:
                screenplay_data = json.loads(self.screenplay_json)
            except Exception:
                screenplay_data = self.screenplay_json

        return {
            "id": self.id,
            "topic": self.topic,
            "age_group": self.age_group,
            "voice_id": self.voice_id,
            "visual_style_id": self.visual_style_id,
            "status": self.status,
            "render_progress": self.render_progress,
            "duration": self.duration,
            "credits_spent": self.credits_spent,
            "audio_url": self.audio_url,
            "video_url": self.video_url,
            "thumbnail_url": self.thumbnail_url,
            "screenplay": screenplay_data,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class PaymentOrder(Base):
    __tablename__ = "payment_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(64), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    package_id = Column(String(64), nullable=False)
    package_name = Column(String(128), nullable=False)
    credits_amount = Column(Integer, nullable=False)
    amount_uzs = Column(Integer, nullable=False)
    payment_provider = Column(String(32), nullable=False)  # payme, click, uzum
    status = Column(String(32), default="pending", nullable=False)  # pending, paid, cancelled, failed
    provider_transaction_id = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    paid_at = Column(DateTime, nullable=True)

    user = relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "user_id": self.user_id,
            "package_id": self.package_id,
            "package_name": self.package_name,
            "credits_amount": self.credits_amount,
            "amount_uzs": self.amount_uzs,
            "payment_provider": self.payment_provider,
            "status": self.status,
            "provider_transaction_id": self.provider_transaction_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None
        }

