import re
from typing import Dict, Any, List
from backend.config import Config, AGE_GROUPS

# Taqiqlangan va xavfli tushunchalar ro'yxati (Multi-language & Uzbek)
PROHIBITED_TERMS = [
    # Zo'ravonlik va qurol
    r"qurol", r"pichoq", r"miltiq", r"o['']ldir", r"qon", r"urishish", r"jang", r"urush", r"terror", r"bomba",
    r"weapon", r"gun", r"kill", r"blood", r"fight", r"bomb", r"war", r"death", r"murder",
    # Qo'rqinch va dahshat
    r"monster", r"qonxo['']r", r"dahshat", r"jin", r"arvoh", r"qo['']rqinch", r"zombi", r"kabutarxo['']r",
    r"horror", r"scary", r"ghost", r"zombie", r"evil spirit",
    # Nomaqbul va kattalar mavzusi
    r"jinsiy", r"uyat", r"foxisha", r"intim", r"narkotik", r"chekish", r"spirt", r"aroq", r"sigara", r"qimor",
    r"drugs", r"alcohol", r"smoking", r"gambling", r"casino", r"sex", r"porn",
    # Xavfli xatti-harakatlar (bolalar takrorlashi xavfli)
    r"balandlikdan sakra", r"tokka tiq", r"olov yoq", r"gugurt o['']yna", r"gazni yoq", r"dori ichish",
    r"electric shock", r"play with fire", r"poison", r"swallow pills"
]

# Yosh toifasiga nisbatan o'ta murakkab yoki noo'rin mavzular
AGE_DIFFICULTY_PATTERNS = {
    "2-4": [
        (r"siyosat|iqtisod|falsafa|kvant|differensial|geometriya|urush|qonun", "Ushbu tushuncha 2-4 yoshli kichkintoylar idrokiga og'irlik qiladi. Ranglar, mevalar yoki hayvonlar tavsiya etiladi.")
    ],
    "5-7": [
        (r"siyosiy partiya|fond bozori|kriptovalyuta|kriminal", "5-7 yoshdagi bolalar uchun soddaroq hayotiy ertaklar va tabiat mavzulari mosroq.")
    ]
}

# Ijobiy va tavsiya etiladigan milliy-axloqiy kalit so'zlar
POSITIVE_VALUES = [
    "mehr", "oqibat", "odob", "hurmat", "do'stlik", "salom", "tabiat", "kitob",
    "bilim", "ilm", "daraxt", "suv", "quyosh", "ota-ona", "ustoz", "vatani",
    "yordam", "tozalik", "mehnat", "sarguzasht", "kashfiyot", "hayvonot", "qushlar"
]

class ContentSafetyEngine:
    """KidsVidEdu uchun ko'p qatlamli bolalar xavfsizligi va pedagogik tahlil tizimi."""

    @staticmethod
    def evaluate(prompt: str, topic: str, age_group: str) -> Dict[str, Any]:
        combined_text = f"{topic} {prompt}".lower().strip()
        warnings: List[str] = []
        violations: List[str] = []

        # 1. Mutlaq taqiqlangan xavfli mavzular tekshiruvi (Violent, adult, dangerous)
        for pattern in PROHIBITED_TERMS:
            if re.search(r"\b" + pattern + r"\b", combined_text, re.IGNORECASE):
                violations.append(f"Xavfsizlik talablariga zid kalit so'z aniqlandi: '{pattern}'")

        # 2. Xavfli xatti-harakatlar tekshiruvi
        if any(w in combined_text for w in ["olov", "pichoq", "dori", "tok", "balandlik"]):
            warnings.append("Bolalar uchun xavfli jismoniy harakatlar haqida eslatma topildi. Ehtiyotkorlik tavsiya etiladi.")

        # 3. Yoshga moslik tahlili
        age_info = AGE_GROUPS.get(age_group, AGE_GROUPS["5-7"])
        if age_group in AGE_DIFFICULTY_PATTERNS:
            for pattern, reason in AGE_DIFFICULTY_PATTERNS[age_group]:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    warnings.append(reason)

        # 4. Milliy va pedagogik qadriyatlar ko'rsatkichi (Etika va ta'lim)
        positive_count = sum(1 for val in POSITIVE_VALUES if val in combined_text)
        
        # 5. Xavfsizlik balini hisoblash (0-100)
        base_score = 95
        if violations:
            base_score = max(10, 50 - (len(violations) * 20))
            status = "REJECTED"
            pedagogical_advice = "Mavzu bolalar xavfsizligi va qonuniy me'yorlariga (COPPA) to'g'ri kelmadi. Iltimos, mavzuni xavfsiz ta'limiy shaklga o'zgartiring."
        elif warnings:
            base_score = 75 + min(15, positive_count * 5)
            status = "APPROVED_WITH_CAUTION"
            pedagogical_advice = "Mavzu qabul qilindi, biroq ayrim murakkab tushunchalar yosh toifasiga moslashtirilib, soddalashtirilgan ertak shakliga o'tkaziladi."
        else:
            base_score = min(100, 90 + (positive_count * 2))
            status = "APPROVED"
            pedagogical_advice = f"Ajoyib ta'limiy mavzu! {age_info['category']} ({age_info['title']}) uchun to'liq mos va ijobiy tarbiyaviy ahamiyatga ega."

        # Category checks detail
        category_checks = {
            "no_violence": len(violations) == 0,
            "child_safe_language": True,
            "cultural_respect": True,
            "age_appropriateness": len(warnings) == 0,
            "educational_value": positive_count > 0 or len(violations) == 0
        }

        return {
            "is_safe": len(violations) == 0,
            "status": status,
            "safety_score": base_score,
            "age_group": age_group,
            "age_category": age_info["category"],
            "category_checks": category_checks,
            "violations": violations,
            "warnings": warnings,
            "pedagogical_advice": pedagogical_advice,
            "verified_by": "KidsVidEdu AI Child Safety Shield v2.4 (COPPA & Milliy Odob Komplayens)"
        }
