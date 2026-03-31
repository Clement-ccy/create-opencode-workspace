#!/usr/bin/env python3
"""Validate a video recipe JSON file against the expected schema."""

import json
import sys
import os

REQUIRED_TOP_FIELDS = ["title", "slides"]
VALID_SLIDE_TYPES = ["title", "content", "quote", "code", "image", "closing"]
VALID_ANIMATIONS = ["fadeIn", "slideLeft", "slideRight", "slideUp", "typewriter", "zoomIn", "none"]

def validate(recipe: dict) -> list:
    errors = []

    # Top-level fields
    for field in REQUIRED_TOP_FIELDS:
        if field not in recipe:
            errors.append(f"Missing required field: '{field}'")

    # Slides
    slides = recipe.get("slides", [])
    if not slides:
        errors.append("'slides' array is empty")
    else:
        for i, slide in enumerate(slides):
            slide_id = slide.get("id", i + 1)
            prefix = f"slides[{i}] (id={slide_id})"

            # Type
            slide_type = slide.get("type")
            if not slide_type:
                errors.append(f"{prefix}: missing 'type'")
            elif slide_type not in VALID_SLIDE_TYPES:
                errors.append(f"{prefix}: invalid type '{slide_type}', must be one of {VALID_SLIDE_TYPES}")

            # Narration (required for most types)
            if slide_type in ("title", "content", "quote", "closing") and not slide.get("narration"):
                errors.append(f"{prefix}: missing 'narration'")

            # Animation
            anim = slide.get("animation")
            if anim and anim not in VALID_ANIMATIONS:
                errors.append(f"{prefix}: invalid animation '{anim}', must be one of {VALID_ANIMATIONS}")

            # Duration
            duration = slide.get("duration_hint")
            if duration is not None and (not isinstance(duration, (int, float)) or duration <= 0):
                errors.append(f"{prefix}: 'duration_hint' must be a positive number")

            # Type-specific validation
            if slide_type == "content":
                if not slide.get("bullets"):
                    errors.append(f"{prefix}: 'content' type requires 'bullets'")
            elif slide_type == "code":
                if not slide.get("code"):
                    errors.append(f"{prefix}: 'code' type requires 'code'")
            elif slide_type == "quote":
                if not slide.get("text"):
                    errors.append(f"{prefix}: 'quote' type requires 'text'")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_recipe.py <recipe.json> [--dry-run]")
        sys.exit(1)

    recipe_path = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    if not os.path.exists(recipe_path):
        print(f"ERROR: File not found: {recipe_path}")
        sys.exit(1)

    with open(recipe_path, "r", encoding="utf-8") as f:
        recipe = json.load(f)

    errors = validate(recipe)

    if dry_run:
        print(f"[DRY RUN] Would validate: {recipe_path}")

    if errors:
        print(f"VALIDATION FAILED ({len(errors)} errors):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"VALIDATION PASSED: {len(recipe.get('slides', []))} slides found")
        sys.exit(0)


if __name__ == "__main__":
    main()
