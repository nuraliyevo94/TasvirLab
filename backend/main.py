import sys
from pathlib import Path

# Loyiha bosh papkasini sys.path ga qo'shamiz (Docker va Render muhitida backend topilishi uchun)
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import wave
import httpx
from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from backend.config import Config, AGE_GROUPS, MOHIRAI_VOICES, VISUAL_STYLES, SAMPLE_TOPICS, BGM_TRACKS
from backend.safety import ContentSafetyEngine
from backend.screenwriter import ScreenwriterEngine
from backend.tts_mohirai import MohirAITTSEngine
from backend.video_engine import GenerativeVideoEngine
from backend.scene_illustrator import SceneIllustrator
from backend.quiz_engine import QuizEngine

# Autentifikatsiya, billing va ma'lumotlar bazasi modullari
from backend.database import init_db, get_db
from backend.models import User, CreditTransaction, UserVideo
from backend.auth import get_current_user, get_optional_current_user
from backend.routes import auth_routes, billing_routes, video_routes, admin_routes
from backend.topics_store import TopicsStore
from fastapi import Depends
from sqlalchemy.orm import Session

app = FastAPI(
    title="TasvirLab Platform API",
    description="Bolalar va o'smirlar uchun sun'iy intellekt asosida pedagogik xavfsiz ta'limiy video platformasi va professional veb-studiyasi",
    version="3.5.0"
)

from backend.telegram_service import TelegramBotWorker

# Ma'lumotlar bazasini ishga tushirish va Telegram bot xizmatini ulash
@app.on_event("startup")
async def on_startup():
    init_db()
    await TelegramBotWorker.start()

# Marshrutlarni ulash
app.include_router(auth_routes.router)
app.include_router(billing_routes.router)
app.include_router(video_routes.router)
app.include_router(admin_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    if request.url.path.startswith("/static") or request.url.path == "/" or request.url.path.startswith("/renders") or request.url.path.startswith("/audio") or request.url.path.startswith("/images"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# Static and Frontend files
static_dir = Path(__file__).resolve().parent.parent / "static"
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
renders_dir = static_dir / "renders"
audio_dir = static_dir / "audio"
images_dir = static_dir / "images"
static_dir.mkdir(exist_ok=True)
frontend_dir.mkdir(exist_ok=True)
renders_dir.mkdir(exist_ok=True)
audio_dir.mkdir(exist_ok=True)
images_dir.mkdir(exist_ok=True)

# /renders, /audio, /images va /static papkalarini mount qilamiz
app.mount("/renders", StaticFiles(directory=str(renders_dir)), name="renders")
app.mount("/audio", StaticFiles(directory=str(audio_dir)), name="audio")
app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static_frontend")

# Request Models
class SafetyCheckRequest(BaseModel):
    topic: str
    prompt: Optional[str] = ""
    age_group: str = "5-7"

class ScreenplayRequest(BaseModel):
    topic: str
    prompt: Optional[str] = ""
    age_group: str = "5-7"
    duration_seconds: int = 60
    visual_style_id: str = "pixar_3d"
    language: str = "uz"
    api_key: Optional[str] = ""

class PrepareSceneRequest(BaseModel):
    project_id: str = "project_kids"
    scene: Dict[str, Any]
    topic: str
    voice_id: str = "lola"

class VoiceRequest(BaseModel):
    text: str
    voice_id: str = "lola"
    speed: float = 1.0
    api_key: Optional[str] = ""

class VideoRenderRequest(BaseModel):
    screenplay: Dict[str, Any]
    voice_id: str = "lola"
    engine_type: str = "kling"
    api_key: Optional[str] = ""

class SettingsRequest(BaseModel):
    mohirai_api_key: Optional[str] = None
    kling_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None

class QuizGenerateRequest(BaseModel):
    topic: str
    age_group: str = "5-7"
    screenplay: Optional[Dict[str, Any]] = None
    api_key: Optional[str] = ""

# Endpoints
@app.get("/")
async def serve_index():
    index_path = frontend_dir / "index.html"
    if not index_path.exists():
        return JSONResponse({"status": "KidsVidEdu Studio is starting up. Creating UI..."})
    return FileResponse(str(index_path))

@app.get("/api/presets")
async def get_presets():
    return {
        "age_groups": list(AGE_GROUPS.values()),
        "voices": MOHIRAI_VOICES,
        "visual_styles": VISUAL_STYLES,
        "sample_topics": TopicsStore.get_all_topics(),
        "bgm_tracks": BGM_TRACKS,
        "api_status": {
            "mohirai_configured": bool(Config.MOHIRAI_API_KEY),
            "kling_configured": bool(Config.KLING_API_KEY),
            "gemini_configured": bool(Config.GEMINI_API_KEY)
        }
    }

@app.post("/api/safety-check")
async def check_safety(req: SafetyCheckRequest):
    result = ContentSafetyEngine.evaluate(
        prompt=req.prompt or "",
        topic=req.topic or "",
        age_group=req.age_group
    )
    return result

@app.post("/api/generate-screenplay")
async def generate_screenplay(req: ScreenplayRequest):
    # Dastlab xavfsizlikni yana bir bor tekshiramiz
    safety = ContentSafetyEngine.evaluate(req.prompt or "", req.topic, req.age_group)
    if not safety["is_safe"]:
        raise HTTPException(
            status_code=400,
            detail=f"Xavfsizlik tekshiruvidan o'tmadi: {', '.join(safety['violations'])}"
        )
    
    screenplay = await ScreenwriterEngine.generate_screenplay(
        topic=req.topic,
        prompt=req.prompt or "",
        age_group=req.age_group,
        duration_seconds=req.duration_seconds,
        visual_style_id=req.visual_style_id,
        language=req.language,
        api_key=req.api_key or ""
    )
    return {
        "screenplay": screenplay,
        "safety_audit": safety
    }

@app.post("/api/generate-quiz")
async def generate_quiz(req: QuizGenerateRequest):
    quiz = await QuizEngine.generate_quiz(
        topic=req.topic,
        age_group=req.age_group,
        screenplay=req.screenplay or {},
        api_key=req.api_key or ""
    )
    return quiz

@app.post("/api/generate-voice")
async def generate_voice(req: VoiceRequest):
    result = await MohirAITTSEngine.synthesize(
        text=req.text,
        voice_id=req.voice_id,
        speed=req.speed,
        api_key=req.api_key
    )
    return result

@app.get("/api/audio/demo")
async def get_demo_audio(voice: str = "sevinch"):
    greeting_text = "Assalomu alaykum, jajji do'stim! KidsVidEdu ga xush kelibsiz!"
    try:
        synth = await MohirAITTSEngine.synthesize(text=greeting_text, voice_id=voice)
        remote_url = synth.get("audio_url")
        if remote_url and remote_url.startswith("http"):
            async with httpx.AsyncClient(timeout=15.0) as client:
                r = await client.get(remote_url)
                if r.status_code == 200:
                    return Response(content=r.content, media_type="audio/wav")
    except Exception as e:
        print(f"Demo audio xatolik: {e}")
    # Zaxira yoqimli qo'ng'iroq
    freq = 523.25 if "lola" in voice else (440.0 if "shoira" in voice else 392.0)
    wav_bytes = MohirAITTSEngine.generate_demo_wav(frequency=freq, duration=1.2)
    return Response(content=wav_bytes, media_type="audio/wav")

@app.post("/api/prepare-scene")
async def prepare_scene(req: PrepareSceneRequest):
    """Har bir sahnaning haqiqiy Mohir AI ovozi va multfilm tasvirini hosil qiladi va saqlaydi."""
    scene = req.scene
    s_num = scene.get("scene_number", 1)
    narration = scene.get("narration", "")
    
    renders_dir = static_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Haqiqiy Mohir AI Ovozini generatsiya qilish va saqlash
    audio_filename = f"{req.project_id}_scene_{s_num}.wav"
    audio_path = renders_dir / audio_filename
    
    exact_duration = 5.0
    audio_url = f"/renders/{audio_filename}"
    
    try:
        synth = await MohirAITTSEngine.synthesize(text=narration, voice_id=req.voice_id)
        remote_url = synth.get("audio_url")
        if remote_url and remote_url.startswith("http"):
            async with httpx.AsyncClient(timeout=25.0) as client:
                r = await client.get(remote_url)
                if r.status_code == 200:
                    with open(audio_path, "wb") as f:
                        f.write(r.content)
                    with wave.open(str(audio_path), "rb") as wf:
                        exact_duration = round(wf.getnframes() / float(wf.getframerate()), 2)
    except Exception as e:
        print(f"Audio saqlashda xatolik: {e}")
        wav_bytes = MohirAITTSEngine.generate_demo_wav(duration=max(3.0, len(narration.split()) * 0.45))
        with open(audio_path, "wb") as f:
            f.write(wav_bytes)

    # 2. Haqiqiy 1080p Multfilm Tasvirini generatsiya qilish va saqlash
    image_filename = f"{req.project_id}_scene_{s_num}.svg"
    image_path = renders_dir / image_filename
    svg_content = await SceneIllustrator.generate_scene_svg(scene, req.topic)
    with open(image_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    image_url = f"/renders/{image_filename}"

    return {
        "status": "ready",
        "scene_number": s_num,
        "title": scene.get("title", f"{s_num}-sahna"),
        "narration": narration,
        "audio_url": audio_url,
        "image_url": image_url,
        "duration": exact_duration,
        "emotion": scene.get("emotion", "quvnoq"),
        "camera_movement": scene.get("camera_movement", "slow_dolly_in"),
        "visual_beats": scene.get("visual_beats", [])
    }

@app.post("/api/render-video")
async def render_video(req: VideoRenderRequest):
    voice_info = next((v for v in MOHIRAI_VOICES if v["id"] == req.voice_id), MOHIRAI_VOICES[0])
    full_package = GenerativeVideoEngine.assemble_full_video_package(
        screenplay=req.screenplay,
        voice_info=voice_info
    )
    return full_package

@app.post("/api/save-settings", include_in_schema=False)
async def save_settings():
    raise HTTPException(
        status_code=403,
        detail="Dastur sozlamalari faqat Administrator Boshqaruv Panelida o'zgartirilishi mumkin."
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
