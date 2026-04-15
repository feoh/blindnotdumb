# Blind, Not Dumb

This branch contains a Zensical-based version of the blog, migrated from Nikola.

## Local development

```bash
uv sync
uv run zensical serve
```

## Build

```bash
uv run zensical build
```

The generated site is written to `site/`.

## Migration notes

- Original Nikola source content is preserved under `posts/`
- Zensical content lives under `docs/`
- The migration helper used to generate the Zensical content is `scripts/convert_nikola_to_zensical.py`
