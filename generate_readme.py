#!/usr/bin/env python3
"""Generate README.md from data.json.

Single-file, dependency-free generator. Uses only the Python standard library.
Run: python generate_readme.py
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# The awesome-badge image is not stored in data.json (metadata.badge only has
# "text" and "url"), so it is hardcoded here.
BADGE_IMAGE_URL = (
    "https://cdn.rawgit.com/sindresorhus/awesome/"
    "d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg"
)

CONTRIBUTING_FOOTER = (
    "# Contributing\n"
    "\n"
    "Your contributions are always welcome! Please take a look at the "
    "[contribution guidelines](CONTRIBUTING.md) first.\n"
    "\n"
    "I will keep some pull requests open if I'm not sure whether those "
    "libraries are awesome, you could [vote for them](pulls) by adding :+1: to "
    "them. Pull requests will be merged when their votes reach **20**."
)


def slugify(title: str) -> str:
    """Derive a GitHub-style heading anchor from a title.

    GitHub lowercases the text, strips characters that are not letters, numbers,
    spaces, or hyphens, and converts runs of whitespace to a single hyphen.
    """
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def label_from_url(url: str) -> str:
    """Return a human label for a URL, using its final path segment."""
    path = url.rstrip("/")
    return path.rsplit("/", 1)[-1] or path


def validate(data: dict) -> list[str]:
    """Validate data.json structure. Returns a list of human-readable errors."""
    errors: list[str] = []

    metadata = data.get("metadata")
    if not isinstance(metadata, dict) or not metadata.get("title"):
        errors.append("metadata.title is required")

    categories = data.get("categories")
    if not isinstance(categories, list) or not categories:
        errors.append("categories must be a non-empty list")

    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("entries must be a list")

    ids: dict[str, dict] = {}
    for category in categories or []:
        if not isinstance(category, dict):
            errors.append("every category must be an object")
            continue
        cid = category.get("id")
        if not cid:
            errors.append("a category is missing its 'id'")
            continue
        if cid in ids:
            errors.append(f"duplicate category id: {cid}")
        ids[cid] = category
        if not category.get("title"):
            errors.append(f"category '{cid}' is missing its 'title'")

    for category in categories or []:
        if not isinstance(category, dict):
            continue
        parent = category.get("parent")
        if parent is not None and parent not in ids:
            errors.append(
                f"category '{category.get('id')}' has unknown parent: {parent}"
            )

    for index, entry in enumerate(entries or []):
        category = entry.get("category")
        if category not in ids:
            errors.append(
                f"entry #{index} ({entry.get('name')}) has unknown category: "
                f"{category}"
            )

    return errors


def generate(data: dict) -> str:
    """Render the full README.md content from parsed data.json."""
    metadata = data["metadata"]
    categories = data["categories"]
    entries = data["entries"]

    children: dict[str, list[dict]] = defaultdict(list)
    roots: list[dict] = []
    for category in categories:
        if category.get("parent") is None:
            roots.append(category)
        else:
            children[category["parent"]].append(category)

    entries_by_category: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        entries_by_category[entry["category"]].append(entry)

    # Document order is a depth-first traversal of the category tree.
    order: list[tuple[dict, int]] = []

    def walk(category: dict, depth: int) -> None:
        order.append((category, depth))
        for child in children[category["id"]]:
            walk(child, depth + 1)

    for root in roots:
        walk(root, 0)

    # Assign anchors in document order, disambiguating duplicate titles the
    # same way GitHub does (-1, -2, ...).
    seen: dict[str, int] = {}
    anchors: dict[str, str] = {}
    for category, _ in order:
        base = slugify(category["title"])
        count = seen.get(base, 0)
        seen[base] = count + 1
        anchors[category["id"]] = base if count == 0 else f"{base}-{count}"

    lines: list[str] = []

    # Header banner.
    banner = metadata.get("banner")
    if banner:
        lines.append(f'<div style="text-align:center"><img src="{banner}"/></div>')
        lines.append("")

    # Title and badge.
    title_line = f"# {metadata['title']}"
    badge = metadata.get("badge")
    if badge:
        title_line += f" [![{badge['text']}]({BADGE_IMAGE_URL})]({badge['url']})"
    lines.append(title_line)

    # Description.
    if metadata.get("description"):
        lines.append(metadata["description"])

    lines.append("")

    # Inspiration.
    if metadata.get("inspiration"):
        url = metadata["inspiration"]
        lines.append(f"Inspired by [{label_from_url(url)}]({url}).")
        lines.append("")

    # Summary / table of contents.
    lines.append("# Summary")
    for category, depth in order:
        indent = "    " * depth
        lines.append(f"{indent}- [{category['title']}](#{anchors[category['id']]})")
    lines.append("- [Contributing](#contributing)")
    lines.append("")

    # Sections.
    def render(category: dict, depth: int, out: list[str]) -> None:
        out.append("#" * (depth + 1) + " " + category["title"])
        if category.get("description"):
            out.append("*" + category["description"] + "*")
        if category.get("description") and entries_by_category[category["id"]]:
            out.append("")
        for entry in entries_by_category[category["id"]]:
            line = f"- [{entry['name']}]({entry['url']})"
            if entry.get("description"):
                line += f" - {entry['description']}"
            if entry.get("deprecated"):
                line += " *(deprecated)*"
            out.append(line)
            for note in entry.get("notes", []):
                if note.get("url"):
                    out.append(f"    - [{note['text']}]({note['url']})")
                else:
                    out.append(f"    - {note['text']}")
        for child in children[category["id"]]:
            out.append("")
            render(child, depth + 1, out)

    for root in roots:
        if lines and lines[-1] != "":
            lines.append("")
        render(root, 0, lines)

    lines.append("")
    lines.append(CONTRIBUTING_FOOTER)

    return "\n".join(lines) + "\n"


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    data_path = script_dir / "data.json"
    readme_path = script_dir / "README.md"

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: {data_path} not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {data_path}: {exc}", file=sys.stderr)
        sys.exit(1)

    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)

    readme_path.write_text(generate(data), encoding="utf-8")
    print(f"Wrote {readme_path.name}")


if __name__ == "__main__":
    main()
