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

        async with httpx.AsyncClient(timeout=20.0) as client:
            for model_name in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-flash-latest"]:
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
    def has_keyword(text: str, keywords: list) -> bool:
        """Tekst ichidan kalit so'zlarni butun so'z sifatida to'g'ri qidirish ('oy' 'ajoyib' ichida topilmaydi)."""
        t = f" {text.lower()} "
        for kw in keywords:
            k = kw.lower()
            if len(k) <= 4:
                if re.search(r'(?<![a-zA-Z\u0400-\u04FF\'])' + re.escape(k) + r'(?![a-zA-Z\u0400-\u04FF\'])', t):
                    return True
            else:
                if k in t:
                    return True
        return False

    @staticmethod
    def _split_narration_into_beats(narration: str) -> tuple:
        """Gapni so'zlarni aslo kesmasdan butun jumlalarga ajratish."""
        if not narration:
            return ("", "")
        
        # Nuqta, undov yoki so'roq belgilari bo'yicha mustaqil gaplarga ajratish
        sentences = re.findall(r'[^.!?]+[.!?]*', narration)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) >= 2:
            return (sentences[0], " ".join(sentences[1:]))
        
        # Agar bitta uzun gap bo'lsa, butun so'zlar bo'yicha ikkiga bo'lish
        words = narration.split()
        if len(words) <= 7:
            return (narration, narration)
        
        mid = len(words) // 2
        return (" ".join(words[:mid]), " ".join(words[mid:]))

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
        part1, part2 = ScreenwriterEngine._split_narration_into_beats(narration)

        # 1. Suv, tomchi, yomg'ir, daryo, bulut (ENG BIRINCHI O'RINDA!)
        if ScreenwriterEngine.has_keyword(full_text, ["suv", "tomchi", "tomchivoy", "yomg'ir", "bulut", "daryo", "dengiz", "okean", "muz", "bug'", "oqim", "suv tomchisi"]):
            scene_num = scene.get("scene_number", 1)
            icons1 = ["💧", "☀️", "🌊", "✨"]
            icons2 = ["☁️", "🌧️", "🌈", "🌱"]
            if scene_num == 2:
                icons1 = ["☀️", "✨", "☁️", "💧"]
                icons2 = ["☁️", "💨", "🏔️", "✨"]
            elif scene_num >= 3:
                icons1 = ["☁️", "🌧️", "💧", "☔"]
                icons2 = ["🌈", "🌸", "🌱", "💧"]

            scene["visual_beats"] = [
                {
                    "time_pct": 0.0,
                    "main_text": clean_title,
                    "sub_text": part1,
                    "icons": icons1,
                    "highlight": False
                },
                {
                    "time_pct": 0.55,
                    "main_text": "Tabiat Mo'jizasi",
                    "sub_text": part2,
                    "icons": icons2,
                    "highlight": True
                }
            ]
            return

        # 2. Haqiqiy Matematika (qo'shish/ayirish/hisoblash)
        is_math = ("+" in full_text or ScreenwriterEngine.has_keyword(full_text, ["qo'shish", "ayirish", "karra", "matematika", "hisoblaymiz"])) and not any(w in full_text for w in ["qo'shiq", "qo'shni"])
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
                    "sub_text": part1,
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

        # 3. Tabiat, Fasllar va Daraxtlar (Kuz, Bahor, Qish, Daraxt, Barg)
        if ScreenwriterEngine.has_keyword(full_text, ["daraxt", "barg", "kuz", "bahor", "yoz", "qish", "fasl", "chinor", "oltin", "o'rmon"]):
            icons = ["🌳", "🍃", "🍁", "☀️"]
            if ScreenwriterEngine.has_keyword(full_text, ["qish", "qor", "muz"]):
                icons = ["❄️", "⛄", "🌲", "✨"]
            elif ScreenwriterEngine.has_keyword(full_text, ["bahor", "gul"]):
                icons = ["🌸", "🌱", "🦋", "☀️"]

            scene["visual_beats"] = [
                {
                    "time_pct": 0.0,
                    "main_text": clean_title,
                    "sub_text": part1,
                    "icons": icons,
                    "highlight": False
                },
                {
                    "time_pct": 0.55,
                    "main_text": "Tabiat Sabog'i",
                    "sub_text": part2,
                    "icons": icons,
                    "highlight": True
                }
            ]
            return

        # 4. Hayvonlar va Jonivorlar olami
        if ScreenwriterEngine.has_keyword(full_text, ["hayvon", "ayiq", "quyon", "tulki", "bo'ri", "sher", "mushuk", "kuchuk", "it", "fil", "baliq", "delfin", "qush"]):
            icons = ["🐻", "🐰", "🦊", "🦁"]
            if ScreenwriterEngine.has_keyword(full_text, ["baliq", "delfin", "akula"]):
                icons = ["🐬", "🌊", "🐠", "🫧"]
            elif ScreenwriterEngine.has_keyword(full_text, ["qush", "chumchuq", "burgut"]):
                icons = ["🐦", "🌿", "🐣", "✨"]
            elif ScreenwriterEngine.has_keyword(full_text, ["mushuk", "kuchuk", "it"]):
                icons = ["🐱", "🐶", "🐾", "❤️"]

            scene["visual_beats"] = [
                {
                    "time_pct": 0.0,
                    "main_text": clean_title,
                    "sub_text": part1,
                    "icons": icons,
                    "highlight": False
                },
                {
                    "time_pct": 0.55,
                    "main_text": "Do'stona Tabiat",
                    "sub_text": part2,
                    "icons": icons,
                    "highlight": True
                }
            ]
            return

        # 5. Fazoviy olam / Kosmos va Quyosh sistemasi (FAQAT BUTUN SO'Z!)
        if ScreenwriterEngine.has_keyword(full_text, ["kosmos", "sayyora", "quyosh sistemasi", "yulduz", "raketa", "koinot", "mars", "saturn", "oy"]):
            icons = ["🚀", "🌍", "🌕", "⭐"]
            scene["visual_beats"] = [
                {
                    "time_pct": 0.0,
                    "main_text": clean_title,
                    "sub_text": part1,
                    "icons": icons,
                    "highlight": False
                },
                {
                    "time_pct": 0.55,
                    "main_text": "Mo'jizaviy Koinot",
                    "sub_text": part2,
                    "icons": ["🪐", "✨", "☀️", "🌟"],
                    "highlight": True
                }
            ]
            return

        # 6. Mevalar va Ranglar
        if ScreenwriterEngine.has_keyword(full_text, ["meva", "olma", "banan", "nok", "uzum", "anor", "shaftoli", "rang", "qizil", "sariq", "yashil", "ko'k"]):
            icons = ["🍎", "🍌", "🍇", "🍓"] if ScreenwriterEngine.has_keyword(full_text, ["meva", "olma", "banan", "nok"]) else ["🎨", "🔴", "🟡", "🟢"]
            scene["visual_beats"] = [
                {
                    "time_pct": 0.0,
                    "main_text": clean_title,
                    "sub_text": part1,
                    "icons": icons,
                    "highlight": False
                },
                {
                    "time_pct": 0.55,
                    "main_text": "Yorqin Dunyo",
                    "sub_text": part2,
                    "icons": icons,
                    "highlight": True
                }
            ]
            return

        # 7. Umumiy va Boshqa barcha ta'limiy mavzular (Doimo butun so'z va matnga mos)
        icons = ["💡", "✨", "📚", "⭐"]
        if ScreenwriterEngine.has_keyword(full_text, ["mashina", "poyezd", "avtomobil"]):
            icons = ["🚗", "🚦", "🚂", "✈️"]
        elif ScreenwriterEngine.has_keyword(full_text, ["musiqa", "qo'shiq", "kuy"]):
            icons = ["🎵", "🎶", "🎸", "🎹"]
        elif ScreenwriterEngine.has_keyword(full_text, ["sport", "to'p", "futbol"]):
            icons = ["⚽", "🏀", "🏃", "🏆"]

        scene["visual_beats"] = [
            {
                "time_pct": 0.0,
                "main_text": clean_title,
                "sub_text": part1,
                "icons": icons,
                "highlight": False
            },
            {
                "time_pct": 0.55,
                "main_text": "Foydali Bilim",
                "sub_text": part2,
                "icons": icons,
                "highlight": True
            }
        ]

    @staticmethod
    def _generate_contextual_screenplay(topic, prompt, age_info, total_duration, scene_count, style_info, language):
        """Aniq, jonli va pedagogik virtual o'qituvchi ssenariysi (Offline rejimda ham to'liq ishlaydi)."""
        clean_topic = topic.strip()
        sec_per_scene = round(total_duration / scene_count)
        text_lower = f"{clean_topic} {prompt}".lower()
        
        # A) Suv, Tomchivoy va Yomg'ir sarguzashti (Suv aylanishi)
        if ScreenwriterEngine.has_keyword(text_lower, ["suv", "tomchi", "tomchivoy", "yomg'ir", "bulut", "daryo", "dengiz", "oqim"]):
            return {
                "title": f"Tabiat Darsi: {clean_topic}",
                "moral_summary": "Suv quyosh nuri ostida bug'lanib bulutga aylanadi va yomg'ir bo'lib yerga hayot ulashadi.",
                "scenes": [
                    {
                        "scene_number": 1,
                        "title": "Jajji Tomchivoy bilan tanishuv",
                        "duration_seconds": sec_per_scene,
                        "stage": "hook",
                        "narration": "Salom, mening jajji do'stim! Katta moviy daryoda quvnoq Tomchivoy yashar ekan. Bir kuni iliq quyosh nuri tushib, u yengil bug'ga aylanib osmonga ucha boshlabdi!",
                        "visual_prompt": "Cheerful smiling water droplet rising from a blue river towards the warm sun",
                        "camera_movement": "Sekin yaqinlashish (Dolly In)",
                        "emotion": "quvnoq"
                    },
                    {
                        "scene_number": 2,
                        "title": "Momiq bulutlar va sayohat",
                        "duration_seconds": sec_per_scene,
                        "stage": "cause",
                        "narration": "Osmonda u millionlab do'stlari bilan uchrashib, oppoq va momiq bulutga aylanibdi! Shamol bu mehribon bulutni baland tog'lar va yashil vodiylar uzra uzoqlarga uchirib ketibdi.",
                        "visual_prompt": "Cute water droplets gathering into a friendly fluffy white cloud floating over mountains",
                        "camera_movement": "Yon tomondan kuzatish (Pan Right)",
                        "emotion": "hayrat"
                    },
                    {
                        "scene_number": 3,
                        "title": "Mayin yomg'ir va tabiat quvonchi",
                        "duration_seconds": sec_per_scene,
                        "stage": "solution",
                        "narration": "Bulut to'lishib, yerga shirin yomg'ir bo'lib yog'ibdi! Chanqagan gullar, baland daraxtlar suv ichib quvonishibdi. Tomchivoy yana ona yerga qaytib, tabiatga yangi hayot bag'ishlabdi!",
                        "visual_prompt": "Gentle rain drops nourishing colorful blooming flowers and a rainbow arc in the sky",
                        "camera_movement": "Sekin uzoqlashish (Zoom Out)",
                        "emotion": "quvonch"
                    }
                ],
                "screenplay_author": "KidsVidEdu Virtual O'qituvchi v4.0"
            }

        # B) Matematika mavzusi (Masalan: 2 ga 2 ni qo'shish)
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

        # C) Daraxtlar va fasllar mavzusi
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

        # D) Koinot va Sayyoralar mavzusi
        if ScreenwriterEngine.has_keyword(text_lower, ["kosmos", "sayyora", "quyosh sistemasi", "yulduz", "raketa", "mars", "saturn"]):
            return {
                "title": f"Koinot Sirlari: {clean_topic}",
                "moral_summary": "Bizning Yer sayyoramiz va quyosh sistemasi cheksiz koinotning ajoyib mo'jizasidir.",
                "scenes": [
                    {
                        "scene_number": 1,
                        "title": "Cheksiz va sirli koinot",
                        "duration_seconds": sec_per_scene,
                        "stage": "hook",
                        "narration": "Salom, yosh astronom do'stim! Tunda osmonga qarab porloq yulduzlarni ko'rganmisan? Koinotda qanchadan-qancha ajoyib sayyoralar borligini bilasanmi?",
                        "visual_prompt": "Kids looking at starry night sky with twinkling stars and crescent moon",
                        "camera_movement": "Sekin yaqinlashish (Dolly In)",
                        "emotion": "hayrat"
                    },
                    {
                        "scene_number": 2,
                        "title": "Quyosh va uning do'stlari",
                        "duration_seconds": sec_per_scene,
                        "stage": "cause",
                        "narration": "Quyosh atrofida sakkizta ulkan sayyora aylanadi. Biz yashaydigan moviy Yer sayyorasi esa hayot mavjud bo'lgan eng go'zal va yagona makonimizdir!",
                        "visual_prompt": "Solar system with bright sun in the center and colorful planets orbiting smoothly",
                        "camera_movement": "Aylanma harakat",
                        "emotion": "qiziqish"
                    },
                    {
                        "scene_number": 3,
                        "title": "Orzular va yulduzlar sari",
                        "duration_seconds": sec_per_scene,
                        "stage": "solution",
                        "narration": "Yaxshi o'qisang, kelajakda ulkan raketada kosmosga uchib, yangi yulduzlarni kashf qilishing mumkin! Ilm o'rganish koinot sirlarini ochishga yordam beradi.",
                        "visual_prompt": "Friendly white cartoon rocket flying past a purple ringed planet with twinkling stars",
                        "camera_movement": "Sekin uzoqlashish (Zoom Out)",
                        "emotion": "quvonch"
                    }
                ],
                "screenplay_author": "KidsVidEdu Virtual O'qituvchi v4.0"
            }

        # E) Jonivorlar va Hayvonlar olami
        if ScreenwriterEngine.has_keyword(text_lower, ["hayvon", "ayiq", "quyon", "tulki", "bo'ri", "sher", "fil", "jonivor", "o'rmon"]):
            return {
                "title": f"Jonivorlar Olami: {clean_topic}",
                "moral_summary": "Hayvonlar tabiatning ajralmas qismi bo'lib, ularni asrash va mehr ko'rsatish bizning burchimizdir.",
                "scenes": [
                    {
                        "scene_number": 1,
                        "title": "Do'stona jonivorlar bilan uchrashuv",
                        "duration_seconds": sec_per_scene,
                        "stage": "hook",
                        "narration": "Salom, aziz bolajonim! O'rmon va tabiatda qanday qiziqarli jonivorlar yashashini bilasanmi? Har bir hayvonning o'ziga xos ajoyib xislatlari bor!",
                        "visual_prompt": "Lush green forest glade with cheerful animals gathered near a crystal stream",
                        "camera_movement": "Sekin yaqinlashish (Dolly In)",
                        "emotion": "quvnoq"
                    },
                    {
                        "scene_number": 2,
                        "title": "Har bir jonivorning o'z siri",
                        "duration_seconds": sec_per_scene,
                        "stage": "cause",
                        "narration": "Ayiqlar qishda shirin uyquga ketadi, chaqqon quyonlar esa xavfdan tezda qochadi. Ular tabiatning muvozanatini saqlashda juda muhim o'rin tutadi.",
                        "visual_prompt": "Animated forest animals demonstrating their natural habits in a colorful woodland",
                        "camera_movement": "Yon tomondan kuzatish (Pan Right)",
                        "emotion": "qiziqish"
                    },
                    {
                        "scene_number": 3,
                        "title": "Tabiatni va hayvonlarni asraymiz",
                        "duration_seconds": sec_per_scene,
                        "stage": "solution",
                        "narration": "Biz jonivorlarga doimo mehribon bo'lishimiz, tabiatni toza saqlashimiz kerak. Shunda barcha hayvonlar bizning vafodor do'stimiz bo'lib qoladi!",
                        "visual_prompt": "Smiling child feeding birds in a sunny meadow surrounded by friendly animals",
                        "camera_movement": "Sekin uzoqlashish (Zoom Out)",
                        "emotion": "quvonch"
                    }
                ],
                "screenplay_author": "KidsVidEdu Virtual O'qituvchi v4.0"
            }

        # F) Boshqa har qanday umumiy dars (Boyitilgan, jonli pedagogik matn)
        scenes = [
            {
                "scene_number": 1,
                "title": f"{clean_topic} bilan tanishuv",
                "duration_seconds": sec_per_scene,
                "stage": "hook",
                "narration": f"Salom, mening aqlli do'stim! Bugun biz sen bilan juda ajoyib va qiziqarli mavzu — {clean_topic} haqida bilib olamiz. Bu qanday yuz berishini hech o'ylab ko'rganmisan?",
                "visual_prompt": f"Bright engaging educational chalkboard introducing {clean_topic} with vivid colorful elements",
                "camera_movement": "Sekin yaqinlashish (Dolly In)",
                "emotion": "hayrat"
            },
            {
                "scene_number": 2,
                "title": "Qiziqarli hodisa siri",
                "duration_seconds": sec_per_scene,
                "stage": "cause",
                "narration": f"Diqqat bilan qara, tabiatda va hayotda har bir narsaning o'z tartibi va ajoyib sababi bor! {clean_topic} ham bosqichma-bosqich sodir bo'ladi va atrofdagi olamga o'zgacha go'zallik bag'ishlaydi.",
                "visual_prompt": f"Detailed educational explanation illustration revealing the inner mechanism of {clean_topic}",
                "camera_movement": "Yon tomondan kuzatish (Pan Right)",
                "emotion": "qiziqish"
            },
            {
                "scene_number": 3,
                "title": "Katta saboq va xulosa",
                "duration_seconds": sec_per_scene,
                "stage": "solution",
                "narration": f"Ofarin, do'stim! Bugun biz yangi va foydali bilimni o'rganib oldik. Har bir o'rgangan biliming seni yanada dono va zehnli qiladi. Yangi bilimlarni kashf etishdan aslo to'xtama!",
                "visual_prompt": f"Celebratory colorful achievement screen with gold stars and cheerful elements for {clean_topic}",
                "camera_movement": "Sekin uzoqlashish (Zoom Out)",
                "emotion": "quvonch"
            }
        ]
        return {
            "title": f"Tushunarli Darslik: {clean_topic}",
            "moral_summary": f"{clean_topic} mavzusini qunt bilan o'rganish bolajonga dunyoni yanada yaxshiroq anglashga yordam beradi.",
            "scenes": scenes[:scene_count] if scene_count <= len(scenes) else scenes,
            "screenplay_author": "KidsVidEdu Virtual O'qituvchi v4.0"
        }
