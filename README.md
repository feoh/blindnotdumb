# Blind Not Dumb, Hugo branch

This branch is a Hugo-based migration path for the blog.

## Local development

If Hugo is installed globally:

```bash
hugo server
```

If not, you can use the local workspace binary I bootstrapped while testing:

```bash
.tools/hugo/hugo server
```

## Build

```bash
python scripts/convert_nikola_to_hugo.py
.tools/hugo/hugo --destination public
```

## Migration notes

- Original source posts remain under `posts/`
- Hugo content is generated into `content/`
- Static images are copied into `static/images/`
- Tags work through Hugo taxonomies out of the box
