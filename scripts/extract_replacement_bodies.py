from pathlib import Path
import re
import unicodedata

INPUT = Path("tmp/extracted/gt/reform-decree-13-2013.txt")
OUT = Path("tmp/extracted/gt/replacement-bodies-13-2013.txt")


def normalize_for_matching(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.lower()


text = INPUT.read_text(encoding="utf-8", errors="replace")
lines = text.splitlines()

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


def affects_budget_law(body: str) -> bool:
    return bool(re.search(r"101[\-·\s]*97", body[:1200]))


def clean_replacement(text: str) -> str:
    lines = text.splitlines()
    cleaned_lines = []

    skip_patterns = [
        r"^\s*Congreso de la República de Guatemala, Departamento de Información Legislativa\.?\s*$",
        r"^\s*N[ÚU]MERO\s*\d+.*$",
        r"^\s*DIARIO\s+de\s+CENTRO\s+AM[ÉE]RICA\s*$",
        r"^\s*Guatemala,\s+(LUNES|MARTES|MI[ÉE]RCOLES|JUEVES|VIERNES|S[ÁA]BADO|DOMINGO).*$",
        r"^\s*\d+\s*$",
        r"^\s*/\s*$",
        r"^\s*/~\s*$",
        r"^\s*\.\s*$",
        r"^\s*N[ÚU]MER[O0]?\s*\d+\s*$",
    ]

    for line in lines:
        stripped = line.strip()

        if not stripped:
            cleaned_lines.append("")
            continue

        should_skip = any(re.search(pattern, stripped, flags=re.IGNORECASE)
                          for pattern in skip_patterns)
        if should_skip:
            continue

        cleaned_lines.append(stripped)

    cleaned = "\n".join(cleaned_lines)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def extract_replacement(body: str) -> str | None:
    normalized = normalize_for_matching(body)
    marker = "el cual queda asi"
    idx = normalized.find(marker)

    if idx == -1:
        return None

    # Map normalized index approximately back to original.
    # Since normalization may remove accents but does not greatly change length
    # for this marker, start from the first colon after the phrase.
    original_after = body[idx:]
    colon_idx = original_after.find(":")
    if colon_idx == -1:
        return None

    replacement = original_after[colon_idx + 1:]

    # Trim leading quote-like noise.
    replacement = replacement.lstrip(' ."“”qQ·')

    return clean_replacement(replacement)


results = []

for chunk in chunks:
    header = chunk[0].strip()
    body = "\n".join(chunk)

    if not affects_budget_law(body):
        continue

    replacement = extract_replacement(body)
    if not replacement:
        continue

    decree_article_match = article_header.search(header)
    decree_article = decree_article_match.group(
        1) if decree_article_match else "unknown"

    results.append((decree_article, header, replacement))

out_lines = []

for decree_article, header, replacement in results:
    out_lines.append("=" * 80)
    out_lines.append(f"DECREE_ARTICLE: {decree_article}")
    out_lines.append(f"HEADER: {header}")
    out_lines.append("REPLACEMENT_PREVIEW:")
    out_lines.append(replacement[:1200])
    out_lines.append("")

OUT.write_text("\n".join(out_lines), encoding="utf-8")
print(f"Extracted {len(results)} replacement bodies -> {OUT}")
