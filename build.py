import markdown
from pathlib import Path
from jinja2 import Template

NOTES = Path("notes")
OUT = Path("dist")

TEMPLATE = Template("""
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
  </main>
</body>
</html>
""")

def build():
    OUT.mkdir(parents=True, exist_ok=True)

    for md_file in NOTES.rglob("*.md"):
        rel_path = md_file.relative_to(NOTES).with_suffix(".html")
        out_file = OUT / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)

        raw = md_file.read_text(encoding="utf-8")
        html = markdown.markdown(raw, extensions=["fenced_code", "tables"])
        page = TEMPLATE.render(title=md_file.stem.replace("-", " ").title(), content=html)

        out_file.write_text(page, encoding="utf-8")
        print(f"Built {rel_path}")

if __name__ == "__main__":
    build()
