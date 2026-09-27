import os
import re
import httpx
from typing import Dict, Any, Optional
from backend.config import Config

class SceneIllustrator:
    """Har bir sahna matniga aynan mos keluvchi 1080p multfilm kadrlari generatori."""

    @staticmethod
    async def generate_scene_svg(scene: Dict[str, Any], topic: str, api_key: str = "") -> str:
        """Sahnaning nutq matni va tavsifiga to'liq mos keluvchi SVG yaratadi."""
        gemini_key = api_key or Config.GEMINI_API_KEY
        
        # 1. Gemini orqali matnga 100% mos vektor multfilm kadrini yaratish
        if gemini_key and gemini_key.strip():
            try:
                ai_svg = await SceneIllustrator._generate_with_gemini(scene, topic, gemini_key.strip())
                if ai_svg and "<svg" in ai_svg and "</svg>" in ai_svg:
                    return ai_svg
            except Exception as e:
                print(f"Gemini SVG yaratishda xatolik: {e}. Zaxira illyustratsiyaga o'tilmoqda.")

        # 2. Zaxira kontekstli vektor generatori (Mavzular bo'yicha boyitilgan)
        return SceneIllustrator._generate_contextual_svg(scene, topic)

    @staticmethod
    async def _generate_with_gemini(scene: Dict[str, Any], topic: str, api_key: str) -> Optional[str]:
        title = scene.get("title", "")
        narration = scene.get("narration", "")
        visual_prompt = scene.get("visual_prompt", "")
        emotion = scene.get("emotion", "quvnoq")
        stage = scene.get("stage", "")

        prompt = f"""You are a world-class vector cartoon illustrator for animated children's movies (Pixar, Disney, Studio Ghibli style).
Create a beautiful, colorful, professional 16:9 SVG cartoon illustration that DIRECTLY and VIVIDLY illustrates this scene:

Main Topic: {topic}
Scene Title: {title}
Spoken Narration: "{narration}"
Visual Concept: {visual_prompt}
Emotional Tone: {emotion}
Story Stage: {stage}

CRITICAL INSTRUCTIONS:
1. The visual MUST accurately represent the subjects, characters, objects, and setting described in the spoken narration and visual concept. (e.g. if an apple or fruit is mentioned, show the cute smiling fruit; if a historical landmark like Registan is mentioned, show the turquoise domes; if animals or water drops or space or robots, clearly depict them).
2. Clean vector cartoon aesthetic for children: soft pleasant gradients, vibrant joyful colors, expressive friendly character faces/shapes.
3. Use SVG dimensions: viewBox="0 0 1280 720" width="1280" height="720".
4. You MUST output ONLY valid raw SVG starting with <svg and ending with </svg>.
5. DO NOT enclose in markdown backticks or commentary."""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 8192
            }
        }

        async with httpx.AsyncClient(timeout=25.0) as client:
            for model_name in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-flash-latest"]:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                try:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        raw_text = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        raw_text = re.sub(r'^```(?:xml|svg)?\s*', '', raw_text.strip(), flags=re.IGNORECASE)
                        raw_text = re.sub(r'\s*```$', '', raw_text.strip())
                        match = re.search(r'(<svg[\s\S]*?</svg>)', raw_text, re.IGNORECASE)
                        if match:
                            svg_code = match.group(1).strip()
                            if 'viewBox' not in svg_code:
                                svg_code = svg_code.replace('<svg', '<svg viewBox="0 0 1280 720" width="1280" height="720"', 1)
                            return svg_code
                except Exception as ex:
                    print(f"Gemini SVG model {model_name} xatolik: {ex}")
        return None

    @staticmethod
    def _has_kw(text: str, keywords: list) -> bool:
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
    def _generate_contextual_svg(scene: Dict[str, Any], topic: str) -> str:
        """Offline fallback: matn kalit so'zlari bo'yicha to'liq 1080p SVG kadrlar."""
        text = f"{topic} {scene.get('title', '')} {scene.get('narration', '')}".lower()
        s_num = scene.get('scene_number', 1)
        title = scene.get('title', f'{s_num}-sahna')

        # 1. Suv, tomchi, yomg'ir, daryo, bulut (Birinchi o'ringa qo'yiladi!)
        if SceneIllustrator._has_kw(text, ['suv', 'tomchi', 'tomchivoy', 'daryo', 'bulut', 'yomg', 'dengiz', 'okean', 'oqim', 'muz']):
            return SceneIllustrator._draw_water_scene(s_num, scene)

        # 2. Mevalar (olma, banan, nok, anor, uzum, shaftoli)
        elif SceneIllustrator._has_kw(text, ['olma', 'banan', 'nok', 'anor', 'meva', 'tarvuz', 'shaftoli']):
            return SceneIllustrator._draw_fruit_scene(s_num, scene, text)

        # 3. Kuz, daraxtlar, oltin barglar
        elif SceneIllustrator._has_kw(text, ['daraxt', 'barg', 'kuz', 'chinor', 'oltin', 'fasl', 'xlorofill']):
            return SceneIllustrator._draw_autumn_scene(s_num, scene)

        # 4. Hayvonlar (sher, sichqon, quyon, ayiq, qush, baliq)
        elif SceneIllustrator._has_kw(text, ['sher', 'sichqon', 'quyon', 'ayiq', 'qush', 'baliq', 'hayvon', 'bo\'ri', 'kuchuk', 'mushuk']):
            return SceneIllustrator._draw_animal_scene(s_num, scene, text)

        # 5. Koinot, sayyoralar, yulduzlar, raketa (faqat aniq koinot bo'lsa)
        elif SceneIllustrator._has_kw(text, ['quyosh sistemasi', 'kosmos', 'sayyora', 'yulduz', 'raketa', 'koinot', 'mars', 'saturn', 'oy']):
            return SceneIllustrator._draw_space_scene(s_num, scene)

        # 6. Robotlar, sun'iy intellekt, texnologiya
        elif SceneIllustrator._has_kw(text, ['robot', 'sun\'iy intellekt', 'kompyuter', 'texnologiya', 'kiber', 'dasturlash']):
            return SceneIllustrator._draw_robot_scene(s_num, scene)

        # 7. Samarqand, Registon, O'zbekiston, tarixiy obidalar
        elif SceneIllustrator._has_kw(text, ['samarqand', 'registon', 'buxoro', 'xiva', 'toshkent', 'gumbaz', 'minora', 'temur']):
            return SceneIllustrator._draw_oriental_scene(s_num, scene)

        # 8. Umumiy rang-barang tabiat va sahna
        else:
            return SceneIllustrator._draw_rich_landscape_scene(s_num, scene, topic)

    @staticmethod
    def _draw_fruit_scene(num: int, scene: Dict[str, Any], text: str) -> str:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="orchardSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#38BDF8"/><stop offset="100%" stop-color="#BAE6FD"/></linearGradient>
    <linearGradient id="greenHill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#4ADE80"/><stop offset="100%" stop-color="#16A34A"/></linearGradient>
    <linearGradient id="appleGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#EF4444"/><stop offset="100%" stop-color="#991B1B"/></linearGradient>
    <linearGradient id="bananaGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#FDE047"/><stop offset="100%" stop-color="#EAB308"/></linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#orchardSky)"/>
  <circle cx="1080" cy="140" r="80" fill="#FBBF24" opacity="0.9"/>
  <!-- Gentle Hills -->
  <path d="M-100,500 Q400,380 900,480 T1400,490 L1400,720 L-100,720 Z" fill="url(#greenHill)"/>
  
  <!-- Smiling Apple Character -->
  <g transform="translate(480, 340) scale(1.4)">
    <ellipse cx="0" cy="0" rx="90" ry="85" fill="url(#appleGrad)"/>
    <path d="M-5,-80 Q0,-120 20,-115" stroke="#78350F" stroke-width="8" fill="none" stroke-linecap="round"/>
    <ellipse cx="25" cy="-105" rx="20" ry="10" fill="#22C55E" transform="rotate(-20 25 -105)"/>
    <!-- Cute Face -->
    <circle cx="-30" cy="-10" r="10" fill="#0F172A"/><circle cx="-26" cy="-14" r="3.5" fill="#FFFFFF"/>
    <circle cx="30" cy="-10" r="10" fill="#0F172A"/><circle cx="34" cy="-14" r="3.5" fill="#FFFFFF"/>
    <ellipse cx="-45" cy="10" rx="12" ry="6" fill="#F87171" opacity="0.6"/>
    <ellipse cx="45" cy="10" rx="12" ry="6" fill="#F87171" opacity="0.6"/>
    <path d="M-20,15 Q0,35 20,15" stroke="#0F172A" stroke-width="4.5" fill="none" stroke-linecap="round"/>
  </g>

  <!-- Smiling Banana Character -->
  <g transform="translate(820, 360) scale(1.3)">
    <path d="M-60,-80 Q30,-20 30,80 Q20,10 0,-30 Z" fill="url(#bananaGrad)" stroke="#CA8A04" stroke-width="4"/>
    <circle cx="5" cy="10" r="7" fill="#0F172A"/><circle cx="8" cy="8" r="2.5" fill="#FFFFFF"/>
    <path d="M0,25 Q10,35 15,25" stroke="#0F172A" stroke-width="3" fill="none"/>
  </g>
</svg>"""

    @staticmethod
    def _draw_oriental_scene(num: int, scene: Dict[str, Any]) -> str:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="orientSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#38BDF8"/><stop offset="100%" stop-color="#FEF08A"/></linearGradient>
    <linearGradient id="domeBlue" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#06B6D4"/><stop offset="50%" stop-color="#0284C7"/><stop offset="100%" stop-color="#0369A1"/></linearGradient>
    <linearGradient id="sandGround" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FDE047"/><stop offset="100%" stop-color="#D97706"/></linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#orientSky)"/>
  <circle cx="240" cy="160" r="85" fill="#FDE047" opacity="0.9"/>
  <rect y="520" width="1280" height="200" fill="url(#sandGround)"/>
  
  <!-- Registan Madrasah Arch and Minarets -->
  <!-- Left Minaret -->
  <rect x="260" y="240" width="40" height="280" fill="#D97706"/>
  <polygon points="250,240 280,180 310,240" fill="url(#domeBlue)"/>
  
  <!-- Right Minaret -->
  <rect x="980" y="240" width="40" height="280" fill="#D97706"/>
  <polygon points="970,240 1000,180 1030,240" fill="url(#domeBlue)"/>
  
  <!-- Main Grand Portal (Peshtak) -->
  <rect x="360" y="260" width="560" height="260" fill="#B45309" rx="10"/>
  <!-- Inner Arch -->
  <path d="M460,520 L460,380 Q640,280 820,380 L820,520 Z" fill="#1E293B"/>
  
  <!-- Turquoise Main Dome behind -->
  <ellipse cx="640" cy="220" rx="140" ry="110" fill="url(#domeBlue)"/>
  <polygon points="630,110 640,70 650,110" fill="#FBBF24"/>
  
  <!-- Flying Birds -->
  <text x="360" y="160" font-size="34">🕊️</text>
  <text x="880" y="140" font-size="36">🕊️</text>
</svg>"""

    @staticmethod
    def _draw_space_scene(num: int, scene: Dict[str, Any]) -> str:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="deepSpace" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0F172A"/><stop offset="50%" stop-color="#1E1B4B"/><stop offset="100%" stop-color="#311042"/></linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#deepSpace)"/>
  <!-- Stars -->
  <circle cx="150" cy="120" r="3" fill="#FFFFFF"/><circle cx="340" cy="80" r="4" fill="#FDE047"/>
  <circle cx="850" cy="160" r="3" fill="#FFFFFF"/><circle cx="1120" cy="110" r="4" fill="#67E8F9"/>
  <circle cx="200" cy="540" r="3" fill="#FFFFFF"/><circle cx="1040" cy="580" r="4" fill="#F43F5E"/>
  
  <!-- Big Friendly Glowing Planet -->
  <circle cx="320" cy="380" r="140" fill="#6366F1" opacity="0.95"/>
  <ellipse cx="320" cy="380" rx="210" ry="40" fill="none" stroke="#A5B4FC" stroke-width="14" transform="rotate(-20 320 380)"/>
  
  <!-- Cute Cartoon Rocket -->
  <g transform="translate(820, 280) rotate(25) scale(1.5)">
    <!-- Exhaust flame -->
    <polygon points="-12,70 0,110 12,70" fill="#F97316"/>
    <polygon points="-6,70 0,95 6,70" fill="#FDE047"/>
    <!-- Rocket Body -->
    <path d="M-25,70 Q-25,0 0,-60 Q25,0 25,70 Z" fill="#F8FAFC"/>
    <!-- Red Top Cone -->
    <path d="M-18,-20 Q0,-60 0,-60 Q0,-60 18,-20 Z" fill="#EF4444"/>
    <!-- Wings -->
    <polygon points="-25,40 -50,75 -25,70" fill="#EF4444"/>
    <polygon points="25,40 50,75 25,70" fill="#EF4444"/>
    <!-- Window -->
    <circle cx="0" cy="15" r="14" fill="#0284C7"/>
    <circle cx="0" cy="15" r="10" fill="#38BDF8"/>
  </g>
</svg>"""

    @staticmethod
    def _draw_water_scene(num: int, scene: Dict[str, Any]) -> str:
        s_num = num or scene.get("scene_number", 1)
        if s_num == 2:
            # 2-sahna: Bug'lanish va Momiq bulutlar
            return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="cloudSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0284C7"/><stop offset="60%" stop-color="#38BDF8"/><stop offset="100%" stop-color="#BAE6FD"/></linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#cloudSky)"/>
  
  <!-- Warm Smiling Sun -->
  <g transform="translate(1050, 140)">
    <circle cx="0" cy="0" r="80" fill="#FBBF24"/>
    <circle cx="0" cy="0" r="65" fill="#F59E0B"/>
    <circle cx="-18" cy="-10" r="7" fill="#1E293B"/><circle cx="18" cy="-10" r="7" fill="#1E293B"/>
    <path d="M-15,15 Q0,28 15,15" stroke="#1E293B" stroke-width="4" fill="none"/>
  </g>

  <!-- Big Fluffy Cloud with Happy Face -->
  <g transform="translate(600, 200)">
    <circle cx="-130" cy="30" r="90" fill="#F8FAFC"/>
    <circle cx="130" cy="30" r="90" fill="#F8FAFC"/>
    <circle cx="0" cy="0" r="130" fill="#FFFFFF"/>
    <rect x="-130" y="50" width="260" height="70" fill="#FFFFFF"/>
    <circle cx="-35" cy="-15" r="9" fill="#0F172A"/><circle cx="35" cy="-15" r="9" fill="#0F172A"/>
    <ellipse cx="-55" cy="5" rx="10" ry="6" fill="#F43F5E" opacity="0.4"/>
    <ellipse cx="55" cy="5" rx="10" ry="6" fill="#F43F5E" opacity="0.4"/>
    <path d="M-20,10 Q0,28 20,10" stroke="#0F172A" stroke-width="4" fill="none"/>
  </g>

  <!-- Rising Steam and Tiny Flying Droplets -->
  <g opacity="0.85">
    <circle cx="320" cy="420" r="22" fill="#E0F2FE"/>
    <circle cx="480" cy="380" r="28" fill="#BAE6FD"/>
    <circle cx="760" cy="400" r="24" fill="#E0F2FE"/>
    <circle cx="890" cy="440" r="18" fill="#BAE6FD"/>
  </g>

  <!-- Lake Surface below -->
  <path d="M0,540 Q320,510 640,540 T1280,530 L1280,720 L0,720 Z" fill="#0369A1"/>
</svg>"""
        elif s_num >= 3:
            # 3-sahna: Mayin Yomg'ir, Kamalak va Gullar
            return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="rainSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#38BDF8"/><stop offset="100%" stop-color="#BAE6FD"/></linearGradient>
    <linearGradient id="grassGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#4ADE80"/><stop offset="100%" stop-color="#16A34A"/></linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#rainSky)"/>

  <!-- Rainbow Arc -->
  <g transform="translate(640, 500)" opacity="0.75">
    <ellipse cx="0" cy="0" rx="420" ry="300" fill="none" stroke="#EF4444" stroke-width="10"/>
    <ellipse cx="0" cy="0" rx="410" ry="290" fill="none" stroke="#F97316" stroke-width="10"/>
    <ellipse cx="0" cy="0" rx="400" ry="280" fill="none" stroke="#FBBF24" stroke-width="10"/>
    <ellipse cx="0" cy="0" rx="390" ry="270" fill="none" stroke="#10B981" stroke-width="10"/>
    <ellipse cx="0" cy="0" rx="380" ry="260" fill="none" stroke="#06B6D4" stroke-width="10"/>
    <ellipse cx="0" cy="0" rx="370" ry="250" fill="none" stroke="#8B5CF6" stroke-width="10"/>
  </g>

  <!-- Cheerful Rain Droplets -->
  <g fill="#0284C7" opacity="0.8">
    <path d="M220,180 C230,195 235,210 230,220 C220,230 205,225 205,215 C205,200 215,185 220,180 Z"/>
    <path d="M420,130 C430,145 435,160 430,170 C420,180 405,175 405,165 C405,150 415,135 420,130 Z"/>
    <path d="M820,140 C830,155 835,170 830,180 C820,190 805,185 805,175 C805,160 815,145 820,140 Z"/>
    <path d="M1020,190 C1030,205 1035,220 1030,230 C1020,240 1005,235 1005,225 C1005,210 1015,195 1020,190 Z"/>
  </g>

  <!-- Blooming Green Meadow -->
  <path d="M0,520 Q320,490 640,525 T1280,510 L1280,720 L0,720 Z" fill="url(#grassGrad)"/>

  <!-- Happy Blooming Flower -->
  <g transform="translate(640, 520)">
    <circle cx="-16" cy="-16" r="16" fill="#F43F5E"/><circle cx="16" cy="-16" r="16" fill="#F43F5E"/>
    <circle cx="-16" cy="16" r="16" fill="#F43F5E"/><circle cx="16" cy="16" r="16" fill="#F43F5E"/>
    <circle cx="0" cy="0" r="18" fill="#FBBF24"/>
    <circle cx="-5" cy="-4" r="3" fill="#0F172A"/><circle cx="5" cy="-4" r="3" fill="#0F172A"/>
    <path d="M-4,4 Q0,8 4,4" stroke="#0F172A" stroke-width="2" fill="none"/>
  </g>
</svg>"""
        else:
            # 1-sahna: Kichik Tomchivoy Qahramon (Jajji Tomchivoy va Iliq Quyosh)
            return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#38BDF8"/><stop offset="100%" stop-color="#BAE6FD"/></linearGradient>
    <linearGradient id="seaGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0284C7"/><stop offset="100%" stop-color="#0369A1"/></linearGradient>
    <linearGradient id="dropGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#67E8F9"/><stop offset="100%" stop-color="#0284C7"/></linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#skyGrad)"/>

  <!-- Warm Smiling Sun -->
  <g transform="translate(220, 160)">
    <circle cx="0" cy="0" r="75" fill="#FBBF24"/>
    <circle cx="0" cy="0" r="60" fill="#F59E0B"/>
    <circle cx="-18" cy="-8" r="7" fill="#1E293B"/><circle cx="18" cy="-8" r="7" fill="#1E293B"/>
    <path d="M-12,12 Q0,24 12,12" stroke="#1E293B" stroke-width="3.5" fill="none"/>
  </g>

  <!-- Big Smiling Water Drop Hero (Tomchivoy) -->
  <g transform="translate(640, 340) scale(1.45)">
    <path d="M0,-85 C50,-20 60,35 50,60 C35,85 -35,85 -50,60 C-60,35 -50,-20 0,-85 Z" fill="url(#dropGrad)"/>
    <ellipse cx="-18" cy="-20" rx="8" ry="14" fill="#FFFFFF" opacity="0.6" transform="rotate(-25 -18 -20)"/>
    <circle cx="-16" cy="20" r="7" fill="#0F172A"/><circle cx="-14" cy="18" r="2.5" fill="#FFFFFF"/>
    <circle cx="16" cy="20" r="7" fill="#0F172A"/><circle cx="18" cy="18" r="2.5" fill="#FFFFFF"/>
    <ellipse cx="-25" cy="32" rx="7" ry="4" fill="#F43F5E" opacity="0.5"/>
    <ellipse cx="25" cy="32" rx="7" ry="4" fill="#F43F5E" opacity="0.5"/>
    <path d="M-10,35 Q0,46 10,35" stroke="#0F172A" stroke-width="3" fill="none"/>
  </g>

  <!-- Flowing Blue River below -->
  <path d="M0,520 Q320,480 640,530 T1280,510 L1280,720 L0,720 Z" fill="url(#seaGrad)"/>
</svg>"""

    @staticmethod
    def _draw_robot_scene(num: int, scene: Dict[str, Any]) -> str:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="labBg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1E293B"/><stop offset="100%" stop-color="#0F172A"/></linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#labBg)"/>
  
  <!-- Glowing Circuit Lines -->
  <path d="M100,100 L300,100 L350,180 L500,180" stroke="#06B6D4" stroke-width="4" fill="none" opacity="0.6"/>
  <path d="M1180,600 L950,600 L900,520 L780,520" stroke="#8B5CF6" stroke-width="4" fill="none" opacity="0.6"/>
  
  <!-- Friendly Cartoon Robot in Center -->
  <g transform="translate(640, 360) scale(1.3)">
    <!-- Antenna -->
    <line x1="0" y1="-120" x2="0" y2="-90" stroke="#94A3B8" stroke-width="6"/>
    <circle cx="0" cy="-125" r="12" fill="#EF4444"/>
    <!-- Head -->
    <rect x="-70" y="-90" width="140" height="95" rx="20" fill="#E2E8F0" stroke="#94A3B8" stroke-width="5"/>
    <!-- Glowing Visor Screen -->
    <rect x="-55" y="-75" width="110" height="55" rx="12" fill="#0284C7"/>
    <!-- Cheerful Eyes -->
    <circle cx="-25" cy="-48" r="10" fill="#67E8F9"/>
    <circle cx="25" cy="-48" r="10" fill="#67E8F9"/>
    <path d="M-15,-30 Q0,-20 15,-30" stroke="#67E8F9" stroke-width="4" fill="none" stroke-linecap="round"/>
    <!-- Body -->
    <rect x="-85" y="15" width="170" height="130" rx="25" fill="#3B82F6"/>
    <!-- Heart Meter -->
    <circle cx="0" cy="80" r="28" fill="#1E3A8A"/>
    <text x="0" y="88" font-size="28" text-anchor="middle" fill="#F43F5E">❤️</text>
  </g>
</svg>"""

    @staticmethod
    def _draw_animal_scene(num: int, scene: Dict[str, Any], text: str) -> str:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="savannahSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FDE047"/><stop offset="100%" stop-color="#FB923C"/></linearGradient>
    <linearGradient id="savannahGround" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#EAB308"/><stop offset="100%" stop-color="#B45309"/></linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#savannahSky)"/>
  <circle cx="200" cy="180" r="90" fill="#FEF08A" opacity="0.9"/>
  <path d="M-100,520 Q400,440 900,530 T1400,500 L1400,720 L-100,720 Z" fill="url(#savannahGround)"/>
  
  <!-- Friendly Lion / King of Animals in Center -->
  <g transform="translate(640, 420) scale(1.3)">
    <!-- Mane -->
    <circle cx="0" cy="-40" r="95" fill="#C2410C"/>
    <!-- Face -->
    <circle cx="0" cy="-40" r="65" fill="#FBBF24"/>
    <!-- Ears -->
    <circle cx="-50" cy="-90" r="18" fill="#FBBF24"/><circle cx="-50" cy="-90" r="9" fill="#F87171"/>
    <circle cx="50" cy="-90" r="18" fill="#FBBF24"/><circle cx="50" cy="-90" r="9" fill="#F87171"/>
    <!-- Eyes -->
    <circle cx="-22" cy="-45" r="9" fill="#0F172A"/><circle cx="-19" cy="-48" r="3" fill="#FFFFFF"/>
    <circle cx="22" cy="-45" r="9" fill="#0F172A"/><circle cx="25" cy="-48" r="3" fill="#FFFFFF"/>
    <!-- Nose & Mouth -->
    <polygon points="-10,-30 0,-15 10,-30" fill="#78350F"/>
    <path d="M-14,-10 Q0,5 14,-10" stroke="#78350F" stroke-width="4" fill="none" stroke-linecap="round"/>
    <!-- Body -->
    <path d="M-45,25 Q0,-10 45,25 L55,110 L-55,110 Z" fill="#F59E0B"/>
  </g>
</svg>"""

    @staticmethod
    def _draw_autumn_scene(num: int, scene: Dict[str, Any]) -> str:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="autSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#38BDF8"/><stop offset="100%" stop-color="#FEF08A"/></linearGradient>
    <linearGradient id="autHill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FBBF24"/><stop offset="100%" stop-color="#D97706"/></linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#autSky)"/>
  <circle cx="200" cy="150" r="70" fill="#FDE047" opacity="0.9"/>
  <path d="M-100,520 Q400,450 800,510 T1400,530 L1400,720 L-100,720 Z" fill="url(#autHill)"/>
  
  <!-- Grand Tree with Green and Gold Leaves -->
  <path d="M780,680 Q810,480 800,320 Q830,480 860,680 Z" fill="#78350F"/>
  <circle cx="700" cy="260" r="110" fill="#84CC16" opacity="0.95"/>
  <circle cx="880" cy="240" r="115" fill="#EAB308" opacity="0.95"/>
  <circle cx="800" cy="180" r="125" fill="#F97316" opacity="0.95"/>
  <!-- Friendly Cartoon Eyes on Tree -->
  <circle cx="785" cy="380" r="12" fill="#FFFFFF"/><circle cx="787" cy="380" r="6" fill="#1E293B"/>
  <circle cx="825" cy="380" r="12" fill="#FFFFFF"/><circle cx="827" cy="380" r="6" fill="#1E293B"/>
  
  <!-- Swirling Leaves -->
  <text x="320" y="340" font-size="44">🍂</text>
  <text x="540" y="440" font-size="52">🍁</text>
  <text x="960" y="380" font-size="48">🍃</text>
</svg>"""

    @staticmethod
    def _draw_rich_landscape_scene(num: int, scene: Dict[str, Any], topic: str) -> str:
        colors = [
            ("#38BDF8", "#FDE047", "#4ADE80", "#16A34A"),
            ("#818CF8", "#F472B6", "#FBBF24", "#D97706"),
            ("#34D399", "#67E8F9", "#A7F3D0", "#059669"),
            ("#FB923C", "#FDE047", "#FED7AA", "#EA580C")
        ]
        c1, c2, g1, g2 = colors[(num - 1) % len(colors)]
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="genSky{num}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c1}"/><stop offset="100%" stop-color="{c2}"/></linearGradient>
    <linearGradient id="genGround{num}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{g1}"/><stop offset="100%" stop-color="{g2}"/></linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#genSky{num})"/>
  <circle cx="200" cy="150" r="75" fill="#FEF08A" opacity="0.95"/>
  <path d="M-100,480 Q400,390 850,470 T1400,460 L1400,720 L-100,720 Z" fill="url(#genGround{num})"/>
  
  <!-- Friendly Clouds -->
  <circle cx="850" cy="180" r="50" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="910" cy="170" r="65" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="970" cy="180" r="50" fill="#FFFFFF" opacity="0.9"/>
  
  <!-- Center Star/Badge -->
  <circle cx="640" cy="350" r="100" fill="#FFFFFF" opacity="0.3"/>
  <text x="640" y="380" font-size="100" text-anchor="middle">✨</text>
</svg>"""
