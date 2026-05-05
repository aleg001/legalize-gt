from pathlib import Path

import pytest

from legalize.fetcher.gt.metadata import (
    FIXTURE_METADATA,
    metadata_for_fixture,
    metadata_for_identifier,
    metadata_to_dict,
    sha256_file,
)

from legalize.fetcher.gt.metadata import SOURCES_YAML, load_fixture_metadata


FIXTURE_DIR = Path("engine/tests/fixtures/gt")


def test_sha256_file_matches_length():
    path = FIXTURE_DIR / "sample-ordinary-law-laip-official.pdf"
    digest = sha256_file(path)

    assert len(digest) == 64
    assert all(char in "0123456789abcdef" for char in digest)


def test_metadata_for_official_laip():
    meta = metadata_for_fixture("sample-ordinary-law-laip-official")

    assert meta.country == "gt"
    assert meta.identifier == "decreto-57-2008"
    assert meta.title == "Ley de Acceso a la Información Pública"
    assert meta.short_title == "LAIP"
    assert meta.rank == "decreto"
    assert meta.decree_number == "57-2008"
    assert meta.source_type == "official_primary"
    assert meta.source_pdf == "sample-ordinary-law-laip-official.pdf"
    assert len(meta.source_sha256) == 64
    assert meta.extraction_method == "pymupdf"
    assert meta.confidence == "high"
    assert meta.source_url == "https://www.congreso.gob.gt/assets/uploads/info_legislativo/decretos/2008/57-2008.pdf"
    assert meta.issuing_body == "Congreso de la República de Guatemala"


def test_metadata_for_budget_law():
    meta = metadata_for_fixture("sample-budget-law")

    assert meta.identifier == "decreto-101-97"
    assert meta.title == "Ley Orgánica del Presupuesto"
    assert meta.decree_number == "101-97"
    assert meta.confidence == "medium"


def test_metadata_for_identifier():
    meta = metadata_for_identifier("decreto-57-2008")

    assert meta.title == "Ley de Acceso a la Información Pública"
    assert meta.source_pdf == "sample-ordinary-law-laip-official.pdf"


def test_all_fixture_metadata_has_existing_pdf():
    for stem, raw in FIXTURE_METADATA.items():
        source_pdf = raw["source_pdf"]
        assert source_pdf
        assert (FIXTURE_DIR / str(source_pdf)).exists(), stem


def test_metadata_to_dict():
    meta = metadata_for_fixture("sample-ordinary-law-laip-official")
    data = metadata_to_dict(meta)

    assert data["country"] == "gt"
    assert data["identifier"] == "decreto-57-2008"
    assert data["source_sha256"] == meta.source_sha256


def test_unknown_fixture_raises_key_error():
    with pytest.raises(KeyError):
        metadata_for_fixture("does-not-exist")


def test_unknown_identifier_raises_key_error():
    with pytest.raises(KeyError):
        metadata_for_identifier("does-not-exist")


def test_sources_yaml_loads():
    data = load_fixture_metadata(SOURCES_YAML)

    assert "sample-ordinary-law-laip-official" in data
    assert data["sample-ordinary-law-laip-official"]["identifier"] == "decreto-57-2008"
