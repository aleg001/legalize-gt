from pathlib import Path
import fitz

FIXTURES = Path("engine/tests/fixtures/gt")
OUT = Path("tmp/extracted/gt")
OUT.mkdir(parents=True, exist_ok=True)

for pdf_path in sorted(FIXTURES.glob("*.pdf")):
    doc = fitz.open(pdf_path)
    pages = []

    for page in doc:
        pages.append(page.get_text("text"))

    text = "\n\n".join(pages).strip()
    out_path = OUT / f"{pdf_path.stem}.txt"
    out_path.write_text(text, encoding="utf-8")

    print(f"{pdf_path.name}: {len(doc)} pages, {len(text)} chars -> {out_path}")
