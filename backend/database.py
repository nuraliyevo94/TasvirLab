import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from backend.config import Config

database_url = Config.DATABASE_URL

# SQLite uchun connect_args kerak, PostgreSQL uchun shart emas
connect_args = {}
if database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    database_url,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """FastAPI marshrutlarida ma'lumotlar bazasi sessiyasini olish uchun generator."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Barcha jadvallarni ma'lumotlar bazasida yaratish va yangi ustunlarni tekshirib qo'shish."""
    import backend.models  # Modellar ro'yxatdan o'tishi uchun import qilamiz
    Base.metadata.create_all(bind=engine)

    # SQLite jadvallariga yangi qo'shilgan ustunlarni avtomatik qo'shish (Auto-migration)
    if database_url.startswith("sqlite"):
        from sqlalchemy import text
        with engine.connect() as conn:
            # users jadvali ustunlari
            existing_user_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(users)")).fetchall()]
            new_user_cols = {
                "email": "VARCHAR(128)",
                "google_id": "VARCHAR(128)",
                "apple_id": "VARCHAR(128)",
                "telegram_id": "VARCHAR(64)",
                "telegram_username": "VARCHAR(128)",
                "avatar_url": "VARCHAR(512)",
                "auth_provider": "VARCHAR(32) DEFAULT 'phone'",
                "is_verified": "BOOLEAN DEFAULT 0",
                "fcm_token": "VARCHAR(255)"
            }
            for col_name, col_type in new_user_cols.items():
                if col_name not in existing_user_cols:
                    try:
                        conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                        conn.commit()
                    except Exception as e:
                        print(f"[init_db] users.{col_name} ustunini qo'shishda xatolik: {e}")

            # user_videos jadvali ustunlari
            existing_video_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(user_videos)")).fetchall()]
            new_video_cols = {
                "render_progress": "INTEGER DEFAULT 100",
                "error_message": "TEXT"
            }
            for col_name, col_type in new_video_cols.items():
                if col_name not in existing_video_cols:
                    try:
                        conn.execute(text(f"ALTER TABLE user_videos ADD COLUMN {col_name} {col_type}"))
                        conn.commit()
                    except Exception as e:
                        print(f"[init_db] user_videos.{col_name} ustunini qo'shishda xatolik: {e}")

