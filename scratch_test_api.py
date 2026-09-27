import httpx
import json

payload = {
    'topic': "2 ga 2 ni qo'shish",
    'prompt': '',
    'age_group': '5-7',
    'duration_seconds': 36,
    'visual_style_id': 'pixar_3d',
    'language': 'uz'
}

try:
    r = httpx.post('http://127.0.0.1:8000/api/generate-screenplay', json=payload, timeout=30.0)
    print("STATUS:", r.status_code)
    data = r.json()
    sc = data.get('screenplay', {})
    print("TITLE:", sc.get('title'))
    for s in sc.get('scenes', []):
        print(f"Scene {s.get('scene_number')}: {s.get('narration')}")
        beats = s.get('visual_beats', [])
        for b in beats:
            print(f"  Step: {b.get('badge')} | Main: {b.get('main_text')} | Sub: {b.get('sub_text')} | Icons count: {len(b.get('icons', []))}")
except Exception as e:
    print("ERROR:", e)
