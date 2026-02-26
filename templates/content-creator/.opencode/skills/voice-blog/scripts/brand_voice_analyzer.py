#!/usr/bin/env python3
"""
Brand Voice Analyzer - Analyzes content to establish and maintain brand voice consistency
Supports both English and Chinese content with language-specific analysis
"""

import re
from typing import Dict, List, Tuple, Optional
import json


# Language detection
def detect_language(text: str) -> str:
    """Detect if text is primarily Chinese or English"""
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    total_chars = len(re.sub(r"\s", "", text))

    if total_chars == 0:
        return "en"

    chinese_ratio = chinese_chars / total_chars
    return "zh" if chinese_ratio > 0.3 else "en"


# Chinese word segmentation (simple implementation, falls back to character-based if jieba unavailable)
def segment_chinese(text: str) -> List[str]:
    """Segment Chinese text into words"""
    try:
        import jieba

        return list(jieba.cut(text))
    except ImportError:
        # Fallback: simple character-based segmentation
        words = []
        current_word = ""
        for char in text:
            if "\u4e00" <= char <= "\u9fff":
                if current_word:
                    words.append(current_word)
                    current_word = ""
                words.append(char)
            elif char.isalnum():
                current_word += char
            else:
                if current_word:
                    words.append(current_word)
                    current_word = ""
        if current_word:
            words.append(current_word)
        return words


class BrandVoiceAnalyzer:
    def __init__(self):
        # English voice dimensions
        self.voice_dimensions_en = {
            "formality": {
                "formal": [
                    "hereby",
                    "therefore",
                    "furthermore",
                    "pursuant",
                    "regarding",
                    "consequently",
                    "accordingly",
                ],
                "casual": [
                    "hey",
                    "cool",
                    "awesome",
                    "stuff",
                    "yeah",
                    "gonna",
                    "kinda",
                    "sorta",
                    "pretty much",
                ],
            },
            "tone": {
                "professional": [
                    "expertise",
                    "solution",
                    "optimize",
                    "leverage",
                    "strategic",
                    "implement",
                    "framework",
                ],
                "friendly": [
                    "happy",
                    "excited",
                    "love",
                    "enjoy",
                    "together",
                    "share",
                    "helpful",
                    "wonderful",
                ],
            },
            "perspective": {
                "authoritative": [
                    "proven",
                    "research shows",
                    "experts agree",
                    "data indicates",
                    "studies confirm",
                ],
                "conversational": [
                    "you might",
                    "let's explore",
                    "we think",
                    "imagine if",
                    "consider this",
                ],
            },
        }

        # Chinese voice dimensions
        self.voice_dimensions_zh = {
            "formality": {
                "formal": [
                    "因此",
                    "鉴于",
                    "综上所述",
                    "应当",
                    "兹",
                    "据此",
                    "特此",
                    "谨此",
                ],
                "casual": ["嗯", "啊", "呢", "吧", "哈", "嘛", "呗", "啦", "呀"],
            },
            "tone": {
                "professional": [
                    "专业",
                    "解决方案",
                    "优化",
                    "策略",
                    "框架",
                    "实现",
                    "架构",
                    "核心",
                ],
                "friendly": [
                    "开心",
                    "分享",
                    "一起",
                    "喜欢",
                    "希望",
                    "感谢",
                    "欢迎",
                    "推荐",
                ],
            },
            "perspective": {
                "authoritative": [
                    "研究表明",
                    "数据显示",
                    "专家指出",
                    "事实证明",
                    "公认",
                ],
                "conversational": ["你可以", "让我们", "我觉得", "试想一下", "不妨"],
            },
            "emotion": {
                "rational": ["分析", "逻辑", "原因", "结果", "结论", "数据", "证据"],
                "emotional": ["感动", "震撼", "温暖", "美好", "遗憾", "惊喜", "心动"],
            },
        }

        # Chinese stop words
        self.stop_words_zh = {
            "的",
            "是",
            "在",
            "了",
            "和",
            "与",
            "或",
            "有",
            "这",
            "那",
            "我",
            "你",
            "他",
            "她",
            "它",
            "们",
            "就",
            "也",
            "都",
            "而",
            "及",
            "着",
            "把",
            "被",
            "让",
            "给",
            "从",
            "到",
            "为",
            "以",
            "对",
            "于",
            "但",
            "如",
            "若",
            "因",
            "所",
            "能",
            "会",
            "可以",
            "已经",
            "可能",
            "应该",
            "需要",
            "这个",
            "那个",
            "什么",
            "怎么",
            "如何",
            "为什么",
            "因为",
            "所以",
            "但是",
            "然而",
            "不过",
            "如果",
            "虽然",
            "即使",
            "无论",
        }

        # English stop words
        self.stop_words_en = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "as",
            "is",
            "was",
            "are",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "can",
            "shall",
        }

    def analyze_text(self, text: str) -> Dict:
        """Analyze text for brand voice characteristics"""
        language = detect_language(text)

        if language == "zh":
            return self._analyze_chinese(text)
        else:
            return self._analyze_english(text)

    def _analyze_chinese(self, text: str) -> Dict:
        """Analyze Chinese text for brand voice characteristics"""
        words = segment_chinese(text)
        word_count = len([w for w in words if w.strip()])
        char_count = len(re.findall(r"[\u4e00-\u9fff]", text))

        results = {
            "language": "zh",
            "word_count": word_count,
            "char_count": char_count,
            "readability_score": self._calculate_readability_zh(text),
            "voice_profile": {},
            "sentence_analysis": self._analyze_sentences_zh(text),
            "emotion_analysis": self._analyze_emotion_zh(text),
            "recommendations": [],
        }

        # Analyze voice dimensions
        for dimension, categories in self.voice_dimensions_zh.items():
            dim_scores = {}
            for category, keywords in categories.items():
                score = sum(1 for keyword in keywords if keyword in text)
                dim_scores[category] = score

            if sum(dim_scores.values()) > 0:
                dominant = max(dim_scores, key=dim_scores.get)
                results["voice_profile"][dimension] = {
                    "dominant": dominant,
                    "scores": dim_scores,
                }

        # Generate recommendations
        results["recommendations"] = self._generate_recommendations_zh(results)

        return results

    def _analyze_english(self, text: str) -> Dict:
        """Analyze English text for brand voice characteristics"""
        text_lower = text.lower()
        word_count = len(text.split())

        results = {
            "language": "en",
            "word_count": word_count,
            "readability_score": self._calculate_readability_en(text),
            "voice_profile": {},
            "sentence_analysis": self._analyze_sentences_en(text),
            "recommendations": [],
        }

        # Analyze voice dimensions
        for dimension, categories in self.voice_dimensions_en.items():
            dim_scores = {}
            for category, keywords in categories.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                dim_scores[category] = score

            if sum(dim_scores.values()) > 0:
                dominant = max(dim_scores, key=dim_scores.get)
                results["voice_profile"][dimension] = {
                    "dominant": dominant,
                    "scores": dim_scores,
                }

        # Generate recommendations
        results["recommendations"] = self._generate_recommendations_en(results)

        return results

    def _calculate_readability_zh(self, text: str) -> float:
        """Calculate readability score for Chinese text"""
        # For Chinese, we use sentence length and punctuation density
        sentences = re.split(r"[。！？；\n]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 0

        # Average sentence length in characters
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)

        # Punctuation density (more punctuation = easier to read)
        punct_count = len(re.findall(r'[，。！？、；：""' "【】（）《》]", text))
        char_count = len(re.findall(r"[\u4e00-\u9fff]", text))
        punct_density = punct_count / char_count if char_count > 0 else 0

        # Score calculation (0-100)
        # Ideal: avg sentence length 15-25 chars, punct density 0.1-0.2
        length_score = 100 - abs(avg_sentence_length - 20) * 2
        length_score = max(0, min(100, length_score))

        punct_score = 50 + punct_density * 250
        punct_score = max(0, min(100, punct_score))

        return round((length_score * 0.7 + punct_score * 0.3), 1)

    def _calculate_readability_en(self, text: str) -> float:
        """Calculate Flesch Reading Ease score for English"""
        sentences = re.split(r"[.!?]+", text)
        words = text.split()
        syllables = sum(self._count_syllables(word) for word in words)

        if len(sentences) == 0 or len(words) == 0:
            return 0

        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)

        # Flesch Reading Ease formula
        score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        return max(0, min(100, score))

    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified)"""
        word = word.lower()
        vowels = "aeiou"
        syllable_count = 0
        previous_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent e
        if word.endswith("e"):
            syllable_count -= 1

        return max(1, syllable_count)

    def _analyze_sentences_zh(self, text: str) -> Dict:
        """Analyze Chinese sentence structure"""
        sentences = re.split(r"[。！？；\n]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return {"average_length": 0, "variety": "low", "count": 0}

        lengths = [len(s) for s in sentences]
        avg_length = sum(lengths) / len(lengths) if lengths else 0

        # Calculate variety
        unique_lengths = len(set(lengths))
        if unique_lengths < 3:
            variety = "low"
        elif unique_lengths < 5:
            variety = "medium"
        else:
            variety = "high"

        return {
            "average_length": round(avg_length, 1),
            "variety": variety,
            "count": len(sentences),
        }

    def _analyze_sentences_en(self, text: str) -> Dict:
        """Analyze English sentence structure"""
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return {"average_length": 0, "variety": "low", "count": 0}

        lengths = [len(s.split()) for s in sentences]
        avg_length = sum(lengths) / len(lengths) if lengths else 0

        if len(set(lengths)) < 3:
            variety = "low"
        elif len(set(lengths)) < 5:
            variety = "medium"
        else:
            variety = "high"

        return {
            "average_length": round(avg_length, 1),
            "variety": variety,
            "count": len(sentences),
        }

    def _analyze_emotion_zh(self, text: str) -> Dict:
        """Analyze emotional content in Chinese text"""
        emotional_words = {
            "positive": [
                "开心",
                "快乐",
                "幸福",
                "美好",
                "喜欢",
                "爱",
                "感谢",
                "希望",
                "温暖",
                "惊喜",
                "精彩",
                "棒",
                "赞",
            ],
            "negative": [
                "难过",
                "伤心",
                "遗憾",
                "失望",
                "痛苦",
                "烦恼",
                "焦虑",
                "担忧",
                "困扰",
                "麻烦",
            ],
            "excited": ["激动", "兴奋", "震撼", "惊艳", "期待", "迫不及待"],
            "calm": ["平静", "安静", "宁静", "淡然", "从容"],
        }

        scores = {}
        for emotion, words in emotional_words.items():
            count = sum(1 for word in words if word in text)
            scores[emotion] = count

        dominant = (
            max(scores, key=scores.get) if sum(scores.values()) > 0 else "neutral"
        )

        return {"dominant": dominant, "scores": scores}

    def _generate_recommendations_zh(self, analysis: Dict) -> List[str]:
        """Generate recommendations for Chinese content"""
        recommendations = []

        # Readability recommendations
        if analysis["readability_score"] < 40:
            recommendations.append("建议简化句子结构，提高可读性")
        elif analysis["readability_score"] > 80:
            recommendations.append("内容非常易读，适合大众阅读")

        # Sentence variety
        if analysis["sentence_analysis"]["variety"] == "low":
            recommendations.append("建议增加句子长度变化，提升阅读节奏感")

        # Sentence length
        avg_len = analysis["sentence_analysis"]["average_length"]
        if avg_len > 50:
            recommendations.append(f"平均句长{avg_len:.0f}字偏长，建议拆分长句")
        elif avg_len < 10:
            recommendations.append(f"平均句长{avg_len:.0f}字偏短，可以适当增加句子深度")

        # Voice consistency
        if analysis["voice_profile"]:
            recommendations.append("保持统一的写作风格")

        return recommendations

    def _generate_recommendations_en(self, analysis: Dict) -> List[str]:
        """Generate recommendations for English content"""
        recommendations = []

        if analysis["readability_score"] < 30:
            recommendations.append(
                "Consider simplifying language for better readability"
            )
        elif analysis["readability_score"] > 70:
            recommendations.append(
                "Content is very easy to read - consider if this matches your audience"
            )

        if analysis["sentence_analysis"]["variety"] == "low":
            recommendations.append(
                "Vary sentence length for better flow and engagement"
            )

        if analysis["voice_profile"]:
            recommendations.append("Maintain consistent voice across all content")

        return recommendations


def analyze_content(content: str, output_format: str = "json") -> str:
    """Main function to analyze content"""
    analyzer = BrandVoiceAnalyzer()
    results = analyzer.analyze_text(content)
    language = results.get("language", "en")

    if output_format == "json":
        return json.dumps(results, indent=2, ensure_ascii=False)
    else:
        # Human-readable format
        if language == "zh":
            output = [
                "=== 品牌语调分析 ===",
                f"语言: 中文",
                f"字数: {results.get('char_count', results['word_count'])}",
                f"可读性评分: {results['readability_score']:.1f}/100",
                "",
                "语调特征:",
            ]

            for dimension, profile in results.get("voice_profile", {}).items():
                dim_name = {
                    "formality": "正式程度",
                    "tone": "语气",
                    "perspective": "视角",
                    "emotion": "情感",
                }.get(dimension, dimension)
                dominant_name = {
                    "formal": "正式",
                    "casual": "随意",
                    "professional": "专业",
                    "friendly": "友好",
                    "authoritative": "权威",
                    "conversational": "对话式",
                    "rational": "理性",
                    "emotional": "感性",
                }.get(profile["dominant"], profile["dominant"])
                output.append(f"  {dim_name}: {dominant_name}")

            output.extend(
                [
                    "",
                    "句子分析:",
                    f"  平均句长: {results['sentence_analysis']['average_length']} 字",
                    f"  句式变化: {results['sentence_analysis']['variety']}",
                    f"  总句数: {results['sentence_analysis']['count']}",
                    "",
                    "建议:",
                ]
            )

            for rec in results.get("recommendations", []):
                output.append(f"  • {rec}")

        else:
            output = [
                "=== Brand Voice Analysis ===",
                f"Language: English",
                f"Word Count: {results['word_count']}",
                f"Readability Score: {results['readability_score']:.1f}/100",
                "",
                "Voice Profile:",
            ]

            for dimension, profile in results.get("voice_profile", {}).items():
                output.append(f"  {dimension.title()}: {profile['dominant']}")

            output.extend(
                [
                    "",
                    "Sentence Analysis:",
                    f"  Average Length: {results['sentence_analysis']['average_length']} words",
                    f"  Variety: {results['sentence_analysis']['variety']}",
                    f"  Total Sentences: {results['sentence_analysis']['count']}",
                    "",
                    "Recommendations:",
                ]
            )

            for rec in results.get("recommendations", []):
                output.append(f"  • {rec}")

        return "\n".join(output)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read()

        output_format = sys.argv[2] if len(sys.argv) > 2 else "text"
        print(analyze_content(content, output_format))
    else:
        print("Usage: python brand_voice_analyzer.py <file> [json|text]")
        print("用法: python brand_voice_analyzer.py <文件> [json|text]")
