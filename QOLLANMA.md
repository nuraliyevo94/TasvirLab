# 🎬 TasvirLab — Professional AI Veb-Platformasi Qo'llanmasi

Ushbu loyiha 2–19 yoshdagi bolalar va o'smirlar uchun ta'limiy AI videolarni (ssenariy, Mohir AI o'zbekcha ovozi, animatsiya, subtitr va fon musiqasi) to'liq avtomatik tarzda yaratib beruvchi **professional veb-platforma** hisoblanadi.

---

## 🚀 1. Platformani Ishga Tushirish (Tezkor)

1. **`E:\TasvirLab`** papkasiga kiring.
2. **`ishga_tushirish.bat`** fayli ustiga sichqoncha bilan **2 marta bosing**.
3. Server avtomatik tarzda virtual muhitni aniqlaydi va brauzeringizda **[http://localhost:8000](http://localhost:8000)** sahifasini ochadi!

---

## 💻 2. Terminal Orqali Ishga Tushirish

```powershell
# Virtual muhit mavjud bo'lsa:
.\.venv\Scripts\activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Yoki to'g'ridan-to'g'ri python orqali:
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Brauzerda: **`http://localhost:8000`** sahifasini oching.

---

## 🌟 3. Platformaning Asosiy Modullari

1. **Studiyaviy Generator (5 bosqichli):**
   - **1-bosqich:** 6 xil yosh toifasi (2-4, 5-7, 8-10, 11-12, 13-15, 16-19 yosh);
   - **2-bosqich:** Mavzu, prompt va vizual uslub tanlash (Pixar 3D, Ghibli Anime, Ertaknamo Akvarel, Ilmiy Kiber, Vektor);
   - **3-bosqich:** COPPA va bolalar xavfsizligi auditi (Safety Shield);
   - **4-bosqich:** Gemini AI ssenariysi, sahnalar taqsimoti, subtitrlar;
   - **5-bosqich:** Mohir AI ovoz sintezi, fon musiqasi (BGM ducking) va MP4 video eksporti.

2. **Foydalanuvchi Tizimi va Xavfsizlik:**
   - SMS OTP (Eskiz.uz) orqali O'zbekiston raqamlariga tasdiqlash;
   - Telegram Login Widget va Google OAuth qo'llab-quvvatlovi;
   - JWT autentifikatsiya va sessiyalarni boshqarish.

3. **To'lov va Kreditlar Tizimi:**
   - 3 ta bepul sinov videosi (ro'yxatdan o'tganda);
   - Payme va Click integratsiyasi uchun tayyor billing tizimi;
   - 7 tadan 150 tagacha dars paketlari va oylik obuna.

---

## 🔑 4. API Kalitlar (.env fayli)

`E:\TasvirLab\.env` faylida barcha kalitlar saqlanadi:
- **`MOHIRAI_API_KEY`**: O'zbekcha bolalar nutqi (Mohir AI Lola ustoz);
- **`GEMINI_API_KEY`**: Google Gemini AI (ssenariy yaratish va xavfsizlik filtri);
- **`ELEVENLABS_API_KEY`**: Qo'shimcha xalqaro ovozlar;
- **`TELEGRAM_BOT_TOKEN`**: Telegram orqali avtorizatsiya va bot integratsiyasi;
- **`ESKIZ_EMAIL` & `ESKIZ_PASSWORD`**: O'zbekiston raqamlariga SMS OTP yuborish.

---

## 📁 5. Toza Loyiha Tuzilishi:

```
E:\TasvirLab/
├── backend/                  # FastAPI server, AI dvigatellari va marshrutlar
│   ├── routes/               # auth_routes, billing_routes, video_routes
│   ├── auth.py               # JWT va xavfsizlik
│   ├── config.py             # Global sozlamalar va konfiguratsiya
│   ├── database.py           # SQLAlchemy SQLite bazasi
│   ├── main.py               # FastAPI asosiy kirish nuqtasi
│   ├── models.py             # User, Video, Transaction modellari
│   ├── safety.py             # Bolalar xavfsizligi auditi (COPPA)
│   ├── scene_illustrator.py  # Tasvirlar generatsiyasi
│   ├── screenwriter.py       # Gemini AI pedagogik ssenarist
│   ├── sms_service.py        # Eskiz.uz SMS xizmati
│   ├── tts_mohirai.py        # Mohir AI o'zbekcha ovoz sintezi
│   ├── video_engine.py       # Generative video dvigateli
│   └── video_export_engine.py# FFmpeg / Canvas video eksport
├── frontend/                 # Professional veb-interfeys
│   ├── images/               # Dizayn va toifalar rasmlari
│   ├── index.html            # Asosiy veb sahifa
│   ├── style.css             # Zamonaviy Tailwind/Custom stillar
│   └── app.js                # Studiya boshqaruvi, audio ducking, canvas
├── static/                   # Statik resurslar
│   ├── audio/                # Studiya BGM musiqalari va ovoz namunalari
│   ├── images/               # Tizim rasmlari
│   └── renders/              # Generatsiya qilingan fayllar
├── tests/                    # Tizim testlari
├── tools/                    # Yordamchi vositalar
├── .env                      # API kalitlar
├── requirements.txt          # Python kutubxonalari
├── tasvirlab.db              # SQLite ma'lumotlar bazasi
└── ishga_tushirish.bat       # 1-bosishda ishga tushiruvchi fayl
```
