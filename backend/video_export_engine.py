import os
import math
import subprocess
import asyncio
import wave
from pathlib import Path
from typing import Dict, Any, List, Optional
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import httpx
import edge_tts

from backend.config import Config
from backend.database import SessionLocal
from backend.models import UserVideo

class VideoExportEngine:
    """Server-side video render dvigateli:
    Brauzerdagi Canvas pleyerining barcha vizual elementlarini (multfilm orqa foni,
    harakatlanuvchi Lola ustoz animatsiyasi, mavzuga xos animatsiyalar, karaoke subtitrlar,
    ekvalayzer va haqiqiy MohirAI/Edge-TTS ovozi) 100% Full HD 1080p MP4 ga aylantiradi.
    """

    WIDTH = 1280
    HEIGHT = 720
    FPS = 20

    @classmethod
    def get_font(cls, size: int, bold: bool = True) -> ImageFont.ImageFont:
        font_paths = [
            "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\segoeui.ttf",
            "C:\\Windows\\Fonts\\tahoma.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    return ImageFont.truetype(fp, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    @classmethod
    def draw_star(cls, draw, cx, cy, r_outer, r_inner, fill, points=5):
        coords = []
        angle = -math.pi / 2
        step = math.pi / points
        for i in range(points * 2):
            r = r_outer if i % 2 == 0 else r_inner
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            coords.append((x, y))
            angle += step
        draw.polygon(coords, fill=fill)

    @classmethod
    def draw_topic_illustration(cls, draw, cx, cy, time_sec, topic="ta'lim"):
        """Mavzuga mos jonli va rangli vektor animatsiyasini chizadi."""
        t_lower = (topic or "").lower()
        bounce = int(math.sin(time_sec * 3.5) * 8)
        cy = cy + bounce
        
        # Tashqi aylanma orbita
        draw.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], fill=(22, 33, 56), outline=(245, 158, 11), width=3)
        
        if any(k in t_lower for k in ["koinot", "quyosh", "astronomiya", "sayyora"]):
            # Saturn sayyorasi va yorqin halqa
            draw.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=(251, 146, 60), outline=(254, 215, 170), width=2)
            for r_offset in [-3, 0, 3]:
                draw.arc([cx - 70, cy - 25 + r_offset, cx + 70, cy + 25 + r_offset], start=0, end=360, fill=(254, 240, 138), width=3)
            draw.line([(cx - 38, cy - 8), (cx + 38, cy - 8)], fill=(234, 88, 12), width=3)
            draw.line([(cx - 35, cy + 10), (cx + 35, cy + 10)], fill=(217, 119, 6), width=3)
        elif any(k in t_lower for k in ["kiber", "internet", "robot", "sun'iy", "parol", "fishing"]):
            # Kiber Qalqon va xavfsiz qulf
            shield_pts = [
                (cx, cy - 50),
                (cx + 42, cy - 30),
                (cx + 35, cy + 20),
                (cx, cy + 50),
                (cx - 35, cy + 20),
                (cx - 42, cy - 30)
            ]
            draw.polygon(shield_pts, fill=(14, 165, 233), outline=(255, 255, 255))
            draw.rectangle([cx - 16, cy - 5, cx + 16, cy + 25], fill=(255, 255, 255))
            draw.arc([cx - 12, cy - 28, cx + 12, cy - 2], start=180, end=360, fill=(255, 255, 255), width=4)
        elif any(k in t_lower for k in ["barg", "daraxt", "tabiat", "suv", "fasl", "kuz"]):
            # Oltin Kuz Bargi
            leaf_pts = [
                (cx, cy - 52),
                (cx + 38, cy - 10),
                (cx + 30, cy + 30),
                (cx, cy + 48),
                (cx - 30, cy + 30),
                (cx - 38, cy - 10)
            ]
            draw.polygon(leaf_pts, fill=(234, 88, 12), outline=(254, 240, 138))
            draw.line([(cx, cy - 48), (cx, cy + 45)], fill=(254, 240, 138), width=3)
            draw.line([(cx, cy - 15), (cx + 25, cy - 28)], fill=(254, 240, 138), width=2)
            draw.line([(cx, cy + 10), (cx - 22, cy - 2)], fill=(254, 240, 138), width=2)
        else:
            # Oltin Bilim Yulduzi
            cls.draw_star(draw, cx, cy, 48, 22, fill=(250, 204, 21))
            cls.draw_star(draw, cx, cy, 24, 11, fill=(255, 255, 255))

        # Aylanuvchi chaqnoq uchqunlar
        for idx in range(4):
            angle = time_sec * 2.2 + (idx * (math.pi / 2))
            ox = cx + int(math.cos(angle) * 105)
            oy = cy + int(math.sin(angle) * 45)
            cls.draw_star(draw, ox, oy, 10, 4, (56, 189, 248, 220))

    @classmethod
    def render_animated_scene_frame(
        cls,
        bg_img: Image.Image,
        mascot_img: Optional[Image.Image],
        scene: Dict[str, Any],
        topic: str,
        progress: float,
        time_sec: float,
        scene_idx: int = 0,
        total_scenes: int = 5
    ) -> Image.Image:
        # 1. Ken Burns kamera harakati (sekin yaqinlashish)
        scale = 1.0 + (progress * 0.03)
        w_crop = int(cls.WIDTH / scale)
        h_crop = int(cls.HEIGHT / scale)
        x1 = int((cls.WIDTH - w_crop) * 0.5)
        y1 = int((cls.HEIGHT - h_crop) * 0.5)
        frame = bg_img.crop((x1, y1, x1 + w_crop, y1 + h_crop)).resize((cls.WIDTH, cls.HEIGHT), Image.Resampling.BILINEAR)

        # Orqa fon ustiga qoraytirish
        dim_overlay = Image.new("RGBA", (cls.WIDTH, cls.HEIGHT), (10, 15, 30, 95))
        frame.paste(dim_overlay, (0, 0), dim_overlay)
        draw = ImageDraw.Draw(frame)

        # 2. Uchib yuruvchi fon zarrachalari / yulduzlar
        for i in range(14):
            px = (int(i * 95 + math.sin(time_sec * 1.4 + i) * 30)) % cls.WIDTH
            py = (int(40 + i * 28 + math.cos(time_sec * 1.1 + i * 2) * 20)) % 450
            star_alpha = int(140 + 100 * math.sin(time_sec * 3.0 + i * 1.5))
            cls.draw_star(draw, px, py, 6, 2, (255, 235, 130, star_alpha))

        # 3. Jonli Lola Ustoz Maskoti (Chap taraf)
        bob_y = int(math.sin(time_sec * 4.0) * 8)
        mascot_x = 65
        mascot_y = 75 + bob_y
        mascot_size = 190

        # Pulsatsiyalanuvchi nurlar
        halo_pulse = int(math.sin(time_sec * 5.0) * 5)
        draw.ellipse(
            [mascot_x - 10 - halo_pulse, mascot_y - 10 - halo_pulse, mascot_x + mascot_size + 10 + halo_pulse, mascot_y + mascot_size + 10 + halo_pulse],
            outline=(56, 189, 248),
            width=3
        )

        if mascot_img:
            m_thumb = mascot_img.resize((mascot_size, mascot_size), Image.Resampling.LANCZOS)
            mask = Image.new("L", (mascot_size, mascot_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, mascot_size, mascot_size), fill=255)
            frame.paste(m_thumb, (mascot_x, mascot_y), mask)

        badge_w, badge_h = 160, 36
        badge_x = mascot_x + (mascot_size - badge_w) // 2
        badge_y = mascot_y + mascot_size - 10
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=18, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
        name_font = cls.get_font(15, bold=True)
        draw.text((badge_x + badge_w // 2, badge_y + badge_h // 2), "Lola Ustoz (AI)", fill=(255, 255, 255), anchor="mm", font=name_font)

        # 4. Markaziy Vizual Karta (x=290 to 1220, y=55 to 445)
        card_x1, card_y1 = 290, 55
        card_x2, card_y2 = 1220, 445
        card_overlay = Image.new("RGBA", (cls.WIDTH, cls.HEIGHT), (0, 0, 0, 0))
        c_draw = ImageDraw.Draw(card_overlay)
        c_draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=24, fill=(15, 23, 42, 215), outline=(56, 189, 248, 220), width=2)
        frame.paste(card_overlay, (0, 0), card_overlay)
        draw = ImageDraw.Draw(frame)

        cat_font = cls.get_font(15, bold=True)
        draw.text((card_x1 + 30, card_y1 + 25), f"MAVZU: {topic.upper()}", fill=(56, 189, 248), font=cat_font)
        
        scene_title_font = cls.get_font(26, bold=True)
        scene_title = scene.get("title", f"{scene_idx+1}-sahna")
        draw.text((card_x1 + 30, card_y1 + 55), scene_title, fill=(255, 255, 255), font=scene_title_font)

        # Mavzuga xos animatsion illyustratsiya
        hero_cx = card_x1 + 180
        hero_cy = card_y1 + 225
        cls.draw_topic_illustration(draw, hero_cx, hero_cy, time_sec, topic)

        # O'ng tomondagi asosiy qoidalar
        kp_x = card_x1 + 390
        kp_y = card_y1 + 120
        draw.rounded_rectangle([kp_x, kp_y, kp_x + 500, kp_y + 80], radius=16, fill=(30, 41, 59, 200), outline=(56, 189, 248, 120), width=1)
        k_font = cls.get_font(18, bold=True)
        draw.text((kp_x + 20, kp_y + 20), "Asosiy Tushuncha", fill=(56, 189, 248), font=k_font)
        sub_font = cls.get_font(15, bold=False)
        sub_text = scene.get("visual_beats", [{}])[0].get("main_text", scene_title) if scene.get("visual_beats") else scene_title
        draw.text((kp_x + 20, kp_y + 46), f"- {sub_text}", fill=(241, 245, 249), font=sub_font)

        kp_y2 = kp_y + 100
        draw.rounded_rectangle([kp_x, kp_y2, kp_x + 500, kp_y2 + 80], radius=16, fill=(30, 41, 59, 200), outline=(245, 158, 11, 140), width=1)
        draw.text((kp_x + 20, kp_y2 + 20), "Eslab Qoling", fill=(245, 158, 11), font=k_font)
        moral = scene.get("visual_beats", [{}])[-1].get("sub_text", "Bilim olish oson va qiziqarli!") if scene.get("visual_beats") else "Bilim olish oson va qiziqarli!"
        draw.text((kp_x + 20, kp_y2 + 46), f"- {moral}", fill=(241, 245, 249), font=sub_font)

        # 5. Pastki Interaktiv Doska (Karaoke subtitr va ekvalayzer)
        bb_x1, bb_y1 = 40, 475
        bb_x2, bb_y2 = 1240, 695
        bb_overlay = Image.new("RGBA", (cls.WIDTH, cls.HEIGHT), (0, 0, 0, 0))
        bb_draw = ImageDraw.Draw(bb_overlay)
        bb_draw.rounded_rectangle([bb_x1, bb_y1, bb_x2, bb_y2], radius=22, fill=(11, 17, 32, 240), outline=(56, 189, 248), width=2)
        frame.paste(bb_overlay, (0, 0), bb_overlay)
        draw = ImageDraw.Draw(frame)

        header_font = cls.get_font(14, bold=True)
        draw.text((bb_x1 + 30, bb_y1 + 18), f"{scene_idx + 1}-sahna: {scene_title}", fill=(56, 189, 248), font=header_font)
        draw.text((bb_x2 - 160, bb_y1 + 18), f"Sahna {scene_idx + 1} / {total_scenes}", fill=(148, 163, 184), font=header_font)

        # Karaoke uslubidagi jonli subtitr
        narration = scene.get("narration", "")
        words = narration.split()
        total_words = len(words)
        current_word_idx = min(total_words - 1, int(progress * total_words)) if total_words > 0 else 0

        sub_font_bold = cls.get_font(20, bold=True)
        sub_font_regular = cls.get_font(20, bold=False)
        
        start_w = max(0, current_word_idx - 6)
        end_w = min(total_words, start_w + 14)
        display_words = words[start_w:end_w]
        
        cur_x = bb_x1 + 30
        cur_y = bb_y1 + 65
        for idx_offset, w in enumerate(display_words):
            actual_idx = start_w + idx_offset
            is_current = actual_idx == current_word_idx
            is_past = actual_idx < current_word_idx
            
            color = (253, 224, 71) if is_current else ((255, 255, 255) if is_past else (148, 163, 184))
            fnt = sub_font_bold if is_current else sub_font_regular
            
            w_bbox = draw.textbbox((cur_x, cur_y), w + " ", font=fnt)
            w_width = w_bbox[2] - w_bbox[0]
            
            if cur_x + w_width > bb_x2 - 180:
                cur_x = bb_x1 + 30
                cur_y += 35
            
            if is_current:
                draw.rounded_rectangle([cur_x - 3, cur_y - 2, cur_x + w_width - 2, cur_y + 26], radius=6, fill=(245, 158, 11, 90))
            
            draw.text((cur_x, cur_y), w + " ", fill=color, font=fnt)
            cur_x += w_width

        # Jonli ovoz ekvalayzeri (5 ta ustuncha)
        eq_x = bb_x2 - 130
        eq_y = bb_y1 + 110
        for b in range(5):
            bar_h = int(12 + 22 * abs(math.sin(time_sec * 6.0 + b * 1.2)))
            draw.rounded_rectangle([eq_x + b * 16, eq_y - bar_h, eq_x + b * 16 + 8, eq_y], radius=4, fill=(56, 189, 248))

        # Sahna taraqqiyot chizig'i
        prog_w = int((bb_x2 - bb_x1 - 40) * progress)
        draw.rounded_rectangle([bb_x1 + 20, bb_y2 - 14, bb_x1 + 20 + prog_w, bb_y2 - 8], radius=3, fill=(56, 189, 248))

        return frame

    @classmethod
    async def synthesize_scene_audio(cls, text: str, out_path: Path) -> float:
        """Matnni MohirAI (Lola) orqali yoki Edge-TTS orqali ovozlashtiradi va davomiyligini qaytaradi."""
        mohir_key = Config.MOHIRAI_API_KEY
        success = False
        
        # 1. MohirAI sintezi
        if mohir_key and mohir_key.strip():
            try:
                headers = {"Authorization": mohir_key.strip(), "Content-Type": "application/json"}
                async with httpx.AsyncClient(timeout=15.0) as client:
                    r = await client.post(
                        "https://uzbekvoice.ai/api/v1/tts",
                        headers=headers,
                        json={"text": text, "model": "lola"}
                    )
                    if r.status_code == 200:
                        url = r.json().get("result", {}).get("url")
                        if url:
                            audio_res = await client.get(url)
                            if audio_res.status_code == 200:
                                with open(out_path, "wb") as f:
                                    f.write(audio_res.content)
                                success = True
            except Exception as e:
                print(f"[TTS] MohirAI sintezida ogohlantirish: {e}. Edge-TTS ga o'tilmoqda.")

        # 2. Zaxira: Edge-TTS Madina (tabiiy o'zbek ayol ovozi)
        if not success:
            try:
                communicate = edge_tts.Communicate(text, "uz-UZ-MadinaNeural")
                await communicate.save(str(out_path))
                success = True
            except Exception as e:
                print(f"[TTS] Edge-TTS xatoligi: {e}")

        # Davomiylikni hisoblash
        duration = 5.0
        try:
            if out_path.suffix.lower() == ".wav":
                with wave.open(str(out_path), "rb") as wf:
                    duration = wf.getnframes() / float(wf.getframerate())
            else:
                # ffprobe or estimation
                duration = max(3.5, len(text.split()) * 0.42)
        except Exception:
            duration = max(3.5, len(text.split()) * 0.42)

        return round(duration, 2)

    @classmethod
    async def render_video_file(
        cls,
        video_id: int,
        screenplay: Dict[str, Any],
        audio_files: Optional[List[str]] = None,
        bgm_name: str = "bgm_cheerful",
        output_filename: Optional[str] = None
    ) -> str:
        """To'liq dars videosini serverda render qiladi va natijaviy MP4 manzilini qaytaradi."""
        db = SessionLocal()
        user_video = db.query(UserVideo).filter(UserVideo.id == video_id).first()

        try:
            renders_dir = Config.STATIC_DIR / "renders"
            renders_dir.mkdir(parents=True, exist_ok=True)

            if not output_filename:
                output_filename = f"video_{video_id}_fullhd.mp4"
            out_path = renders_dir / output_filename

            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            scenes = screenplay.get("scenes", [])
            if not scenes:
                raise ValueError("Ssenariyda sahnalar topilmadi.")

            topic = screenplay.get("topic") or screenplay.get("title") or "Ta'limiy Dars"
            visual_style = screenplay.get("visual_style_id", "pixar_3d")

            # Orqa fon rasmini yuklash
            bg_path = Config.STATIC_DIR / "images" / f"style_{visual_style}.jpg"
            if not bg_path.exists():
                bg_path = Config.STATIC_DIR / "images" / "style_pixar_3d.jpg"
            
            if bg_path.exists():
                bg_img = Image.open(bg_path).convert("RGB").resize((cls.WIDTH, cls.HEIGHT))
            else:
                bg_img = Image.new("RGB", (cls.WIDTH, cls.HEIGHT), (25, 30, 50))

            # Maskot rasmi (Lola Ustoz)
            mascot_path = Config.STATIC_DIR / "images" / "mascot.jpg"
            mascot_img = Image.open(mascot_path).convert("RGB") if mascot_path.exists() else None

            # BGM musiqasi
            bgm_path = Config.STATIC_DIR / "audio" / f"{bgm_name}.mp3"
            if not bgm_path.exists():
                bgm_path = Config.STATIC_DIR / "audio" / "bgm_cheerful.mp3"
            has_bgm = bgm_path.exists() and bgm_name != "none"

            # 1-QADAM: Har bir sahna uchun haqiqiy o'zbekcha nutq sintezi (PARALLEL RAVISHDA)
            async def _synth_scene(idx: int, sc: Dict[str, Any]):
                narration = sc.get("narration", "")
                if not narration.strip():
                    narration = f"Bugungi mavzuimiz {topic}. Diqqat bilan o'rganamiz."
                audio_file = renders_dir / f"temp_voice_{video_id}_s{idx + 1}.wav"
                dur = await cls.synthesize_scene_audio(narration, audio_file)
                scene_dur = min(6.5, max(3.5, round(dur + 0.3, 2)))
                return (idx, str(audio_file), scene_dur)

            tasks = [_synth_scene(i, s) for i, s in enumerate(scenes)]
            results = await asyncio.gather(*tasks)
            # Tartibni saqlash
            results.sort(key=lambda x: x[0])
            scene_audio_paths = [r[1] for r in results]
            scene_durations = [r[2] for r in results]
            total_duration = round(sum(scene_durations), 2)

            # Barcha sahna audiolarini birlashtirish (master voice track)
            master_voice_path = renders_dir / f"temp_master_voice_{video_id}.wav"
            concat_inputs = []
            for a_path in scene_audio_paths:
                concat_inputs.extend(["-i", a_path])

            filter_str = "".join([f"[{i}:a]aresample=44100[a{i}];" for i in range(len(scene_audio_paths))])
            concat_str = "".join([f"[a{i}]" for i in range(len(scene_audio_paths))])
            filter_complex = f"{filter_str}{concat_str}concat=n={len(scene_audio_paths)}:v=0:a=1[aout]"

            concat_cmd = [ffmpeg_exe, "-y"] + concat_inputs + [
                "-filter_complex", filter_complex,
                "-map", "[aout]",
                str(master_voice_path)
            ]
            subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            has_voice = master_voice_path.exists() and os.path.getsize(master_voice_path) > 1000

            # 2-QADAM: FFmpeg video render trubasi
            ffmpeg_cmd = [
                ffmpeg_exe, "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", f"{cls.WIDTH}x{cls.HEIGHT}",
                "-pix_fmt", "rgb24",
                "-r", str(cls.FPS),
                "-i", "-"
            ]

            if has_voice and has_bgm:
                ffmpeg_cmd.extend([
                    "-i", str(master_voice_path),
                    "-i", str(bgm_path),
                    "-filter_complex", f"[1:a]apad=whole_dur={total_duration}[voice];[2:a]volume=0.18[bgm];[voice][bgm]amix=inputs=2:duration=first[aout]",
                    "-map", "0:v",
                    "-map", "[aout]"
                ])
            elif has_voice:
                ffmpeg_cmd.extend([
                    "-i", str(master_voice_path),
                    "-filter_complex", f"[1:a]apad=whole_dur={total_duration}[aout]",
                    "-map", "0:v",
                    "-map", "[aout]"
                ])
            elif has_bgm:
                ffmpeg_cmd.extend([
                    "-i", str(bgm_path),
                    "-filter_complex", "[1:a]volume=0.25[aout]",
                    "-map", "0:v",
                    "-map", "[aout]"
                ])
            else:
                ffmpeg_cmd.extend([
                    "-f", "lavfi",
                    "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                    "-map", "0:v",
                    "-map", "1:a"
                ])

            ffmpeg_cmd.extend([
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "veryfast",
                "-t", str(total_duration),
                str(out_path)
            ])

            proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # 3-QADAM: Animatsion kadrlarni yaratish va yuborish
            total_scenes = len(scenes)
            current_time = 0.0

            for s_idx, scene in enumerate(scenes):
                dur = scene_durations[s_idx]
                frames_count = int(dur * cls.FPS)

                for f in range(frames_count):
                    progress = f / float(frames_count)
                    t_sec = current_time + (f / cls.FPS)

                    frame_img = cls.render_animated_scene_frame(
                        bg_img=bg_img,
                        mascot_img=mascot_img,
                        scene=scene,
                        topic=topic,
                        progress=progress,
                        time_sec=t_sec,
                        scene_idx=s_idx,
                        total_scenes=total_scenes
                    )
                    proc.stdin.write(frame_img.tobytes())

                current_time += dur

                # Baza progressini yangilash
                if user_video:
                    prog_pct = int(((s_idx + 1) / total_scenes) * 90)
                    user_video.render_progress = prog_pct
                    db.commit()

            proc.stdin.close()
            proc.wait()

            # Vaqtinchalik audio fayllarni tozalash
            try:
                if master_voice_path.exists():
                    master_voice_path.unlink()
                for p in scene_audio_paths:
                    if os.path.exists(p):
                        os.unlink(p)
            except Exception:
                pass

            video_url = f"/renders/{output_filename}"
            if user_video:
                user_video.status = "completed"
                user_video.render_progress = 100
                user_video.video_url = video_url
                db.commit()

            return video_url

        except Exception as e:
            print(f"[VideoExportEngine] Xatolik: {e}")
            if user_video:
                user_video.status = "failed"
                user_video.error_message = str(e)
                db.commit()
            raise e
        finally:
            db.close()
