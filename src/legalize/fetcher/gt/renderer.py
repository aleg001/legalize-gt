from __future__ import annotations

from pathlib import Path
import json
import re

from legalize.fetcher.gt.parser import ParsedBlock


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


def title_from_identifier(identifier: str) -> str:
    return identifier.replace("-", " ").title()


def render_reform_note(title: str) -> str:
    return f"> {title.strip()}"


def render_block(block: ParsedBlock) -> str:
    block_type = block.block_type
    title = block.title.strip()
    text = block.text.strip()

    if block_type == "preamble":
        return normalize_blank_lines(text)

    if block_type == "reform_note":
        return render_reform_note(title)

    prefix = HEADING_PREFIX.get(block_type)

    if prefix:
        body = text

        if body.startswith(title):
            body = body[len(title):].strip()

        if body:
            return f"{prefix} {title}\n\n{normalize_blank_lines(body)}"

        return f"{prefix} {title}"

    return normalize_blank_lines(text)


def render_markdown(
    blocks: list[ParsedBlock],
    *,
    identifier: str,
    title: str | None = None,
    status: str = "parsed",
    source_type: str = "fixture",
    parser_version: str = "gt-structural-0.1.0",
) -> str:
    document_title = title or title_from_identifier(identifier)

    parts = [
        "---",
        "country: gt",
        f"identifier: {identifier}",
        f"title: {yaml_quote(document_title)}",
        f'status: "{status}"',
        f'source_type: "{source_type}"',
        f'parser_version: "{parser_version}"',
        "---",
        "",
        f"# {document_title}",
        "",
    ]

    for block in blocks:
        rendered = render_block(block)

        if rendered:
            parts.append(rendered)
            parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def blocks_from_json(path: Path) -> list[ParsedBlock]:
    raw_blocks = json.loads(path.read_text(encoding="utf-8"))

    return [
        ParsedBlock(
            block_type=item["block_type"],
            marker=item["marker"],
            title=item["title"],
            text=item["text"],
            line_start=item["line_start"],
            line_end=item["line_end"],
        )
        for item in raw_blocks
    ]


def render_json_file(json_path: Path, output_path: Path) -> None:
    blocks = blocks_from_json(json_path)
    markdown = render_markdown(blocks, identifier=json_path.stem)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
