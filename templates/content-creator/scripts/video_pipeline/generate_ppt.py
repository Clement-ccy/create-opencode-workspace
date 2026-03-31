#!/usr/bin/env python3
"""Generate HTML slide files from a video recipe JSON."""

import json
import sys
import os

CSS_BASE = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1920px;
  height: 1080px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Noto Sans SC', 'Inter', 'Source Han Sans CN', sans-serif;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #eee;
}
.content {
  max-width: 1400px;
  text-align: center;
  padding: 60px;
}
.title { font-size: 72px; font-weight: 700; margin-bottom: 40px; line-height: 1.3; }
.subtitle { font-size: 36px; opacity: 0.8; margin-top: 20px; }
.slide-title { font-size: 52px; font-weight: 600; margin-bottom: 50px; color: #e94560; }
.bullet { font-size: 32px; margin: 24px 0; text-align: left; padding-left: 40px; line-height: 1.6; }
.bullet::before { content: "▸ "; color: #e94560; }
.quote { font-size: 42px; font-style: italic; line-height: 1.6; max-width: 1200px; }
.attribution { font-size: 24px; opacity: 0.6; margin-top: 30px; }
.code {
  background: #0f3460;
  padding: 40px;
  border-radius: 12px;
  font-family: 'Fira Code', 'JetBrains Mono', monospace;
  font-size: 28px;
  text-align: left;
  line-height: 1.8;
  white-space: pre-wrap;
  max-width: 1400px;
}
.code-lang { font-size: 18px; opacity: 0.5; margin-bottom: 10px; text-align: left; }
.closing { font-size: 64px; font-weight: 700; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideLeft {
  from { transform: translateX(100px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
@keyframes slideRight {
  from { transform: translateX(-100px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
@keyframes slideUp {
  from { transform: translateY(80px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
@keyframes zoomIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
.animate { animation: {animation} 0.8s ease-in-out forwards; }
"""

def render_slide(slide: dict) -> str:
    slide_type = slide.get("type", "content")
    animation = slide.get("animation", "fadeIn")
    css = CSS_BASE.replace("{animation}", animation)

    body = ""

    if slide_type == "title":
        body = f'<h1 class="title">{slide.get("text", "")}</h1>'
        if slide.get("visual_note"):
            body += f'<p class="subtitle">{slide["visual_note"]}</p>'

    elif slide_type == "content":
        title = slide.get("title", "")
        if title:
            body += f'<h2 class="slide-title">{title}</h2>'
        for bullet in slide.get("bullets", []):
            body += f'<div class="bullet">{bullet}</div>'

    elif slide_type == "quote":
        body = f'<blockquote class="quote">"{slide.get("text", "")}"</blockquote>'
        if slide.get("attribution"):
            body += f'<p class="attribution">— {slide["attribution"]}</p>'

    elif slide_type == "code":
        lang = slide.get("language", "")
        code = slide.get("code", "")
        if lang:
            body += f'<div class="code-lang">{lang}</div>'
        body += f'<pre class="code"><code>{escape_html(code)}</code></pre>'

    elif slide_type == "closing":
        body = f'<h1 class="closing">{slide.get("text", "")}</h1>'

    return f"""<!DOCTYPE html>
<html lang="{slide.get('lang', 'zh-CN')}">
<head>
<meta charset="utf-8">
<style>{css}</style>
</head>
<body>
<div class="content animate">
{body}
</div>
</body>
</html>"""


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_ppt.py <recipe.json> <output_dir> [--dry-run]")
        sys.exit(1)

    recipe_path = sys.argv[1]
    output_dir = sys.argv[2]
    dry_run = "--dry-run" in sys.argv

    with open(recipe_path, "r", encoding="utf-8") as f:
        recipe = json.load(f)

    if dry_run:
        print(f"[DRY RUN] Would generate {len(recipe['slides'])} slides to {output_dir}")
        return

    os.makedirs(output_dir, exist_ok=True)

    for slide in recipe["slides"]:
        slide_id = slide.get("id", 0)
        html = render_slide(slide)
        output_path = os.path.join(output_dir, f"slide-{slide_id:02d}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated: {output_path}")

    print(f"Done: {len(recipe['slides'])} slides generated in {output_dir}")


if __name__ == "__main__":
    main()
