#!/usr/bin/env python3
"""
Backbyrner blog preprocessor.

Reads Markdown files from  articles/*.md  and writes flat HTML into  blog/ :
  - blog/<slug>.html   one styled page per article
  - blog/index.html    the article list (title + date + ~100-word excerpt)

On GitHub Pages the deploy workflow runs this automatically -- pushing the .md
is the publish step -- so `blog/` is generated output and is git-ignored. You
can still run it locally to preview:

    python3 build.py

Markdown file format (front matter is optional):

    ---
    title: My First Post
    date: 2026-09-02
    ---

    The body, in **Markdown**.

If `title` is missing it falls back to the first `# Heading`, then the slug.
If `date` is missing it falls back to a `YYYY-MM-DD-` filename prefix, then the
file's modification date. The slug is the filename minus any date prefix.

Images: put them in  articles/assets/  and reference them from Markdown any way
you like -- `![x](assets/x.png)`, `![x](x.png)` and `![x](/articles/assets/x.png)`
all resolve to `/articles/assets/x.png` in the built page.

Dependency: markdown-it-py  (Arch: `sudo pacman -S python-markdown-it-py`)
"""

import html
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    from markdown_it import MarkdownIt
except ModuleNotFoundError:
    sys.exit(
        "build.py needs markdown-it-py.\n"
        "  Arch:  sudo pacman -S python-markdown-it-py\n"
        "  pip :  pip install --user markdown-it-py"
    )

ROOT = Path(__file__).resolve().parent
ARTICLES = ROOT / "articles"
BLOG = ROOT / "blog"
CSS = "/resources/css/style.css?v=4"
EXCERPT_WORDS = 100

md = (
    MarkdownIt("commonmark", {"html": True, "linkify": True, "typographer": True})
    .enable("table")
    .enable("strikethrough")
)

DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})[-_]?(.*)$")
FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LEADING_H1 = re.compile(r"^\s*#\s+(.+?)\s*\n+", re.DOTALL)
IMG_SRC = re.compile(r'(<img\b[^>]*?\bsrc=")([^"]*)(")', re.IGNORECASE)
ASSETS_URL = "/articles/assets/"


def fix_img_src(src):
    """Point every non-absolute image at articles/assets/."""
    if re.match(r"^(https?:)?//|^/|^data:|^mailto:", src, re.IGNORECASE):
        return src
    name = src[7:] if src.startswith("assets/") else src
    return ASSETS_URL + name.lstrip("./")


def page(title, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} &mdash; Backbyrner</title>
<link href="https://fonts.googleapis.com/css?family=Fugaz+One|Rock+Salt|Montserrat" rel="stylesheet">
<link href="{CSS}" rel="stylesheet" type="text/css">
</head>
<body>
<div class="blogTop">
<h1 class="blogTitle"><a href="/">Backbyrner</a></h1>
<span class="mainNavMenu"><a href="/blog/">blog</a> | about | <a href="/links">links</a></span>
</div>
<div class="blogWrap">
{body}
</div>
</body>
</html>
"""


def parse(path):
    raw = path.read_text(encoding="utf-8")
    meta = {}
    m = FRONT_MATTER.match(raw)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip().lower()] = v.strip()
        raw = raw[m.end():]

    stem = path.stem
    dm = DATE_PREFIX.match(stem)
    slug = (dm.group(2) if dm else stem) or stem
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", slug).strip("-").lower()

    title = meta.get("title")
    if not title:
        hm = LEADING_H1.match(raw)
        if hm:
            title = hm.group(1).strip()
    if not title:
        title = slug.replace("-", " ").title()

    # Don't render the title twice: drop a leading H1 from the body.
    raw = LEADING_H1.sub("", raw, count=1)

    when = meta.get("date")
    if not when and dm:
        when = dm.group(1)
    if when:
        try:
            when = datetime.strptime(when[:10], "%Y-%m-%d").date()
        except ValueError:
            when = None
    if not when:
        when = date.fromtimestamp(path.stat().st_mtime)

    return {"slug": slug, "title": title, "date": when, "body": raw}


def excerpt(rendered_html):
    text = re.sub(r"<[^>]+>", " ", rendered_html)
    text = html.unescape(text)
    words = text.split()
    if len(words) <= EXCERPT_WORDS:
        return " ".join(words)
    return " ".join(words[:EXCERPT_WORDS]) + "…"


def build():
    if not ARTICLES.is_dir():
        sys.exit(f"no articles directory at {ARTICLES}")
    BLOG.mkdir(exist_ok=True)

    posts = [parse(p) for p in sorted(ARTICLES.glob("*.md"))]
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)

    seen = set()
    for post in posts:
        if post["slug"] in seen:
            sys.exit(f"duplicate slug: {post['slug']}")
        seen.add(post["slug"])

        rendered = md.render(post["body"])
        rendered = IMG_SRC.sub(
            lambda m: m.group(1) + fix_img_src(m.group(2)) + m.group(3), rendered
        )
        post["excerpt"] = excerpt(rendered)
        article = (
            f'<article class="articleBody">\n'
            f'<h1>{html.escape(post["title"])}</h1>\n'
            f'<div class="articleMeta">{post["date"]:%B %-d, %Y}</div>\n'
            f'{rendered}\n'
            f'<div><a class="backLink" href="/blog/">&larr; all articles</a></div>\n'
            f'</article>\n'
        )
        out = BLOG / f'{post["slug"]}.html'
        out.write_text(page(post["title"], article), encoding="utf-8")
        print(f'  blog/{post["slug"]}.html')

    items = []
    for post in posts:
        items.append(
            '<li>\n'
            f'<div class="entryTitle"><a href="/blog/{post["slug"]}.html">'
            f'{html.escape(post["title"])}</a>'
            f'<span class="entryDate">{post["date"]:%B %-d, %Y}</span></div>\n'
            f'<p class="entryExcerpt">{html.escape(post["excerpt"])}</p>\n'
            '</li>'
        )
    body = (
        '<div class="blogPanel">\n'
        '<h2 class="blogPanelHead">Articles</h2>\n'
        + (f'<ul class="articleList">\n{chr(10).join(items)}\n</ul>\n'
           if items else '<p>Nothing here yet.</p>\n')
        + '</div>\n'
    )
    (BLOG / "index.html").write_text(page("Blog", body), encoding="utf-8")
    print("  blog/index.html")

    # Drop generated pages whose source .md is gone.
    keep = {"index.html"} | {f'{p["slug"]}.html' for p in posts}
    for stale in BLOG.glob("*.html"):
        if stale.name not in keep:
            stale.unlink()
            print(f"  removed blog/{stale.name}")

    print(f"built {len(posts)} article(s)")


if __name__ == "__main__":
    build()
