from __future__ import annotations

from pathlib import Path
import json
import re


INPUT_DIR = Path("tmp/parsed/gt")
OUTPUT_DIR = Path("tmp/rendered/gt")


HEADING_PREFIX = {
    "title": "##",
    "chapter": "###",
    "section": "####",
    "article": "#####",
}


def normalize_blank_lines(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def yaml_quote(value: str) -> str:
    escaped = value.replace('"', '\\"')
    return f'"{escaped}"'


def title_from_stem(stem: str) -> str:
    return stem.replace("-", " ").title()


def render_reform_note(title: str) -> str:
    return f"> {title.strip()}"


def render_block(block: dict) -> str:
    block_type = block["block_type"]
    title = block["title"].strip()
    text = block["text"].strip()

    if block_type == "preamble":
        return normalize_blank_lines(text)

    if block_type == "reform_note":
        return render_reform_note(title)

    prefix = HEADING_PREFIX.get(block_type)

    if prefix:
        body = text

        # Avoid duplicating heading text in the body.
        if body.startswith(title):
            body = body[len(title):].strip()

        if body:
            return f"{prefix} {title}\n\n{normalize_blank_lines(body)}"

        return f"{prefix} {title}"

    return normalize_blank_lines(text)


def render_document(path: Path) -> str:
    blocks = json.loads(path.read_text(encoding="utf-8"))
    identifier = path.stem
    title = title_from_stem(path.stem)

    parts = [
        "---",
        "country: gt",
        f"identifier: {identifier}",
        f"title: {yaml_quote(title)}",
        'status: "parsed"',
        'source_type: "fixture"',
        'parser_version: "gt-structural-0.1.0"',
        "---",
        "",
        f"# {title}",
        "",
    ]

    for block in blocks:
        rendered = render_block(block)
        if rendered:
            parts.append(rendered)
            parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for json_path in sorted(INPUT_DIR.glob("*.json")):
        md = render_document(json_path)
        out_path = OUTPUT_DIR / f"{json_path.stem}.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"{json_path.name} -> {out_path}")


if __name__ == "__main__":
    main()
