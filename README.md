# 🎬 TasvirLab — Bolalar va O'smirlar uchun Ta'limiy AI Video Platformasi

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v3-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**TasvirLab** — 2 yoshdan 19 yoshgacha bo'lgan bolalar va o'smirlar uchun yuqori sifatli, pedagogik talablarga mos, animatsion ta'limiy videolarni (ssenariy, Mohir AI o'zbekcha Lola ustoz ovozi, animatsion sahnalar, subtitrlar va fon musiqasi) to'liq avtomatik tarzda yaratuvchi professional sun'iy intellekt veb-platformasi.

---

## 🌟 Asosiy Imkoniyatlar

1. **Studiyaviy Video Generator (5 bosqichli):**
   - **Yosh toifalari:** 6 xil pedagogik toifa (2-4, 5-7, 8-10, 11-12, 13-15, 16-19 yosh).
   - **Vizual uslublar:** Pixar 3D, Ghibli Anime, Ertaknamo Akvarel, Ilmiy Kiber, Zamonaviy Vektor.
   - **Xavfsizlik qalqoni (Safety Shield):** COPPA va bolalar psixologiyasi talablariga mos ssenariy auditi.
   - **Sun'iy Intellekt:** Google Gemini AI orqali yoshga moslashtirilgan pedagogik matn va interaktiv savollar.
   - **O'zbekcha Ovoz Sintezi:** Mohir AI (Lola ustoz) professional nutq sintezi, dinamik audio ducking va MP4 render.

2. **Foydalanuvchi va Xavfsizlik Tizimi:**
   - O'zbekiston telefon raqamlari orqali SMS OTP tasdiqlash (Eskiz.uz API).
   - Google Sign-In (OAuth 2.0) va rasmiy Telegram avtorizatsiya.
   - JWT sessiyalar va himoyalangan API endpointlar.

3. **To'lov va Monetizatsiya Tizimi:**
   - Yangi ro'yxatdan o'tganlarga 3 ta bepul video sovg'a.
   - O'zbekistonning yetakchi to'lov tizimlari: **Payme, Click, Uzum Bank va Paynet** integratsiyalari.
   - Xavfsiz webhooklar va tranzaksiyalar auditi.

4. **Administrator Boshqaruv Markazi (Admin Dashboard):**
   - Real-vaqtli moliyaviy va iqtisodiy tahlil (foydalanuvchilar soni, tushum, kreditlar sarfi).
   - Foydalanuvchilarni qidirish, bloklash va balanslarini to'g'ridan-to'g'ri boshqarish.
   - Tavsiyaviy ta'lim mavzularini qo'shish va tahrirlash.
   - Barcha tashqi API kalitlari (Gemini, Mohir AI, Telegram, Google, Payme, Click)ni xavfsiz boshqarish.

---

## 🚀 Ishga Tushirish

### 1. Talablar:
- [Python 3.10](https://www.python.org/) yoki undan yuqori
- FFmpeg (video render uchun)

### 2. O'rnatish:
```bash
# Loyihani klonlash:
git clone https://github.com/username/tasvirlab.git
cd tasvirlab

# Virtual muhit yaratish va faollashtirish:
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Kerakli paketlarni o'rnatish:
pip install -r requirements.txt
```

### 3. Muhit Sozlamalari (.env):
`.env.example` faylidan nusxa oling va kalitlarni to'ldiring:
```bash
cp .env.example .env
```
Kerakli kalitlar:
- `MOHIRAI_API_KEY` — [mohir.ai](https://mohir.ai) dan olingan token
- `GEMINI_API_KEY` — [Google AI Studio](https://aistudio.google.com) kaliti

### 4. Serverni Ishga Tushirish:
**Windows uchun qulay usul:** `ishga_tushirish.bat` fayliga 2 marta bosing.

**Terminal orqali:**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Brauzerda oching: **[http://localhost:8000](http://localhost:8000)**

---

## 📂 Loyiha Tuzilmasi

```
TasvirLab/
├── backend/
│   ├── config.py              # Markaziy konfiguratsiya va muhit o'zgaruvchilari
│   ├── database.py            # SQLite / SQLAlchemy bazaga ulanish
│   ├── models.py              # Foydalanuvchi, Tranzaksiya, Video modellari
│   ├── security.py            # Parol xesh va JWT token xizmatlari
│   ├── main.py                # FastAPI ilovasi va markaziy marshrutlar
│   ├── video_engine.py        # Kadrlar yig'ish, audio va MP4 render vositasi
│   ├── audio_engine.py        # Mohir AI TTS va audio montaj
│   ├── screenplay_engine.py   # Gemini AI pedagogik ssenariy generatori
│   ├── safety_shield.py       # Bolalar xavfsizligi va axloqiy filtr
│   └── routes/
│       ├── admin_routes.py    # Admin paneli (statistika, foydalanuvchilar, kalitlar)
│       ├── auth_routes.py     # SMS OTP, Google, Telegram avtorizatsiya
│       └── billing_routes.py  # Payme, Click, Uzum, Paynet webhook va tariflar
├── frontend/
│   ├── index.html             # Asosiy studiya interfeysi
│   ├── app.js                 # Reaktiv mijoz mantig'i va API integratsiyasi
│   └── main.css               # Maxsus animatsiyalar va dizayn
├── static/
│   ├── images/                # Uslub rasmlari, logotiplar va avatarlar
│   └── renders/               # Yaratilgan video va audiolarning lokal xotirasi
├── requirements.txt           # Python bog'liqliklar ro'yxati
├── .env.example               # Muhit o'zgaruvchilari namunasi
├── .gitignore                 # Maxfiy va render fayllarini himoyalash
├── Dockerfile                 # Docker konteyner fayli
├── docker-compose.yml         # Konteynerlarni birgalikda yurgazish
├── ishga_tushirish.bat        # 1-bosishda tezkor ishga tushirish skripti
└── README.md                  # Loyiha hujjatlari
```

---

## 🛡️ Xavfsizlik

- Barcha maxfiy kalitlar va tokenlar `.env` faylida saqlanadi va `.gitignore` orqali himoyalangan.
- Administrator paneli kuchli xesh parollar va JWT orqali himoyalangan.
- To'lov webhooklari tranzaksiya yaxlitligini tekshiradi.

---

## 📄 Litsenziya
Ushbu loyiha MIT litsenziyasi ostida taqdim etiladi.
