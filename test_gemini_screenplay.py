import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY", "")
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={key}'

prompt = """
Sen jahon darajasidagi bolalar multfilm rejissyori va ssenarisisan (Disney, Pixar, O'zbekfilm).
Mavzu: Daraxtlar nega barg to'kadi?
Yosh toifasi: 5-7 yosh
Davomiyligi: 50 soniya
Sahnalar soni: 5 ta

QAT'IY TALABLAR:
1. Sahnalar bir-birini mutlaqo takrorlamasin! 1 va 2, 3 va 4 bir xil bo'lishi qat'iyan man etiladi.
2. Har bir sahna mavzuning aniq bir yangi qadamini ochib bersin:
   - 1-sahna: Kuz kelishi va qiziq jumboq (Nega daraxtlar yashil kiyimini yechyapti?).
   - 2-sahna: Asosiy ilmiy sabab (Qishda sovuq bo'ladi, suv muzlaydi. Daraxt o'z tanasidagi suvni saqlash uchun barglarini to'kadi).
   - 3-sahna: Ranglar mo'jizasi (Xlorofill kamayib, oltin, sariq va qizil bo'yoqlar jilvalanadi).
   - 4-sahna: Yerga tushgan barglarning foydasi (Ular yerga issiq adyol bo'lib, daraxt ildizlarini sovuqdan himoya qiladi).
   - 5-sahna: Shirin qishki uyqu va bahor umidi (Daraxtlar orom oladi, bahorda yangi kurtaklar yozadi).
3. Har bir sahna nutqi (narration) kamida 2-3 ta samimiy, bolalarbop gapdan iborat bo'lsin.

Javobni quyidagi JSON formatida qaytar:
{
  "title": "Daraxtlarning Oltin Ko'rpasi",
  "moral_summary": "Tabiatdagi har bir o'zgarishda katta hikmat va go'zallik bor.",
  "scenes": [
    {
      "scene_number": 1,
      "title": "1-sahna nomi",
      "duration_seconds": 10,
      "stage": "hook",
      "narration": "O'zbekcha ifodali 2-3 gap",
      "visual_prompt": "3D Pixar cartoon style scene prompt",
      "camera_movement": "Sekin yaqinlashish (Dolly in)",
      "emotion": "hayrat"
    }
  ]
}
"""

payload = {
    'contents': [{'parts': [{'text': prompt}]}],
    'generationConfig': {'response_mime_type': 'application/json'}
}

with httpx.Client(timeout=35.0) as client:
    res = client.post(url, json=payload)
    data = res.json()
    script = json.loads(data['candidates'][0]['content']['parts'][0]['text'])
    print("Title:", script['title'])
    for s in script['scenes']:
        print(f"Sahna {s['scene_number']}: {s['title']}")
        print(f"   Nutq: {s['narration']}")
        print(f"   Kamera: {s['camera_movement']}")
