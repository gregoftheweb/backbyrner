# Blogging

The blog is flat HTML generated from Markdown. There is no framework and no
database.

## Publish a post

1. Add a file to `articles/`, named `YYYY-MM-DD-some-slug.md`:

   ```markdown
   ---
   title: The Title
   date: 2026-09-02
   ---

   The body, in Markdown.
   ```

   Front matter is optional. Without `title` it uses the first `# Heading` or
   the slug; without `date` it uses the filename's date prefix or the file date.

2. Images go in `articles/assets/`. Reference them as `![alt](assets/pic.png)`.

3. Commit and push:

   ```sh
   git add articles
   git commit -m "post: the title"
   git push
   ```

That's it. The **Deploy site** GitHub Action runs `build.py` and publishes the
site. The post appears at `https://backbyrner.com/blog/<slug>.html` and in the
list at `/blog/`.

## Preview locally (optional)

```sh
python3 build.py            # writes blog/ (git-ignored)
python3 -m http.server 8000 # then open http://localhost:8000/blog/
```

`build.py` needs `markdown-it-py` (`sudo pacman -S python-markdown-it-py`).

## Links page

`/links/` is generated from `links.xml`. Add a link inside a `<category>`:

```xml
<link url="https://example.com">Label</link>
```

Categories and links render in document order. Commit, push, done.

## What generates what

| Source | Output |
|---|---|
| `articles/*.md` | `blog/<slug>.html`, one per post |
| all posts | `blog/index.html`, the list with 100-word excerpts |
| `links.xml` | `links/index.html`, one card per category |
| `build.py` | the generator; templates live inside it |
| `.github/workflows/deploy.yml` | runs the build and deploys on every push |
