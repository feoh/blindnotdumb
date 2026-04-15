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
DOCS_TAGS_DIR = DOCS_DIR / 'tags'
DOCS_IMAGES_DIR = DOCS_DIR / 'images'
DOCS_STYLES_DIR = DOCS_DIR / 'stylesheets'
IMAGES_DIR = ROOT / 'images'

MD_META_RE = re.compile(r"^<!--\n(?P<meta>.*?)\n-->\n*", re.S)
MD_FIELD_RE = re.compile(r"^\.\.\s+(?P<key>[a-z_]+):\s*(?P<value>.*)$")
PEL_FIELD_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_]*):\s*(?P<value>.*)$")
RST_FIELD_RE = re.compile(r"^:(?P<key>[a-z_]+):\s*(?P<value>.*)$")

SKIP_SLUGS = {'article_template'}
ABOUT_SLUGS = {'about', 'about-2'}

EXTRA_CSS = """.frontpage-hero {
  display: grid;
  grid-template-columns: 128px 1fr;
  gap: 1.5rem;
  align-items: center;
  margin: 1rem 0 2.5rem;
  padding: 1.25rem 0 1.75rem;
  border-bottom: 1px solid var(--md-default-fg-color--lightest);
}

.frontpage-avatar {
  width: 128px;
  height: 128px;
  border-radius: 18px;
  object-fit: cover;
  box-shadow: 0 0 0 4px rgba(86, 112, 212, 0.15);
}

.frontpage-title {
  margin: 0 0 0.35rem;
}

.frontpage-dek {
  font-size: 1.05rem;
  line-height: 1.6;
  margin: 0 0 0.85rem;
  max-width: 44rem;
}

.frontpage-links a {
  margin-right: 1rem;
  font-weight: 600;
}

.frontpage-featured {
  margin: 0 0 2.75rem;
  padding: 0 0 2.25rem;
  border-bottom: 1px solid var(--md-default-fg-color--lightest);
}

.frontpage-featured .featured-label {
  color: var(--md-default-fg-color--light);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.frontpage-featured h2 {
  margin-bottom: 0.4rem;
}

.frontpage-featured .featured-excerpt {
  font-size: 1rem;
  line-height: 1.7;
  max-width: 48rem;
}

.post-preview {
  margin: 0 0 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--md-default-fg-color--lightest);
}

.post-preview h3 {
  margin-bottom: 0.35rem;
}

.post-preview-date {
  color: var(--md-default-fg-color--light);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.8rem;
}

.post-preview-tags {
  margin-top: 0.85rem;
}

.post-preview-tags .md-tag {
  margin-right: 0.35rem;
  margin-bottom: 0.35rem;
}

@media (max-width: 720px) {
  .frontpage-hero {
    grid-template-columns: 1fr;
  }
}
"""


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


def strip_markdown(text: str) -> str:
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'^[#>*\-\s]+', '', text, flags=re.M)
    text = re.sub(r'[_*~]+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def make_excerpt(meta: dict[str, object], body: str, max_len: int = 420) -> str:
    if meta.get('description'):
        return str(meta['description'])
    blocks = [strip_markdown(block) for block in re.split(r'\n\s*\n', body) if block.strip()]
    for block in blocks:
        if not block or block.startswith('Embedded post:'):
            continue
        if len(block) < 60:
            continue
        return block[: max_len - 1].rstrip() + ('…' if len(block) > max_len else '')
    for block in blocks:
        if block and not block.startswith('Embedded post:'):
            return block[: max_len - 1].rstrip() + ('…' if len(block) > max_len else '')
    return ''


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
    featured = posts[0] if posts else None
    recent = posts[1:10] if len(posts) > 1 else []
    lines = [
        '---',
        'title: Blind Not Dumb',
        'template: blog_index.html',
        'hide:',
        '  - navigation',
        '  - toc',
        '---',
        '',
        '<div class="frontpage-hero">',
        '  <img src="/images/profile_pic.jpg" alt="Chris Patti" class="frontpage-avatar">',
        '  <div>',
        '    <h1 class="frontpage-title">Blind Not Dumb</h1>',
        '    <p class="frontpage-dek">Chris Patti writes about software, systems, accessibility, books, platform work, and the occasional well-deserved rant.</p>',
        '    <p class="frontpage-links"><a href="about/">About</a> <a href="archive/">Archive</a></p>',
        '  </div>',
        '</div>',
        '',
    ]
    if featured:
        title = featured['title']
        slug = featured['slug']
        date = display_date(featured.get('date'))
        excerpt = featured.get('excerpt') or ''
        tags = featured.get('tags') or []
        lines.extend([
            '<section class="frontpage-featured">',
            '<p class="featured-label">Latest post</p>',
            f'<h2><a href="posts/{slug}/">{title}</a></h2>',
            f'<p class="post-preview-date">{date}</p>' if date else '',
            f'<p class="featured-excerpt">{excerpt}</p>' if excerpt else '',
            f'<p><a href="posts/{slug}/">Keep reading</a></p>',
        ])
        if tags:
            lines.append('<p class="post-preview-tags">' + ' '.join(f'<a class="md-tag" href="tags/{slugify(tag)}/">{tag}</a>' for tag in tags) + '</p>')
        lines.extend(['</section>', '', '## Recent posts', ''])

    for post in recent:
        title = post['title']
        slug = post['slug']
        date = display_date(post.get('date'))
        excerpt = post.get('excerpt') or ''
        tags = post.get('tags') or []
        suffix = f' ({date})' if date else ''
        lines.extend([
            '<article class="post-preview">',
            f'<h3><a href="posts/{slug}/">{title}</a></h3>',
            f'<p class="post-preview-date">{date}</p>' if date else '',
            f'<p>{excerpt}</p>' if excerpt else '',
            f'<p><a href="posts/{slug}/">Read more</a></p>',
        ])
        if tags:
            lines.append('<p class="post-preview-tags">' + ' '.join(f'<a class="md-tag" href="tags/{slugify(tag)}/">{tag}</a>' for tag in tags) + '</p>')
        lines.extend(['</article>', ''])
    lines += ['Browse the full back catalog in the [archive](archive.md).', '']
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
            lines.append('  - Tags: ' + ', '.join(f'[{tag}](../tags/{slugify(tag)}/)' for tag in tags))
    lines.append('')
    return '\n'.join(lines)


def render_tag_page(tag: str, posts: list[dict[str, object]]) -> str:
    lines = [
        '---',
        f'title: Tag: {tag}',
        'hide:',
        '  - toc',
        '---',
        '',
        f'# Tag: {tag}',
        '',
        f'Posts filed under **{tag}**.',
        '',
        '[Back to archive](../archive.md)',
        '',
    ]
    for post in posts:
        title = post['title']
        slug = post['slug']
        date = display_date(post.get('date'))
        excerpt = post.get('excerpt') or ''
        suffix = f' ({date})' if date else ''
        lines.extend([
            f'## [{title}](../posts/{slug}/){suffix}',
            '',
            excerpt,
            '',
        ])
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


def write_support_files() -> None:
    DOCS_STYLES_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_STYLES_DIR / 'extra.css').write_text(EXTRA_CSS)


def main() -> None:
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    if IMAGES_DIR.exists():
        shutil.copytree(IMAGES_DIR, DOCS_IMAGES_DIR, dirs_exist_ok=True)
    DOCS_TAGS_DIR.mkdir(parents=True, exist_ok=True)

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
        entry['excerpt'] = make_excerpt(meta, body)

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

    tags: dict[str, list[dict[str, object]]] = {}
    for post in posts:
        for tag in post.get('tags') or []:
            tags.setdefault(tag, []).append(post)
    for tag, tagged_posts in sorted(tags.items(), key=lambda item: item[0].lower()):
        (DOCS_TAGS_DIR / f'{slugify(tag)}.md').write_text(render_tag_page(tag, tagged_posts))

    if not about_written:
        (DOCS_DIR / 'about.md').write_text('---\ntitle: About\n---\n\n# About\n\nComing soon.\n')

    write_support_files()
    ensure_image_aliases()


if __name__ == '__main__':
    main()
