# 🎬 KidsVidEdu — Bolalar Uchun AI Ta'limiy Video Studiyasi

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688?logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?logo=google&logoColor=white)
![Mohir AI](https://img.shields.io/badge/TTS-Mohir%20AI%20Uzbek-8A2BE2)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**12 yoshgacha bo'lgan bolalar uchun sun'iy intellekt asosida pedagogik xavfsiz, o'zbekcha ovozli (Mohir AI) va multfilm animatsiyali ta'limiy video kontent yaratuvchi to'liq avtomatlashtirilgan platforma.**

[Asosiy Imkoniyatlar](#-asosiy-imkoniyatlar) • [Tezkor Ishga Tushirish](#-tezkor-ishga-tushirish-lokal) • [Bulutga Joylash (Server)](#-server-va-bulutga-joylash-deploy) • [Arxitektura](#-arxitektura-va-texnologiyalar) • [Portfolio Tavsiyalari](#-portfolio-uchun-afzalliklari)

</div>

---

## 🌟 Asosiy Imkoniyatlar

### 1. 🛡️ Bolalar Xavfsizligi va COPPA Standarti (Safety Shield)
- Har bir mavzu avtomatlashtirilgan pedagogik va axloqiy tahlildan o'tkaziladi.
- Bolalar psixologiyasiga salbiy ta'sir ko'rsatuvchi, xavfli yoki yoshiga nomunosib elementlar cheklanadi.
- Milliy odob-axloq, mehr-oqibat va kattalarga hurmat tamoyillari integratsiya qilingan.

### 2. 🧠 Gemini AI Ta'limiy Ssenarist
- Bolalarning yosh toifasi (3-4, 5-7, 8-10, 11-12 yosh) bo'yicha maxsus moslashtirilgan pedagogik ssenariy.
- Har bir dars qadamba-qadam tushuntirish, qiziqarli savol va mustahkamlovchi xulosani o'z ichiga oladi.
- Nutqda sonlar doimo to'liq o'zbekcha so'z bilan ifodalanadi (nutq sintezi to'g'ri va ravon o'qishi uchun).

### 3. 👩‍🏫 Mohir AI O'zbek Tili Nutq Sintezi (Lola ustoz)
- O'zbek tilining fonetik qoidalariga to'liq mos keluvchi, bolalarbop samimiy va mehrli ovoz.
- Audio va kadr animatsiyasining millisekund darajasida aniq sinxronizatsiyasi.

### 4. 🎨 Interaktiv Multfilm Doskasi va Suzuvchi Piktogrammalar
- HTML5 Canvas 2D texnologiyasiga asoslangan Full HD (1080p) dinamik video kadrlar.
- Mavzuga doir suzuvchi piktogrammalar (emojilar), formulalar va so'zma-so'z ravshan subtitrlar.
- Kadrlarda ortiqcha texnik yozuvlar yo'q — faqat toza, rang-barang ta'limiy multfilm dizayni.

### 5. 🎵 Studiya Darajasidagi BGM va Sidechain Audio Ducking
- Bolalar kayfiyatiga mos 5 xil professional studiya va orkestr kuylari (Quvnoq marimba, Multfilm ritmi, Mayin pianino, Sehrli ertak, Shijoatli ragtime).
- **Sidechain Audio Ducking (Web Audio API):** Ustoz gapirganda fon musiqasi avtomatik silliq -64% ga pasayadi, pauzada esa to'liq ko'tariladi.
- **Ikki kanalli miksher va maxsus musiqa:** Nutq va musiqa balandligini alohida boshqarish hamda o'z MP3 musiqangizni yuklash imkoniyati.

### 6. 📥 Ovozli Haqiqiy Video Eksport (MP4 / WebM)
- Video va audio (Mohir AI nutqi + balanslangan fon musiqasi) bitta oqimga birlashtirilib, to'liq ovozli haqiqiy video formatida yuklab olinadi.

---

## 🚀 Tezkor Ishga Tushirish (Lokal)

### 1. Repozitoriyani klonlash:
```bash
git clone https://github.com/USERNAME/kidsvidedu.git
cd kidsvidedu
```

### 2. Virtual muhit yaratish va faollashtirish:
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

### 4. API kalitlarni sozlash:
`.env.example` faylidan `.env` nusxasini oling:
```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```
`.env` fayliga o'z kalitlaringizni kiriting (kalitsiz ham zaxira rejimida to'liq ishlaydi):
- `MOHIRAI_API_KEY` — [UzbekVoice.ai](https://uzbekvoice.ai)
- `GEMINI_API_KEY` — [Google AI Studio](https://aistudio.google.com)

### 5. Loyihani ishga tushirish:
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Brauzerda oching: **`http://localhost:8000`** 🎉

---

## 🐳 Docker Orqali Ishga Tushirish

Birgina buyruq bilan butun tizimni konteynerda ishga tushirishingiz mumkin:

```bash
docker-compose up --build
```
Server avtomatik tarzda `http://localhost:8000` manzilida ishga tushadi.

---

## ☁️ Server va Bulutga Joylash (Deploy)

Loyihani istalgan bepul bulutli xizmatga osonlik bilan joylab, boshqalar ko'rishi uchun havolani (link) ulashishingiz mumkin:

### Usul 1: Render.com (Bepul & Tavsiya etiladi)
1. [Render.com](https://render.com) ga kiring va GitHub profilingiz bilan bog'lang.
2. **New +** tugmasini bosing va **Web Service** ni tanlang.
3. Ushbu GitHub repozitoriyangizni tanlang.
4. Render loyihadagi `render.yaml` faylini avtomatik taniydi:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables** bo'limida `MOHIRAI_API_KEY` va `GEMINI_API_KEY` ni kiriting.
6. **Create Web Service** tugmasini bosing. 2 daqiqada loyihangiz bepul onlayn URL (`https://kidsvidedu.onrender.com`) orqali hamma uchun ishlaydi!

### Usul 2: Railway.app
1. [Railway.app](https://railway.app) ga kiring.
2. **New Project** -> **Deploy from GitHub repo** ni tanlang.
3. Repozitoriyani tanlang, `Procfile` avtomatik ishga tushadi.
4. O'zgaruvchilarni (Variables) qo'shing va sayt tayyor!

### Usul 3: Hugging Face Spaces (Docker)
1. [Hugging Face Spaces](https://huggingface.co/spaces) ga kiring.
2. **Create New Space** bosing, SDK sifatida **Docker** ni tanlang.
3. Repozitoriya fayllarini yuklang yoki GitHub bilan sinxronlang.

---

## 🏗️ Arxitektura va Texnologiyalar

```
kidsvidedu/
├── backend/
│   ├── main.py              # FastAPI server, REST API va Static mountlar
│   ├── config.py            # Yosh guruhlari, BGM treklari va mavzular
│   ├── safety.py            # COPPA xavfsizlik va axloqiy filtrlash dvigateli
│   ├── screenwriter.py      # Gemini AI asosidagi bolalar ta'limiy ssenaristi
│   ├── scene_illustrator.py # Dinamik multfilm kadrlar vizualizatori
│   ├── tts_mohirai.py       # Mohir AI o'zbekcha nutq sintezi (Lola ustoz)
│   └── video_engine.py      # Audio-vizual sinxronizatsiya
│
├── frontend/
│   ├── index.html           # 5 bosqichli zamonaviy interaktiv UI
│   ├── style.css            # Glassmorphic dizayn va moslashuvchan maket
│   └── app.js               # Canvas 2D Cinema Player, Web Audio DSP va eksport
│
├── static/
│   ├── audio/               # 5 xil ta'limiy fon musiqalari (WAV loop)
│   └── renders/             # Generatsiya qilingan kadr va audio fayllar
│
├── Dockerfile               # Konteynerizatsiya
├── docker-compose.yml       # Docker orkestratsiyasi
├── Procfile                 # Cloud PaaS (Render, Railway)
├── render.yaml              # 1-klikda deploy sozlamalari
├── requirements.txt         # Python paketlari
├── .env.example             # Konfiguratsiya shabloni
├── .gitignore               # Xavfsizlik va keraksiz fayllar filtri
└── README.md                # Hujjatlashtirish
```

### 🛠️ Texnologiyalar:
- **Backend:** Python 3.11, FastAPI, Uvicorn, HTTPX, Pydantic, Python-dotenv.
- **Frontend:** Vanilla JavaScript (ES6+), HTML5 Canvas 2D, Web Audio API, MediaRecorder API, TailwindCSS.
- **Sun'iy Intellekt:** Google Gemini API (Pedagogik ssenariy), Mohir AI / UzbekVoice API (O'zbek tili TTS).

---

## 💼 Portfolio Uchun Afzalliklari

Ushbu loyiha sizning **GitHub portfoliongizda** quyidagi kuchli muhandislik jihatlarini namoyish etadi:

1. **Full-Stack AI Integratsiyasi:** Katta til modellari (LLM) va nutq sintezini (TTS) yagona real-vaqt tizimiga birlashtirish.
2. **Web Audio API va Raqamli Audio Ishlov (DSP):** Brauzer ichida nutq va fon musiqalarini mikslash, gain boshqaruvi va stereo sinxronizatsiya.
3. **HTML5 Canvas 2D Animatsiya:** SVG/Vektor va matnlarni to'qnashuvlarsiz (clipping & dynamic auto-scale) 60 FPS rejimida renderlash.
4. **Haqiqiy Video Eksport:** MediaRecorder va canvas capture yordamida brauzerning o'zida Full HD video va audioni generatsiya qilib fayl sifatida yuklab olish.
5. **Mahsulot Dizayni va Pedagogik Xavfsizlik:** Bolalar psixologiyasi va COPPA standartlariga mos real muammoni hal qiluvchi amaliy yechim.

---

## 📄 Litsenziya

Ushbu loyiha [MIT Litsenziyasi](LICENSE) asosida ochiq manbalidir.
Ta'limiy va notijorat maqsadlarda bemalol foydalanish, o'zgartirish va rivojlantirish mumkin.
