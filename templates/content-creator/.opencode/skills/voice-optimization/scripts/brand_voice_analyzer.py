#!/usr/bin/env python3
"""Brand voice analyzer — checks content against voice-optimization rules."""

import json
import re
import sys
import os

# AI-sounding filler phrases (Chinese)
AI_FILLERS_ZH = [
    "值得注意的是", "首先", "其次", "最后", "此外", "总之",
    "总而言之", "综上所述", "不言而喻", "众所周知",
    "在当今时代", "随着", "不得不承认", "毫无疑问",
]

# AI-sounding filler phrases (English)
AI_FILLERS_EN = [
    "it is worth noting", "furthermore", "moreover", "in conclusion",
    "to sum up", "in today's world", "as we all know",
    "it goes without saying", "without a doubt",
]

# AI buzzword replacements
BUZZWORDS = {
    "至关重要": "重要",
    "深入探讨": "讨论",
    "不断演变的格局": "变化",
    "充满活力": "活跃",
    "宝贵的": "有用的",
}


def analyze_zh(text: str) -> dict:
    issues = []
    score = 100

    # Check filler phrases
    for filler in AI_FILLERS_ZH:
        count = text.count(filler)
        if count > 0:
            issues.append(f"发现 AI 味填充词「{filler}」×{count}")
            score -= count * 3

    # Check buzzwords
    for bad, good in BUZZWORDS.items():
        count = text.count(bad)
        if count > 0:
            issues.append(f"发现 AI 高频词「{bad}」×{count}，建议改为「{good}」")
            score -= count * 2

    # Check sentence length uniformity
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    if len(sentences) > 5:
        lengths = [len(s) for s in sentences]
        avg = sum(lengths) / len(lengths)
        uniform = sum(1 for l in lengths if abs(l - avg) < avg * 0.2)
        if uniform / len(lengths) > 0.8:
            issues.append("句子长度过于统一，缺乏节奏变化")
            score -= 10

    # Check for "一、二、三" style numbering
    numbering_pattern = re.findall(r'[一二三四五六七八九十]+、', text)
    if numbering_pattern:
        issues.append(f"发现中文序号标记（{'、'.join(numbering_pattern[:3])}），请改用 Markdown 标题或 1. 2. 3.")
        score -= len(numbering_pattern) * 5

    # Check for em-dash abuse
    em_dash_count = text.count('——')
    if em_dash_count > 3:
        issues.append(f"破折号使用过多（{em_dash_count} 次），建议控制在 3 次以内")
        score -= 5

    score = max(0, min(100, score))
    return {"score": score, "issues": issues, "language": "zh"}


def analyze_en(text: str) -> dict:
    issues = []
    score = 100

    for filler in AI_FILLERS_EN:
        count = text.lower().count(filler.lower())
        if count > 0:
            issues.append(f"Found AI filler phrase: '{filler}' ×{count}")
            score -= count * 3

    # Check sentence variety
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    if len(sentences) > 5:
        lengths = [len(s) for s in sentences]
        avg = sum(lengths) / len(lengths)
        uniform = sum(1 for l in lengths if abs(l - avg) < avg * 0.2)
        if uniform / len(lengths) > 0.8:
            issues.append("Sentence lengths too uniform — vary rhythm")
            score -= 10

    score = max(0, min(100, score))
    return {"score": score, "issues": issues, "language": "en"}


def detect_language(text: str) -> str:
    zh_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    return "zh" if zh_chars > len(text) * 0.1 else "en"


def main():
    if len(sys.argv) < 2:
        print("Usage: python brand_voice_analyzer.py <file-path> [domain]")
        sys.exit(1)

    file_path = sys.argv[1]
    domain = sys.argv[2] if len(sys.argv) > 2 else "general"

    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    lang = detect_language(text)
    if lang == "zh":
        result = analyze_zh(text)
    else:
        result = analyze_en(text)

    result["file"] = file_path
    result["domain"] = domain

    # Output as JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # Exit code based on score
    if result["score"] >= 85:
        sys.exit(0)
    elif result["score"] >= 70:
        sys.exit(0)  # Pass with warnings
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
