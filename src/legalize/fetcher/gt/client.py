from __future__ import annotations

from pathlib import Path

from legalize.fetcher.gt.discovery import GTDocument, discover_fixture_documents, get_fixture_document


class GuatemalaFixtureClient:
    def __init__(self, extracted_dir: Path = Path("tmp/extracted/gt")) -> None:
        self.extracted_dir = extracted_dir

    def discover_documents(self) -> list[GTDocument]:
        return discover_fixture_documents(self.extracted_dir)

    def get_document(self, identifier: str) -> GTDocument:
        return get_fixture_document(identifier, self.extracted_dir)

    def get_text(self, document: GTDocument) -> str:
        return document.extracted_text_path.read_text(encoding="utf-8", errors="replace")

    def get_text_by_identifier(self, identifier: str) -> str:
        document = self.get_document(identifier)
        return self.get_text(document)
