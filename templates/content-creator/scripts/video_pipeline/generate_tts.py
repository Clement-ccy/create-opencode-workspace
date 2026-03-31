#!/usr/bin/env python3
"""Generate TTS audio files from a video recipe JSON using edge-tts."""

import asyncio
import json
import sys
import os
import edge_tts

VOICE_MAP = {
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "zh": "zh-CN-XiaoxiaoNeural",
    "en-US": "en-US-JennyNeural",
    "en": "en-US-JennyNeural",
}


async def generate_audio(text: str, voice: str, output_path: str):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


async def generate_all(recipe: dict, output_dir: str):
    language = recipe.get("language", "zh-CN")
    voice = VOICE_MAP.get(language, VOICE_MAP["zh-CN"])

    tasks = []
    for slide in recipe.get("slides", []):
        narration = slide.get("narration", "").strip()
        if not narration:
            continue

        slide_id = slide.get("id", 0)
        output_path = os.path.join(output_dir, f"slide-{slide_id:02d}.mp3")
        tasks.append((narration, voice, output_path))

    os.makedirs(output_dir, exist_ok=True)

    for text, v, path in tasks:
        await generate_audio(text, v, path)
        print(f"Generated: {path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_tts.py <recipe.json> <output_dir> [--dry-run]")
        sys.exit(1)

    recipe_path = sys.argv[1]
    output_dir = sys.argv[2]
    dry_run = "--dry-run" in sys.argv

    with open(recipe_path, "r", encoding="utf-8") as f:
        recipe = json.load(f)

    if dry_run:
        narration_count = sum(1 for s in recipe.get("slides", []) if s.get("narration"))
        print(f"[DRY RUN] Would generate {narration_count} audio files to {output_dir}")
        return

    asyncio.run(generate_all(recipe, output_dir))
    print("Done: TTS generation complete")


if __name__ == "__main__":
    main()
