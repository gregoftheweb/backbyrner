---
title: Hello, Backbyrner
date: 2026-09-02
---

This is the first post on the rebuilt Backbyrner. The whole blog is flat HTML —
no framework, no database, no server-side anything.

## How it works

Write a Markdown file in `articles/`, run `python3 build.py`, and commit the
result. The build script turns each `.md` into a styled page under `blog/` and
regenerates `blog/index.html` with the title, date, and first hundred words of
every article, newest first.

That is the entire engine. If GitHub Pages is serving the site, pushing the
commit is the publish step.

## Images

Drop image files in `articles/assets/` and link them from the post:

![a sample banner](assets/sample-banner.png)

## Formatting

Normal Markdown works: **bold**, *italic*, [links](https://grok.com/), lists,

- like
- this

and fenced code blocks:

```
python3 build.py
git add articles blog
git commit -m "new post"
git push
```

That's it.
