from pathlib import Path
import re
import unicodedata

INPUT = Path("tmp/extracted/gt/reform-decree-13-2013.txt")
OUT = Path("tmp/extracted/gt/reform-operations-13-2013.txt")


def normalize_for_matching(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.lower()


text = INPUT.read_text(encoding="utf-8", errors="replace")
lines = text.splitlines()

# Only split on decree-level article headers, not on lowercase references
# such as "artículo 8 del Decreto..."
#
# Handles:
#   ARTÍCULO 1.
#   . ARTÍCULO 1.
#   · ARTÍCULO 5.
#   ARTICULO 32.
article_header = re.compile(
    r"^\s*[\.\·\-\–\—_]*\s*ART[ÍI]CULO\s+(\d+)\s*[\.\-·:]",
    re.IGNORECASE,
)

chunks = []
current = None

for line in lines:
    if article_header.search(line):
        if current:
            chunks.append(current)
        current = [line]
    elif current:
        current.append(line)

if current:
    chunks.append(current)

operation_patterns = [
    ("reforma", re.compile(r"\bse\s+reforma(?:n)?\b", re.IGNORECASE)),
    ("adiciona", re.compile(r"\bse\s+adiciona(?:n)?\b", re.IGNORECASE)),
    ("deroga", re.compile(r"\bse\s+deroga(?:n)?\b", re.IGNORECASE)),
]

# Target extraction should focus on the opening sentence before "el cual queda así"
# or before the first quoted replacement body.


def opening_segment(body: str) -> str:
    normalized = normalize_for_matching(body)
    idx = normalized.find("el cual queda asi")
    if idx != -1:
        return body[:idx]
    quote_idx = body.find('"')
    if quote_idx != -1:
        return body[:quote_idx]
    return body[:800]


target_patterns = [
    re.compile(
        r"(?:el|al|del)\s+art[íi]culo[_\s]+([0-9]+(?:\s*(?:Bis|Ter|Qu[aá]ter|Quater))?)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:el|al|del)\s+articulo[_\s]+([0-9]+(?:\s*(?:Bis|Ter|Quater|Qu[aá]ter))?)",
        re.IGNORECASE,
    ),
    re.compile(
        r"art[íi]culo[_\s]+([0-9]+(?:\s*(?:Bis|Ter|Qu[aá]ter|Quater))?)\s+al\s+Decreto",
        re.IGNORECASE,
    ),
    re.compile(
        r"articulo[_\s]+([0-9]+(?:\s*(?:Bis|Ter|Quater|Qu[aá]ter))?)\s+al\s+Decreto",
        re.IGNORECASE,
    ),
]


def normalize_target(value: str) -> str:
    value = " ".join(value.split())
    parts = value.split()
    if len(parts) == 1:
        return parts[0]
    return parts[0] + " " + parts[1].capitalize()


results = []

for chunk in chunks:
    header = chunk[0].strip()
    body = "\n".join(chunk)
    normalized = normalize_for_matching(body)
    segment = opening_segment(body)

    decree_article_match = article_header.search(header)
    decree_article = decree_article_match.group(
        1) if decree_article_match else "unknown"

    operation = "unknown"
    for op_name, op_regex in operation_patterns:
        if op_regex.search(segment):
            operation = op_name
            break

    targets = []
    for pattern in target_patterns:
        for match in pattern.finditer(segment):
            value = normalize_target(match.group(1))
            if value not in targets:
                targets.append(value)

    has_replacement = "queda asi" in normalized or "queda así" in body.lower()

    affects_101_97 = bool(
        re.search(r"101[\-·\s]*97", segment)
        or re.search(r"101[\-·\s]*97", body[:1200])
    )

    if not affects_101_97:
        continue

    results.append({
        "decree_article": decree_article,
        "header": header,
        "operation": operation,
        "targets": targets,
        "has_replacement": has_replacement,
        "preview": " ".join(body.split())[:600],
    })

lines_out = []
for item in results:
    lines_out.append(f"DECREE_ARTICLE: {item['decree_article']}")
    lines_out.append(f"HEADER: {item['header']}")
    lines_out.append(f"OPERATION: {item['operation']}")
    lines_out.append(
        f"TARGETS: {', '.join(item['targets']) if item['targets'] else 'TBD'}")
    lines_out.append(f"HAS_REPLACEMENT: {item['has_replacement']}")
    lines_out.append(f"PREVIEW: {item['preview']}")
    lines_out.append("")

OUT.write_text("\n".join(lines_out), encoding="utf-8")
print(f"Extracted {len(results)} operation chunks -> {OUT}")
