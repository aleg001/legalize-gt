from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import re
import unicodedata


@dataclass
class ParsedBlock:
    block_type: str
    marker: str
    title: str
    text: str
    line_start: int
    line_end: int


def normalize_for_matching(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.lower()


def clean_line(line: str) -> str:
    line = line.replace("\u00a0", " ")
    line = re.sub(r"[ \t]+", " ", line)
    return line.strip()


def is_page_artifact(line: str) -> bool:
    stripped = clean_line(line)

    if not stripped:
        return False

    patterns = [
        r"^\d+$",
        r"^N[ÚU]MERO\s*\d+.*$",
        r"^N[ÚU]MER[O0]?\s*\d+$",
        r"^DIARIO\s+de\s+CENTRO\s+AM[ÉE]RICA$",
        r"^Congreso de la República de Guatemala, Departamento de Información Legislativa\.?$",
        r"^Guatemala,\s+(LUNES|MARTES|MI[ÉE]RCOLES|JUEVES|VIERNES|S[ÁA]BADO|DOMINGO).*$",
        r"^Queda rigurosamente prohibida, sin la autorización escrita de las autoridades administrativas de INFILE, S\.A\..*$",
        r"^en las leyes; la reproducción parcial o total de este documento.*$",
        r"^alquiler o préstamo públicos\.$",
        r"^El documento fue generado para el uso exclusivo de:.*$",
        r"^Página\s+\d+/\d+$",
        r"^/{1,2}$",
        r"^/~$",
        r"^\.$",
    ]

    return any(re.search(pattern, stripped, re.IGNORECASE) for pattern in patterns)


def classify_line(line: str) -> tuple[str, str, str] | None:
    original = clean_line(line)
    normalized = normalize_for_matching(original)

    if not original:
        return None

    if re.search(r"\.{5,}\s*\d+$", original):
        return None

    title_match = re.match(
        r"^titulo\s+([ivxlcdm]+|primero|segundo|tercero|cuarto|quinto|sexto|septimo|octavo|noveno|decimo|\d+)\b(.*)$",
        normalized,
        re.IGNORECASE,
    )
    if title_match:
        return ("title", title_match.group(1), original)

    chapter_match = re.match(
        r"^capitulo\s+([ivxlcdm]+|unico|primero|segundo|tercero|cuarto|quinto|sexto|septimo|octavo|noveno|decimo|\d+)\b(.*)$",
        normalized,
        re.IGNORECASE,
    )
    if chapter_match:
        return ("chapter", chapter_match.group(1), original)

    section_match = re.match(
        r"^seccion\s+([ivxlcdm]+|primera|segunda|tercera|cuarta|quinta|sexta|septima|octava|novena|decima|\d+)\b(.*)$",
        normalized,
        re.IGNORECASE,
    )
    if section_match:
        return ("section", section_match.group(1), original)

    article_match = re.match(
        r"^articulo\s+([0-9]+(?:\s*(?:bis|ter|quater|quáter))?)\s*[\.\-º°\*]*\s*(.*)$",
        normalized,
        re.IGNORECASE,
    )
    if article_match:
        marker = " ".join(article_match.group(1).split())
        return ("article", marker, original)

    reform_match = re.search(
        r"\b(reformado|reformada|reformadas|adicionado|adicionada|adicionadas|derogado|derogada|derogadas)\b",
        normalized,
        re.IGNORECASE,
    )
    if reform_match and "decreto numero" in normalized:
        return ("reform_note", reform_match.group(1), original)

    return None


def parse_text(text: str) -> list[ParsedBlock]:
    raw_lines = text.splitlines()

    blocks: list[ParsedBlock] = []
    current_type = "preamble"
    current_marker = ""
    current_title = "Preamble"
    current_lines: list[str] = []
    current_start = 1

    def flush(line_end: int) -> None:
        nonlocal current_lines, current_type, current_marker, current_title, current_start

        block_text = "\n".join(current_lines).strip()
        if not block_text and current_type == "preamble":
            current_lines = []
            return

        blocks.append(
            ParsedBlock(
                block_type=current_type,
                marker=current_marker,
                title=current_title,
                text=block_text,
                line_start=current_start,
                line_end=line_end,
            )
        )
        current_lines = []

    for idx, line in enumerate(raw_lines, start=1):
        cleaned = clean_line(line)

        if is_page_artifact(cleaned):
            continue

        classification = classify_line(cleaned)

        if classification:
            flush(idx - 1)
            current_type, current_marker, current_title = classification
            current_start = idx
            current_lines = [cleaned]
        elif cleaned:
            current_lines.append(cleaned)

    flush(len(raw_lines))

    return blocks


def parse_text_file(path: Path) -> list[ParsedBlock]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return parse_text(text)


def blocks_to_dicts(blocks: list[ParsedBlock]) -> list[dict]:
    return [asdict(block) for block in blocks]


def write_blocks_json(blocks: list[ParsedBlock], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(blocks_to_dicts(blocks), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def count_blocks(blocks: list[ParsedBlock]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for block in blocks:
        counts[block.block_type] = counts.get(block.block_type, 0) + 1
    return counts
