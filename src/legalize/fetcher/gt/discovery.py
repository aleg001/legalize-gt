from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from legalize.fetcher.gt.metadata import FIXTURE_METADATA, GTMetadata, metadata_for_fixture


EXTRACTED_DIR = Path("tmp/extracted/gt")


@dataclass(frozen=True)
class GTDocument:
    fixture_name: str
    identifier: str
    title: str
    source_pdf: str
    extracted_text_path: Path
    metadata: GTMetadata


def discover_fixture_documents(extracted_dir: Path = EXTRACTED_DIR) -> list[GTDocument]:
    documents: list[GTDocument] = []

    for fixture_name in sorted(FIXTURE_METADATA):
        metadata = metadata_for_fixture(fixture_name)
        extracted_text_path = extracted_dir / f"{fixture_name}.txt"

        if not extracted_text_path.exists():
            continue

        documents.append(
            GTDocument(
                fixture_name=fixture_name,
                identifier=metadata.identifier,
                title=metadata.title,
                source_pdf=metadata.source_pdf,
                extracted_text_path=extracted_text_path,
                metadata=metadata,
            )
        )

    return documents


def get_fixture_document(identifier: str, extracted_dir: Path = EXTRACTED_DIR) -> GTDocument:
    for document in discover_fixture_documents(extracted_dir):
        if document.identifier == identifier:
            return document

    raise KeyError(
        f"No GT fixture document found for identifier: {identifier}")
