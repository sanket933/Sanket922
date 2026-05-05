import json
import subprocess
from pathlib import Path


def build_reel_manifest(script: str, scenes: list[dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        'aspect_ratio': '9:16',
        'resolution': '1080x1920',
        'script': script,
        'scenes': scenes,
        'subtitle_style': {'font': 'Inter', 'position': 'bottom', 'max_words_per_line': 5},
    }
    path = output_dir / 'reel_manifest.json'
    path.write_text(json.dumps(manifest, indent=2))
    return path


def render_vertical_video(image_sequence_glob: str, audio_path: str | None, output_path: str) -> None:
    command = [
        'ffmpeg', '-y', '-framerate', '1', '-pattern_type', 'glob', '-i', image_sequence_glob,
        '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1',
    ]
    if audio_path:
        command.extend(['-i', audio_path, '-shortest'])
    command.extend(['-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_path])
    subprocess.run(command, check=True)
