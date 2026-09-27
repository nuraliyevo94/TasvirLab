import asyncio
import sys

# Windows terminal UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

from backend.safety import ContentSafetyEngine
from backend.screenwriter import ScreenwriterEngine
from backend.tts_mohirai import MohirAITTSEngine
from backend.video_engine import GenerativeVideoEngine

async def test_full_pipeline():
    print("=== 1. Xavfsizlik & COPPA tekshiruvi ===")
    safe_topic = "Quyosh sistemasidagi sayyoralar"
    safe_prompt = "Sayyoralarni bolalarga qiziqarli qilib tushuntirib bering"
    res_safe = ContentSafetyEngine.evaluate(safe_prompt, safe_topic, "5-7")
    print("Xavfsiz mavzu natijasi:", res_safe["status"], f"Ball: {res_safe['safety_score']}%")
    assert res_safe["is_safe"] == True

    unsafe_topic = "Bolalar uchun qurol va pichoq bilan o'ynash"
    res_unsafe = ContentSafetyEngine.evaluate("", unsafe_topic, "5-7")
    print("Xavfli mavzu natijasi:", res_unsafe["status"], f"Ball: {res_unsafe['safety_score']}%")
    assert res_unsafe["is_safe"] == False
    print("[OK] Xavfsizlik filtri bekamu-ko'st ishladi!")

    print("\n=== 2. AI Ssenarist va Storyboard ===")
    screenplay = await ScreenwriterEngine.generate_screenplay(
        topic="Suv tomchisining sarguzashti",
        prompt="Kichkina tomchi daryoga aylanadi",
        age_group="5-7",
        duration_seconds=60,
        visual_style_id="pixar_3d",
        language="uz"
    )
    print(f"Ssenariy nomi: {screenplay['title']}")
    print(f"Sahnalar soni: {len(screenplay['scenes'])}")
    print(f"1-sahna nutqi: {screenplay['scenes'][0]['narration']}")
    print(f"1-sahna Kling/Runway promti: {screenplay['scenes'][0]['visual_prompt']}")
    assert len(screenplay["scenes"]) > 0
    print("[OK] Ssenarist muvaffaqiyatli sahnama-sahna rejalashtirdi!")

    print("\n=== 3. MohirAI O'zbek Tili Ovoz Dvigateli ===")
    voice_res = await MohirAITTSEngine.synthesize(
        text=screenplay["scenes"][0]["narration"],
        voice_id="dilnoza",
        speed=1.0
    )
    print(f"Ovoz holati: {voice_res['status']}, Ovoz: {voice_res['voice']['name']}")
    assert voice_res["success"] == True
    print("[OK] MohirAI ovoz sintezi tayyor!")

    print("\n=== 4. Kling AI / Runway Video Render & Montaj ===")
    video_pkg = GenerativeVideoEngine.assemble_full_video_package(screenplay, voice_res["voice"])
    print(f"Loyiha: {video_pkg['project_name']}, Jami vaqt: {video_pkg['total_duration']}s")
    print(f"Tayyor timeline qadamlari: {len(video_pkg['timeline'])}")
    assert len(video_pkg["timeline"]) == len(screenplay["scenes"])
    print("[OK] Video montaj va sinxronizatsiya paketi tayyor!")
    print("\n[SUCCESS] Barcha modullar bekamu-ko'st sinovdan o'tdi!")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
