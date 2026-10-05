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

    # Ma'lumotlar bazasi va avtorizatsiya sozlamalari
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'tasvirlab.db'}")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "tasvirlab_secret_jwt_key_super_secure_2026")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS = 30
    
    # Bepul kreditlar va monetizatsiya
    INITIAL_FREE_CREDITS = int(os.getenv("INITIAL_FREE_CREDITS", "3"))
    CREDITS_PER_VIDEO = int(os.getenv("CREDITS_PER_VIDEO", "1"))
    
    # SMS shlyuz sozlamalari (Eskiz.uz / PlayMobile)
    ESKIZ_EMAIL = os.getenv("ESKIZ_EMAIL", "")
    ESKIZ_PASSWORD = os.getenv("ESKIZ_PASSWORD", "")
    OTP_EXPIRE_MINUTES = int(os.getenv("OTP_EXPIRE_MINUTES", "5"))
    DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"
    
    # Bulutli xotira (Cloudflare R2 / AWS S3)
    R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID", "")
    R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID", "")
    R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
    R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "tasvirlab-videos")
    R2_PUBLIC_DOMAIN = os.getenv("R2_PUBLIC_DOMAIN", "")

    # Telegram orqali autentifikatsiya sozlamalari
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "tasvirlab_bot")

    # Administrator boshqaruv hisobi sozlamalari
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "tasvir2026admin")

    # Google OAuth sozlamalari
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

    # To'lov tizimlari sozlamalari (Payme, Click, Uzum, Paynet)
    PAYME_MERCHANT_ID = os.getenv("PAYME_MERCHANT_ID", "")
    PAYME_SECRET_KEY = os.getenv("PAYME_SECRET_KEY", "")
    CLICK_SERVICE_ID = os.getenv("CLICK_SERVICE_ID", "")
    CLICK_MERCHANT_ID = os.getenv("CLICK_MERCHANT_ID", "")
    CLICK_SECRET_KEY = os.getenv("CLICK_SECRET_KEY", "")
    UZUM_MERCHANT_ID = os.getenv("UZUM_MERCHANT_ID", "")
    UZUM_SECRET_KEY = os.getenv("UZUM_SECRET_KEY", "")
    PAYNET_SERVICE_ID = os.getenv("PAYNET_SERVICE_ID", "")
    PAYNET_SECRET_KEY = os.getenv("PAYNET_SECRET_KEY", "")
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")

AGE_GROUPS = {
    "2-4": {
        "id": "2-4",
        "title": "2 – 4 yosh",
        "category": "Kichkintoylar",
        "icon": "🧸",
        "color": "from-amber-400 to-orange-400",
        "target_words_per_minute": 60,
        "max_duration_seconds": 60,
        "recommended_duration": 45,
        "style_desc": "O'ta sodda so'zlar, yorqin ranglar, mevalar, sevimli hayvonlar va mehrli ohang."
    },
    "5-7": {
        "id": "5-7",
        "title": "5 – 7 yosh",
        "category": "Bog'cha va Tayyorlov",
        "icon": "🎨",
        "color": "from-pink-400 to-rose-500",
        "target_words_per_minute": 80,
        "max_duration_seconds": 120,
        "recommended_duration": 60,
        "style_desc": "Qiziqarli ertaklar, multfilm qahramonlari, do'stlik, tozalik va quvnoq saboqlar."
    },
    "8-10": {
        "id": "8-10",
        "title": "8 – 10 yosh",
        "category": "Boshlang'ich Maktab",
        "icon": "🚀",
        "color": "from-blue-400 to-indigo-600",
        "target_words_per_minute": 100,
        "max_duration_seconds": 180,
        "recommended_duration": 90,
        "style_desc": "Qiziqarli kashfiyotlar, tabiat sirlari, buyuk bobolarimiz va ibratli hikoyalar."
    },
    "11-12": {
        "id": "11-12",
        "title": "11 – 12 yosh",
        "category": "Katta Bolalar",
        "icon": "🔬",
        "color": "from-emerald-400 to-teal-600",
        "target_words_per_minute": 120,
        "max_duration_seconds": 240,
        "recommended_duration": 120,
        "style_desc": "Tabiat qonunlari, koinot mo'jizalari, inson salomatligi va yangi bilimlar."
    },
    "13-15": {
        "id": "13-15",
        "title": "13 – 15 yosh",
        "category": "O'smirlar",
        "icon": "💻",
        "color": "from-cyan-500 to-blue-600",
        "target_words_per_minute": 130,
        "max_duration_seconds": 300,
        "recommended_duration": 150,
        "style_desc": "Kompyuter va dasturlash, zamonaviy texnologiyalar, vaqtni boshqarish va koinot."
    },
    "16-19": {
        "id": "16-19",
        "title": "16 – 19 yosh",
        "category": "Katta Sinf va Yoshlar",
        "icon": "🎓",
        "color": "from-violet-500 to-purple-700",
        "target_words_per_minute": 140,
        "max_duration_seconds": 360,
        "recommended_duration": 180,
        "style_desc": "Mustaqil hayot, to'g'ri kasb tanlash, pulni tejash va kelajak maqsadlari."
    }
}

MOHIRAI_VOICES = [
    {
        "id": "lola",
        "name": "O'zbekcha Ovoz (Lola)",
        "role": "Mehribon o'qituvchi va ertakchi",
        "tone": "Yorqin, quvnoq, bolalarga mos, muloyim va ravon talaffuz",
        "suitable_ages": ["2-4", "5-7", "8-10", "11-12", "13-15", "16-19"],
        "gender": "female",
        "recommended": True
    }
]

VISUAL_STYLES = [
    {
        "id": "pixar_3d",
        "title": "Yorqin 3D Multfilm",
        "prompt_prefix": "3D cartoon animated Pixar Disney style, soft volumetric lighting, vibrant vivid colors, expressive child-friendly characters, 8k render, Unreal Engine 5 aesthetic, family friendly",
        "icon": "✨"
    },
    {
        "id": "watercolor_2d",
        "title": "Ertaknamo Mo'yqalam",
        "prompt_prefix": "Whimsical children's book illustration, soft watercolor and gouache texture, cozy fairytale aesthetic, bright warm pastel palette, high artistic quality",
        "icon": "🎨"
    },
    {
        "id": "ghibli_anime",
        "title": "Mayin Tabiat va Quyosh",
        "prompt_prefix": "Studio Ghibli anime style, lush hand-painted background, warm sunlight, gentle breeze, peaceful nature, emotional and heartwarming, beautiful aesthetic",
        "icon": "🍃"
    },
    {
        "id": "sci_fi_3d",
        "title": "Koinot va Texnologiya",
        "prompt_prefix": "Futuristic clean 3D educational animation, holographic science visual, cosmic neon stars, bright inviting laboratory, highly engaging for smart kids",
        "icon": "🪐"
    },
    {
        "id": "modern_flat",
        "title": "Oddiy va Chiroyli Chizmalar",
        "prompt_prefix": "Clean modern 2D flat vector art, minimalist infographic illustration, geometric elegance, smooth color harmony, sophisticated aesthetic",
        "icon": "📊"
    }
]

SAMPLE_TOPICS = [
    # 1. Kichkintoylar (2-4 yosh)
    {
        "id": "colors_fun",
        "age": "2-4",
        "age_group": "2-4",
        "title": "Ranglarni birga o'rganamiz",
        "prompt": "Qizil olma, sariq banan va yashil nok misolida ranglarni quvnoq o'rgatuvchi dars."
    },
    {
        "id": "forest_animals",
        "age": "2-4",
        "age_group": "2-4",
        "title": "O'rmondagi do'stlarimiz",
        "prompt": "Quyoncha va ayiqvoyning do'stligi hamda o'rmon hayvonlari haqida mayin ertak darsi."
    },
    {
        "id": "magic_polite_words",
        "age": "2-4",
        "age_group": "2-4",
        "title": "Sehrli 'Rahmat' va 'Iltimos' so'zlari",
        "prompt": "Kichkintoylar uchun shirin muomala, salom berish va rahmat aytish odobi haqida saboq."
    },
    {
        "id": "morning_sunshine",
        "age": "2-4",
        "age_group": "2-4",
        "title": "Quyosh uyg'ondi: Quvnoq ertalab",
        "prompt": "Ertalab yuvinish, tishlarni tozalash va quvnoq badantarbiya haqida ertak dars."
    },
    {
        "id": "farm_animal_sounds",
        "age": "2-4",
        "age_group": "2-4",
        "title": "Uy hayvonlari va ularning ovozlari",
        "prompt": "Kuchukcha, mushukcha va qo'zichoq ovozlarini kichkintoylarga tanishtiruvchi saboq."
    },

    # 2. Bog'cha va Tayyorlov (5-7 yosh)
    {
        "id": "kindness_friends",
        "age": "5-7",
        "age_group": "5-7",
        "title": "Do'stlik va ahillik odobi",
        "prompt": "Bolalarga do'stlar bilan o'rtoqlashish, samimiy va ahil bo'lish haqida ibratli ertak darsi."
    },
    {
        "id": "autumn_leaves",
        "age": "5-7",
        "age_group": "5-7",
        "title": "Daraxtlar nega barg to'kadi?",
        "prompt": "Kuz faslida daraxtlar nega barglarini oltin rangga bo'yab to'kishi va qishki uyqusi haqida samimiy dars."
    },
    {
        "id": "water_cycle_intro",
        "age": "5-7",
        "age_group": "5-7",
        "title": "Yomg'ir qayerdan keladi?",
        "prompt": "Kichik suv tomchisining bulutlarga chiqib, yerga shifobaxsh yomg'ir bo'lib qaytishi haqida saboq."
    },
    {
        "id": "bread_journey",
        "age": "5-7",
        "age_group": "5-7",
        "title": "Non qanday dasturxonga keladi?",
        "prompt": "Bug'doy donidan issiq va xushbo'y nonga qadar bo'lgan mashaqqatli mehnat haqida hikoya."
    },
    {
        "id": "traffic_lights",
        "age": "5-7",
        "age_group": "5-7",
        "title": "Yo'l harakati qoidalari: Svetofor",
        "prompt": "Qizil, sariq va yashil chiroqlarning ma'nosi va ko'chani xavfsiz kesib o'tish qoidalari."
    },

    # 3. Boshlang'ich Maktab (8-10 yosh)
    {
        "id": "solar_system",
        "age": "8-10",
        "age_group": "8-10",
        "title": "Quyosh sistemasiga sayohat",
        "prompt": "Sayyoralar, Quyosh va ularning fazoda aylanish sirlari haqida qiziqarli sayohat."
    },
    {
        "id": "ocean_depths",
        "age": "8-10",
        "age_group": "8-10",
        "title": "Okean tubidagi sirli hayot",
        "prompt": "Moviy kitlar, rang-barang marjon riflari va dengiz mo'jizalari haqida dars."
    },
    {
        "id": "reading_superpower",
        "age": "8-10",
        "age_group": "8-10",
        "title": "Kitob o'qish qanday kuch beradi?",
        "prompt": "Kitoblar inson tasavvurini qanday kengaytirishi va allomalar ilmi haqida suhbat."
    },
    {
        "id": "honeybee_wonder",
        "age": "8-10",
        "age_group": "8-10",
        "title": "Asalarilar uyasi va asal mo'jizasi",
        "prompt": "Asalarilarning intizomi, tabiatni changlatishi va shirin asal tayyorlashi haqida biologik dars."
    },
    {
        "id": "ulughbeg_astronomy",
        "age": "8-10",
        "age_group": "8-10",
        "title": "Mirzo Ulug'bek va yulduzlar jadvali",
        "prompt": "Samarqand rasadxonasida yulduzlarni xaritaga tushirgan buyuk alloma haqida tarixiy saboq."
    },

    # 4. Katta Bolalar (11-12 yosh)
    {
        "id": "photosynthesis",
        "age": "11-12",
        "age_group": "11-12",
        "title": "Fotosintez: Yaproq laboratoriyasi",
        "prompt": "O'simliklar quyosh nuri orqali qanday toza kislorod ishlab chiqarishi va ekologiya sirlari."
    },
    {
        "id": "gravity_secret",
        "age": "11-12",
        "age_group": "11-12",
        "title": "Gravitatsiya kuchi va vaznsizlik",
        "prompt": "Nega yer narsalarni tortadi va fazogirlar kosmosda qanday suzib yuradi?"
    },
    {
        "id": "human_brain_memory",
        "age": "11-12",
        "age_group": "11-12",
        "title": "Inson miyasi qanday xotirlaydi?",
        "prompt": "Neyronlar va xotira qanday ishlashi, bilimlarni tez va oson eslab qolish texnikasi."
    },
    {
        "id": "electricity_basics",
        "age": "11-12",
        "age_group": "11-12",
        "title": "Elektr energiyasi qanday hosil bo'ladi?",
        "prompt": "Gidro va quyosh elektr stansiyalari, elektronlar oqimi va xavfsiz foydalanish."
    },
    {
        "id": "ibn_sina_health",
        "age": "11-12",
        "age_group": "11-12",
        "title": "Ibn Sino: Tabobat va sog'lom hayot",
        "prompt": "Buyuk tabib Ibn Sinoning to'g'ri ovqatlanish, sport va salomatlik bo'yicha tavsiyalari."
    },

    # 5. O'smirlar (13-15 yosh)
    {
        "id": "cyber_security",
        "age": "13-15",
        "age_group": "13-15",
        "title": "Internetda xavfsizlik: Shaxsiy ma'lumotlarni asrash",
        "prompt": "Internetda shaxsiy ma'lumotlarni asrash, firibgarlardan himoyalanish va mustahkam parollar tuzish."
    },
    {
        "id": "ai_machine_learning",
        "age": "13-15",
        "age_group": "13-15",
        "title": "Sun'iy intellekt qanday o'rganadi?",
        "prompt": "Neyrotarmoqlar va sun'iy intellekt ma'lumotlardan qanday o'rganishi va insonlarga yordam berishi."
    },
    {
        "id": "coding_logic_algorithms",
        "age": "13-15",
        "age_group": "13-15",
        "title": "Dasturlash tili va algoritmlar",
        "prompt": "Algoritmlar mantiqi, ketma-ketlik va kompyuterga buyruq berish san'ati."
    },
    {
        "id": "time_management",
        "age": "13-15",
        "age_group": "13-15",
        "title": "Vaqtni to'g'ri taqsimlash va unumdorlik",
        "prompt": "O'smirlar uchun darslar va dam olishni to'g'ri rejalashtirish, vaqtni behuda sarflamaslik sirlari."
    },
    {
        "id": "mars_space_exploration",
        "age": "13-15",
        "age_group": "13-15",
        "title": "Kosmik kashfiyotlar va Marsga safar",
        "prompt": "Mars sayyorasi, qizil tuproqdagi muz izlari va fazogirlarning kelajak rejalari."
    },

    # 6. Yoshlar (16-19 yosh)
    {
        "id": "financial_literacy",
        "age": "16-19",
        "age_group": "16-19",
        "title": "Moliyaviy savodxonlik va shaxsiy byudjet",
        "prompt": "Pulni oqilona boshqarish, jamg'arma shakllantirish, tejash va birinchi daromadlar."
    },
    {
        "id": "critical_thinking_media",
        "age": "16-19",
        "age_group": "16-19",
        "title": "Tanqidiy fikrlash va yolg'on xabarlarni aniqlash",
        "prompt": "Axborot oqimida ishonchli manbalarni topish, aldovlarga uchmaslik va mustaqil xulosa chiqarish."
    },
    {
        "id": "future_careers",
        "age": "16-19",
        "age_group": "16-19",
        "title": "Kelajak kasblari va to'g'ri yo'nalish tanlash",
        "prompt": "Zamonaviy texnologiyalar davrida talab yuqori bo'lgan sohalar, hayotiy qobiliyatlar va kasbiy ko'nikmalar."
    },
    {
        "id": "public_speaking",
        "age": "16-19",
        "age_group": "16-19",
        "title": "Notiqlik san'ati va taqdimot siri",
        "prompt": "Odamlar oldida ishonchli so'zlash, g'oyalarni chiroyli yetkazish va hayajonni yengish."
    },
    {
        "id": "startup_innovation",
        "age": "16-19",
        "age_group": "16-19",
        "title": "Yangi loyiha va foydali g'oyani boshlash",
        "prompt": "Muammoni aniqlash, birinchi oddiy namunani yaratish va foydali loyihalarni boshlash qadamlari."
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
