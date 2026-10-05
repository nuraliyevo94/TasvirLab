import json
import re
import httpx
from typing import Dict, Any, List, Optional
from backend.config import Config, AGE_GROUPS

class QuizEngine:
    """O'qituvchilar va ota-onalar uchun professional ta'limiy test va viktorina generatori."""

    @staticmethod
    async def generate_quiz(
        topic: str,
        age_group: str = "5-7",
        screenplay: Optional[Dict[str, Any]] = None,
        api_key: str = ""
    ) -> Dict[str, Any]:
        """Video ssenariysida aynan o'rgatilgan bilimlar bo'yicha professional nazariy test savollarini yaratadi."""
        gemini_key = api_key or Config.GEMINI_API_KEY
        screenplay = screenplay or {}

        # 1. Gemini AI orqali ssenariyga 100% bog'langan nazariy test yaratish
        if gemini_key:
            try:
                quiz = await QuizEngine._generate_with_gemini(
                    topic, age_group, screenplay, gemini_key
                )
                if quiz and quiz.get("questions") and len(quiz["questions"]) >= 2:
                    return quiz
            except Exception as e:
                print(f"[QuizEngine] Gemini xatolik: {e}. Zaxira generator ishga tushirilmoqda.")

        # 2. Zaxira pedagogik generator (Offline / Ssenariyga qat'iy bog'langan nazariy savollar)
        return QuizEngine._generate_contextual_quiz(topic, age_group, screenplay)

    @staticmethod
    async def _generate_with_gemini(
        topic: str,
        age_group: str,
        screenplay: Dict[str, Any],
        api_key: str
    ) -> Optional[Dict[str, Any]]:
        age_info = AGE_GROUPS.get(age_group, AGE_GROUPS.get("5-7", {}))
        age_desc = age_info.get("style_desc", "Bolalar uchun sodda va qiziqarli")
        
        # Ssenariy matnini to'plash
        scenes = screenplay.get("scenes", [])
        scenes_text = "\n".join([
            f"- {s.get('title', '')}: {s.get('narration', '')}"
            for s in scenes
        ])
        moral = screenplay.get("moral_summary", "")

        prompt = f"""Siz maktabgacha va maktab ta'limi bo'yicha professional metodist va tajribali pedagog-o'qituvchisiz.
Quyida keltirilgan video darsning SSENARIY MATNI asosida o'quvchining mavzuni qanday o'zlashtirganini baholash uchun 3 ta aniq, jiddiy va mazmunli nazariy test savolini tuzing.

MAVZU: {topic}
YOSH GURUHI: {age_group} yosh ({age_desc})

DARSNING ANIQ SSENARIY MATNI (SAHNALAR):
{scenes_text if scenes_text else topic}

TARBIYAVIY SABOQ / XULOSA:
{moral if moral else "Dars sabog'i"}

QAT'IY PEDAGOGIK TALABLAR (BUZILMAS QOIDALAR):
1. ANIQ NAZARIY SAVOL BERILSIN (SAVIYASI YUQORI BO'LSIN):
   - Savollar bevosita mavzudagi qoida, tabiiy yoki mantiqiy tushuncha, fakt yoki amaliy ko'nikma bo'yicha professional tilda berilsin.
   - "Ustoz nima dedi?", "Videoda nima deb aytildi?", "1-sahnada nima bo'ldi?", "Eshitganingizdek..." kabi yuzaki, saviyasi past so'zlar ASLO ISHLATILMASIN!
   - Savolning o'zida javobni ochib qo'yuvchi yoki to'g'ri javobni bildirib qo'yuvchi ishoralar mutlaqo bo'lmasin! Savol bolani mustaqil o'ylashga undasin.
   Misollar:
   ❌ XATO (saviyasi past / javobni ochib qo'ygan): "Videoda ustoz 2 ga 2 ni qo'shganda 4 ta olma bo'ldi dedi, nechta bo'ldi?"
   ✅ TO'G'RI (aniq nazariy): "Ikkita olmaga yana ikkita olma qo'shilsa, natijada jami nechta olma hosil bo'ladi?"
   ❌ XATO (saviyasi past): "Videoda aytilganidek, qizil chiroqda to'xtaladi, qizil chiroqda nima qilish kerak?"
   ✅ TO'G'RI (aniq nazariy): "Svetoforning qizil chirog'i yo'l harakati qatnashchilariga qanday talabni bildiradi?"
   ❌ XATO: "Videodagi 'Piyodalar yo'lagi' qismida nima deb tushuntirildi?"
   ✅ TO'G'RI (aniq nazariy): "Piyodalar yo'lning qatnov qismini xavfsiz kesib o'tishlari uchun qaysi maxsus yo'lakdan foydalanishlari shart?"

2. MAZMUN CHEGARASI (FAQAT SSENARIY FAKTLARI):
   - Savol va to'g'ri javob FAQAT yuqoridagi ssenariy matnida tushuntirilgan bilim va ma'lumotlarga tayansin.
   - Ssenariyda aytilmagan, videoda tilga olinmagan begona faktlar yoki mavzudan tashqari yangi narsalar aslo so'ralmasin.

3. VARIANTLAR VA DISTRAKTORLAR:
   - Har bir savol uchun 3 ta mantiqiy variant (A, B, C) bering.
   - Noto'g'ri variantlar mavzuga yaqin, mantiqli, lekin qoidaga zid bo'lsin.
   - "correct_index" — to'g'ri javob indeksi (0, 1 yoki 2).

4. IZOH (EXPLANATION):
   - Nega bu javob to'g'ri ekanligini tushuntiruvchi 1-2 gaplik aniq pedagogik xulosa.

5. JSON FORMAT:
   - Javobni FAQAT quyidagi JSON formatida qaytaring:

{{
  "quiz_title": "Darslik Testi: {topic}",
  "topic": "{topic}",
  "age_group": "{age_group}",
  "moral_takeaway": "{moral if moral else 'Bilim olish insonni dono qiladi.'}",
  "questions": [
    {{
      "id": 1,
      "question": "Aniq nazariy savol matni?",
      "options": ["A varianti", "B varianti", "C varianti"],
      "correct_index": 0,
      "explanation": "To'g'ri javobning pedagogik izohi..."
    }}
  ]
}}"""

        models_to_try = [
            "models/gemini-flash-latest",
            "models/gemini-2.5-flash",
            "models/gemini-pro-latest"
        ]

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.15,
                "topP": 0.8,
                "maxOutputTokens": 1024
            }
        }

        async with httpx.AsyncClient(timeout=14.0) as client:
            for model_name in models_to_try:
                url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
                try:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        match = re.search(r'(\{[\s\S]*\})', raw_text)
                        json_str = match.group(1) if match else raw_text
                        parsed = json.loads(json_str)
                        if parsed and "questions" in parsed and len(parsed["questions"]) >= 2:
                            return parsed
                except Exception as ex:
                    print(f"[QuizEngine] Model {model_name} xatolik: {ex}")

        return None

    @staticmethod
    def _generate_contextual_quiz(
        topic: str,
        age_group: str,
        screenplay: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ssenariy asosida professional nazariy test savollarini tuzish (Zaxira generator)."""
        t_lower = topic.lower()
        scenes = screenplay.get("scenes", [])
        narrations = " ".join([s.get("narration", "") for s in scenes]).lower()
        combined = f"{t_lower} {narrations}"
        moral = screenplay.get("moral_summary", "Bilim — eng katta boylikdir!")

        questions = []

        # 1. Matematika (qo'shish/ayirish/sanash)
        if any(w in combined for w in ["matematika", "qo'shish", "ayirish", "karra", "2 + 2", "sanaymiz", "raqam"]):
            questions = [
                {
                    "id": 1,
                    "question": "Ikkita buyumga yana ikkita buyum qo'shilsa, jami soni nechaga teng bo'ladi?",
                    "options": ["4 ga", "3 ga", "5 ga"],
                    "correct_index": 0,
                    "explanation": "To'g'ri! 2 ga 2 ni qo'shganda natija 4 bo'ladi (2 + 2 = 4)!"
                },
                {
                    "id": 2,
                    "question": "Narsalarni bir-biriga birlashtirish va umumiy miqdorini aniqlash uchun qaysi matematik amal bajariladi?",
                    "options": ["Qo'shish amali (+)", "Ayirish amali (-)", "Bo'lish amali (÷)"],
                    "correct_index": 0,
                    "explanation": "Ofarin! Narsalarni qo'shib umumiy sonini topish uchun qo'shuv (+) amali ishlatiladi!"
                },
                {
                    "id": 3,
                    "question": "Hisoblash va sanash qoidalarini bilish inson uchun qanday amaliy ahamiyatga ega?",
                    "options": [
                        "Narsalarni to'g'ri taqsimlash va hisoblash imkonini beradi",
                        "Faqat daftarga chizish uchun xizmat qiladi",
                        "Hech qanday foydasi yo'q"
                    ],
                    "correct_index": 0,
                    "explanation": "Juda to'g'ri! Matematika hayotda adolatli taqsimlash va aniq hisoblashda eng zarur fandir!"
                }
            ]
        # 2. Yo'l harakati va xavfsizlik
        elif any(w in combined for w in ["yo'l", "zebra", "svetofor", "piyoda", "harakat", "qizil chiroq", "yashil chiroq"]):
            questions = [
                {
                    "id": 1,
                    "question": "Piyodalar yo'lning qatnov qismini xavfsiz kesib o'tishlari uchun qaysi maxsus yo'lakdan foydalanishlari shart?",
                    "options": [
                        "Zebra (piyodalar o'tish) chizig'idan",
                        "Yo'lning mashinalar to'xtamasdan o'tayotgan istalgan qismidan",
                        "Faqat yo'lning o'rtasidagi to'siqlar ustidan"
                    ],
                    "correct_index": 0,
                    "explanation": "To'ppa-to'g'ri! Piyodalar yo'lni faqat maxsus chizilgan zebra yo'lagidan kesib o'tishlari shart!"
                },
                {
                    "id": 2,
                    "question": "Svetoforning qizil chirog'i yo'l harakati qatnashchilariga qanday talabni bildiradi?",
                    "options": [
                        "Harakatni qat'iy to'xtatish va kutishni",
                        "Tezroq yugurib o'tib ketishni",
                        "Faqat atrofdagilarga qo'l siltashni"
                    ],
                    "correct_index": 0,
                    "explanation": "Ofarin! Qizil chiroq taqiqlovchi belgi bo'lib, harakatni darhol to'xtatishni talab qiladi!"
                },
                {
                    "id": 3,
                    "question": "Svetoforning qaysi chirog'i yonganda piyodalarga yo'ldan xotirjam qadam tashlab o'tishga ruxsat beriladi?",
                    "options": ["Yashil chiroq", "Qizil chiroq", "Sariq chiroq"],
                    "correct_index": 0,
                    "explanation": "Barakalla! Yashil chiroq piyodalar uchun yo'ldan xotirjam o'tishga ruxsat etuvchi belgidir!"
                }
            ]
        # 3. Suv va tabiat hodisalari
        elif any(w in combined for w in ["suv", "tomchi", "yomg'ir", "bulut", "daryo", "dengiz", "bug'"]):
            questions = [
                {
                    "id": 1,
                    "question": "Suv quyosh issiqligi ta'sirida qiziganida qanday tabiiy holatga o'tadi?",
                    "options": [
                        "Bug'ga aylanib yuqoriga ko'tariladi",
                        "Muzga aylanib pastga cho'kadi",
                        "Qumga aylanib qoladi"
                    ],
                    "correct_index": 0,
                    "explanation": "To'g'ri! Suv isiganda bug'lanib, yengil holatda yuqoriga parvoz qiladi!"
                },
                {
                    "id": 2,
                    "question": "Osmonda to'plangan mayda suv tomchilari birikib og'irlashganda yerga nima bo'lib tushadi?",
                    "options": [
                        "Yomg'ir yoki qor ko'rinishida",
                        "Kuchli quyosh nuri ko'rinishida",
                        "Rangli sharlar ko'rinishida"
                    ],
                    "correct_index": 0,
                    "explanation": "Ofarin! Suv tomchilari birlashib og'irlashadi va yomg'ir bo'lib yerga yog'adi!"
                },
                {
                    "id": 3,
                    "question": "Tabiatdagi o'simliklar va tirik organizmlar rivojlanishi uchun suv nima sababdan zarur?",
                    "options": [
                        "Chanqoqni qondirish va hayotiy o'sishni ta'minlash uchun",
                        "Faqat tuproqni sovitish uchun",
                        "Hech qanday ahamiyati yo'q"
                    ],
                    "correct_index": 0,
                    "explanation": "Barakalla! Suv barcha tirik organizmlarning yashashi va gullab-yashnashi uchun asosiy manbadir!"
                }
            ]
        # 4. Koinot va sayyoralar
        elif any(w in combined for w in ["koinot", "quyosh", "sayyora", "oy", "yulduz", "yer"]):
            questions = [
                {
                    "id": 1,
                    "question": "Yer yuziga tabiiy yorug'lik va iliqlik yetkazib beruvchi eng asosiy manba nima?",
                    "options": ["Quyosh yulduzi", "Oy", "Kometa"],
                    "correct_index": 0,
                    "explanation": "To'g'ri! Quyosh — sayyoramizni yorituvchi va isituvchi yagona markaziy yulduzdir!"
                },
                {
                    "id": 2,
                    "question": "Biz yashab turgan va hayot mavjud bo'lgan sayyora qanday ataladi?",
                    "options": ["Yer sayyorasi", "Yupiter", "Mars"],
                    "correct_index": 0,
                    "explanation": "Barakalla! Biz yashaydigan ona sayyoramiz — Yer deb ataladi!"
                },
                {
                    "id": 3,
                    "question": "Tungi osmonda Yer atrofida aylanib yorug'lik taratuvchi tabiiy yo'ldosh nima?",
                    "options": ["Oy", "Quyosh", "Katta ayiq"],
                    "correct_index": 0,
                    "explanation": "Ofarin! Oy — Yerning yagona tabiiy yo'ldoshi hisoblanadi!"
                }
            ]
        # 5. Umumiy ta'limiy mavzular
        else:
            questions = [
                {
                    "id": 1,
                    "question": f"«{topic}» mavzusida o'rganilgan asosiy qoidaning mohiyati nimadan iborat?",
                    "options": [
                        f"{topic} qoidalariga doimo to'g'ri amal qilish",
                        "O'rganilgan bilimlarni darhol unutish",
                        "Mavzuga e'tiborsiz qarash"
                    ],
                    "correct_index": 0,
                    "explanation": f"Ofarin! «{topic}» bo'yicha to'g'ri bilimlarga ega bo'lish har birimiz uchun muhimdir!"
                },
                {
                    "id": 2,
                    "question": "Olingan yangi ta'limiy saboqni esda saqlab qolish uchun nima qilish tavsiya etiladi?",
                    "options": [
                        "Uni kundalik hayotda qo'llash va mustahkamlash",
                        "Hech kimga aytmasdan yashirish",
                        "Vaqtni behuda narsalarga sarflash"
                    ],
                    "correct_index": 0,
                    "explanation": "Barakalla! Olingan bilimni amalda qo'llash uni mustahkam qiladi!"
                },
                {
                    "id": 3,
                    "question": "Ushbu darsning bosh tarbiyaviy sabog'i nima hisoblanadi?",
                    "options": [
                        moral,
                        "Tartibsizlik va e'tiborsizlik",
                        "Faqat o'yin o'ynash"
                    ],
                    "correct_index": 0,
                    "explanation": f"To'ppa-to'g'ri! Darsimizning eng muhim sabog'i: «{moral}»!"
                }
            ]

        return {
            "quiz_title": f"Darslik Testi: {topic}",
            "topic": topic,
            "age_group": age_group,
            "moral_takeaway": moral,
            "questions": questions
        }
