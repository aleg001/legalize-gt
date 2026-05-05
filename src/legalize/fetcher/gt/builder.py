from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from legalize.fetcher.gt.client import GuatemalaFixtureClient
from legalize.fetcher.gt.discovery import GTDocument
from legalize.fetcher.gt.parser import ParsedBlock, parse_text, write_blocks_json
from legalize.fetcher.gt.renderer import render_markdown


@dataclass(frozen=True)
class BuildResult:
    identifier: str
    title: str
    json_path: Path
    markdown_path: Path
    block_count: int


def build_document(
    document: GTDocument,
    *,
    output_json_dir: Path,
    output_markdown_dir: Path,
) -> BuildResult:
    text = document.extracted_text_path.read_text(
        encoding="utf-8", errors="replace")
    blocks = parse_text(text)

    json_path = output_json_dir / f"{document.identifier}.json"
    markdown_path = output_markdown_dir / f"{document.identifier}.md"

    write_blocks_json(blocks, json_path)

    markdown = render_markdown(blocks, metadata=document.metadata)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(markdown, encoding="utf-8")

    return BuildResult(
        identifier=document.identifier,
        title=document.title,
        json_path=json_path,
        markdown_path=markdown_path,
        block_count=len(blocks),
    )


def build_all_fixture_documents(
    *,
    extracted_dir: Path = Path("tmp/extracted/gt"),
    output_json_dir: Path = Path("tmp/parsed/gt"),
    output_markdown_dir: Path = Path("tmp/rendered/gt"),
    clean: bool = False,
) -> list[BuildResult]:
    if clean:
        for directory in [output_json_dir, output_markdown_dir]:
            if directory.exists():
                for item in directory.glob("*"):
                    if item.is_file():
                        item.unlink()
            directory.mkdir(parents=True, exist_ok=True)

    client = GuatemalaFixtureClient(extracted_dir)
    documents = client.discover_documents()

    results: list[BuildResult] = []

    for document in documents:
        result = build_document(
            document,
            output_json_dir=output_json_dir,
            output_markdown_dir=output_markdown_dir,
        )
        results.append(result)

    return results
