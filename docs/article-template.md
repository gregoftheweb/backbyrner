---
title: Your Post Title
date: 2026-09-04
author: Greg Byrne
---

Open with a sentence or two that stands on its own — the blog index shows the
first ~100 words as the excerpt, so make them count.

## A section heading

Body copy in plain Markdown. **Bold**, *italic*, ~~strikethrough~~, and
`inline code` all work. Links auto-linkify: https://backbyrner.com

- Bullet lists
- work fine

1. So do
2. numbered lists

> Block quotes render too.

```
Fenced code blocks are fine.
```

| Tables | Also |
|--------|------|
| work   | yes  |

![alt text](assets/picture.jpg)

---

## How to use this file

1. Copy it to `articles/` and rename to `YYYY-MM-DD-some-slug.md`.
   The slug (filename minus the date prefix) becomes the URL:
   `2026-09-04-my-post.md` → `/blog/my-post.html`.
2. Edit the front matter:
   - `title` — optional. Falls back to the first `# Heading`, then the slug.
   - `date` — optional. Falls back to the `YYYY-MM-DD-` filename prefix, then
     the file's modification date.
   - `author` — optional. Shown next to the date; omit the line to hide it.
3. Put any images in `articles/assets/` and reference them as
   `![alt](assets/name.jpg)`.
4. Publish:
   ```sh
   git add articles
   git commit -m "post: your post title"
   git push
   ```
   The Deploy site Action runs `build.py` and publishes. Saving locally alone
   does nothing.

Preview before pushing (optional):
```sh
python3 build.py
python3 -m http.server 8000   # open http://localhost:8000/blog/
```
