# Blind Not Dumb, Hugo branch

This branch is a Hugo-based version of the blog.

## Local development

If Hugo is installed globally:

```bash
hugo server
```

If not, you can use a local Hugo binary:

```bash
.tools/hugo/hugo server
```

## Build

```bash
python scripts/generate_legacy_feeds.py
hugo --destination public
```

## Notes

- `content/` is the canonical source for posts and pages
- `static/images/` contains site images
- Hugo tags/taxonomies provide tag index pages
- Legacy Nikola and Pelican source/config files have been removed from this branch
