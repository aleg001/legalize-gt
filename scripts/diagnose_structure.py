from pathlib import Path
import re
import unicodedata

BASE = Path("tmp/extracted/gt")

SOURCE_STEMS = {
    "sample-budget-law",
    "sample-civic-service",
    "sample-code-codigo-municipal",
    "sample-constitution",
    "sample-ordinary-law-laip-official",
    "reform-decree-13-2013",
}


def normalize_for_matching(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.lower()


PATTERNS = {
    "article_headings": re.compile(
        r"^\s*(articulo|art\.)\s+\d+[a-zA-Z]*\s*(bis|ter|quater|quáter)?[\.\-\*º°]*",
        re.IGNORECASE,
    ),
    "title_headings": re.compile(
        r"^\s*titulo\s+([ivxlcdm]+|primero|segundo|tercero|cuarto|quinto|sexto|septimo|octavo|noveno|decimo|\d+)",
        re.IGNORECASE,
    ),
    "chapter_headings": re.compile(
        r"^\s*capitulo\s+([ivxlcdm]+|unico|primero|segundo|tercero|cuarto|quinto|sexto|septimo|octavo|noveno|decimo|\d+)",
        re.IGNORECASE,
    ),
    "reform_notes": re.compile(
        r"\b(reformado|reformada|reformadas|adicionado|adicionada|adicionadas|derogado|derogada|derogadas)\b",
        re.IGNORECASE,
    ),
    "mojibake": re.compile(r"(Ã|�|â)"),
}


for path in sorted(BASE.glob("*.txt")):
    # Skip intermediate/generated research files.
    # Only diagnose source texts extracted directly from PDF fixtures.
    if path.stem not in SOURCE_STEMS:
        continue

    original_text = path.read_text(encoding="utf-8", errors="replace")
    lines = original_text.splitlines()
    normalized_lines = [normalize_for_matching(line) for line in lines]

    counts = {key: 0 for key in PATTERNS}
    examples = {key: [] for key in PATTERNS}

    for original, normalized in zip(lines, normalized_lines):
        for key, pattern in PATTERNS.items():
            target = original if key == "mojibake" else normalized

            if pattern.search(target):
                counts[key] += 1

                if len(examples[key]) < 5:
                    examples[key].append(original.strip())

    print(f"---- {path.name} ----")

    for key, count in counts.items():
        print(f"{key}: {count}")

    print("examples:")

    for key, sample_lines in examples.items():
        if sample_lines:
            print(f"  {key}:")
            for sample in sample_lines:
                print(f"    - {sample[:180]}")

    print()
