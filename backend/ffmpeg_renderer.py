import os
import sys
import re
import html
import shutil
import tempfile
import subprocess
import wave
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import httpx
from PIL import Image

logger = logging.getLogger("tasvirlab.ffmpeg")

class FFmpegRenderer:
    """
    TasvirLab Server 1080p Full HD MP4 Render Dvigateli (FFmpeg).
    Barcha sahnalar (SVG/AI tasvirlar, pastki ta'limiy doska va subtitr paneli,
    Lola ustoz audio treki va fon musiqasi)ni haqiqiy broadcast sifatli H.264/AAC
    MP4 video faylga jamlaydi.
    """

    @staticmethod
    def get_ffmpeg_exe() -> str:
        """FFmpeg dasturining bajariluvchi faylini aniqlash."""
        try:
            import imageio_ffmpeg
            exe = imageio_ffmpeg.get_ffmpeg_exe()
            if exe and Path(exe).exists():
                return exe
        except Exception:
            pass

        which_ffmpeg = shutil.which("ffmpeg")
        if which_ffmpeg:
            return which_ffmpeg

        raise RuntimeError("FFmpeg dasturi topilmadi. 'pip install imageio-ffmpeg' o'rnatilganini tekshiring.")

    @staticmethod
    def get_edge_exe() -> Optional[str]:
        """SVG rasmlarni 1080p ga rasterizatsiya qilish uchun headless brauzerni topish."""
        candidates = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            shutil.which("msedge"),
            shutil.which("chrome")
        ]
        for c in candidates:
            if c and Path(c).exists():
                return str(c)
        return None

    @staticmethod
    def sanitize_svg_text(svg_text: str) -> str:
        """Kichik XML sintaksis xatolarini tuzatish (takrorlangan atributlar, buzilgan teglar)."""
        if not svg_text:
            return ""
        # 1. Teg ichida buzilgan boshqa ochiluvchi tegni tozalash
        svg_text = re.sub(r'<([a-zA-Z0-9_\-]+)[^>]*?(<[a-zA-Z0-9_\-]+)', r'\2', svg_text)

        # 2. Bitta teg ichidagi takroriy atributlarni tozalash (masalan duplicate d="" or r="")
        def dedupe_tag_attributes(match):
            full_tag = match.group(0)
            tag_name_match = re.match(r'<([a-zA-Z0-9_\-]+)', full_tag)
            if not tag_name_match:
                return full_tag
            tag_name = tag_name_match.group(1)
            is_self_closing = full_tag.strip().endswith('/>')

            attr_matches = list(re.finditer(r'([a-zA-Z0-9_\-:]+)\s*=\s*([\'\"][^\'\"]*[\'\"])', full_tag))
            seen_attrs = set()
            kept_attrs = []
            for m in reversed(attr_matches):
                key = m.group(1).lower()
                if key not in seen_attrs:
                    seen_attrs.add(key)
                    kept_attrs.append(f'{m.group(1)}={m.group(2)}')
            kept_attrs.reverse()
            attrs_str = ' '.join(kept_attrs)
            if attrs_str:
                attrs_str = ' ' + attrs_str
            return f'<{tag_name}{attrs_str} />' if is_self_closing else f'<{tag_name}{attrs_str}>'

        svg_text = re.sub(r'<[a-zA-Z0-9_\-]+(?:\s+[a-zA-Z0-9_\-:]+\s*=\s*[\'\"][^\'\"]*[\'\"])+\s*/?>', dedupe_tag_attributes, svg_text)
        return svg_text

    @classmethod
    def render_scene_1080p_complete_frame(
        cls,
        img_path: Path,
        out_png: Path,
        scene_num: int,
        total_scenes: int,
        title: str,
        narration: str,
        moral: str
    ) -> bool:
        """
        Sahna illyustratsiyasi, pastki yumshoq soya hamda rasmiy ta'limiy doska va subtitr panelini
        yagona 1920x1080 Full HD kadrga yuqori sifatda birlashtiradi.
        """
        browser_exe = cls.get_edge_exe()
        if not browser_exe:
            return False

        is_svg = str(img_path).lower().endswith(".svg")
        img_content = ""
        if is_svg and img_path.exists():
            try:
                svg_raw = img_path.read_text(encoding="utf-8")
            except Exception:
                svg_raw = ""
            svg_raw = cls.sanitize_svg_text(svg_raw)
            if "viewBox" not in svg_raw and "<svg" in svg_raw:
                svg_raw = svg_raw.replace("<svg", '<svg viewBox="0 0 1280 720"', 1)
            img_content = f'<div class="svg-wrap">{svg_raw}</div>'
        elif img_path.exists():
            uri = img_path.resolve().as_uri()
            img_content = f'<img src="{uri}" class="bg-img" />'
        else:
            img_content = '<div class="fallback-bg"></div>'

        clean_title = html.escape(title.strip() if title else f"{scene_num}-sahna")
        clean_narration = html.escape(narration.strip() if narration else "")
        clean_moral = html.escape(moral.strip() if moral else "Bilim — eng katta boylik va kuchdir!")

        html_code = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    background: #0B0F19;
    font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    position: relative;
  }}
  .bg-container {{
    position: absolute;
    top: 0; left: 0;
    width: 1920px;
    height: 1080px;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0B0F19;
  }}
  .svg-wrap {{
    width: 1920px;
    height: 1080px;
  }}
  .svg-wrap svg {{
    width: 1920px;
    height: 1080px;
    display: block;
  }}
  .bg-img {{
    width: 1920px;
    height: 1080px;
    object-fit: cover;
  }}
  .fallback-bg {{
    width: 1920px;
    height: 1080px;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
  }}
  .bot-vignette {{
    position: absolute;
    bottom: 0; left: 0;
    width: 1920px;
    height: 480px;
    background: linear-gradient(to bottom, rgba(8, 12, 22, 0) 0%, rgba(8, 12, 22, 0.45) 40%, rgba(8, 12, 22, 0.92) 100%);
    z-index: 2;
  }}
  .edu-board {{
    position: absolute;
    bottom: 36px;
    left: 48px;
    right: 48px;
    height: 172px;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
    border: 2.5px solid rgba(56, 189, 248, 0.75);
    border-radius: 28px;
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    z-index: 3;
    display: flex;
    align-items: center;
    padding: 0 36px;
    gap: 32px;
  }}
  .board-left {{
    width: 440px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 8px;
  }}
  .badge-row {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .badge-chip {{
    font-size: 14px;
    font-weight: 800;
    color: #FDE047;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }}
  .scene-indicator {{
    font-size: 12px;
    font-weight: 700;
    color: #94A3B8;
    background: rgba(255, 255, 255, 0.1);
    padding: 2px 10px;
    border-radius: 12px;
  }}
  .scene-title {{
    font-size: 28px;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.2;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }}
  .divider {{
    width: 2px;
    height: 110px;
    background: rgba(255, 255, 255, 0.18);
    flex-shrink: 0;
  }}
  .board-right {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
    min-width: 0;
  }}
  .narration-text {{
    font-size: 21px;
    font-weight: 600;
    color: #F8FAFC;
    line-height: 1.38;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
  }}
  .summary-text {{
    font-size: 15px;
    font-weight: 600;
    color: #C084FC;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }}
  .summary-text strong {{
    color: #E9D5FF;
    font-weight: 800;
  }}
</style>
</head>
<body>
  <div class="bg-container">
    {img_content}
  </div>
  <div class="bot-vignette"></div>
  <div class="edu-board">
    <div class="board-left">
      <div class="badge-row">
        <span class="badge-chip">✨ DARS SABOG'I</span>
        <span class="scene-indicator">{scene_num} / {total_scenes} sahna</span>
      </div>
      <div class="scene-title">{clean_title}</div>
    </div>
    <div class="divider"></div>
    <div class="board-right">
      <div class="narration-text">{clean_narration}</div>
      <div class="summary-text">💡 <strong>XULOSA:</strong> {clean_moral}</div>
    </div>
  </div>
</body>
</html>"""

        temp_html = out_png.parent / f"temp_{out_png.stem}.html"
        try:
            temp_html.write_text(html_code, encoding="utf-8")
            cmd = [
                browser_exe,
                "--headless=new",
                "--disable-gpu",
                "--window-size=1920,1080",
                "--hide-scrollbars",
                f"--screenshot={str(out_png.resolve())}",
                temp_html.resolve().as_uri()
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            return res.returncode == 0 and out_png.exists() and out_png.stat().st_size > 15000
        except Exception as e:
            logger.error(f"Kadrni rasterizatsiya qilishda xatolik: {e}")
            return False
        finally:
            if temp_html.exists():
                try:
                    temp_html.unlink()
                except Exception:
                    pass

    @classmethod
    async def render_full_project_to_mp4(
        cls,
        scenes: List[Dict[str, Any]],
        topic: str,
        output_mp4_path: Path,
        bgm_track: Optional[str] = "bgm_cheerful.mp3",
        bgm_volume: float = 0.12,
        moral_summary: Optional[str] = None,
        static_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Barcha sahnalardan to'liq 1080p Full HD MP4 video yaratish (fon rasmlari + pastki ta'limiy doska).
        """
        ffmpeg_exe = cls.get_ffmpeg_exe()
        if not static_dir:
            static_dir = Path(__file__).resolve().parent.parent / "static"
        renders_dir = static_dir / "renders"

        output_mp4_path.parent.mkdir(parents=True, exist_ok=True)

        if not moral_summary:
            moral_summary = "Bilim — eng katta boylik va kuchdir!"

        with tempfile.TemporaryDirectory(prefix="tasvirlab_render_") as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            clip_paths: List[Path] = []
            total_duration = 0.0
            total_scenes_count = len(scenes)

            async with httpx.AsyncClient(timeout=30.0) as http_client:
                for idx, sc in enumerate(scenes):
                    s_num = sc.get("scene_number", idx + 1)
                    raw_img_url = sc.get("image_url", "")
                    raw_audio_url = sc.get("audio_url", "")
                    duration = float(sc.get("duration", 5.0))
                    scene_title = sc.get("title", f"Sahna {s_num}")
                    scene_narration = sc.get("narration", "")

                    # 1. Rasmni topish yoki yuklab olish
                    local_img_raw = temp_dir / f"scene_{s_num}_raw"
                    if raw_img_url.startswith("http://") or raw_img_url.startswith("https://"):
                        try:
                            resp = await http_client.get(raw_img_url)
                            ext = ".svg" if "<svg" in resp.text[:100] else ".png"
                            local_img_raw = local_img_raw.with_suffix(ext)
                            local_img_raw.write_bytes(resp.content)
                        except Exception as e:
                            logger.warning(f"Rasm yuklanmadi ({raw_img_url}): {e}")
                            local_img_raw = static_dir / "images" / "cinema_idle_poster.jpg"
                    elif raw_img_url.startswith("/renders/"):
                        rel = raw_img_url.replace("/renders/", "").lstrip("/")
                        local_img_raw = renders_dir / rel
                    elif raw_img_url.startswith("/images/"):
                        rel = raw_img_url.replace("/images/", "").lstrip("/")
                        local_img_raw = static_dir / "images" / rel
                    else:
                        local_img_raw = renders_dir / Path(raw_img_url).name

                    if not local_img_raw.exists():
                        local_img_raw = static_dir / "images" / "cinema_idle_poster.jpg"

                    # 2. To'liq 1080p kadr (illyustratsiya + pastki doska + subtitr) yaratish
                    scene_frame_1080p = temp_dir / f"scene_{s_num}_frame_1080p.png"
                    success_frame = cls.render_scene_1080p_complete_frame(
                        img_path=local_img_raw,
                        out_png=scene_frame_1080p,
                        scene_num=s_num,
                        total_scenes=total_scenes_count,
                        title=scene_title,
                        narration=scene_narration,
                        moral=moral_summary
                    )

                    if not success_frame or not scene_frame_1080p.exists():
                        # Zaxira sifatida bo'sh to'q fon
                        blank = Image.new("RGB", (1920, 1080), color=(15, 23, 42))
                        blank.save(scene_frame_1080p, "PNG")

                    # 3. Audio treki topish yoki yuklab olish
                    scene_audio = temp_dir / f"scene_{s_num}_audio.wav"
                    if raw_audio_url.startswith("http://") or raw_audio_url.startswith("https://"):
                        try:
                            a_resp = await http_client.get(raw_audio_url)
                            scene_audio.write_bytes(a_resp.content)
                        except Exception as e:
                            logger.warning(f"Audio yuklanmadi ({raw_audio_url}): {e}")
                            scene_audio = None
                    elif raw_audio_url.startswith("/renders/"):
                        rel = raw_audio_url.replace("/renders/", "").lstrip("/")
                        scene_audio = renders_dir / rel
                    elif raw_audio_url.startswith("/audio/"):
                        rel = raw_audio_url.replace("/audio/", "").lstrip("/")
                        scene_audio = static_dir / "audio" / rel
                    else:
                        scene_audio = renders_dir / Path(raw_audio_url).name

                    exact_dur = duration
                    if scene_audio and scene_audio.exists():
                        try:
                            with wave.open(str(scene_audio), "rb") as wf:
                                exact_dur = round(wf.getnframes() / float(wf.getframerate()), 2)
                        except Exception:
                            pass

                    exact_dur = max(2.5, exact_dur)
                    total_duration += exact_dur

                    # 4. Sahna klipini ultrafast 1080p render qilish
                    scene_clip = temp_dir / f"clip_{s_num:03d}.mp4"

                    if scene_audio and scene_audio.exists():
                        audio_input_args = ["-i", str(scene_audio)]
                    else:
                        audio_input_args = ["-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=24000"]

                    cmd_scene = [
                        ffmpeg_exe, "-y",
                        "-loop", "1", "-i", str(scene_frame_1080p),
                        *audio_input_args,
                        "-c:v", "libx264",
                        "-preset", "ultrafast",
                        "-crf", "20",
                        "-c:a", "aac",
                        "-b:a", "192k",
                        "-pix_fmt", "yuv420p",
                        "-t", str(exact_dur),
                        "-shortest",
                        str(scene_clip)
                    ]

                    res_scene = subprocess.run(cmd_scene, capture_output=True, text=True)
                    if res_scene.returncode == 0 and scene_clip.exists():
                        clip_paths.append(scene_clip)
                    else:
                        logger.error(f"Sahna {s_num} renderida xatolik: {res_scene.stderr}")

            if not clip_paths:
                raise RuntimeError("Hech bir sahna muvaffaqiyatli render qilinmadi.")

            # 5. Sahnalarni ketma-ket birlashtirish (Concat)
            concat_list = temp_dir / "concat_list.txt"
            with open(concat_list, "w", encoding="utf-8") as f:
                for cp in clip_paths:
                    escaped_path = str(cp.resolve()).replace("\\", "/")
                    f.write(f"file '{escaped_path}'\n")

            combined_video = temp_dir / "combined_scenes.mp4"
            cmd_concat = [
                ffmpeg_exe, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list),
                "-c", "copy",
                str(combined_video)
            ]
            res_concat = subprocess.run(cmd_concat, capture_output=True, text=True)
            if res_concat.returncode != 0:
                raise RuntimeError(f"Kliplarni birlashtirishda xatolik: {res_concat.stderr}")

            # 6. Fon musiqasini (BGM) professional mikslash
            bgm_file = None
            if bgm_track and bgm_track != "none":
                candidate_bgm = static_dir / "audio" / bgm_track
                if candidate_bgm.exists():
                    bgm_file = candidate_bgm
                else:
                    fallback_bgm = static_dir / "audio" / "bgm_cheerful.mp3"
                    if fallback_bgm.exists():
                        bgm_file = fallback_bgm

            if bgm_file:
                fade_start = max(0.5, total_duration - 2.5)
                cmd_final = [
                    ffmpeg_exe, "-y",
                    "-i", str(combined_video),
                    "-stream_loop", "-1", "-i", str(bgm_file),
                    "-filter_complex",
                    f"[1:a]volume={bgm_volume},afade=t=out:st={fade_start}:d=2.0[bgm];"
                    f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
                    "-map", "0:v",
                    "-map", "[aout]",
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-movflags", "+faststart",
                    str(output_mp4_path)
                ]
            else:
                cmd_final = [
                    ffmpeg_exe, "-y",
                    "-i", str(combined_video),
                    "-c", "copy",
                    "-movflags", "+faststart",
                    str(output_mp4_path)
                ]

            res_final = subprocess.run(cmd_final, capture_output=True, text=True)
            if res_final.returncode != 0:
                raise RuntimeError(f"Yakuniy MP4 video eksportida xatolik: {res_final.stderr}")

        # Natija ma'lumotlari
        file_size_bytes = output_mp4_path.stat().st_size
        file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

        return {
            "status": "success",
            "video_path": str(output_mp4_path),
            "filename": output_mp4_path.name,
            "duration": round(total_duration, 1),
            "size_mb": file_size_mb,
            "resolution": "1920x1080 (Full HD)",
            "codec": "H.264 / AAC",
            "fps": 30
        }
