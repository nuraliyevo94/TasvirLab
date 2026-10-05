import re
from typing import Dict, Any, List
from backend.config import AGE_GROUPS

# 1. Mutlaq taqiqlangan va bolalar uchun xavfli tushunchalar (kategoriyalarga bo'lingan)
PROHIBITED_CATEGORIES = {
    "violence_weapons": {
        "title": "Zo'ravonlik, qurol va tajovuz",
        "patterns": [
            r"qurol", r"miltiq", r"to['']pponcha", r"pichoq", r"o['']ldir", r"qon(?:\b|li|to['']k)", r"urishish",
            r"jang", r"urush", r"terror", r"bomba", r"qatl(?:\b|i|om)", r"o['']lim", r"vahshiylik",
            r"weapon", r"gun", r"kill", r"blood", r"fight", r"bomb", r"war", r"death", r"murder"
        ]
    },
    "fear_horror": {
        "title": "Qo'rqinch, vahima va dahshat",
        "patterns": [
            r"monster", r"qonxo['']r", r"dahshat", r"jin\b", r"arvoh", r"qo['']rqinch", r"zombi",
            r"horror", r"scary", r"ghost", r"zombie", r"evil spirit"
        ]
    },
    "inappropriate_adult": {
        "title": "Yoshga nomunosib va kattalar mavzulari",
        "patterns": [
            r"jinsiy", r"uyat", r"fohisha", r"intim", r"yalang['']och", r"erotik",
            r"sex", r"porn", r"erotic", r"nude"
        ]
    },
    "harmful_substances": {
        "title": "Zararli odatlar, qimor va moddalar",
        "patterns": [
            r"narkotik", r"chekish", r"sigaret", r"veyp", r"spirt", r"aroq", r"pivo", r"mast", r"qimor", r"kazino",
            r"drugs", r"alcohol", r"smoking", r"gambling", r"casino"
        ]
    },
    "dangerous_actions": {
        "title": "Bolalar takrorlashi xavfli bo'lgan jismoniy harakatlar",
        "patterns": [
            r"balandlikdan sakra", r"tokka tiq", r"rozetka", r"olov yoq", r"gugurt",
            r"gazni yoq", r"dori ichish", r"tabletka", r"zahar", r"pichoq bilan o['']yna",
            r"electric shock", r"play with fire", r"poison", r"swallow pills"
        ]
    },
    "bullying_toxicity": {
        "title": "Kamsitish, haqorat va yomon muomala",
        "patterns": [
            r"ahmoq", r"tentak", r"jinni", r"mayib", r"kamsitish", r"haqorat", r"masxara",
            r"stupid", r"idiot", r"ugly", r"bully"
        ]
    }
}

# 2. Yosh toifalariga kognitiv moslik mezonlari
AGE_COGNITIVE_CHECKS = {
    "2-4": [
        (r"siyosat|iqtisod|falsafa|kvant|differensial|geometriya|qonunchilik|kripto|valyuta",
         "Ushbu tushuncha 2–4 yoshli kichkintoylar idrokiga og'irlik qiladi. Ranglar, mevalar, hayvonlar va tovushlar tavsiya etiladi.")
    ],
    "5-7": [
        (r"fond bozori|kriptovalyuta|siyosiy partiya|sud jarayoni|kriminal",
         "5–7 yoshdagi bolalar uchun soddaroq hayotiy ertaklar, tabiat sirlari va boshlang'ich tushunchalar mosroq.")
    ],
    "8-10": [
        (r"og['']ir jinoyat|kriminalistika|siyosiy ziddiyat",
         "8–10 yosh uchun kashfiyotlar, ilmiy faktlar va sarguzashtli ta'limiy mavzular tavsiya etiladi.")
    ]
}

# 3. Haqiqiy ta'limiy va axloqiy mavzular lug'ati
EDUCATIONAL_THEMES = {
    "Tabiatshunoslik va Ekologiya": ["tabiat", "daraxt", "suv", "quyosh", "yomg'ir", "qor", "fasl", "ekologiya", "o'simlik", "qushlar", "hayvonot", "o'rmon"],
    "Matematika va Mantiq": ["matematika", "sonlar", "qo'shish", "ayirish", "hisob", "shakl", "geometriya", "mantiq", "raqam"],
    "Fan, Koinot va Texnologiya": ["koinot", "sayyora", "yulduz", "fizika", "kimyo", "robot", "kompyuter", "kashfiyot", "ilm", "texnologiya", "sun'iy intellekt", "dasturlash"],
    "Odob-axloq va Insoniylik": ["mehr", "oqibat", "odob", "hurmat", "do'stlik", "salom", "ota-ona", "ustoz", "yordam", "mehnat", "tozalik", "saxovat"],
    "Madaniyat va San'at": ["kitob", "ertak", "she'r", "musiqa", "san'at", "tarix", "vatani", "hunarmandchilik"]
}

class ContentSafetyEngine:
    """TasvirLab — Real, dalillangan va yolg'on statistikasiz pedagogik xavfsizlik auditi."""

    @staticmethod
    def evaluate(prompt: str, topic: str, age_group: str) -> Dict[str, Any]:
        combined_text = f"{topic} {prompt}".strip()
        words = re.findall(r"\w+", combined_text.lower())
        word_count = len(words)
        
        violations: List[str] = []
        warnings: List[str] = []
        category_results: List[Dict[str, Any]] = []

        # 1. Xavfli kategoriyalar bo'yicha real tekshiruv
        for cat_id, cat_info in PROHIBITED_CATEGORIES.items():
            matched_terms = []
            for pattern in cat_info["patterns"]:
                # So'z boshi chegarasi (\b) bilan tekshirish (boshqa begunoh so'zlar ichidagi harflar xato tushmasligi uchun)
                regex = r"\b" + pattern
                if re.search(regex, combined_text, re.IGNORECASE):
                    clean_term = pattern.split("(")[0].replace(r"['']", "'").replace(r"\b", "").strip()
                    matched_terms.append(clean_term)

            if matched_terms:
                unique_terms = list(set(matched_terms))
                violation_msg = f"{cat_info['title']}: '{', '.join(unique_terms)}' iboralari aniqlandi"
                violations.append(violation_msg)
                category_results.append({
                    "id": cat_id,
                    "title": cat_info["title"],
                    "is_safe": False,
                    "status_text": "Cheklov aniqlandi",
                    "details": f"Taqiqlangan so'zlar: {', '.join(unique_terms)}"
                })
            else:
                category_results.append({
                    "id": cat_id,
                    "title": cat_info["title"],
                    "is_safe": True,
                    "status_text": "Toza (Xavf aniqlanmadi)",
                    "details": "Talablarga to'liq muvofiq"
                })

        # 2. Yosh toifasiga kognitiv moslik tekshiruvi
        age_info = AGE_GROUPS.get(age_group, AGE_GROUPS.get("5-7", {"title": f"{age_group} yosh", "category": "Ta'lim"}))
        age_is_appropriate = True
        age_notes = f"{age_info['category']} ({age_info['title']}) idrokiga mos"

        if age_group in AGE_COGNITIVE_CHECKS:
            for pattern, reason in AGE_COGNITIVE_CHECKS[age_group]:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    warnings.append(reason)
                    age_is_appropriate = False
                    age_notes = reason
                    break

        category_results.append({
            "id": "age_cognitive",
            "title": f"Bolalar yoshiga mosligi ({age_info['title']})",
            "is_safe": age_is_appropriate,
            "status_text": "Mos keladi" if age_is_appropriate else "Ehtiyotkorlik talab etiladi",
            "details": age_notes
        })

        # 3. Aniqlangan ijobiy pedagogik yo'nalishlar
        detected_themes = []
        for theme_name, keywords in EDUCATIONAL_THEMES.items():
            if any(kw in combined_text.lower() for kw in keywords):
                detected_themes.append(theme_name)

        if not detected_themes and word_count > 0:
            detected_themes.append("Umumiy ta'limiy mavzu")

        # 4. Yakuniy xulosa (Tushunarli, ochiq va samimiy)
        if violations:
            status = "REJECTED"
            status_label = "Rad etildi (Bolalarga tavsiya etilmaydi)"
            pedagogical_advice = (
                "Kiritilgan mavzuda bolalar uchun xavfli, qo'rqinchli yoki nomunosib so'zlar aniqlandi. "
                "Iltimos, bolajonlar uchun foydali boshqa mavzu tanlang yoki yozing."
            )
        elif warnings:
            status = "APPROVED_WITH_CAUTION"
            status_label = "Qabul qilindi (Bolalarga moslashtirish bilan)"
            pedagogical_advice = (
                f"Mavzu qabul qilindi. Ayrim tushunchalar {age_info['title']} guruhi uchun "
                "biroz murakkab bo'lgani sababli, ssenariy yanada sodda, bolalar tushunadigan misollar bilan tuziladi."
            )
        else:
            status = "APPROVED"
            status_label = "Tasdiqlandi — Bolalar uchun xavfsiz va foydali"
            pedagogical_advice = (
                f"Ajoyib ta'limiy mavzu! {age_info['category']} ({age_info['title']}) uchun to'liq mos "
                "hamda bolajonlarga yaxshi tarbiya va bilim beradi."
            )

        return {
            "is_safe": len(violations) == 0,
            "status": status,
            "status_label": status_label,
            "topic_analyzed": topic,
            "word_count": word_count,
            "age_group": age_group,
            "age_category": age_info["category"],
            "category_results": category_results,
            "detected_themes": detected_themes,
            "violations": violations,
            "warnings": warnings,
            "pedagogical_advice": pedagogical_advice,
            "verified_by": "TasvirLab Bolalar Xavfsizligi Tizimi"
        }
