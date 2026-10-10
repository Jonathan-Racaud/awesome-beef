# Contributing

Your contributions are always welcome!

## The single source of truth

This list is maintained in [`curated.json`](curated.json). Do **not** edit
[`README.md`](README.md) or [`site/index.html`](site/index.html) directly — they
are generated from `curated.json` by
[`generate_readme.py`](generate_readme.py) and
[`generate_site.py`](generate_site.py), and a GitHub Action regenerates them
automatically whenever `curated.json` changes. Edit `curated.json` instead.

The static website's stylesheet, [`site/style.css`](site/style.css), is the only
hand-edited file in the `site/` directory.

## Guidelines

- Add one link per Pull Request.
    - Make sure the PR title is in the format `Add project-name`.
    - Write down the reason why the library is awesome.
- Add a new entry to `curated.json` in the appropriate `categories` bucket.
    - Use the format: `{ "name": "project-name", "url": "https://example.com/", "description": "A short description ends with a period.", "category": "some-category", "tags": ["..."] }`.
    - Keep descriptions concise.
- Add a category if needed.
    - Give it an `id`, `title`, `parent` (or `null` for a top-level section), and optionally a `description`.
- Keep entries in alphabetical order within each category.
- Search previous Pull Requests or Issues before making a new one, as yours may be a duplicate.
- Check your spelling and grammar.
- Remove any trailing whitespace.
- The *Frameworks and Libraries* and *Projects and Articles* sections should keep the same organization to make searching for a specific type of project or article easier.
