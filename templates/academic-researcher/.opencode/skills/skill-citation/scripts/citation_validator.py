#!/usr/bin/env python3
"""
Citation Validator - Validate citations using Semantic Scholar, CrossRef, and arXiv.
"""

import json
import os
import re
import sys
import time
from typing import Dict, List, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class CitationValidator:
    """Validate citations against multiple public APIs."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.semantic_url = (
            "https://api.semanticscholar.org/graph/v1/paper/search"
            "?query={query}&limit=3&fields=title,year,authors"
        )
        self.crossref_url = "https://api.crossref.org/works?query.title={query}&rows=3"
        self.arxiv_url = (
            "http://export.arxiv.org/api/query?search_query=ti:{query}&max_results=3"
        )

    def load_references(self, path: str) -> List[Dict]:
        """Load references from a directory or a BibTeX file."""
        if os.path.isdir(path):
            return self._load_from_directory(path)
        if os.path.isfile(path) and path.lower().endswith(".bib"):
            return self._parse_bibtex_file(path)
        raise FileNotFoundError(
            "Provide a .bib file or a directory containing references."
        )

    def _load_from_directory(self, base_path: str) -> List[Dict]:
        """Load references from a directory with meta files."""
        references = []
        for root, _, files in os.walk(base_path):
            if "bibtex.txt" in files:
                bibtex_path = os.path.join(root, "bibtex.txt")
                references.extend(self._parse_bibtex_file(bibtex_path))
            if "meta_info.txt" in files:
                meta_path = os.path.join(root, "meta_info.txt")
                references.extend(self._parse_meta_info(meta_path))
        return references

    def _parse_meta_info(self, meta_path: str) -> List[Dict]:
        """Parse meta_info.txt for title entries."""
        references = []
        try:
            with open(meta_path, "r", encoding="utf-8") as file:
                content = file.read()
            title_match = re.search(r"title\s*:\s*(.+)", content, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                key = self._slugify_key(title)
                references.append({"key": key, "title": title, "source": meta_path})
        except Exception:
            if self.verbose:
                print(f"[WARN] Failed to parse {meta_path}")
        return references

    def _parse_bibtex_file(self, path: str) -> List[Dict]:
        """Parse BibTeX entries with a simple regex-based parser."""
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        entries = []
        entry_matches = re.finditer(r"@\w+\s*\{([^,]+),([\s\S]*?)\}\s*", content)
        for match in entry_matches:
            key = match.group(1).strip()
            fields_blob = match.group(2)
            title = self._extract_bibtex_field(fields_blob, "title")
            author = self._extract_bibtex_field(fields_blob, "author")
            year = self._extract_bibtex_field(fields_blob, "year")

            if not title:
                continue

            entries.append(
                {
                    "key": key,
                    "title": title,
                    "author": author,
                    "year": year,
                    "source": path,
                }
            )

        return entries

    def _extract_bibtex_field(self, blob: str, field: str) -> str:
        match = re.search(
            rf"{field}\s*=\s*[{{\"](.+?)[}}\"]\s*,",
            blob,
            re.IGNORECASE,
        )
        return match.group(1).strip() if match else ""

    def validate_references(self, references: List[Dict]) -> List[Dict]:
        """Validate each reference and return results."""
        results = []
        for ref in references:
            title = ref.get("title", "").strip()
            if not title:
                continue
            if self.verbose:
                print(f"[INFO] Validating: {title}")

            try:
                status, source, closest = self._validate_title(title)
                results.append(
                    {
                        "reference": ref,
                        "status": status,
                        "source": source,
                        "closest": closest,
                    }
                )
            except Exception as error:
                results.append(
                    {
                        "reference": ref,
                        "status": "UNCERTAIN",
                        "source": "",
                        "closest": "",
                        "error": str(error),
                    }
                )
            time.sleep(1)
        return results

    def _validate_title(self, title: str) -> Tuple[str, str, str]:
        """Validate a title using multiple APIs."""
        validators = [
            (self._search_semantic_scholar, "Semantic Scholar"),
            (self._search_crossref, "CrossRef"),
            (self._search_arxiv, "arXiv"),
        ]

        for func, label in validators:
            matches = func(title)
            if matches:
                status, closest = self._evaluate_matches(title, matches)
                if status == "VALID":
                    return "VALID", label, closest
                if status == "UNCERTAIN":
                    return "UNCERTAIN", label, closest

        return "INVALID", "", ""

    def _search_semantic_scholar(self, title: str) -> List[str]:
        query = quote(title)
        url = self.semantic_url.format(query=query)
        data = self._fetch_json(url)
        return [item.get("title", "") for item in data.get("data", [])]

    def _search_crossref(self, title: str) -> List[str]:
        query = quote(title)
        url = self.crossref_url.format(query=query)
        data = self._fetch_json(url)
        items = data.get("message", {}).get("items", [])
        return [item.get("title", [""])[0] for item in items]

    def _search_arxiv(self, title: str) -> List[str]:
        query = quote(title)
        url = self.arxiv_url.format(query=query)
        xml_text = self._fetch_text(url)
        return re.findall(r"<title>(.*?)</title>", xml_text, re.DOTALL)[1:]

    def _fetch_json(self, url: str) -> Dict:
        request = Request(url, headers={"User-Agent": "OpenCode Citation Validator"})
        try:
            with urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            if error.code == 429:
                raise RuntimeError("Rate limit reached. Retry later.")
            raise RuntimeError(f"HTTP error: {error}")
        except URLError as error:
            raise RuntimeError(f"Network error: {error}")
        except json.JSONDecodeError as error:
            raise RuntimeError(f"JSON parse error: {error}")

    def _fetch_text(self, url: str) -> str:
        request = Request(url, headers={"User-Agent": "OpenCode Citation Validator"})
        try:
            with urlopen(request, timeout=20) as response:
                return response.read().decode("utf-8")
        except HTTPError as error:
            if error.code == 429:
                raise RuntimeError("Rate limit reached. Retry later.")
            raise RuntimeError(f"HTTP error: {error}")
        except URLError as error:
            raise RuntimeError(f"Network error: {error}")

    def _evaluate_matches(
        self, query_title: str, matches: List[str]
    ) -> Tuple[str, str]:
        """Evaluate match list against query title."""
        best_overlap = 0.0
        best_match = ""
        query_words = self._normalize_words(query_title)

        for title in matches:
            overlap = self._jaccard(query_words, self._normalize_words(title))
            if overlap > best_overlap:
                best_overlap = overlap
                best_match = title

        if best_overlap >= 0.8:
            return "VALID", best_match
        if best_overlap >= 0.5:
            return "UNCERTAIN", best_match
        return "INVALID", best_match

    def _normalize_words(self, title: str) -> set:
        clean = re.sub(r"[^a-z0-9\s]", "", title.lower())
        return {word for word in clean.split() if word}

    def _jaccard(self, a: set, b: set) -> float:
        if not a or not b:
            return 0.0
        intersection = a.intersection(b)
        union = a.union(b)
        return len(intersection) / len(union) if union else 0.0

    def _slugify_key(self, title: str) -> str:
        words = re.findall(r"[a-z0-9]+", title.lower())
        return "_".join(words[:4]) or "unknown_reference"

    def format_report(self, results: List[Dict]) -> str:
        """Format structured validation report."""
        valid = sum(1 for item in results if item["status"] == "VALID")
        invalid = sum(1 for item in results if item["status"] == "INVALID")
        uncertain = sum(1 for item in results if item["status"] == "UNCERTAIN")
        total = len(results)
        validation_rate = (valid / total * 100) if total else 0

        lines = [
            "====================================",
            "CITATION VALIDATION REPORT",
            "====================================",
            "",
            f"References Checked: {total}",
            f"Valid: {valid} | Invalid: {invalid} | Uncertain: {uncertain}",
            "",
            "------------------------------------",
            "RESULTS",
            "------------------------------------",
            "",
        ]

        if not results:
            lines.append("No references found.")
            lines.append("")

        for item in results:
            ref = item["reference"]
            key = ref.get("key", "unknown")
            title = ref.get("title", "Unknown Title")
            status = item["status"]

            lines.append(f"[{status}] {key}")
            lines.append(f'  Title: "{title}"')

            if status == "VALID":
                lines.append(f"  Verified via: {item['source']}")
            elif status == "INVALID":
                lines.append("  Reason: No matching paper found in any database")
                lines.append("  Suggestion: Verify this citation manually or remove it")
            else:
                lines.append(
                    "  Reason: Multiple partial matches found, manual review recommended"
                )
                if item.get("closest"):
                    lines.append(f'  Closest match: "{item["closest"]}"')

            if item.get("error"):
                lines.append(f"  Error: {item['error']}")

            lines.append("")

        recommendation = "PASS"
        if invalid > 0:
            recommendation = "FAIL"
        elif uncertain > 0:
            recommendation = "REVIEW_NEEDED"

        lines.extend(
            [
                "------------------------------------",
                "SUMMARY",
                "------------------------------------",
                "",
                f"Validation Rate: {validation_rate:.1f}%",
                f"Recommendation: {recommendation}",
                "",
                "====================================",
            ]
        )

        return "\n".join(lines)


def _print_usage() -> None:
    print(
        "Usage: python citation_validator.py <references-dir-or-bib-file> [--verbose] [--json]"
    )


def main() -> None:
    if len(sys.argv) < 2:
        _print_usage()
        return

    target_path = sys.argv[1]
    verbose = "--verbose" in sys.argv
    json_output = "--json" in sys.argv

    validator = CitationValidator(verbose=verbose)

    try:
        references = validator.load_references(target_path)
        results = validator.validate_references(references)
        if json_output:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(validator.format_report(results))
    except Exception as error:
        print("====================================")
        print("CITATION VALIDATION ERROR")
        print("====================================")
        print(str(error))
        if verbose:
            print("\nTip: Ensure the references path is correct and retry.")


if __name__ == "__main__":
    main()
