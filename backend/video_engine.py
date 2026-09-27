import os
import json
import urllib.parse
import httpx
from typing import Dict, Any, List, Optional
from backend.config import Config

class GenerativeVideoEngine:
    """Video generatsiya moduli: Kling AI, Runway hamda 100% BEPUL Pollinations Flux animatsion vositasi."""

    KLING_API_URL = "https://api.klingai.com/v1/videos/text2video"
    RUNWAY_API_URL = "https://api.runwayml.com/v1/tasks"

    @staticmethod
    async def render_scene_video(
        scene: Dict[str, Any],
        visual_style: str,
        engine_type: str = "kling",
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        
        prompt = scene.get("visual_prompt", "")
        duration = min(10, scene.get("duration_seconds", 8))
        scene_num = scene.get("scene_number", 1)
        
        # 1. Bepul va ultra-tezkor Flux AI illyustratsiya havolasi (Pollinations AI - $0 xarajat)
        encoded_prompt = urllib.parse.quote(prompt[:300])
        free_ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=flux&nologo=true&seed={scene_num * 103}"

        # 2. Agar Kling AI yoki Runway API kaliti kiritilgan bo'lsa
        if engine_type == "kling" and (api_key or Config.KLING_API_KEY):
            token = api_key or Config.KLING_API_KEY
            try:
                headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
                payload = {
                    "model": "kling-v1.5-pro",
                    "prompt": prompt,
                    "duration": duration,
                    "aspect_ratio": "16:9",
                    "mode": "high_quality"
                }
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(GenerativeVideoEngine.KLING_API_URL, json=payload, headers=headers)
                    if resp.status_code in [200, 201, 202]:
                        return {
                            "status": "processing",
                            "engine": "Kling AI Pro",
                            "task_id": resp.json().get("task_id", f"kling_task_{scene_num}"),
                            "scene_number": scene_num,
                            "image_url": free_ai_image_url
                        }
            except Exception as e:
                print(f"Kling AI xatolik: {e}")

        # 3. Tejamkor va bepul AI video/animatsiya paketi
        palette = GenerativeVideoEngine._get_scene_palette(scene_num)
        
        return {
            "status": "completed",
            "engine": "KidsVidEdu Free AI Visual Storyboard Engine (Pollinations Flux + Remotion Motion)",
            "scene_number": scene_num,
            "title": scene.get("title", ""),
            "duration": duration,
            "visual_prompt": prompt,
            "image_url": free_ai_image_url,
            "palette": palette,
            "camera_movement": scene.get("camera_movement", "slow_dolly_in"),
            "sound_effect": scene.get("sound_effect", "sparkle"),
            "preview_type": "dynamic_canvas_render"
        }

    @staticmethod
    def assemble_full_video_package(screenplay: Dict[str, Any], voice_info: Dict[str, Any]) -> Dict[str, Any]:
        """Barcha sahnalar, ovoz, bepul AI rasmlar va subtitrlarni yaxlit montajga birlashtiradi."""
        scenes = screenplay.get("scenes", [])
        total_duration = sum(s.get("duration_seconds", 8) for s in scenes)
        
        timeline = []
        current_time = 0.0

        for s in scenes:
            dur = s.get("duration_seconds", 8)
            s_num = s.get("scene_number", 1)
            palette = GenerativeVideoEngine._get_scene_palette(s_num)
            
            # Har bir sahna uchun bepul Flux AI tasvir havolasi
            encoded_prompt = urllib.parse.quote(s.get("visual_prompt", "")[:300])
            ai_image = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=flux&nologo=true&seed={s_num * 103}"

            timeline.append({
                "scene_number": s_num,
                "title": s.get("title"),
                "start_time": current_time,
                "end_time": current_time + dur,
                "duration": dur,
                "narration": s.get("narration"),
                "visual_prompt": s.get("visual_prompt"),
                "image_url": ai_image,
                "camera_movement": s.get("camera_movement"),
                "emotion": s.get("emotion"),
                "sound_effect": s.get("sound_effect"),
                "palette": palette
            })
            current_time += dur

        return {
            "project_name": screenplay.get("title", "KidsVidEdu Loyihasi"),
            "age_group": screenplay.get("age_group"),
            "total_duration": total_duration,
            "voice": voice_info,
            "timeline": timeline,
            "status": "ready_to_play",
            "render_quality": "1080p Full HD (Animated Visual Storyboard)",
            "aspect_ratio": "16:9"
        }

    @staticmethod
    def _get_scene_palette(scene_num: int) -> Dict[str, str]:
        palettes = [
            {"bg_gradient": "linear-gradient(135deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%)", "accent": "#FFEAA7", "text": "#FFFFFF"},
            {"bg_gradient": "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)", "accent": "#FEE140", "text": "#1E293B"},
            {"bg_gradient": "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)", "accent": "#FA709A", "text": "#0F172A"},
            {"bg_gradient": "linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)", "accent": "#FFDF00", "text": "#1E1B4B"},
            {"bg_gradient": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)", "accent": "#4FACFE", "text": "#312E81"}
        ]
        return palettes[(scene_num - 1) % len(palettes)]
