#!/usr/bin/env python3
"""Small, dependency-free smoke test for the generated static site."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: set[str] = set()
        self.h1_count = 0
        self.has_description = False
        self.has_lang = False
        self.image_without_alt = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html" and values.get("lang"):
            self.has_lang = True
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.has_description = True
        if tag == "img" and "alt" not in values:
            self.image_without_alt += 1


def target_file(root: Path, source: Path, href: str) -> tuple[Path, str]:
    parsed = urlsplit(href)
    path = unquote(parsed.path)
    if path.startswith("/"):
        candidate = root / path.lstrip("/")
    else:
        candidate = source.parent / path
    if path.endswith("/") or not candidate.suffix:
        candidate /= "index.html"
    return candidate.resolve(), parsed.fragment


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    if not (root / "index.html").is_file():
        print(f"error: {root}/index.html is missing")
        return 1

    pages: dict[Path, PageParser] = {}
    errors: list[str] = []
    for page in sorted(root.rglob("*.html")):
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        pages[page.resolve()] = parser
        rel = page.relative_to(root)
        if not parser.has_lang:
            errors.append(f"{rel}: missing html lang")
        if not parser.has_description:
            errors.append(f"{rel}: missing meta description")
        if parser.h1_count != 1:
            errors.append(f"{rel}: expected one h1, found {parser.h1_count}")
        if parser.image_without_alt:
            errors.append(f"{rel}: image without alt text")

    for page, parser in pages.items():
        for href in parser.hrefs:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "tel:")):
                continue
            target, fragment = target_file(root, page, href)
            rel_page = page.relative_to(root)
            if not target.exists():
                errors.append(f"{rel_page}: broken internal link {href}")
                continue
            if fragment and target.suffix == ".html":
                target_parser = pages.get(target)
                if target_parser and fragment not in target_parser.ids:
                    errors.append(f"{rel_page}: missing fragment #{fragment} in {target.relative_to(root)}")

    if errors:
        print("Site checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Site checks passed: {len(pages)} HTML pages inspected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

