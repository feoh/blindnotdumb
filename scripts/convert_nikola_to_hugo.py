#!/home/feoh/.openclaw/workspace/.venv/bin/python
from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

import yaml
from docutils.core import publish_parts
from markdownify import markdownify as md

ROOT = Path('/home/feoh/.openclaw/workspace/blindnotdumb')
POSTS_DIR = ROOT / 'posts'
CONTENT_DIR = ROOT / 'content'
CONTENT_POSTS_DIR = CONTENT_DIR / 'posts'
STATIC_IMAGES_DIR = ROOT / 'static' / 'images'
IMAGES_DIR = ROOT / 'images'

SKIP_SLUGS = {'article-template', 'article_template'}
ABOUT_SLUGS = {'about', 'about-2'}
MD_META_RE = re.compile(r'^<!--\n(?P<meta>.*?)\n-->\n*', re.S)
MD_FIELD_RE = re.compile(r'^\.\.\s+(?P<key>[a-z_]+):\s*(?P<value>.*)$')
PEL_FIELD_RE = re.compile(r'^(?P<key>[A-Za-z_][A-Za-z0-9_]*):\s*(?P<value>.*)$')
RST_FIELD_RE = re.compile(r'^:(?P<key>[a-z_]+):\s*(?P<value>.*)$')


def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9-]+', '-', name.lower()).strip('-')


def normalize_title(title: str) -> str:
    replacements = {
        'IOS ': 'iOS ',
        'IPad': 'iPad',
        'Macbook': 'MacBook',
        'China Town': 'Chinatown',
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title


def clean_value(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def clean_markdown_body(text: str) -> str:
    text = text.replace('```winget install git```', '`winget install git`')
    text = re.sub(r'!\[/images/([^\]]+)\]\(/images/[^)]+\)', lambda m: f'![{Path(m.group(1)).stem.replace("_", " ")}](/images/{m.group(1)})', text)
    text = re.sub(r'<iframe[^>]*src="([^"]+)"[^>]*></iframe>', r'Embedded post: <\1>', text)
    text = re.sub(r'##\s+(.+?)\s+##', r'## \1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


def normalize_date(value: str | None) -> str | None:
    value = clean_value(value)
    if not value:
        return None
    normalized = value.replace(' UTC-05:00', '-05:00').replace(' UTC-04:00', '-04:00')
    normalized = re.sub(r'^0(\d{4}-)', r'\1', normalized)
    for fmt in ('%Y-%m-%d %H:%M:%S %z', '%Y-%m-%d %H:%M:%S%z', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'):
        try:
            dt = datetime.strptime(normalized, fmt)
            if dt.tzinfo is None:
                return dt.strftime('%Y-%m-%dT%H:%M:%S')
            return dt.strftime('%Y-%m-%dT%H:%M:%S%z')[:-2] + ':' + dt.strftime('%z')[-2:]
        except ValueError:
            pass
    return value


def normalize_meta(meta: dict[str, object], fallback_slug: str) -> dict[str, object]:
    title = normalize_title(str(meta.get('title') or fallback_slug.replace('-', ' ').title()))
    slug = clean_value(str(meta.get('slug') or fallback_slug)) or fallback_slug
    raw_tags = clean_value(str(meta.get('tags') or ''))
    if raw_tags:
        tags = list(dict.fromkeys(t.strip() for t in raw_tags.split(',') if t.strip()))
    else:
        tags = []
    return {
        'title': title,
        'slug': slugify(slug),
        'date': normalize_date(str(meta.get('date') or '')),
        'author': clean_value(str(meta.get('author') or meta.get('authors') or '')),
        'description': clean_value(str(meta.get('description') or meta.get('summary') or '')),
        'tags': tags,
    }


def parse_markdown(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text()
    meta: dict[str, object] = {}
    body = text
    m = MD_META_RE.match(text)
    if m:
        for line in m.group('meta').splitlines():
            line = line.strip()
            m2 = MD_FIELD_RE.match(line)
            if m2:
                meta[m2.group('key')] = m2.group('value')
        body = text[m.end():].lstrip()
    else:
        lines = text.splitlines()
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            if not line.strip():
                idx += 1
                break
            m2 = PEL_FIELD_RE.match(line)
            if not m2:
                break
            meta[m2.group('key').lower()] = m2.group('value')
            idx += 1
        if meta:
            body = '\n'.join(lines[idx:]).lstrip()
    return normalize_meta(meta, path.stem), clean_markdown_body(body)


def parse_rst_meta(lines: list[str], fallback_slug: str) -> tuple[dict[str, object], int]:
    meta: dict[str, object] = {}
    idx = 0
    if len(lines) >= 2 and set(lines[1].strip()) in ({'#'}, {'='}, {'-'}, {'~'}, {'*'}):
        meta['title'] = lines[0].strip()
        idx = 2
    while idx < len(lines):
        line = lines[idx]
        if not line.strip():
            idx += 1
            break
        m = RST_FIELD_RE.match(line)
        if not m:
            break
        meta[m.group('key')] = m.group('value')
        idx += 1
    return normalize_meta(meta, fallback_slug), idx


def convert_rst_body(body: str) -> str:
    parts = publish_parts(source=body, writer_name='html5')
    html = parts['html_body']
    text = md(html, heading_style='ATX')
    text = re.sub(r'(!\[[^\]]*\]\([^\)]+\))(?=[A-Za-z])', r'\1\n\n', text)
    return clean_markdown_body(text)


def write_page(path: Path, meta: dict[str, object], body: str, *, keep_slug: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front = {
        'title': meta['title'],
    }
    if keep_slug:
        front['slug'] = meta['slug']
    if meta.get('date'):
        front['date'] = meta['date']
    if meta.get('author'):
        front['author'] = meta['author']
    if meta.get('description'):
        front['description'] = meta['description']
    if meta.get('tags'):
        front['tags'] = meta['tags']
    text = '---\n' + yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip() + '\n---\n\n' + body.strip() + '\n'
    path.write_text(text)


def make_home_page() -> None:
    home = CONTENT_DIR / '_index.md'
    home.write_text('''---
title: Blind Not Dumb
type: home
---

Chris Patti on software, systems, accessibility, books, and the occasional well-deserved rant.
''')


def make_posts_index() -> None:
    posts_index = CONTENT_POSTS_DIR / '_index.md'
    posts_index.write_text('''---
title: Archive
---

A chronological list of posts from Blind Not Dumb.
''')


def main() -> None:
    if CONTENT_DIR.exists():
        shutil.rmtree(CONTENT_DIR)
    CONTENT_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    if IMAGES_DIR.exists():
        shutil.copytree(IMAGES_DIR, STATIC_IMAGES_DIR, dirs_exist_ok=True)

    about_written = False
    for path in sorted(POSTS_DIR.iterdir()):
        if not path.is_file():
            continue
        stem = slugify(path.stem)
        if stem in SKIP_SLUGS:
            continue
        if path.suffix == '.md':
            meta, body = parse_markdown(path)
        elif path.suffix == '.rst':
            lines = path.read_text().splitlines()
            meta, start = parse_rst_meta(lines, stem)
            body = convert_rst_body('\n'.join(lines[start:]).strip() + '\n')
        else:
            continue
        slug = slugify(str(meta.get('slug') or stem))
        meta['slug'] = slug
        if slug in ABOUT_SLUGS and not about_written:
            write_page(CONTENT_DIR / 'about' / 'index.md', meta, body, keep_slug=False)
            about_written = True
        else:
            write_page(CONTENT_POSTS_DIR / f'{slug}.md', meta, body)
    make_home_page()
    make_posts_index()


if __name__ == '__main__':
    main()
