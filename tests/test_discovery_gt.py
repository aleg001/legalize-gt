from pathlib import Path

import pytest

from legalize.fetcher.gt.client import GuatemalaFixtureClient
from legalize.fetcher.gt.discovery import discover_fixture_documents, get_fixture_document


EXTRACTED_DIR = Path("tmp/extracted/gt")


def test_discover_fixture_documents():
    documents = discover_fixture_documents(EXTRACTED_DIR)

    identifiers = {document.identifier for document in documents}

    assert "decreto-57-2008" in identifiers
    assert "decreto-101-97" in identifiers
    assert "decreto-12-2002" in identifiers
    assert "constitucion-politica-republica-guatemala" in identifiers
    assert "decreto-13-2013" in identifiers


def test_discovered_documents_have_metadata_and_text_paths():
    documents = discover_fixture_documents(EXTRACTED_DIR)

    assert documents

    for document in documents:
        assert document.fixture_name
        assert document.identifier
        assert document.title
        assert document.source_pdf.endswith(".pdf")
        assert document.extracted_text_path.exists()
        assert document.metadata.identifier == document.identifier


def test_get_fixture_document_by_identifier():
    document = get_fixture_document("decreto-57-2008", EXTRACTED_DIR)

    assert document.title == "Ley de Acceso a la Información Pública"
    assert document.fixture_name == "sample-ordinary-law-laip-official"
    assert document.extracted_text_path.name == "sample-ordinary-law-laip-official.txt"


def test_get_fixture_document_unknown_identifier():
    with pytest.raises(KeyError):
        get_fixture_document("does-not-exist", EXTRACTED_DIR)


def test_fixture_client_get_text_by_identifier():
    client = GuatemalaFixtureClient(EXTRACTED_DIR)

    text = client.get_text_by_identifier("decreto-57-2008")

    assert "DECRETO NÚMERO 57-2008" in text
    assert "LEY DE ACCESO A LA" in text or "Ley de Acceso a la Información Pública" in text


def test_fixture_client_discover_documents():
    client = GuatemalaFixtureClient(EXTRACTED_DIR)

    documents = client.discover_documents()

    assert len(documents) >= 5
    assert any(document.identifier ==
               "decreto-101-97" for document in documents)
