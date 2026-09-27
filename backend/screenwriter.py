import json
import re
import httpx
from typing import Dict, Any, List
from backend.config import Config, AGE_GROUPS, VISUAL_STYLES

class ScreenwriterEngine:
    """NotebookLM Explainer uslubidagi professional bolalar ta'limiy ssenaristi va o'qituvchisi."""

    @staticmethod
    async def generate_screenplay(
        topic: str,
        prompt: str,
        age_group: str,
        duration_seconds: int = 60,
        visual_style_id: str = "pixar_3d",
        language: str = "uz",
        api_key: str = ""
    ) -> Dict[str, Any]:
        
        scene_count = max(3, min(6, round(duration_seconds / 12)))
        style_info = next((s for s in VISUAL_STYLES if s["id"] == visual_style_id), VISUAL_STYLES[0])
        age_info = AGE_GROUPS.get(age_group, AGE_GROUPS["5-7"])
        
        gemini_key = api_key or Config.GEMINI_API_KEY
        if gemini_key:
            try:
                screenplay = await ScreenwriterEngine._generate_with_gemini(
                    topic, prompt, age_info, duration_seconds, scene_count, style_info, language, gemini_key
                )
                if screenplay and screenplay.get("scenes") and len(screenplay["scenes"]) > 0:
                    # Har bir sahnada visual_beats mavjudligini ta'minlash va keraksiz so'zlarni tozalash
                    for sc in screenplay["scenes"]:
                        sc["title"] = ScreenwriterEngine.clean_scene_title(sc.get("title", ""))
                        sc["narration"] = ScreenwriterEngine._sanitize_narration(sc.get("narration", ""))
                        ScreenwriterEngine._enrich_scene_visual_beats(sc, topic)
                    return screenplay
            except Exception as e:
                print(f"Gemini o'qituvchi ssenaristida xatolik: {e}. Zaxira generatorga o'tilmoqda.")

        # Zaxira sifatli va tushunarli o'qituvchi generatori (Offline Fallback)
        screenplay = ScreenwriterEngine._generate_contextual_screenplay(
            topic, prompt, age_info, duration_seconds, scene_count, style_info, language
        )
        for sc in screenplay["scenes"]:
            sc["title"] = ScreenwriterEngine.clean_scene_title(sc.get("title", ""))
            sc["narration"] = ScreenwriterEngine._sanitize_narration(sc.get("narration", ""))
            ScreenwriterEngine._enrich_scene_visual_beats(sc, topic)
        return screenplay

    @staticmethod
    def clean_scene_title(title: str) -> str:
        """Sahna sarlavhasidagi har qanday raqamlarni (1-sahna, Sahna 1, 1-qadam, 1.) butunlay tozalash."""
        if not title:
            return ""
        # 1-sahna:, Sahna 1:, 1. Sahna:, 1 - sahna, 1-qadam, Kadr 1:, etc.
        cleaned = re.sub(r'^(?:\d+[\s\-_.:\)]*(?:sahna|kadr|bosqich|qadam)?|(?:sahna|kadr|bosqich|qadam)\s*\d+)[\s\-_.:\)]*', '', title, flags=re.IGNORECASE)
        cleaned = re.sub(r'^\d+[\s\-_.:\)]+', '', cleaned)
        cleaned = cleaned.strip()
        return cleaned if cleaned else title

    @staticmethod
    def convert_numbers_to_uzbek_words(text: str) -> str:
        """Ssenariy nutqidagi barcha sonlar va amallarni sof o'zbekcha so'zlarga aylantirish (TTS to'g'ri o'qishi uchun)."""
        if not text:
            return ""

        units = {
            0: "nol", 1: "bir", 2: "ikki", 3: "uch", 4: "to'rt", 5: "besh",
            6: "olti", 7: "yetti", 8: "sakkiz", 9: "to'qqiz"
        }
        tens = {
            1: "o'n", 2: "yigirma", 3: "o'ttiz", 4: "qirq", 5: "ellik",
            6: "oltmish", 7: "yetmish", 8: "sakson", 9: "to'qson"
        }

        def int_to_word(n: int) -> str:
            if n in units: return units[n]
            if n < 20: return "o'n " + units[n % 10]
            if n < 100:
                t = tens[n // 10]
                u = units.get(n % 10, "")
                return f"{t} {u}".strip() if (n % 10) != 0 else t
            if n == 100: return "yuz"
            if n < 1000:
                h = (units[n // 100] + " yuz") if (n // 100) > 1 else "yuz"
                rem = n % 100
                return f"{h} {int_to_word(rem)}".strip() if rem else h
            return str(n)

        # 1. Matematik tenglamalar: 2 + 2 = 4 yoki 2+2=4
        def replace_equation(match):
            a, op, b, res = match.groups()
            op_words = {"+": "qo'shuv", "-": "ayruv", "*": "karra", "/": "bo'luv"}
            op_word = op_words.get(op.strip(), "qo'shuv")
            return f"{int_to_word(int(a))} {op_word} {int_to_word(int(b))} teng {int_to_word(int(res))}"
        text = re.sub(r'(\d+)\s*([+\-*\/])\s*(\d+)\s*=\s*(\d+)', replace_equation, text)

        # 2. Matematik amallar: 2 + 2
        def replace_expr(match):
            a, op, b = match.groups()
            op_words = {"+": "qo'shuv", "-": "ayruv", "*": "karra", "/": "bo'luv"}
            op_word = op_words.get(op.strip(), "qo'shuv")
            return f"{int_to_word(int(a))} {op_word} {int_to_word(int(b))}"
        text = re.sub(r'(\d+)\s*([+\-*\/])\s*(\d+)', replace_expr, text)

        # 3. Tartib sonlar: 1-, 2-, 1-sahna, 2-qadam
        ordinals = {
            1: "birinchi", 2: "ikkinchi", 3: "uchinchi", 4: "to'rtinchi", 5: "beshinchi",
            6: "oltinchi", 7: "yettinchi", 8: "sakkizinchi", 9: "to'qqizinchi", 10: "o'ninchi"
        }
        def replace_ordinal(m):
            n = int(m.group(1))
            word = ordinals.get(n, int_to_word(n) + "inchi")
            rest = m.group(2) or ""
            if rest and not rest.startswith(" "):
                rest = " " + rest
            return word + rest
        text = re.sub(r'\b(\d+)\s*-(?:chi)?(\s*[\w\']*)', replace_ordinal, text)

        # 4. Qo'shimchalar: 2 ga, 2-ga, 2 ni, 2 ta, 2 dan, 2 da
        def replace_suffix(m):
            n = int(m.group(1))
            suf = m.group(2).lower()
            w = int_to_word(n)
            if suf == "ta":
                if n == 1: return "bitta"
                return w + "ta"
            if suf in ["ga", "ka", "qa"]:
                return w + "ga"
            if suf == "ni":
                return w + "ni"
            if suf == "dan":
                return w + "dan"
            if suf == "da":
                return w + "da"
            return w + " " + suf
        text = re.sub(r'\b(\d+)\s*-?\s*(ga|ka|qa|ni|ta|dan|da)\b', replace_suffix, text, flags=re.IGNORECASE)

        # 5. Mustaqil qolgan sonlar (masalan: 4, 10)
        def replace_standalone(m):
            n = int(m.group(1))
            return int_to_word(n)
        text = re.sub(r'\b(\d+)\b', replace_standalone, text)

        # 6. Gap boshidagi harflarni to'g'ri katta qilish
        text = re.sub(r'(^|[.!?]\s+)([a-zʻʼ\'])', lambda m: m.group(1) + m.group(2).upper(), text)
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def _sanitize_narration(text: str) -> str:
        """Ijtimoiy tarmoq chaqiriqlarini tozalash va sonlarni so'zga aylantirish."""
        if not text:
            return ""
        banned_patterns = [
            r"(?:javobingizni|fikringizni|o'z fikringizni|javobni)?\s*(?:izohda|izohlarda|kommentariyada|kommentda)\s*(?:yozib\s*qoldiring|qoldiring|yozing|qoldir)[.!]?",
            r"(?:fikringizni|o'z fikringizni)\s*(?:izohlarda|izohda|yozib)?\s*qoldiring[.!]?",
            r"(?:kanalimizga|kanalga)?\s*obuna\s*bo'ling[.!]?",
            r"layk\s*bosing[.!]?",
            r"qo'ng'iroqchani\s*bosing[.!]?",
            r"izohda\s*kutamiz[.!]?"
        ]
        cleaned = text
        for pat in banned_patterns:
            cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        # Sonlarni o'qilishi oson bo'lishi uchun so'zga o'giramiz
        return ScreenwriterEngine.convert_numbers_to_uzbek_words(cleaned)

    @staticmethod
    async def _generate_with_gemini(topic, prompt, age_info, duration_seconds, scene_count, style_info, language, api_key):
        models = ["gemini-flash-lite-latest", "gemini-flash-latest"]
        
        system_instruction = (
            f"Sen bolalar uchun dunyodagi eng tajribali va sevimli virtual o'qituvchisan (NotebookLM Explainer va Khan Academy uslubida). "
            f"O'zbek tilida 12 yoshgacha bo'lgan bolalarga berilgan mavzuni (matematika, tabiat, fan, odob-axloq) "
            f"o'ta sodda, qiziqarli, bosqichma-bosqich va vizual tarzda tushuntirib berasan.\n\n"
            f"QAT'IY PEDAGOGIK TALABLAR:\n"
            f"1. MAVZUNI SHUNCHAKI TAVSIF QILMA, BALKI ANIQ TUSHUNTIR VA O'RGAT! Mavzuning mohiyatini sodda, qiziqarli qilib tushuntir.\n"
            f"2. Har bir sahnada o'qituvchi nutqiga (narration) AYNAN HAMOHANG va 100% MOS ravishda ekranda nimalar chiqishi 'visual_beats' orqali berilsin. Mavzu tabiat bo'lsa tabiat tushunchalari va emojilari (masalan daraxt, barg, quyosh), hayvonlar bo'lsa hayvon emojilari (ayiqcha, quyon), kosmos bo'lsa (sayyoralar, yulduzlar), matematika bo'lsa matematika formulasi chiqsin. Boshqa mavzularga aralashtirish qat'iyan man etiladi!\n"
            f"3. 'visual_beats' da har bir bosqich uchun:\n"
            f"   - 'time_pct': 0.0 dan 1.0 gacha vaqt foizi;\n"
            f"   - 'main_text': ekranda katta bo'lib chiqadigan asosiy so'z yoki formula (masalan: 'Kuz Fasli', 'Oltin Barglar', yoki matematika bo'lsa '2 + 2 = 4');\n"
            f"   - 'sub_text': ushbu sahnaning o'qituvchi nutqiga (narration) aynan mos qisqa tushunarli jumla;\n"
            f"   - 'icons': mavzuga aynan mos 3-4 ta emoji (masalan: ['🌳', '🍁', '🍂'], ['🚀', '🪐', '⭐'], ['🐻', '🐰', '🌲']);\n"
            f"   - 'highlight': natija yoki muhim qoidani ta'kidlash uchun true/false.\n"
            f"4. QAT'IYAN TAQIQLANADI: 'izohda qoldiring', 'kommentariyada yozing', 'fikringizni yozib qoldiring', 'layk bosing', 'kanalga obuna bo'ling' kabi ijtimoiy tarmoq chaqiriqlarini ishlatish MUTLAQO TAQIQLANADI! Nutq xuddi mehribon, samimiy va dono o'qituvchisidek faqat bolani qo'llab-quvvatlash, mehr va aniq bilim berishdan iborat bo'lsin.\n"
            f"5. SONLAR VA RAQAMLAR QOIDASI (O'TA MUHIM): 'narration' (o'qituvchi aytadigan nutq matni) ichida sonlarni HECH QACHON raqam bilan yozma (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)! Har doim o'zbekcha so'z bilan to'liq yoz (masalan: 'ikkiga ikkini qo'shsak to'rt bo'ladi', 'ikkita olma', 'bir, ikki, uch, to'rt', 'ikki qo'shuv ikki teng to'rt'). Chunki audio diktor faqat so'zlarni to'g'ri va ravon o'qiydi. Ekranda ko'rinadigan 'visual_beats' ('main_text', 'sub_text') da esa bolaga tushunarli bo'lishi uchun aniq raqamlar yoki qisqa so'zlar bilan yoz.\n"
            f"6. SAHNA SARLAVHASI (QAT'IY TALAB): Sarlavhada hech qachon '1-sahna:', '2-sahna:', 'Sahna 1', '1-qadam' kabi raqamlarni yozma! Faqat sof mavzu nomini yoz (masalan: 'Savol va Tushuncha', 'Olmalarni Sanaymiz', 'Yashil Barglar Siri', 'Daraxtlarning Oromi')."
        )

        user_prompt = (
            f"Mavzu: {topic}\n"
            f"Qo'shimcha izoh: {prompt}\n"
            f"Yosh toifasi: {age_info['title']} ({age_info['category']})\n"
            f"Jami davomiylik: {duration_seconds} soniya\n"
            f"Sahnalar soni: {scene_count} ta sahna\n"
            f"Uslub: NotebookLM bolalar tushuntiruvchi ta'limiy video\n"
            f"Nutq tili: {language}"
        )

        schema_prompt = (
            f"{system_instruction}\n\nTopshiriq:\n{user_prompt}\n\n"
            f"Javobni quyidagi JSON formatida qaytar:\n"
            f"{{\n"
            f"  \"title\": \"Dars / Video nomi\",\n"
            f"  \"moral_summary\": \"Bugungi darsdan olingan asosiy xulosa\",\n"
            f"  \"scenes\": [\n"
            f"    {{\n"
            f"      \"scene_number\": 1,\n"
            f"      \"title\": \"Savol va Tushuncha\",\n"
            f"      \"duration_seconds\": {round(duration_seconds / scene_count)},\n"
            f"      \"stage\": \"hook\",\n"
            f"      \"narration\": \"(O'qituvchining samimiy, jonli, o'rgatuvchi 2-3 ta gapi)\",\n"
            f"      \"visual_prompt\": \"Clean educational explainer scene showing dynamic chalkboard illustration\",\n"
            f"      \"camera_movement\": \"Sekin yaqinlashish (Dolly In)\",\n"
            f"      \"emotion\": \"quvnoq\",\n"
            f"      \"visual_beats\": [\n"
            f"        {{\n"
            f"          \"time_pct\": 0.0,\n"
            f"          \"badge\": \"Boshlanish\",\n"
            f"          \"main_text\": \"Savol\",\n"
            f"          \"sub_text\": \"Tushuncha bilan tanishamiz\",\n"
            f"          \"icons\": [\"💡\", \"✨\", \"🎯\"],\n"
            f"          \"highlight\": false\n"
            f"        }},\n"
            f"        {{\n"
            f"          \"time_pct\": 0.6,\n"
            f"          \"badge\": \"Xulosa\",\n"
            f"          \"main_text\": \"Natija\",\n"
            f"          \"sub_text\": \"Bilimni mustahkamlaymiz\",\n"
            f"          \"icons\": [\"⭐\", \"🎉\", \"🏆\"],\n"
            f"          \"highlight\": true\n"
            f"        }}\n"
            f"      ]\n"
            f"    }}\n"
            f"  ]\n"
            f"}}"
        )

        payload = {
            "contents": [{"parts": [{"text": schema_prompt}]}],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.6
            }
        }

        async with httpx.AsyncClient(timeout=18.0) as client:
            model_name = "gemini-flash-lite-latest"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            try:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    raw_json = data["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(raw_json)
                    parsed["screenplay_author"] = f"Google Gemini AI ({model_name} Explainer)"
                    return parsed
            except Exception as ex:
                print(f"Gemini model {model_name} xatolik: {ex}")

        return None

    @staticmethod
    def _enrich_scene_visual_beats(scene: Dict[str, Any], topic: str):
        """Har bir sahnaning nutqi va mavzusiga 100% mos keluvchi interaktiv vizual bosqichlar."""
        beats = scene.get("visual_beats")
        if beats and len(beats) >= 2:
            return

        narration = scene.get("narration", "")
        title = scene.get("title", "")
        clean_title = re.sub(r'^\d+\s*-\s*(?:sahna|qadam)\s*:\s*', '', title, flags=re.IGNORECASE).strip()
        if not clean_title or len(clean_title) < 3:
            clean_title = topic
        
        full_text = f"{topic} {clean_title} {narration}".lower()
        
        # 1. Haqiqiy Matematika (qo'shish/ayirish/hisoblash) - qo'shiq yoki qo'shni so'zlari bilan chalkashtirmaymiz
        is_math = ("+" in full_text or "qo'shish amali" in full_text or "matematika" in full_text or "hisoblaymiz" in full_text) and not any(w in full_text for w in ["qo'shiq", "qo'shni", "qo'shil"])
        math_digits = re.findall(r'\b(\d+)\b', f"{clean_title} {narration}")
        
        if is_math and len(math_digits) >= 2:
            n1 = int(math_digits[0])
            n2 = int(math_digits[1])
            ans = n1 + n2
            icon = "🍎"
            if "kitob" in full_text: icon = "📚"
            elif "yulduz" in full_text: icon = "⭐"
            elif "shar" in full_text: icon = "🎈"
            elif "gul" in full_text: icon = "🌸"

            scene["visual_beats"] = [
                {
                    "time_pct": 0.0,
                    "main_text": f"{n1} + {n2}",
                    "sub_text": narration[:80] if len(narration) > 80 else narration,
                    "icons": [icon] * min(4, n1) + ["+"] + [icon] * min(4, n2),
                    "highlight": False
                },
                {
                    "time_pct": 0.55,
                    "main_text": f"{n1} + {n2} = {ans}",
                    "sub_text": f"Jami {ans} bo'ldi!",
                    "icons": [icon] * min(8, ans),
                    "highlight": True
                }
            ]
            return

        # 2. Hayvonlar va Jonivorlar olami
        if any(w in full_text for w in ["hayvon", "ayiq", "quyon", "tulki", "bo'ri", "sher", "mushuk", "kuchuk", "it", "fil", "baliq", "delfin", "qush"]):
            icons = ["🐻", "🐰", "🦊", "🦁"]
            if "baliq" in full_text or "delfin" in full_text or "dengiz" in full_text:
                icons = ["🐬", "🌊", "🐠", "🫧"]
            elif "qush" in full_text:
                icons = ["🐦", "🌿", "🐣", "✨"]
            elif "mushuk" in full_text or "kuchuk" in full_text:
                icons = ["🐱", "🐶", "🐾", "❤️"]

            scene["visual_beats"] = [
                {
                    "time_pct": 0.0,
                    "main_text": clean_title,
                    "sub_text": narration[:75] if len(narration) > 75 else narration,
                    "icons": icons,
                    "highlight": False
                },
                {
                    "time_pct": 0.55,
                    "main_text": "Do'stona Tabiat",
                    "sub_text": narration[75:160] if len(narration) > 75 else narration,
                    "icons": icons,
                    "highlight": True
                }
            ]
            return

        # 3. Fazoviy olam / Kosmos va Quyosh
        if any(w in full_text for w in ["kosmos", "sayyora", "quyosh", "oy", "yulduz", "raketa", "mars", "yer"]):
            icons = ["🚀", "🌍", "🌕", "⭐"]
            scene["visual_beats"] = [
                {
                    "time_pct": 0.0,
                    "main_text": clean_title,
                    "sub_text": narration[:75] if len(narration) > 75 else narration,
                    "icons": icons,
                    "highlight": False
                },
                {
                    "time_pct": 0.55,
                    "main_text": "Mo'jizaviy Koinot",
                    "sub_text": narration[75:160] if len(narration) > 75 else narration,
                    "icons": ["🪐", "✨", "☀️", "🌟"],
                    "highlight": True
                }
            ]
            return

        # 4. Tabiat, Fasllar va Daraxtlar (Kuz, Bahor, Yomg'ir, Suv)
        if any(w in full_text for w in ["daraxt", "barg", "kuz", "bahor", "yoz", "qish", "suv", "tomchi", "yomg'ir", "qor", "bulut"]):
            icons = ["🌳", "🍃", "🍁", "☀️"]
            if "suv" in full_text or "yomg" in full_text:
                icons = ["💧", "🌧️", "☁️", "🌱"]
            elif "qish" in full_text or "qor" in full_text:
                icons = ["❄️", "⛄", "🌲", "✨"]

            scene["visual_beats"] = [
                {
                    "time_pct": 0.0,
                    "main_text": clean_title,
                    "sub_text": narration[:75] if len(narration) > 75 else narration,
                    "icons": icons,
                    "highlight": False
                },
                {
                    "time_pct": 0.55,
                    "main_text": "Tabiat Sabog'i",
                    "sub_text": narration[75:160] if len(narration) > 75 else narration,
                    "icons": icons,
                    "highlight": True
                }
            ]
            return

        # 5. Ranglar va Mevalar
        if any(w in full_text for w in ["rang", "qizil", "sariq", "yashil", "ko'k", "meva", "olma", "banan", "nok"]):
            icons = ["🎨", "🔴", "🟡", "🟢"]
            if "meva" in full_text or "olma" in full_text:
                icons = ["🍎", "🍌", "🍇", "🍓"]

            scene["visual_beats"] = [
                {
                    "time_pct": 0.0,
                    "main_text": clean_title,
                    "sub_text": narration[:75] if len(narration) > 75 else narration,
                    "icons": icons,
                    "highlight": False
                },
                {
                    "time_pct": 0.55,
                    "main_text": "Yorqin Dunyo",
                    "sub_text": narration[75:160] if len(narration) > 75 else narration,
                    "icons": icons,
                    "highlight": True
                }
            ]
            return

        # 6. Umumiy va Boshqa barcha ta'limiy mavzular (Doimo matnga mos)
        icons = ["💡", "✨", "📚", "⭐"]
        if "mashina" in full_text or "poyezd" in full_text:
            icons = ["🚗", "🚦", "🚂", "✈️"]
        elif "musiqa" in full_text or "qo'shiq" in full_text:
            icons = ["🎵", "🎶", "🎸", "🎹"]
        elif "sport" in full_text or "to'p" in full_text:
            icons = ["⚽", "🏀", "🏃", "🏆"]

        scene["visual_beats"] = [
            {
                "time_pct": 0.0,
                "main_text": clean_title,
                "sub_text": narration[:80] if len(narration) > 80 else narration,
                "icons": icons,
                "highlight": False
            },
            {
                "time_pct": 0.55,
                "main_text": "Foydali Bilim",
                "sub_text": narration[80:160] if len(narration) > 80 else narration,
                "icons": icons,
                "highlight": True
            }
        ]

    @staticmethod
    def _generate_contextual_screenplay(topic, prompt, age_info, total_duration, scene_count, style_info, language):
        """Aniq va tushunarli virtual o'qituvchi ssenariysi (Offline rejimda ham to'liq ishlaydi)."""
        clean_topic = topic.strip()
        sec_per_scene = round(total_duration / scene_count)
        text_lower = f"{clean_topic} {prompt}".lower()
        
        # A) Matematika mavzusi (Masalan: 2 ga 2 ni qo'shish)
        if any(w in text_lower for w in ["qo'sh", "+", "matematika", "karra", "2 ga 2", "hisoblash", "son"]):
            return {
                "title": f"Matematika O'qituvchisi: {clean_topic}",
                "moral_summary": "Qo'shish orqali narsalarni birga jamlash va to'g'ri hisoblashni o'rganamiz.",
                "scenes": [
                    {
                        "scene_number": 1,
                        "title": "Olmalarni ko'ramiz",
                        "duration_seconds": sec_per_scene,
                        "stage": "hook",
                        "narration": "Salom bolajonim! Bugun biz birga hisoblashni o'rganamiz. Tasavvur qil, senga ikkita qizil olma berishdi. Keyin yana ikkita olma berishdi. Jami nechta bo'ladi?",
                        "visual_prompt": "Clean bright 3D animated chalkboard with 2 red apples on one side and 2 red apples on the other side",
                        "camera_movement": "Sekin yaqinlashish (Dolly In)",
                        "emotion": "quvnoq"
                    },
                    {
                        "scene_number": 2,
                        "title": "Qo'shish amali (2 + 2)",
                        "duration_seconds": sec_per_scene,
                        "stage": "cause",
                        "narration": "Buni bilish uchun biz ikkiga ikkini qo'shamiz! Qara, doskaga ikki qo'shuv ikki deb yozamiz. Keling, barcha olmalarni birga sanaymiz: bir, ikki, uch, to'rt!",
                        "visual_prompt": "3D animated chalkboard showing equation 2 + 2 = ? with counting numbers",
                        "camera_movement": "Markazga fokus",
                        "emotion": "qiziqish"
                    },
                    {
                        "scene_number": 3,
                        "title": "Natija: 2 + 2 = 4!",
                        "duration_seconds": sec_per_scene,
                        "stage": "solution",
                        "narration": "Ofarin! Ikkiga ikkini qo'shsak, to'rt bo'ladi! Qara: ikki qo'shuv ikki teng to'rt! Jami to'rtta shirin olma bo'ldi. Matematika juda qiziq, shunday emasmi?",
                        "visual_prompt": "3D animated chalkboard glowing 2 + 2 = 4 with 4 shiny apples and stars",
                        "camera_movement": "Aylanma harakat",
                        "emotion": "quvonch"
                    }
                ],
                "screenplay_author": "KidsVidEdu Virtual O'qituvchi v4.0"
            }

        # B) Daraxtlar va fasllar mavzusi
        if any(w in text_lower for w in ["daraxt", "barg", "kuz", "chinor", "oltin"]):
            return {
                "title": f"Tabiat Darsi: {clean_topic}",
                "moral_summary": "Daraxtlar qishki sovuqda suvni tejash va orom olish uchun barglarini to'kadi.",
                "scenes": [
                    {
                        "scene_number": 1,
                        "title": "Kuzda nega ranglar o'zgaradi?",
                        "duration_seconds": sec_per_scene,
                        "stage": "hook",
                        "narration": "Assalomu alaykum, aziz do'stim! Kuz kelganda daraxtlarning yashil barglari nega birdan oltin va qizil rangga kirishini bilasanmi? Keling, bu ajoyib sirni birga ochamiz!",
                        "visual_prompt": "Sunny green summer tree transitioning into golden autumn tree",
                        "camera_movement": "Sekin yaqinlashish (Dolly In)",
                        "emotion": "hayrat"
                    },
                    {
                        "scene_number": 2,
                        "title": "Quyosh va yashil bo'yoq siri",
                        "duration_seconds": sec_per_scene,
                        "stage": "cause",
                        "narration": "Yozda barglarda quyosh nuri tufayli yashil xlorofill ko'p bo'ladi. Kuzda esa kunlar qisqarib, havo soviydi. Yashil rang kamayib, barglarning asl oltin va sariq rangi ko'rina boshlaydi.",
                        "visual_prompt": "Macro animated leaf with smiling sun and changing colors from green to yellow",
                        "camera_movement": "Yon tomondan kuzatish (Pan Right)",
                        "emotion": "qiziqish"
                    },
                    {
                        "scene_number": 3,
                        "title": "Daraxtning qishki oromi",
                        "duration_seconds": sec_per_scene,
                        "stage": "solution",
                        "narration": "Qishda yer muzlab qolganda daraxt ildizlari orqali suv icha olmaydi. Shuning uchun daraxt barcha barglarini to'kib, qishki shirin uyquga ketadi. Bahorda esa yangi yaproqlar unib chiqadi!",
                        "visual_prompt": "Peacefully sleeping tree covered in soft winter twilight ready for spring buds",
                        "camera_movement": "Sekin uzoqlashish (Zoom Out)",
                        "emotion": "orom"
                    }
                ],
                "screenplay_author": "KidsVidEdu Virtual O'qituvchi v4.0"
            }

        # C) Boshqa har qanday umumiy dars
        scenes = []
        stages = [
            ("Savol va Tushuncha", f"Salom bolajonim! Bugungi darsimizda biz sen bilan birga {clean_topic} mavzusini eng qiziqarli misollar orqali o'rganamiz!"),
            ("Amaliy Misol va Sir", f"Diqqat bilan qara, bu hodisa qanday yuz berishini bosqichma-bosqich ko'rib chiqamiz. Har bir narsaning o'z sababi va qoidasi bor."),
            ("Asosiy Xulosa va Saboq", f"Mana, do'stim! Biz muhim qoidani tushunib oldik. Bugun o'rgangan biliming senga hayotda har doim kerak bo'ladi!")
        ]
        for i in range(min(scene_count, len(stages))):
            st_title, st_narr = stages[i]
            scenes.append({
                "scene_number": i + 1,
                "title": st_title,
                "duration_seconds": sec_per_scene,
                "stage": f"step_{i+1}",
                "narration": st_narr,
                "visual_prompt": f"Clean colorful modern educational explainer illustration about {clean_topic}",
                "camera_movement": "Sekin yaqinlashish",
                "emotion": "quvnoq"
            })

        return {
            "title": f"{clean_topic} — Virtual Darslik",
            "moral_summary": f"{clean_topic} mavzusi bo'yicha tushunarli va interaktiv bilim beriladi.",
            "scenes": scenes,
            "screenplay_author": "KidsVidEdu Virtual O'qituvchi v4.0"
        }
