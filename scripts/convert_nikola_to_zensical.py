#!/home/feoh/.openclaw/workspace/.venv/bin/python
from __future__ import annotations

import re
import shutil
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

import yaml
from docutils.core import publish_parts
from markdownify import markdownify as md

ROOT = Path('/home/feoh/.openclaw/workspace/blindnotdumb')
POSTS_DIR = ROOT / 'posts'
DOCS_DIR = ROOT / 'docs'
DOCS_POSTS_DIR = DOCS_DIR / 'posts'
DOCS_IMAGES_DIR = DOCS_DIR / 'images'
IMAGES_DIR = ROOT / 'images'

MD_META_RE = re.compile(r"^<!--\n(?P<meta>.*?)\n-->\n*", re.S)
MD_FIELD_RE = re.compile(r"^\.\.\s+(?P<key>[a-z_]+):\s*(?P<value>.*)$")
PEL_FIELD_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_]*):\s*(?P<value>.*)$")
RST_FIELD_RE = re.compile(r"^:(?P<key>[a-z_]+):\s*(?P<value>.*)$")

SKIP_SLUGS = {'article_template'}
ABOUT_SLUGS = {'about', 'about-2'}


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


def clean_markdown_body(text: str) -> str:
    text = text.replace('```winget install git```', '`winget install git`')
    text = re.sub(r'!\[/images/([^\]]+)\]\(/images/[^)]+\)', lambda m: f'![{Path(m.group(1)).stem.replace("_", " ")}](/images/{m.group(1)})', text)
    text = re.sub(r'<iframe[^>]*src="([^"]+)"[^>]*></iframe>', r'Embedded post: <\1>', text)
    text = re.sub(r'##\s+(.+?)\s+##', r'## \1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


def clean_value(value: str):
    value = value.strip()
    return value if value else None


def normalize_date(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    value = re.sub(r'^0(\d{4}-)', r'\1', value)
    return value or None


def normalize_meta(meta: dict[str, object], fallback_slug: str) -> dict[str, object]:
    title = normalize_title(str(meta.get('title') or fallback_slug.replace('-', ' ').title()))
    slug = clean_value(str(meta.get('slug') or fallback_slug)) or fallback_slug
    raw_tags = clean_value(str(meta.get('tags') or ''))
    tags = list(dict.fromkeys(t.strip() for t in raw_tags.split(',') if t.strip())) if raw_tags else []
    date = normalize_date(clean_value(str(meta.get('date') or '')))
    description = clean_value(str(meta.get('description') or '')) or clean_value(str(meta.get('summary') or ''))
    author = clean_value(str(meta.get('author') or meta.get('authors') or ''))
    return {
        'title': title,
        'slug': slug,
        'tags': tags,
        'date': date,
        'description': description,
        'author': author,
    }


def parse_markdown(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text()
    meta = {}
    m = MD_META_RE.match(text)
    body = text
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
            line = lines[idx].rstrip('\n')
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
    meta = {}
    idx = 0
    # Title block
    if len(lines) >= 2 and set(lines[1].strip()) in ({'#'}, {'='}, {'-'}, {'~'}, {'*'}):
        meta['title'] = lines[0].strip()
        idx = 2
    while idx < len(lines):
        line = lines[idx].rstrip('\n')
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


def write_markdown(path: Path, meta: dict[str, object], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front = {
        'title': meta['title'],
        'slug': meta['slug'],
    }
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


def display_date(value: str | None) -> str:
    if not value:
        return ''
    value = value.strip().replace(' UTC-05:00', '-0500').replace(' UTC-04:00', '-0400')
    for fmt in ('%Y-%m-%d %H:%M:%S %z', '%Y-%m-%d %H:%M:%S%z', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'):
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime('%Y-%m-%d')
        except Exception:
            pass
    return value[:10] if re.match(r'^\d{4}-\d{2}-\d{2}', value) else value


def render_index(posts: list[dict[str, object]]) -> str:
    lines = [
        '---',
        'title: Blind Not Dumb',
        'hide:',
        '  - navigation',
        '---',
        '',
        '# Blind Not Dumb',
        '',
        'Chris Patti on software, systems, accessibility, books, and the occasional well-deserved rant.',
        '',
        'Originally built in Nikola, this branch is a Zensical migration using the default theme and a simplified structure.',
        '',
        '## Start here',
        '',
        '- [About](about.md)',
        '- [Archive](archive.md)',
        '',
        '## Recent posts',
        '',
    ]
    for post in posts[:15]:
        title = post['title']
        slug = post['slug']
        date = display_date(post.get('date'))
        suffix = f' ({date})' if date else ''
        lines.append(f'- [{title}](posts/{slug}.md){suffix}')
    lines += ['', 'If you want the full back catalog, head to the [archive](archive.md).', '']
    return '\n'.join(lines)


def render_archive(posts: list[dict[str, object]]) -> str:
    lines = ['---', 'title: Archive', '---', '', '# Archive', '', 'A chronological list of migrated posts from the original Nikola site.', '']
    current_year = None
    for post in posts:
        title = post['title']
        slug = post['slug']
        date = display_date(post.get('date'))
        year = date[:4] if date else 'Undated'
        tags = post.get('tags') or []
        if year != current_year:
            if current_year is not None:
                lines.append('')
            lines.extend([f'## {year}', ''])
            current_year = year
        suffix = f' ({date})' if date else ''
        lines.append(f'- [{title}](posts/{slug}.md){suffix}')
        if tags:
            lines.append(f'  - Tags: {", ".join(tags)}')
    lines.append('')
    return '\n'.join(lines)


def sort_posts(posts: list[dict[str, object]]) -> list[dict[str, object]]:
    def key(post: dict[str, object]):
        raw = str(post.get('date') or '').strip()
        if not raw:
            return ('', '')
        normalized = raw.replace(' UTC-05:00', '-0500').replace(' UTC-04:00', '-0400')
        for fmt in ('%Y-%m-%d %H:%M:%S %z', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'):
            try:
                dt = datetime.strptime(normalized, fmt)
                return ('1', dt.strftime('%Y-%m-%dT%H:%M:%S%z'))
            except Exception:
                pass
        return ('1', raw)
    return sorted(posts, key=key, reverse=True)


def ensure_image_aliases() -> None:
    if not DOCS_IMAGES_DIR.exists():
        return
    by_lower = {p.name.lower(): p for p in DOCS_IMAGES_DIR.iterdir() if p.is_file()}
    for md_file in DOCS_DIR.rglob('*.md'):
        text = md_file.read_text(errors='ignore')
        for ref in re.findall(r'\((/images/[^)]+)\)', text):
            target = DOCS_IMAGES_DIR / Path(ref).name
            if target.exists():
                continue
            source = by_lower.get(target.name.lower())
            if source and source.exists():
                shutil.copy2(source, target)


def main() -> None:
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    if IMAGES_DIR.exists():
        shutil.copytree(IMAGES_DIR, DOCS_IMAGES_DIR, dirs_exist_ok=True)

    posts: list[dict[str, object]] = []
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
        entry = dict(meta)

        out_path = DOCS_POSTS_DIR / f'{slug}.md'
        if slug in ABOUT_SLUGS and not about_written:
            out_path = DOCS_DIR / 'about.md'
            meta['title'] = meta.get('title') or 'About'
            about_written = True
        write_markdown(out_path, meta, body)
        if out_path.name != 'about.md':
            posts.append(entry)

    posts = sort_posts(posts)
    (DOCS_DIR / 'index.md').write_text(render_index(posts))
    (DOCS_DIR / 'archive.md').write_text(render_archive(posts))

    if not about_written:
        (DOCS_DIR / 'about.md').write_text('---\ntitle: About\n---\n\n# About\n\nComing soon.\n')

    ensure_image_aliases()


if __name__ == '__main__':
    main()
