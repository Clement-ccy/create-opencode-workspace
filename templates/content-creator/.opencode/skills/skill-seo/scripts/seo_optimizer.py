#!/usr/bin/env python3
"""
SEO Content Optimizer - Analyzes and optimizes content for SEO
Supports both English and Chinese content with language-specific analysis
"""

import re
from typing import Dict, List, Set, Optional
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


# Chinese word segmentation
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


class SEOOptimizer:
    def __init__(self):
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
            "一个",
            "一种",
            "一些",
            "这些",
            "那些",
            "自己",
            "我们",
            "你们",
            "他们",
            "它们",
        }

        # SEO best practices for English (Google)
        self.best_practices_en = {
            "title_length": (50, 60),
            "meta_description_length": (150, 160),
            "url_length": (50, 60),
            "paragraph_length": (40, 150),
            "heading_keyword_placement": True,
            "keyword_density": (0.01, 0.03),  # 1-3%
        }

        # SEO best practices for Chinese (Baidu)
        self.best_practices_zh = {
            "title_length": (20, 30),  # 20-30 Chinese characters
            "meta_description_length": (80, 120),  # 80-120 Chinese characters
            "url_length": (30, 50),
            "paragraph_length": (100, 300),  # Chinese characters
            "heading_keyword_placement": True,
            "keyword_density": (0.02, 0.08),  # 2-8% for Chinese
        }

    def analyze(
        self,
        content: str,
        target_keyword: str = None,
        secondary_keywords: List[str] = None,
    ) -> Dict:
        """Analyze content for SEO optimization"""

        language = detect_language(content)

        analysis = {
            "language": language,
            "content_length": len(content.split())
            if language == "en"
            else len(re.findall(r"[\u4e00-\u9fff]", content)),
            "keyword_analysis": {},
            "structure_analysis": self._analyze_structure(content, language),
            "readability": self._analyze_readability(content, language),
            "meta_suggestions": {},
            "optimization_score": 0,
            "recommendations": [],
        }

        # Keyword analysis
        if target_keyword:
            analysis["keyword_analysis"] = self._analyze_keywords(
                content, target_keyword, secondary_keywords or [], language
            )

        # Generate meta suggestions
        analysis["meta_suggestions"] = self._generate_meta_suggestions(
            content, target_keyword, language
        )

        # Calculate optimization score
        analysis["optimization_score"] = self._calculate_seo_score(analysis, language)

        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis, language)

        return analysis

    def _analyze_keywords(
        self, content: str, primary: str, secondary: List[str], language: str = "en"
    ) -> Dict:
        """Analyze keyword usage and density"""
        content_lower = content.lower()

        if language == "zh":
            words = segment_chinese(content)
            word_count = len([w for w in words if w.strip()])
        else:
            word_count = len(content.split())

        results = {
            "primary_keyword": {
                "keyword": primary,
                "count": content_lower.count(primary.lower()),
                "density": 0,
                "in_title": False,
                "in_headings": False,
                "in_first_paragraph": False,
            },
            "secondary_keywords": [],
            "lsi_keywords": [],
        }

        # Calculate primary keyword metrics
        if word_count > 0:
            results["primary_keyword"]["density"] = (
                results["primary_keyword"]["count"] / word_count
            )

        # Check keyword placement
        first_para = content.split("\n\n")[0] if "\n\n" in content else content[:200]
        results["primary_keyword"]["in_first_paragraph"] = (
            primary.lower() in first_para.lower()
        )

        # Analyze secondary keywords
        for keyword in secondary:
            count = content_lower.count(keyword.lower())
            results["secondary_keywords"].append(
                {
                    "keyword": keyword,
                    "count": count,
                    "density": count / word_count if word_count > 0 else 0,
                }
            )

        # Extract potential LSI keywords
        results["lsi_keywords"] = self._extract_lsi_keywords(content, primary, language)

        return results

    def _analyze_structure(self, content: str, language: str = "en") -> Dict:
        """Analyze content structure for SEO"""
        lines = content.split("\n")

        structure = {
            "headings": {"h1": 0, "h2": 0, "h3": 0, "total": 0},
            "paragraphs": 0,
            "lists": 0,
            "images": 0,
            "links": {"internal": 0, "external": 0},
            "avg_paragraph_length": 0,
        }

        paragraphs = []
        current_para = []

        for line in lines:
            # Count headings
            if line.startswith("# "):
                structure["headings"]["h1"] += 1
                structure["headings"]["total"] += 1
            elif line.startswith("## "):
                structure["headings"]["h2"] += 1
                structure["headings"]["total"] += 1
            elif line.startswith("### "):
                structure["headings"]["h3"] += 1
                structure["headings"]["total"] += 1

            # Count lists
            if line.strip().startswith(("- ", "* ", "1. ")):
                structure["lists"] += 1

            # Count links
            internal_links = len(re.findall(r"\[.*?\]\(/.*?\)", line))
            external_links = len(re.findall(r"\[.*?\]\(https?://.*?\)", line))
            structure["links"]["internal"] += internal_links
            structure["links"]["external"] += external_links

            # Track paragraphs
            if line.strip() and not line.startswith("#"):
                current_para.append(line)
            elif current_para:
                paragraphs.append(" ".join(current_para))
                current_para = []

        if current_para:
            paragraphs.append(" ".join(current_para))

        structure["paragraphs"] = len(paragraphs)

        if paragraphs:
            if language == "zh":
                avg_length = sum(
                    len(re.findall(r"[\u4e00-\u9fff]", p)) for p in paragraphs
                ) / len(paragraphs)
            else:
                avg_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
            structure["avg_paragraph_length"] = round(avg_length, 1)

        return structure

    def _analyze_readability(self, content: str, language: str = "en") -> Dict:
        """Analyze content readability"""
        if language == "zh":
            return self._analyze_readability_zh(content)
        else:
            return self._analyze_readability_en(content)

    def _analyze_readability_zh(self, content: str) -> Dict:
        """Analyze Chinese content readability"""
        sentences = re.split(r"[。！？；\n]+", content)
        char_count = len(re.findall(r"[\u4e00-\u9fff]", content))

        if not sentences or char_count == 0:
            return {"score": 0, "level": "未知"}

        avg_sentence_length = char_count / len(sentences)

        # Chinese readability scoring
        if avg_sentence_length < 20:
            level = "易读"
            score = 90
        elif avg_sentence_length < 35:
            level = "中等"
            score = 70
        elif avg_sentence_length < 50:
            level = "较难"
            score = 50
        else:
            level = "困难"
            score = 30

        return {
            "score": score,
            "level": level,
            "avg_sentence_length": round(avg_sentence_length, 1),
        }

    def _analyze_readability_en(self, content: str) -> Dict:
        """Analyze English content readability"""
        sentences = re.split(r"[.!?]+", content)
        words = content.split()

        if not sentences or not words:
            return {"score": 0, "level": "Unknown"}

        avg_sentence_length = len(words) / len(sentences)

        # Simple readability scoring
        if avg_sentence_length < 15:
            level = "Easy"
            score = 90
        elif avg_sentence_length < 20:
            level = "Moderate"
            score = 70
        elif avg_sentence_length < 25:
            level = "Difficult"
            score = 50
        else:
            level = "Very Difficult"
            score = 30

        return {
            "score": score,
            "level": level,
            "avg_sentence_length": round(avg_sentence_length, 1),
        }

    def _extract_lsi_keywords(
        self, content: str, primary_keyword: str, language: str = "en"
    ) -> List[str]:
        """Extract potential LSI (semantically related) keywords"""
        if language == "zh":
            return self._extract_lsi_keywords_zh(content, primary_keyword)
        else:
            return self._extract_lsi_keywords_en(content, primary_keyword)

    def _extract_lsi_keywords_zh(self, content: str, primary_keyword: str) -> List[str]:
        """Extract LSI keywords for Chinese content"""
        words = segment_chinese(content)
        word_freq = {}

        for word in words:
            if word not in self.stop_words_zh and len(word) > 1:
                word_freq[word] = word_freq.get(word, 0) + 1

        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

        lsi_keywords = []
        for word, count in sorted_words:
            if word != primary_keyword and count > 1:
                lsi_keywords.append(word)
            if len(lsi_keywords) >= 10:
                break

        return lsi_keywords

    def _extract_lsi_keywords_en(self, content: str, primary_keyword: str) -> List[str]:
        """Extract LSI keywords for English content"""
        words = re.findall(r"\b[a-z]+\b", content.lower())
        word_freq = {}

        # Count word frequencies
        for word in words:
            if word not in self.stop_words_en and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Sort by frequency and return top related terms
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

        # Filter out the primary keyword and return top 10
        lsi_keywords = []
        for word, count in sorted_words:
            if word != primary_keyword.lower() and count > 1:
                lsi_keywords.append(word)
            if len(lsi_keywords) >= 10:
                break

        return lsi_keywords

    def _generate_meta_suggestions(
        self, content: str, keyword: str = None, language: str = "en"
    ) -> Dict:
        """Generate SEO meta tag suggestions"""
        suggestions = {
            "title": "",
            "meta_description": "",
            "url_slug": "",
            "og_title": "",
            "og_description": "",
        }

        if language == "zh":
            return self._generate_meta_suggestions_zh(content, keyword, suggestions)
        else:
            return self._generate_meta_suggestions_en(content, keyword, suggestions)

    def _generate_meta_suggestions_zh(
        self, content: str, keyword: str, suggestions: Dict
    ) -> Dict:
        """Generate meta suggestions for Chinese content (Baidu SEO)"""
        # Extract first sentence for description base
        sentences = re.split(r"[。！？；\n]+", content)
        first_sentence = sentences[0] if sentences else content[:120]

        if keyword:
            # Title suggestion (20-30 Chinese characters for Baidu)
            suggestions["title"] = f"{keyword} - 完整指南"
            if len(suggestions["title"]) > 30:
                suggestions["title"] = suggestions["title"][:27] + "..."

            # Meta description (80-120 Chinese characters for Baidu)
            desc_base = f"了解关于{keyword}的一切。{first_sentence}"
            if len(desc_base) > 120:
                desc_base = desc_base[:117] + "..."
            suggestions["meta_description"] = desc_base

            # URL slug (use pinyin or English equivalent)
            suggestions["url_slug"] = re.sub(
                r"[^a-z0-9-]+", "-", keyword.lower()
            ).strip("-")

            # Open Graph tags
            suggestions["og_title"] = suggestions["title"]
            suggestions["og_description"] = suggestions["meta_description"]

        return suggestions

    def _generate_meta_suggestions_en(
        self, content: str, keyword: str, suggestions: Dict
    ) -> Dict:
        """Generate meta suggestions for English content (Google SEO)"""
        # Extract first sentence for description base
        sentences = re.split(r"[.!?]+", content)
        first_sentence = sentences[0] if sentences else content[:160]

        if keyword:
            # Title suggestion
            suggestions["title"] = f"{keyword.title()} - Complete Guide"
            if len(suggestions["title"]) > 60:
                suggestions["title"] = keyword.title()[:57] + "..."

            # Meta description
            desc_base = f"Learn everything about {keyword}. {first_sentence}"
            if len(desc_base) > 160:
                desc_base = desc_base[:157] + "..."
            suggestions["meta_description"] = desc_base

            # URL slug
            suggestions["url_slug"] = re.sub(
                r"[^a-z0-9-]+", "-", keyword.lower()
            ).strip("-")

            # Open Graph tags
            suggestions["og_title"] = suggestions["title"]
            suggestions["og_description"] = suggestions["meta_description"]

        return suggestions

    def _calculate_seo_score(self, analysis: Dict, language: str = "en") -> int:
        """Calculate overall SEO optimization score"""
        if language == "zh":
            return self._calculate_seo_score_zh(analysis)
        else:
            return self._calculate_seo_score_en(analysis)

    def _calculate_seo_score_zh(self, analysis: Dict) -> int:
        """Calculate SEO score for Chinese content (Baidu)"""
        score = 0
        max_score = 100

        # Content length scoring (20 points) - Chinese characters
        if 500 <= analysis["content_length"] <= 3000:
            score += 20
        elif 300 <= analysis["content_length"] < 500:
            score += 10
        elif analysis["content_length"] > 3000:
            score += 15

        # Keyword optimization (30 points) - 2-8% for Chinese
        if analysis["keyword_analysis"]:
            kw_data = analysis["keyword_analysis"]["primary_keyword"]

            # Density scoring
            if 0.02 <= kw_data["density"] <= 0.08:
                score += 15
            elif 0.01 <= kw_data["density"] < 0.02:
                score += 8

            # Placement scoring
            if kw_data["in_first_paragraph"]:
                score += 10
            if kw_data.get("in_headings"):
                score += 5

        # Structure scoring (25 points)
        struct = analysis["structure_analysis"]
        if struct["headings"]["total"] > 0:
            score += 10
        if struct["paragraphs"] >= 3:
            score += 10
        if struct["links"]["internal"] > 0 or struct["links"]["external"] > 0:
            score += 5

        # Readability scoring (25 points)
        readability_score = analysis["readability"]["score"]
        score += int(readability_score * 0.25)

        return min(score, max_score)

    def _calculate_seo_score_en(self, analysis: Dict) -> int:
        """Calculate SEO score for English content (Google)"""
        score = 0
        max_score = 100

        # Content length scoring (20 points)
        if 300 <= analysis["content_length"] <= 2500:
            score += 20
        elif 200 <= analysis["content_length"] < 300:
            score += 10
        elif analysis["content_length"] > 2500:
            score += 15

        # Keyword optimization (30 points)
        if analysis["keyword_analysis"]:
            kw_data = analysis["keyword_analysis"]["primary_keyword"]

            # Density scoring
            if 0.01 <= kw_data["density"] <= 0.03:
                score += 15
            elif 0.005 <= kw_data["density"] < 0.01:
                score += 8

            # Placement scoring
            if kw_data["in_first_paragraph"]:
                score += 10
            if kw_data.get("in_headings"):
                score += 5

        # Structure scoring (25 points)
        struct = analysis["structure_analysis"]
        if struct["headings"]["total"] > 0:
            score += 10
        if struct["paragraphs"] >= 3:
            score += 10
        if struct["links"]["internal"] > 0 or struct["links"]["external"] > 0:
            score += 5

        # Readability scoring (25 points)
        readability_score = analysis["readability"]["score"]
        score += int(readability_score * 0.25)

        return min(score, max_score)

    def _generate_recommendations(
        self, analysis: Dict, language: str = "en"
    ) -> List[str]:
        """Generate SEO improvement recommendations"""
        if language == "zh":
            return self._generate_recommendations_zh(analysis)
        else:
            return self._generate_recommendations_en(analysis)

    def _generate_recommendations_zh(self, analysis: Dict) -> List[str]:
        """Generate recommendations for Chinese content"""
        recommendations = []

        # Content length recommendations
        if analysis["content_length"] < 500:
            recommendations.append(
                f"建议增加内容长度至少500字（当前{analysis['content_length']}字）"
            )
        elif analysis["content_length"] > 5000:
            recommendations.append("内容较长，建议分页或添加目录")

        # Keyword recommendations
        if analysis["keyword_analysis"]:
            kw_data = analysis["keyword_analysis"]["primary_keyword"]

            if kw_data["density"] < 0.02:
                recommendations.append(
                    f"建议增加关键词密度（当前{kw_data['density']:.1%}，建议2%-8%）"
                )
            elif kw_data["density"] > 0.08:
                recommendations.append(
                    f"关键词密度过高（当前{kw_data['density']:.1%}），可能被判定为关键词堆砌"
                )

            if not kw_data["in_first_paragraph"]:
                recommendations.append("建议在首段包含主要关键词")

        # Structure recommendations
        struct = analysis["structure_analysis"]
        if struct["headings"]["total"] == 0:
            recommendations.append("建议添加标题（H1、H2、H3）优化内容结构")
        if struct["links"]["internal"] == 0:
            recommendations.append("建议添加内链指向相关内容")
        if struct["avg_paragraph_length"] > 300:
            recommendations.append("段落过长，建议拆分提升可读性")

        # Readability recommendations
        if analysis["readability"]["avg_sentence_length"] > 50:
            recommendations.append("句子较长，建议简化提升可读性")

        return recommendations

    def _generate_recommendations_en(self, analysis: Dict) -> List[str]:
        """Generate recommendations for English content"""
        recommendations = []

        # Content length recommendations
        if analysis["content_length"] < 300:
            recommendations.append(
                f"Increase content length to at least 300 words (currently {analysis['content_length']})"
            )
        elif analysis["content_length"] > 3000:
            recommendations.append(
                "Consider breaking long content into multiple pages or adding a table of contents"
            )

        # Keyword recommendations
        if analysis["keyword_analysis"]:
            kw_data = analysis["keyword_analysis"]["primary_keyword"]

            if kw_data["density"] < 0.01:
                recommendations.append(
                    f"Increase keyword density for '{kw_data['keyword']}' (currently {kw_data['density']:.2%})"
                )
            elif kw_data["density"] > 0.03:
                recommendations.append(
                    f"Reduce keyword density to avoid over-optimization (currently {kw_data['density']:.2%})"
                )

            if not kw_data["in_first_paragraph"]:
                recommendations.append("Include primary keyword in the first paragraph")

        # Structure recommendations
        struct = analysis["structure_analysis"]
        if struct["headings"]["total"] == 0:
            recommendations.append(
                "Add headings (H1, H2, H3) to improve content structure"
            )
        if struct["links"]["internal"] == 0:
            recommendations.append("Add internal links to related content")
        if struct["avg_paragraph_length"] > 150:
            recommendations.append("Break up long paragraphs for better readability")

        # Readability recommendations
        if analysis["readability"]["avg_sentence_length"] > 20:
            recommendations.append("Simplify sentences for better readability")

        return recommendations


def optimize_content(
    content: str, keyword: str = None, secondary_keywords: List[str] = None
) -> str:
    """Main function to optimize content"""
    optimizer = SEOOptimizer()

    # Parse secondary keywords from comma-separated string if provided
    if secondary_keywords and isinstance(secondary_keywords, str):
        secondary_keywords = [kw.strip() for kw in secondary_keywords.split(",")]

    results = optimizer.analyze(content, keyword, secondary_keywords)
    language = results.get("language", "en")

    if language == "zh":
        return _format_output_zh(results)
    else:
        return _format_output_en(results)


def _format_output_zh(results: Dict) -> str:
    """Format output for Chinese content"""
    output = [
        "=== SEO 内容分析 ===",
        f"SEO 总分: {results['optimization_score']}/100",
        f"内容长度: {results['content_length']} 字",
        "",
        "内容结构:",
        f"  标题数: {results['structure_analysis']['headings']['total']}",
        f"  段落数: {results['structure_analysis']['paragraphs']}",
        f"  平均段落长度: {results['structure_analysis']['avg_paragraph_length']} 字",
        f"  内链数: {results['structure_analysis']['links']['internal']}",
        f"  外链数: {results['structure_analysis']['links']['external']}",
        "",
        f"可读性: {results['readability']['level']} (评分: {results['readability']['score']})",
        "",
    ]

    if results["keyword_analysis"]:
        kw = results["keyword_analysis"]["primary_keyword"]
        output.extend(
            [
                "关键词分析:",
                f"  主关键词: {kw['keyword']}",
                f"  出现次数: {kw['count']}",
                f"  关键词密度: {kw['density']:.1%}",
                f"  首段包含: {'是' if kw['in_first_paragraph'] else '否'}",
                "",
            ]
        )

        if results["keyword_analysis"]["lsi_keywords"]:
            output.append("  相关关键词:")
            for lsi in results["keyword_analysis"]["lsi_keywords"][:5]:
                output.append(f"    • {lsi}")
            output.append("")

    if results["meta_suggestions"]:
        output.extend(
            [
                "Meta 标签建议:",
                f"  标题: {results['meta_suggestions']['title']}",
                f"  描述: {results['meta_suggestions']['meta_description']}",
                f"  URL: {results['meta_suggestions']['url_slug']}",
                "",
            ]
        )

    output.append("优化建议:")
    for rec in results["recommendations"]:
        output.append(f"  • {rec}")

    return "\n".join(output)


def _format_output_en(results: Dict) -> str:
    """Format output for English content"""
    output = [
        "=== SEO Content Analysis ===",
        f"Overall SEO Score: {results['optimization_score']}/100",
        f"Content Length: {results['content_length']} words",
        "",
        "Content Structure:",
        f"  Headings: {results['structure_analysis']['headings']['total']}",
        f"  Paragraphs: {results['structure_analysis']['paragraphs']}",
        f"  Avg Paragraph Length: {results['structure_analysis']['avg_paragraph_length']} words",
        f"  Internal Links: {results['structure_analysis']['links']['internal']}",
        f"  External Links: {results['structure_analysis']['links']['external']}",
        "",
        f"Readability: {results['readability']['level']} (Score: {results['readability']['score']})",
        "",
    ]

    if results["keyword_analysis"]:
        kw = results["keyword_analysis"]["primary_keyword"]
        output.extend(
            [
                "Keyword Analysis:",
                f"  Primary Keyword: {kw['keyword']}",
                f"  Count: {kw['count']}",
                f"  Density: {kw['density']:.2%}",
                f"  In First Paragraph: {'Yes' if kw['in_first_paragraph'] else 'No'}",
                "",
            ]
        )

        if results["keyword_analysis"]["lsi_keywords"]:
            output.append("  Related Keywords Found:")
            for lsi in results["keyword_analysis"]["lsi_keywords"][:5]:
                output.append(f"    • {lsi}")
            output.append("")

    if results["meta_suggestions"]:
        output.extend(
            [
                "Meta Tag Suggestions:",
                f"  Title: {results['meta_suggestions']['title']}",
                f"  Description: {results['meta_suggestions']['meta_description']}",
                f"  URL Slug: {results['meta_suggestions']['url_slug']}",
                "",
            ]
        )

    output.append("Recommendations:")
    for rec in results["recommendations"]:
        output.append(f"  • {rec}")

    return "\n".join(output)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read()

        keyword = sys.argv[2] if len(sys.argv) > 2 else None
        secondary = sys.argv[3] if len(sys.argv) > 3 else None

        print(optimize_content(content, keyword, secondary))
    else:
        print(
            "Usage: python seo_optimizer.py <file> [primary_keyword] [secondary_keywords]"
        )
        print("用法: python seo_optimizer.py <文件> [主关键词] [次关键词]")
