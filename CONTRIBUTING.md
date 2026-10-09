# Contributing

Your contributions are always welcome!

## The single source of truth

This list is maintained in [`data.json`](data.json). Do **not** edit
[`README.md`](README.md) directly — it is generated from `data.json` by
[`generate_readme.py`](generate_readme.py), and a GitHub Action regenerates it
automatically whenever `data.json` changes. Edit `data.json` instead.

## Guidelines

- Add one link per Pull Request.
    - Make sure the PR title is in the format `Add project-name`.
    - Write down the reason why the library is awesome.
- Add a new entry to `data.json` in the appropriate `categories` bucket.
    - Use the format: `{ "name": "project-name", "url": "https://example.com/", "description": "A short description ends with a period.", "category": "some-category", "tags": ["..."] }`.
    - Keep descriptions concise.
- Add a category if needed.
    - Give it an `id`, `title`, `parent` (or `null` for a top-level section), and optionally a `description`.
- Keep entries in alphabetical order within each category.
- Search previous Pull Requests or Issues before making a new one, as yours may be a duplicate.
- Check your spelling and grammar.
- Remove any trailing whitespace.
- The *Frameworks and Libraries* and *Projects and Articles* sections should keep the same organization to make searching for a specific type of project or article easier.
