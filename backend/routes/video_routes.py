import os
import re
import json
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, UserVideo
from backend.auth import get_current_user, get_optional_current_user
from backend.config import Config
from backend.ffmpeg_renderer import FFmpegRenderer

router = APIRouter(prefix="/api/user/videos", tags=["Foydalanuvchi Videolari"])

class SaveVideoRequest(BaseModel):
    topic: str
    age_group: str = "5-7"
    voice_id: str = "lola"
    visual_style_id: str = "pixar_3d"
    duration: float = 0.0
    thumbnail_url: Optional[str] = None
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    screenplay_data: Optional[Dict[str, Any]] = None
    prepared_scenes: Optional[List[Dict[str, Any]]] = None
    quiz_data: Optional[Dict[str, Any]] = None

class RenderMp4Request(BaseModel):
    video_id: Optional[int] = None
    topic: str
    age_group: str = "5-7"
    voice_id: str = "lola"
    visual_style_id: str = "pixar_3d"
    bgm_track: Optional[str] = "bgm_cheerful.mp3"
    moral_summary: Optional[str] = None
    prepared_scenes: List[Dict[str, Any]]
    quiz_data: Optional[Dict[str, Any]] = None
    save_to_db: bool = True

@router.get("", summary="Foydalanuvchining barcha yaratgan videolari ro'yxati")
async def get_user_videos(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    uid = current_user.id if current_user else 1
    videos = db.query(UserVideo)\
        .filter((UserVideo.user_id == uid) | (UserVideo.user_id == 1))\
        .order_by(UserVideo.created_at.desc())\
        .all()
    
    return {
        "count": len(videos),
        "videos": [v.to_dict() for v in videos]
    }

@router.post("/save", summary="Yaratilgan yangi videoni ma'lumotlar bazasida saqlash")
async def save_video(
    req: SaveVideoRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    uid = current_user.id if current_user else 1

    # Mehmon foydalanuvchi (id=1) mavjudligini ta'minlaymiz
    guest_user = db.query(User).filter(User.id == uid).first()
    if not guest_user:
        guest_user = User(
            id=uid,
            phone_number="+998900000000",
            full_name="Mehmon Foydalanuvchi",
            credits_balance=10,
            auth_provider="guest",
            is_active=True,
            is_verified=True
        )
        db.add(guest_user)
        db.commit()
        db.refresh(guest_user)

    full_payload = {
        "screenplay": req.screenplay_data or {},
        "prepared_scenes": req.prepared_scenes or [],
        "quiz": req.quiz_data or None
    }
    screenplay_json_str = json.dumps(full_payload, ensure_ascii=False)

    thumb = req.thumbnail_url
    if not thumb and req.prepared_scenes and len(req.prepared_scenes) > 0:
        thumb = req.prepared_scenes[0].get("image_url")
    if not thumb:
        thumb = "/images/cinema_idle_poster.jpg"

    video_record = UserVideo(
        user_id=uid,
        topic=req.topic or "Ta'limiy Video",
        age_group=req.age_group or "5-7",
        voice_id=req.voice_id or "lola",
        visual_style_id=req.visual_style_id or "pixar_3d",
        status="completed",
        render_progress=100,
        duration=req.duration or 0.0,
        credits_spent=1,
        thumbnail_url=thumb,
        audio_url=req.audio_url,
        video_url=req.video_url,
        screenplay_json=screenplay_json_str
    )
    db.add(video_record)
    db.commit()
    db.refresh(video_record)

    return {
        "status": "success",
        "message": "Video ma'lumotlar bazasida muvaffaqiyatli saqlandi.",
        "video": video_record.to_dict()
    }

@router.get("/{video_id}", summary="Alohida video tafsilotlari")
async def get_video_detail(
    video_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    video = db.query(UserVideo).filter(UserVideo.id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video topilmadi."
        )
    
    data = video.to_dict()
    data["screenplay"] = video.screenplay_json
    return data

@router.delete("/{video_id}", summary="Videoni o'chirish")
async def delete_video(
    video_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    video = db.query(UserVideo).filter(UserVideo.id == video_id).first()
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video topilmadi."
        )
    
    # Diskdagi MP4 faylni ham tozalash
    if video.video_url:
        try:
            import os
            from backend.config import Config
            filename = os.path.basename(video.video_url)
            file_path = Config.STATIC_DIR / "renders" / filename
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            print(f"[DeleteVideo] Faylni o'chirishda ogohlantirish: {e}")

    db.delete(video)
    db.commit()
    
    return {
        "status": "success",
        "message": "Video muvaffaqiyatli o'chirildi."
    }

@router.post("/render-mp4", summary="Serverda FFmpeg orqali to'liq 1080p Full HD MP4 video render qilish")
async def render_mp4_video(
    req: RenderMp4Request,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    if not req.prepared_scenes or len(req.prepared_scenes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Render qilish uchun sahnalar ro'yxati taqdim etilmadi."
        )

    uid = current_user.id if current_user else 1
    
    # Foydalanuvchini tekshiramiz yoki mehmon yaratamiz
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        user = User(
            id=uid,
            phone_number="+998900000000",
            full_name="Mehmon Foydalanuvchi",
            credits_balance=10,
            auth_provider="guest",
            is_active=True,
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Chiqish fayl nomini shakllantirish
    clean_topic = re.sub(r'[^\w\-]', '_', req.topic.strip().lower())
    clean_topic = re.sub(r'_+', '_', clean_topic)[:30].strip('_')
    if not clean_topic:
        clean_topic = "video"
    rand_suffix = uuid.uuid4().hex[:8]
    mp4_filename = f"TasvirLab_{clean_topic}_{rand_suffix}.mp4"
    output_path = Config.STATIC_DIR / "renders" / mp4_filename

    try:
        render_result = await FFmpegRenderer.render_full_project_to_mp4(
            scenes=req.prepared_scenes,
            topic=req.topic,
            output_mp4_path=output_path,
            bgm_track=req.bgm_track or "bgm_cheerful.mp3",
            moral_summary=req.moral_summary,
            static_dir=Config.STATIC_DIR
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"FFmpeg renderlash jarayonida xatolik yuz berdi: {str(e)}"
        )

    video_url = f"/renders/{mp4_filename}"
    download_url = f"/api/user/videos/download-file/{mp4_filename}"

    video_record_id = req.video_id
    if req.video_id:
        existing_video = db.query(UserVideo).filter(UserVideo.id == req.video_id).first()
        if existing_video:
            existing_video.video_url = video_url
            existing_video.duration = render_result.get("duration", existing_video.duration)
            existing_video.status = "completed"
            existing_video.render_progress = 100
            db.commit()
            db.refresh(existing_video)
            video_record_id = existing_video.id
    elif req.save_to_db:
        thumb = None
        if req.prepared_scenes and len(req.prepared_scenes) > 0:
            thumb = req.prepared_scenes[0].get("image_url")
        if not thumb:
            thumb = "/images/cinema_idle_poster.jpg"

        full_payload = {
            "screenplay": {"topic": req.topic, "age_group": req.age_group},
            "prepared_scenes": req.prepared_scenes,
            "quiz": req.quiz_data or None
        }

        video_record = UserVideo(
            user_id=uid,
            topic=req.topic or "Ta'limiy Video",
            age_group=req.age_group or "5-7",
            voice_id=req.voice_id or "lola",
            visual_style_id=req.visual_style_id or "pixar_3d",
            status="completed",
            render_progress=100,
            duration=render_result.get("duration", 0.0),
            credits_spent=1,
            thumbnail_url=thumb,
            audio_url=req.prepared_scenes[0].get("audio_url") if req.prepared_scenes else None,
            video_url=video_url,
            screenplay_json=json.dumps(full_payload, ensure_ascii=False)
        )
        db.add(video_record)
        db.commit()
        db.refresh(video_record)
        video_record_id = video_record.id

    return {
        "status": "success",
        "message": "1080p Full HD MP4 video muvaffaqiyatli render qilindi!",
        "video_url": video_url,
        "download_url": download_url,
        "filename": mp4_filename,
        "duration": render_result.get("duration", 0.0),
        "size_mb": render_result.get("size_mb", 0.0),
        "resolution": render_result.get("resolution", "1920x1080 (Full HD)"),
        "codec": render_result.get("codec", "H.264 / AAC"),
        "fps": render_result.get("fps", 30),
        "video_id": video_record_id
    }

@router.get("/download-file/{filename}", summary="Render qilingan MP4 videoni yuklab olish")
async def download_rendered_file(filename: str):
    safe_filename = Path(filename).name
    file_path = Config.STATIC_DIR / "renders" / safe_filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Talab qilingan video fayl topilmadi."
        )

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=safe_filename,
        headers={
            "Content-Disposition": f'attachment; filename="{safe_filename}"'
        }
    )

