import asyncio
from backend.screenwriter import ScreenwriterEngine

async def test():
    res = await ScreenwriterEngine.generate_screenplay(
        topic="Daraxtlar nega barg to'kadi?",
        prompt="Kuzgi Bobo Chinor ertagi",
        age_group="5-7",
        duration_seconds=60,
        visual_style_id="pixar_3d",
        language="uz"
    )
    print("Title:", res.get("title"))
    print("Author:", res.get("screenplay_author"))
    for s in res.get("scenes", []):
        print(f"Sahna {s['scene_number']}: {s['title']} -> {s['narration']}")

if __name__ == "__main__":
    asyncio.run(test())
