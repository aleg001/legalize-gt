from __future__ import annotations

from pathlib import Path
import json
import re

from legalize.fetcher.gt.metadata import GTMetadata, metadata_to_dict
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


def render_yaml_value(value: str | None) -> str:
    if value is None:
        return "null"

    return yaml_quote(str(value))


def render_frontmatter_from_metadata(metadata: GTMetadata) -> list[str]:
    data = metadata_to_dict(metadata)

    ordered_keys = [
        "country",
        "identifier",
        "title",
        "short_title",
        "rank",
        "decree_number",
        "source_type",
        "source_pdf",
        "source_sha256",
        "extraction_method",
        "confidence",
        "status",
        "parser_version",
    ]

    lines = ["---"]

    for key in ordered_keys:
        lines.append(f"{key}: {render_yaml_value(data.get(key))}")

    lines.append("---")
    lines.append("")

    return lines


def render_frontmatter_minimal(
    *,
    identifier: str,
    title: str,
    status: str,
    source_type: str,
    parser_version: str,
) -> list[str]:
    return [
        "---",
        "country: gt",
        f"identifier: {identifier}",
        f"title: {yaml_quote(title)}",
        f'status: "{status}"',
        f'source_type: "{source_type}"',
        f'parser_version: "{parser_version}"',
        "---",
        "",
    ]


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
    identifier: str | None = None,
    title: str | None = None,
    metadata: GTMetadata | None = None,
    status: str = "parsed",
    source_type: str = "fixture",
    parser_version: str = "gt-structural-0.1.0",
) -> str:
    if metadata:
        document_identifier = metadata.identifier
        document_title = metadata.title
        frontmatter = render_frontmatter_from_metadata(metadata)
    else:
        if identifier is None:
            raise ValueError(
                "identifier is required when metadata is not provided")

        document_identifier = identifier
        document_title = title or title_from_identifier(identifier)
        frontmatter = render_frontmatter_minimal(
            identifier=document_identifier,
            title=document_title,
            status=status,
            source_type=source_type,
            parser_version=parser_version,
        )

    parts = [
        *frontmatter,
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


def render_json_file(
    json_path: Path,
    output_path: Path,
    *,
    metadata: GTMetadata | None = None,
) -> None:
    blocks = blocks_from_json(json_path)
    markdown = render_markdown(
        blocks, identifier=json_path.stem, metadata=metadata)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
