#!/usr/bin/env python3
"""
Novelty Checker - Evaluate proposal novelty against existing papers.
Uses Semantic Scholar API to find related papers and compute similarity.
"""

import json
import os
import re
import sys
from typing import Dict, List
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen, Request


class NoveltyChecker:
    """Check research proposal novelty using Semantic Scholar search."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.stopwords = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "but",
            "by",
            "for",
            "from",
            "has",
            "have",
            "had",
            "he",
            "her",
            "his",
            "i",
            "if",
            "in",
            "is",
            "it",
            "its",
            "me",
            "my",
            "not",
            "of",
            "on",
            "or",
            "our",
            "she",
            "so",
            "that",
            "the",
            "their",
            "them",
            "there",
            "they",
            "this",
            "to",
            "was",
            "we",
            "were",
            "will",
            "with",
            "you",
            "your",
            "about",
            "into",
            "can",
            "may",
            "might",
            "should",
            "would",
            "also",
            "than",
            "then",
            "which",
            "what",
            "when",
            "where",
            "how",
            "who",
            "whom",
        }
        self.api_url = (
            "https://api.semanticscholar.org/graph/v1/paper/search"
            "?query={query}&limit=10&fields=title,abstract,year,authors,citationCount,url"
        )

    def load_proposal(self, file_path: str) -> Dict[str, str]:
        """Read proposal file and extract title and abstract sections."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Proposal file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        title = self._extract_title(content)
        abstract = self._extract_abstract(content)
        return {"title": title, "abstract": abstract, "content": content}

    def _extract_title(self, content: str) -> str:
        """Extract title from markdown content."""
        title_match = re.search(r"^##\s+Title\s*\n+(.+)$", content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()

        proposal_match = re.search(
            r"^#\s+Research\s+Proposal\s*\n+(.+)$", content, re.MULTILINE
        )
        if proposal_match:
            return proposal_match.group(1).strip()

        h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()

        return "Untitled Proposal"

    def _extract_abstract(self, content: str) -> str:
        """Extract abstract section from markdown content."""
        abstract_match = re.search(
            r"^##\s+Abstract\s*\n+([\s\S]+?)(\n##\s+|\Z)",
            content,
            re.MULTILINE,
        )
        if abstract_match:
            return abstract_match.group(1).strip()

        return content[:1000].strip()

    def extract_keywords(self, title: str, abstract: str, limit: int = 10) -> List[str]:
        """Extract simple keywords from title and abstract."""
        text = f"{title} {abstract}".lower()
        words = re.findall(r"\b[a-z0-9][a-z0-9-]+\b", text)
        frequency: Dict[str, int] = {}

        for word in words:
            if word in self.stopwords or len(word) < 3:
                continue
            frequency[word] = frequency.get(word, 0) + 1

        sorted_terms = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
        return [term for term, _ in sorted_terms[:limit]]

    def query_semantic_scholar(self, terms: List[str]) -> List[Dict]:
        """Query Semantic Scholar API with extracted terms."""
        if not terms:
            return []

        query = quote(" ".join(terms))
        url = self.api_url.format(query=query)
        request = Request(url, headers={"User-Agent": "OpenCode Novelty Checker"})

        try:
            with urlopen(request, timeout=20) as response:
                data = response.read().decode("utf-8")
                payload = json.loads(data)
                return payload.get("data", [])
        except HTTPError as error:
            if error.code == 429:
                raise RuntimeError(
                    "Semantic Scholar API rate limit reached (HTTP 429). "
                    "Please retry later."
                )
            raise RuntimeError(f"HTTP error during API request: {error}")
        except URLError as error:
            raise RuntimeError(f"Network error during API request: {error}")
        except json.JSONDecodeError as error:
            raise RuntimeError(f"Failed to parse API response: {error}")

    def compute_similarity(self, proposal_text: str, paper_abstract: str) -> float:
        """Compute Jaccard similarity between proposal and paper abstract."""
        proposal_words = self._normalize_words(proposal_text)
        paper_words = self._normalize_words(paper_abstract)

        if not proposal_words or not paper_words:
            return 0.0

        intersection = proposal_words.intersection(paper_words)
        union = proposal_words.union(paper_words)
        return len(intersection) / len(union) if union else 0.0

    def _normalize_words(self, text: str) -> set:
        """Normalize text to word set for similarity."""
        words = re.findall(r"\b[a-z0-9][a-z0-9-]+\b", text.lower())
        return {word for word in words if word not in self.stopwords and len(word) > 2}

    def analyze(self, proposal_path: str) -> Dict:
        """Run novelty analysis and return structured data."""
        proposal = self.load_proposal(proposal_path)
        keywords = self.extract_keywords(
            proposal["title"], proposal["abstract"], limit=10
        )

        papers = self.query_semantic_scholar(keywords)
        results = []
        overlap_counter: Dict[str, int] = {}
        proposal_words = self._normalize_words(proposal["abstract"])

        for paper in papers:
            abstract = paper.get("abstract") or ""
            similarity = self.compute_similarity(proposal["abstract"], abstract)
            paper_words = self._normalize_words(abstract)
            overlap = sorted(proposal_words.intersection(paper_words))

            for term in overlap:
                overlap_counter[term] = overlap_counter.get(term, 0) + 1

            results.append(
                {
                    "title": paper.get("title") or "Untitled",
                    "year": paper.get("year") or "Unknown",
                    "authors": ", ".join(
                        author.get("name", "") for author in paper.get("authors", [])
                    ),
                    "citations": paper.get("citationCount", 0),
                    "similarity": similarity,
                    "url": paper.get("url") or "",
                    "overlap": overlap,
                }
            )

        results.sort(key=lambda item: item["similarity"], reverse=True)
        max_similarity = results[0]["similarity"] if results else 0.0
        novelty_label = self._novelty_label(max_similarity)

        differentiators = self._suggest_differentiators(
            proposal_words, overlap_counter, max_similarity
        )

        assessment = {
            "novelty": novelty_label,
            "max_similarity": max_similarity,
            "most_similar": results[0]["title"] if results else "N/A",
            "differentiators": differentiators,
            "recommendation": self._recommendation(novelty_label),
        }

        return {
            "proposal": proposal,
            "keywords": keywords,
            "results": results,
            "assessment": assessment,
        }

    def _novelty_label(self, similarity: float) -> str:
        """Convert similarity score to novelty label."""
        score = similarity * 100
        if score < 30:
            return "HIGH"
        if score <= 60:
            return "MEDIUM"
        return "LOW"

    def _recommendation(self, novelty_label: str) -> str:
        """Map novelty label to recommendation."""
        if novelty_label == "HIGH":
            return "PASS"
        if novelty_label == "MEDIUM":
            return "REVIEW_NEEDED"
        return "FAIL"

    def _suggest_differentiators(
        self, proposal_words: set, overlap_counter: Dict[str, int], similarity: float
    ) -> List[str]:
        """Suggest differentiators based on overlap terms."""
        if not overlap_counter:
            return [
                "Limited overlap detected. Emphasize unique methodology and datasets."
            ]

        common_terms = sorted(
            overlap_counter.items(), key=lambda item: item[1], reverse=True
        )
        top_overlap = [term for term, _ in common_terms[:5]]
        unique_terms = sorted(proposal_words.difference(top_overlap))

        suggestions = [
            "Clarify how your approach differs from existing work using new datasets or objectives.",
            f"Reduce emphasis on common terms: {', '.join(top_overlap)}.",
        ]

        if unique_terms:
            suggestions.append(
                f"Highlight unique contributions around: {', '.join(unique_terms[:5])}."
            )

        if similarity > 0.6:
            suggestions.append(
                "Provide stronger differentiation in methodology or evaluation."
            )

        return suggestions

    def format_report(self, analysis: Dict) -> str:
        """Format structured report output."""
        proposal = analysis["proposal"]
        results = analysis["results"]
        assessment = analysis["assessment"]

        lines = [
            "====================================",
            "NOVELTY CHECK REPORT",
            "====================================",
            "",
            f"Proposal: {proposal['title']}",
            f"Search Query: {' '.join(analysis['keywords'])}",
            f"Papers Found: {len(results)}",
            "",
            "------------------------------------",
            "SIMILAR PAPERS (sorted by similarity)",
            "------------------------------------",
            "",
        ]

        if not results:
            lines.append("No papers found for the query.")
            lines.append("")

        for index, paper in enumerate(results, start=1):
            similarity_pct = int(paper["similarity"] * 100)
            overlap = ", ".join(paper["overlap"][:8]) if paper["overlap"] else "None"
            lines.extend(
                [
                    f"{index}. {paper['title']} ({paper['year']})",
                    f"   Authors: {paper['authors'] or 'Unknown'}",
                    f"   Citations: {paper['citations']}",
                    f"   Similarity: {similarity_pct}%",
                    f"   URL: {paper['url'] or 'N/A'}",
                    f"   Key overlap: {overlap}",
                    "",
                ]
            )

        lines.extend(
            [
                "------------------------------------",
                "NOVELTY ASSESSMENT",
                "------------------------------------",
                "",
                f"Overall Novelty Score: {assessment['novelty']}",
                "",
                f"- Most similar existing work: {assessment['most_similar']}",
                "- Key differentiators needed:",
            ]
        )

        for suggestion in assessment["differentiators"]:
            lines.append(f"  - {suggestion}")

        lines.append(f"- Recommendation: {assessment['recommendation']}")
        lines.append("")
        lines.append("====================================")

        if self.verbose:
            lines.append("")
            lines.append(
                "[Verbose] Max similarity: {:.2%}".format(assessment["max_similarity"])
            )

        return "\n".join(lines)


def _print_usage() -> None:
    print("Usage: python novelty_checker.py <proposal-file> [--verbose] [--json]")


def main() -> None:
    if len(sys.argv) < 2:
        _print_usage()
        return

    proposal_path = sys.argv[1]
    verbose = "--verbose" in sys.argv
    json_output = "--json" in sys.argv

    checker = NoveltyChecker(verbose=verbose)

    try:
        analysis = checker.analyze(proposal_path)
        if json_output:
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
        else:
            print(checker.format_report(analysis))
    except Exception as error:
        print("====================================")
        print("NOVELTY CHECK ERROR")
        print("====================================")
        print(str(error))
        if verbose:
            print("\nTip: Check your network connection or retry later.")


if __name__ == "__main__":
    main()
