#!/usr/bin/env python3
"""Compile frame images and audio into a final video using FFmpeg."""

import json
import sys
import os
import subprocess


def get_audio_duration(audio_path: str) -> float:
    """Get duration of an audio file in seconds using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
            capture_output=True, text=True, check=True
        )
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError):
        return 5.0  # Default fallback


def compile_video(recipe: dict, assets_dir: str, output_path: str):
    """Compile frames and audio into final video."""
    frames_dir = os.path.join(assets_dir, "frames")
    audio_dir = os.path.join(assets_dir, "audio")

    slides = recipe.get("slides", [])
    if not slides:
        print("ERROR: No slides in recipe")
        sys.exit(1)

    # Build input file list with durations
    input_segments = []
    temp_dir = os.path.join(assets_dir, ".temp")
    os.makedirs(temp_dir, exist_ok=True)

    for i, slide in enumerate(slides):
        slide_id = slide.get("id", i + 1)
        frame_file = os.path.join(frames_dir, f"frame-{slide_id:02d}.png")
        audio_file = os.path.join(audio_dir, f"slide-{slide_id:02d}.mp3")

        if not os.path.exists(frame_file):
            print(f"WARNING: Missing frame: {frame_file}, skipping")
            continue

        # Determine duration
        if os.path.exists(audio_file):
            duration = get_audio_duration(audio_file)
        else:
            duration = slide.get("duration_hint", 5)

        segment_path = os.path.join(temp_dir, f"segment-{i:03d}.mp4")

        # Create segment: static image + audio -> video
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", frame_file,
            "-t", str(duration),
            "-vf", "scale=1920:1080",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-r", "30",
        ]

        if os.path.exists(audio_file):
            cmd.extend(["-i", audio_file, "-c:a", "aac", "-shortest"])

        cmd.append(segment_path)

        subprocess.run(cmd, capture_output=True, check=True)
        input_segments.append(segment_path)
        print(f"Segment created: {segment_path} ({duration:.1f}s)")

    if not input_segments:
        print("ERROR: No segments created")
        sys.exit(1)

    # Concatenate all segments
    concat_file = os.path.join(temp_dir, "concat.txt")
    with open(concat_file, "w") as f:
        for seg in input_segments:
            f.write(f"file '{os.path.abspath(seg)}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c:v", "libx264", "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        output_path
    ], capture_output=True, check=True)

    print(f"Done: Final video saved to {output_path}")

    # Cleanup temp files
    for seg in input_segments:
        os.remove(seg)
    os.remove(concat_file)
    os.rmdir(temp_dir)


def main():
    if len(sys.argv) < 4:
        print("Usage: python compile_video.py <recipe.json> <assets_dir> <output.mp4> [--dry-run]")
        sys.exit(1)

    recipe_path = sys.argv[1]
    assets_dir = sys.argv[2]
    output_name = sys.argv[3]
    dry_run = "--dry-run" in sys.argv

    with open(recipe_path, "r", encoding="utf-8") as f:
        recipe = json.load(f)

    output_path = os.path.join(assets_dir, output_name) if not os.path.isabs(output_name) else output_name

    if dry_run:
        slide_count = len(recipe.get("slides", []))
        print(f"[DRY RUN] Would compile {slide_count} slides into {output_path}")
        return

    compile_video(recipe, assets_dir, output_path)


if __name__ == "__main__":
    main()
