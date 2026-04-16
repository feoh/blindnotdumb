#!/home/feoh/.openclaw/workspace/.venv/bin/python
from __future__ import annotations

import html
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'content' / 'posts'
PUBLIC = ROOT / 'public'
BASE = 'https://www.feoh.org/'
SITE_TITLE = 'Blind Not Dumb'
SITE_DESC = 'Chris Patti on software, systems, accessibility, books, and the occasional well-deserved rant.'


def parse_post(path: Path):
    text = path.read_text()
    if not text.startswith('---\n'):
        return None
    _, fm, body = text.split('---\n', 2)
    meta = yaml.safe_load(fm) or {}
    slug = meta.get('slug') or path.stem
    date_raw = meta.get('date')
    if not date_raw:
        return None
    dt = datetime.fromisoformat(str(date_raw).replace('Z', '+00:00'))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    summary = body.strip().split('\n\n', 1)[0].strip()
    return {
        'title': str(meta.get('title') or slug),
        'url': f'{BASE}posts/{slug}/',
        'date': dt,
        'summary': summary,
        'body': body.strip(),
    }


def main() -> None:
    posts = []
    for path in CONTENT.glob('*.md'):
        post = parse_post(path)
        if post:
            posts.append(post)
    posts.sort(key=lambda p: p['date'], reverse=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    updated = posts[0]['date'].isoformat() if posts else datetime.now(timezone.utc).isoformat()
    atom = [
        '<?xml version="1.0" encoding="utf-8" standalone="yes"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        f'  <title>{html.escape(SITE_TITLE)}</title>',
        f'  <id>{BASE}</id>',
        f'  <updated>{updated}</updated>',
        f'  <link href="{BASE}feed.atom" rel="self" />',
        f'  <link href="{BASE}" rel="alternate" />',
        f'  <subtitle>{html.escape(SITE_DESC)}</subtitle>',
    ]
    for post in posts[:20]:
        atom.extend([
            '  <entry>',
            f'    <title>{html.escape(post["title"])}</title>',
            f'    <link href="{post["url"]}" />',
            f'    <id>{post["url"]}</id>',
            f'    <updated>{post["date"].isoformat()}</updated>',
            f'    <published>{post["date"].isoformat()}</published>',
            f'    <summary>{html.escape(post["summary"])}</summary>',
            f'    <content type="html">{html.escape(post["body"])}</content>',
            '  </entry>',
        ])
    atom.append('</feed>')
    out = PUBLIC / 'feed.atom'
    out.write_text('\n'.join(atom) + '\n')
    print(f'wrote {out}')


if __name__ == '__main__':
    main()
