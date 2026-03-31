#!/usr/bin/env python3
"""Render HTML slide files to PNG frames using Playwright."""

import sys
import os
import asyncio
from playwright.async_api import async_playwright


async def render_all(slides_dir: str, frames_dir: str):
    os.makedirs(frames_dir, exist_ok=True)

    slide_files = sorted(
        f for f in os.listdir(slides_dir) if f.endswith(".html")
    )

    if not slide_files:
        print(f"ERROR: No HTML files found in {slides_dir}")
        sys.exit(1)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        for slide_file in slide_files:
            slide_path = os.path.abspath(os.path.join(slides_dir, slide_file))
            frame_name = slide_file.replace("slide-", "frame-").replace(".html", ".png")
            frame_path = os.path.join(frames_dir, frame_name)

            await page.goto(f"file://{slide_path}")
            # Wait for CSS animations to complete
            await page.wait_for_timeout(1000)
            await page.screenshot(path=frame_path, full_page=False)
            print(f"Rendered: {frame_path}")

        await browser.close()

    print(f"Done: {len(slide_files)} frames rendered in {frames_dir}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python render_slides.py <slides_dir> <frames_dir> [--dry-run]")
        sys.exit(1)

    slides_dir = sys.argv[1]
    frames_dir = sys.argv[2]
    dry_run = "--dry-run" in sys.argv

    if not os.path.isdir(slides_dir):
        print(f"ERROR: Slides directory not found: {slides_dir}")
        sys.exit(1)

    if dry_run:
        slide_count = len([f for f in os.listdir(slides_dir) if f.endswith(".html")])
        print(f"[DRY RUN] Would render {slide_count} slides to {frames_dir}")
        return

    asyncio.run(render_all(slides_dir, frames_dir))


if __name__ == "__main__":
    main()
