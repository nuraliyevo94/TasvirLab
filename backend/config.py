import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=False)

class Config:
    MOHIRAI_API_KEY = os.getenv("MOHIRAI_API_KEY", "")
    KLING_API_KEY = os.getenv("KLING_API_KEY", "")
    RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    OUTPUT_DIR = BASE_DIR / "output"
    STATIC_DIR = BASE_DIR / "static"
    FRONTEND_DIR = BASE_DIR / "frontend"

AGE_GROUPS = {
    "2-4": {
        "id": "2-4",
        "title": "2 – 4 yosh",
        "category": "Kichkintoylar (Toddlers)",
        "icon": "🧸",
        "color": "from-amber-400 to-orange-400",
        "target_words_per_minute": 60,
        "max_duration_seconds": 60,
        "recommended_duration": 45,
        "style_desc": "O'ta sodda, yorqin, kontrastli ranglar, ritmik va takrorlanuvchi iboralar, sensor tushunchalar (ranglar, hayvonlar, tovushlar)."
    },
    "5-7": {
        "id": "5-7",
        "title": "5 – 7 yosh",
        "category": "Maktabgacha davr",
        "icon": "🎨",
        "color": "from-pink-400 to-rose-500",
        "target_words_per_minute": 80,
        "max_duration_seconds": 120,
        "recommended_duration": 60,
        "style_desc": "Ertaknamo, qiziqarli multfilm personajlari, do'stlik, gigiyena, harflar, tabiat, quvnoq dialoglar."
    },
    "8-10": {
        "id": "8-10",
        "title": "8 – 10 yosh",
        "category": "Boshlang'ich maktab",
        "icon": "🚀",
        "color": "from-blue-400 to-indigo-600",
        "target_words_per_minute": 100,
        "max_duration_seconds": 180,
        "recommended_duration": 90,
        "style_desc": "Kashfiyotlar, ilmiy-ommabop mo'jizalar, tarixiy milliy qahramonlar, odob-axloq, sarguzashtli syujet."
    },
    "11-12": {
        "id": "11-12",
        "title": "11 – 12 yosh",
        "category": "Kichik o'smirlar",
        "icon": "🧠",
        "color": "from-emerald-400 to-teal-600",
        "target_words_per_minute": 120,
        "max_duration_seconds": 240,
        "recommended_duration": 120,
        "style_desc": "Kognitiv tahlil, texnologiya, kiber-olam, ekologiya, tanqidiy fikrlash va motivatsion hikoyalar."
    }
}

MOHIRAI_VOICES = [
    {
        "id": "lola",
        "name": "Pedagogik O'zbek Ovoz",
        "role": "Mehribon virtual o'qituvchi va ertakchi",
        "tone": "Yorqin, quvnoq, bolalarbop, muloyim va ravon intonatsiya",
        "suitable_ages": ["2-4", "5-7", "8-10", "11-12"],
        "gender": "female",
        "recommended": True
    }
]

VISUAL_STYLES = [
    {
        "id": "pixar_3d",
        "title": "3D Pixar / Disney",
        "prompt_prefix": "3D cartoon animated Pixar Disney style, soft volumetric lighting, vibrant vivid colors, expressive child-friendly characters, 8k render, Unreal Engine 5 aesthetic, family friendly",
        "icon": "✨"
    },
    {
        "id": "watercolor_2d",
        "title": "2D Ertaknamo Akvarel",
        "prompt_prefix": "Whimsical children's book illustration, soft watercolor and gouache texture, cozy fairytale aesthetic, bright warm pastel palette, high artistic quality",
        "icon": "🎨"
    },
    {
        "id": "ghibli_anime",
        "title": "Studio Ghibli Uslubi",
        "prompt_prefix": "Studio Ghibli anime style, lush hand-painted background, warm sunlight, gentle breeze, peaceful nature, emotional and heartwarming, beautiful aesthetic",
        "icon": "🍃"
    },
    {
        "id": "sci_fi_3d",
        "title": "Ilmiy-Ommabop Kiber",
        "prompt_prefix": "Futuristic clean 3D educational animation, holographic science visual, cosmic neon stars, bright inviting laboratory, highly engaging for smart kids",
        "icon": "🪐"
    }
]

SAMPLE_TOPICS = [
    {
        "age": "5-7",
        "title": "2 ga 2 ni qo'shish siri (Matematika darsi)",
        "prompt": "Bolalarga 2 ga 2 ni qo'shish qanday bo'lishini olmalar misolida tushuntirib, 2+2=4 natijasini o'rgatuvchi dars."
    },
    {
        "age": "5-7",
        "title": "Daraxtlar nega barg to'kadi? (Tabiat siri)",
        "prompt": "Kuz faslida daraxtlar nega barglarini oltin rangga bo'yab to'kishi va qishki uyqusi haqida samimiy dars."
    },
    {
        "age": "2-4",
        "title": "Sehrli ranglar olami va shirin mevalar",
        "prompt": "Qizil olma, sariq banan va yashil nok qanday rangda ekanligini kichkintoyga quvnoq qilib o'rgatuvchi dars."
    },
    {
        "age": "8-10",
        "title": "Suv tomchisining ajoyib sarguzashti",
        "prompt": "Suv qanday isiydi, bug'lanib bulutga aylanadi va yomg'ir bo'lib qaytishini bosqichma-bosqich tushuntiring."
    },
    {
        "age": "11-12",
        "title": "Sun'iy intellekt va robotlar qanday o'ylaydi?",
        "prompt": "AI va robotlar qanday hisob-kitob qilishini o'smirlarga qiziqarli misollar orqali tushuntiring."
    }
]

BGM_TRACKS = [
    {
        "id": "bgm_cheerful",
        "name": "Quvnoq Marimba & Ukulele",
        "icon": "🎈",
        "desc": "Carefree (K. MacLeod) — Quvnoq, samimiy va erkalovchi bolalar ohangi",
        "url": "/audio/bgm_cheerful.mp3"
    },
    {
        "id": "bgm_playful",
        "name": "Qiziqarli Multfilm Maromi",
        "icon": "🐒",
        "desc": "Monkeys Spinning Monkeys — Sarguzasht, hayrat va sho'x multfilm ritmi",
        "url": "/audio/bgm_playful.ogg"
    },
    {
        "id": "bgm_gentle",
        "name": "Mayin va Sokin Pianino",
        "icon": "🍃",
        "desc": "Gymnopédie No. 1 (Erik Satie) — Tinchlantiruvchi mayin akustik fortepiano",
        "url": "/audio/bgm_gentle.ogg"
    },
    {
        "id": "bgm_fairytale",
        "name": "Sehrli Ertak & Mo'jiza",
        "icon": "✨",
        "desc": "Sugar Plum Fairy (P. Chaykovskiy) — Sehrli qo'ng'iroq va ertak olami",
        "url": "/audio/bgm_fairytale.ogg"
    },
    {
        "id": "bgm_upbeat",
        "name": "Shijoatli Ragtime Ta'lim",
        "icon": "🚀",
        "desc": "The Entertainer (Scott Joplin) — Jonli dars va intellektual ritm",
        "url": "/audio/bgm_upbeat.ogg"
    },
    {
        "id": "none",
        "name": "Musiqasiz (Faqat ovoz)",
        "icon": "🔇",
        "desc": "Faqat virtual ustozning sof nutq ovozi",
        "url": ""
    }
]
