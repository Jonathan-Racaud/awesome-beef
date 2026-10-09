#!/usr/bin/env python3
"""Generate site/index.html from data.json.

Single-file, dependency-free generator. Uses only the Python standard library
(and reuses the `validate` function from `generate_readme.py`). The companion
`site/style.css` is hand-authored and left untouched by this script.

Run: python generate_site.py
"""

import html
import json
import sys
from collections import defaultdict
from pathlib import Path

# Reuse the shared data.json validation from the README generator.
from generate_readme import validate

# Rotating accent classes so the card grid stays visually varied. Only four are
# defined in style.css; we cycle through them.
ACCENT_CLASSES = ("accent-0", "accent-1", "accent-2", "accent-3")

# Inline GitHub mark (Octicons "mark-github"), reused in every card footer.
GITHUB_ICON = (
    '<svg class="github-icon" viewBox="0 0 16 16" '
    'aria-hidden="true" focusable="false">'
    '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
    '0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52'
    '-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89'
    '-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 '
    '1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75'
    '-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>'
    '</svg>'
)


def display_url(url: str) -> str:
    """Return a human-friendly URL (scheme, www, and trailing slash stripped)."""
    out = url
    if out.startswith("https://"):
        out = out[len("https://"):]
    elif out.startswith("http://"):
        out = out[len("http://"):]
    if out.startswith("www."):
        out = out[len("www."):]
    return out.rstrip("/")


def build_tree(data: dict) -> tuple[list[dict], dict[str, list[dict]]]:
    """Return (roots, children) for the category tree.

    `children` maps a category id to its direct child categories, preserving
    the order in which they appear in data.json (matching generate_readme.py).
    """
    categories = data["categories"]

    children: dict[str, list[dict]] = defaultdict(list)
    roots: list[dict] = []
    for category in categories:
        if category.get("parent") is None:
            roots.append(category)
        else:
            children[category["parent"]].append(category)

    return roots, children


def render_toc(category: dict, depth: int, children: dict[str, list[dict]], out: list[str]) -> None:
    """Render a single TOC entry (with nested children) into `out`."""
    cid = category["id"]
    title = html.escape(category["title"])
    kids = children.get(cid, [])
    sublist_id = f"toc-{cid}"

    out.append(f'<li class="toc-item depth-{depth}">')
    out.append('  <div class="toc-row">')

    if kids:
        out.append(
            '    <button type="button" class="toc-toggle" '
            f'aria-expanded="true" aria-controls="{sublist_id}" '
            f'aria-label="Toggle {title} section">'
            '<span class="chevron" aria-hidden="true">&#9662;</span></button>'
        )
    else:
        out.append('    <span class="toc-toggle toc-toggle--ghost" '
                   'aria-hidden="true"><span class="chevron">&#9662;</span></span>')

    out.append(f'    <a class="toc-title" href="#{cid}">{title}</a>')
    out.append('  </div>')

    if kids:
        out.append(f'  <ul class="toc-sublist" id="{sublist_id}">')
        for child in kids:
            render_toc(child, depth + 1, children, out)
        out.append('  </ul>')

    out.append('</li>')


def render_notes(notes: list[dict]) -> list[str]:
    """Return the lines of an entry's notes list (empty if there are none)."""
    if not notes:
        return []
    lines = ['  <ul class="notes">']
    for note in notes:
        text = html.escape(note["text"])
        if note.get("url"):
            lines.append(
                f'    <li><a href="{html.escape(note["url"], quote=True)}" '
                f'target="_blank" rel="noopener noreferrer">{text}</a></li>'
            )
        else:
            lines.append(f"    <li>{text}</li>")
    lines.append("  </ul>")
    return lines


def render_entry(entry: dict, accent_index: int) -> str:
    """Render a single entry as a card (header, body, divider, footer)."""
    accent = ACCENT_CLASSES[accent_index % len(ACCENT_CLASSES)]
    name = html.escape(entry["name"])
    url = entry["url"]
    url_attr = html.escape(url, quote=True)
    repo_label = html.escape(display_url(url))

    lines = [f'<article class="card {accent}">']

    # Header: label linking to the repo.
    lines.append(
        f'  <h4 class="card-title"><a href="{url_attr}" '
        f'target="_blank" rel="noopener noreferrer">{name}</a></h4>'
    )

    # Body: description (and any notes).
    if entry.get("description"):
        lines.append(f'  <p class="card-description">{html.escape(entry["description"])}</p>')
    lines.extend(render_notes(entry.get("notes", [])))

    # Divider.
    lines.append('  <div class="card-divider" aria-hidden="true"></div>')

    # Footer: explicit repo link (left) and tags (right).
    tags = entry.get("tags", [])
    tag_html = "".join(f'<li class="tag">{html.escape(tag)}</li>' for tag in tags)

    lines.append('  <div class="card-footer">')
    lines.append(
        f'    <a class="card-repo" href="{url_attr}" '
        f'target="_blank" rel="noopener noreferrer">'
        f'{GITHUB_ICON}<span class="card-repo-label">{repo_label}</span></a>'
    )
    if tag_html:
        lines.append(f'    <ul class="tags">{tag_html}</ul>')
    lines.append('  </div>')

    lines.append("</article>")
    return "\n".join(lines)


def render_section(
    category: dict,
    depth: int,
    children: dict[str, list[dict]],
    entries_by_category: dict[str, list[dict]],
    accent_counter: list[int],
    out: list[str],
) -> None:
    """Render a category section (heading, description, cards, nested sections)."""
    cid = category["id"]
    title = html.escape(category["title"])
    heading_level = min(depth + 2, 6)  # top-level sections start at <h2>
    entries = entries_by_category.get(cid, [])

    out.append(f'<section id="{cid}" class="category depth-{depth}">')

    # Heading style: `## << Title >>` for top-level, `### Title`, `#### Title` below.
    marker = "#" * (depth + 2)
    title_html = (
        f'<h{heading_level} class="section-title">'
        f'<span class="marker">{marker}</span> {title}</h{heading_level}>'
    )
    out.append(f"  {title_html}")

    if category.get("description"):
        out.append(f'  <p class="category-description">{html.escape(category["description"])}</p>')

    if entries:
        out.append('  <div class="cards">')
        for entry in entries:
            card = render_entry(entry, accent_counter[0])
            accent_counter[0] += 1
            out.append("    " + card.replace("\n", "\n    "))
        out.append('  </div>')

    # Nested sections follow their parent's cards, matching README order.
    for child in children.get(cid, []):
        out.append("")
        render_section(child, depth + 1, children, entries_by_category, accent_counter, out)

    out.append("</section>")


def render_content(
    roots: list[dict],
    children: dict[str, list[dict]],
    entries_by_category: dict[str, list[dict]],
) -> str:
    """Render the <main> content (page header + all category sections)."""
    out: list[str] = []
    accent_counter = [0]

    for root in roots:
        if out and out[-1] != "":
            out.append("")
        render_section(root, 0, children, entries_by_category, accent_counter, out)

    return "\n".join(out)


def generate(data: dict) -> str:
    """Render the full site/index.html content from parsed data.json."""
    metadata = data["metadata"]
    title = html.escape(metadata["title"])
    description = html.escape(metadata.get("description", ""))

    roots, children = build_tree(data)

    entries_by_category: dict[str, list[dict]] = defaultdict(list)
    for entry in data["entries"]:
        entries_by_category[entry["category"]].append(entry)

    toc_lines: list[str] = ['<ul class="toc">']
    for root in roots:
        render_toc(root, 0, children, toc_lines)
    toc_lines.append("</ul>")

    page_meta = []
    badge = metadata.get("badge")
    if badge:
        page_meta.append(
            f'<a class="badge-chip" href="{html.escape(badge["url"], quote=True)}" '
            f'target="_blank" rel="noopener noreferrer">{html.escape(badge["text"])}</a>'
        )
    inspiration = metadata.get("inspiration")
    if inspiration:
        label = inspiration.rstrip("/").rsplit("/", 1)[-1]
        page_meta.append(
            f'<span>Inspired by <a href="{html.escape(inspiration, quote=True)}" '
            f'target="_blank" rel="noopener noreferrer">{html.escape(label)}</a></span>'
        )

    script = """<script>
  (function () {
    var navToggle = document.getElementById('nav-toggle');
    var sidebar = document.getElementById('sidebar');

    // Mobile drawer toggle.
    navToggle.addEventListener('click', function () {
      var open = sidebar.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    // Collapsible TOC headings.
    document.querySelectorAll('.toc-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var expanded = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        var sublist = document.getElementById(btn.getAttribute('aria-controls'));
        if (sublist) sublist.classList.toggle('is-collapsed', expanded);
      });
    });

    // Close the mobile drawer when a TOC link is clicked.
    document.querySelectorAll('.toc-title').forEach(function (link) {
      link.addEventListener('click', function () {
        sidebar.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });

    // Scroll-spy: highlight the TOC link of the section in view.
    var links = document.querySelectorAll('.toc-title');
    var map = {};
    links.forEach(function (link) {
      var id = link.getAttribute('href').slice(1);
      map[id] = link;
    });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = map[entry.target.id];
        if (!link) return;
        if (entry.isIntersecting) {
          links.forEach(function (l) { l.classList.remove('is-active'); });
          link.classList.add('is-active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });
    document.querySelectorAll('main section[id]').forEach(function (section) {
      observer.observe(section);
    });
  })();
</script>"""

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        f"  <title>{title}</title>",
    ]
    if description:
        parts.append(f'  <meta name="description" content="{description}">')
    parts.extend([
        '  <link rel="stylesheet" href="style.css">',
        "</head>",
        "<body>",
        '  <a class="skip-link" href="#content">Skip to content</a>',
        '  <div class="page-surface">',
        '    <div class="ambient-bg" aria-hidden="true"></div>',
        '    <div class="top-glow" aria-hidden="true"></div>',
        '    <header class="site-header">',
        '      <button type="button" id="nav-toggle" class="nav-toggle"',
        '              aria-controls="sidebar" aria-expanded="false"',
        '              aria-label="Toggle navigation">',
        '        <span class="nav-toggle-bar"></span>',
        '        <span class="nav-toggle-bar"></span>',
        '        <span class="nav-toggle-bar"></span>',
        "      </button>",
        f'      <a class="site-title" href="#content">{title}</a>',
        "    </header>",
        '    <div class="layout">',
        '      <nav id="sidebar" class="sidebar" aria-label="Table of contents">',
        '        <div class="sidebar-card">',
        '          <div class="sidebar-brand">',
        f'            <div class="sidebar-title">{title}</div>',
    ])
    if description:
        parts.append(f'            <p class="sidebar-description">{description}</p>')
    parts.extend([
        "          </div>",
        '          <h2 class="toc-heading">Contents</h2>',
    ])
    parts.extend(toc_lines)
    parts.extend([
        "        </div>",
        "      </nav>",
        '      <main id="content" class="content">',
        '        <header class="page-header">',
        f'          <h1 class="page-title">{title}</h1>',
    ])
    if description:
        parts.append(f'          <p class="page-description">{description}</p>')
    if page_meta:
        parts.append('          <div class="page-meta">')
        parts.append("            " + "\n            ".join(page_meta))
        parts.append("          </div>")
    parts.append("        </header>")
    parts.append("")
    parts.append(render_content(roots, children, entries_by_category))
    parts.extend([
        "      </main>",
        "    </div>",
        '    <footer class="site-footer">',
        f'      Generated from <code>data.json</code> by <code>generate_site.py</code>.',
        "    </footer>",
        "  </div>",
        script,
        "</body>",
        "</html>",
    ])

    return "\n".join(parts) + "\n"


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    data_path = script_dir / "data.json"
    site_dir = script_dir / "site"
    index_path = site_dir / "index.html"

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

    site_dir.mkdir(parents=True, exist_ok=True)
    index_path.write_text(generate(data), encoding="utf-8")
    print(f"Wrote {index_path.name}")


if __name__ == "__main__":
    main()
