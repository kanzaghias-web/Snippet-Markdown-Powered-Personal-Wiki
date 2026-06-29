import markdown
from pathlib import Path
from jinja2 import Template

NOTES = Path("notes")
OUT = Path("dist")

PAGE_TEMPLATE = Template("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
</head>
<body>
  <main>
    <h1>{{ title }}</h1>
    {{ content | safe }}
    <p><a href="index.html">Back to home</a></p>
  </main>
</body>
</html>
""")

INDEX_TEMPLATE = Template("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Snippet</title>
</head>
<body>
  <main>
    <h1>Snippet</h1>
    <p>A personal wiki generated from Markdown notes.</p>
    <ul>
      {% for note in notes %}
      <li><a href="{{ note.href }}">{{ note.title }}</a></li>
      {% endfor %}
    </ul>
  </main>
</body>
</html>
""")

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    notes = []

    for md_file in NOTES.rglob("*.md"):
        rel_path = md_file.relative_to(NOTES).with_suffix(".html")
        out_file = OUT / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)

        raw = md_file.read_text(encoding="utf-8")
        html = markdown.markdown(raw, extensions=["fenced_code", "tables"])
        title = md_file.stem.replace("-", " ").title()

        page = PAGE_TEMPLATE.render(title=title, content=html)
        out_file.write_text(page, encoding="utf-8")

        notes.append({
            "title": title,
            "href": rel_path.as_posix()
        })

        print(f"Built {rel_path}")

    index_html = INDEX_TEMPLATE.render(notes=sorted(notes, key=lambda x: x["title"].lower()))
    (OUT / "index.html").write_text(index_html, encoding="utf-8")
    print("Built index.html")

if __name__ == "__main__":
    build()
