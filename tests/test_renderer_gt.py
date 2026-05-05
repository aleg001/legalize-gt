from pathlib import Path

from legalize.fetcher.gt.metadata import metadata_for_fixture
from legalize.fetcher.gt.parser import parse_text_file
from legalize.fetcher.gt.renderer import render_markdown


FIXTURES = Path("tmp/extracted/gt")


def test_render_official_laip_markdown_headings():
    blocks = parse_text_file(
        FIXTURES / "sample-ordinary-law-laip-official.txt")
    metadata = metadata_for_fixture("sample-ordinary-law-laip-official")

    markdown = render_markdown(blocks, metadata=metadata)

    assert "---" in markdown
    assert 'country: "gt"' in markdown
    assert 'identifier: "decreto-57-2008"' in markdown
    assert 'title: "Ley de Acceso a la Información Pública"' in markdown
    assert 'short_title: "LAIP"' in markdown
    assert 'rank: "decreto"' in markdown
    assert 'decree_number: "57-2008"' in markdown
    assert 'source_type: "official_primary"' in markdown
    assert 'source_pdf: "sample-ordinary-law-laip-official.pdf"' in markdown
    assert 'extraction_method: "pymupdf"' in markdown
    assert 'confidence: "high"' in markdown
    assert "# Ley de Acceso a la Información Pública" in markdown
    assert "## TÍTULO PRIMERO" in markdown
    assert "### CAPÍTULO PRIMERO" in markdown
    assert "##### Artículo 1. Objeto de la Ley." in markdown


def test_render_budget_law_reform_notes_as_blockquotes():
    blocks = parse_text_file(FIXTURES / "sample-budget-law.txt")
    metadata = metadata_for_fixture("sample-budget-law")

    markdown = render_markdown(blocks, metadata=metadata)

    assert 'identifier: "decreto-101-97"' in markdown
    assert 'title: "Ley Orgánica del Presupuesto"' in markdown
    assert "##### ARTICULO 1.- Objeto." in markdown
    assert "> *Reformado por el Artículo 1, del Decreto Número 13-2013" in markdown


def test_render_no_known_artifacts():
    fixture_names = [
        "sample-ordinary-law-laip-official",
        "sample-budget-law",
        "sample-civic-service",
        "sample-code-codigo-municipal",
        "sample-constitution",
    ]

    forbidden = [
        "INFILE",
        "Queda rigurosamente prohibida",
        "uso exclusivo",
        "NÚMER029",
        "Departamento de Información Legislativa",
        "Ã",
        "�",
        "â",
    ]

    for fixture_name in fixture_names:
        blocks = parse_text_file(FIXTURES / f"{fixture_name}.txt")
        metadata = metadata_for_fixture(fixture_name)
        markdown = render_markdown(blocks, metadata=metadata)

        for marker in forbidden:
            assert marker not in markdown, f"{marker} found in {fixture_name}"


def test_render_has_expected_article_counts():
    expected_minimums = {
        "sample-ordinary-law-laip-official": 70,
        "sample-budget-law": 100,
        "sample-civic-service": 50,
        "sample-code-codigo-municipal": 170,
        "sample-constitution": 280,
    }

    for fixture_name, minimum in expected_minimums.items():
        blocks = parse_text_file(FIXTURES / f"{fixture_name}.txt")
        metadata = metadata_for_fixture(fixture_name)
        markdown = render_markdown(blocks, metadata=metadata)

        assert markdown.count("\n##### ") >= minimum


def test_render_requires_identifier_without_metadata():
    blocks = parse_text_file(
        FIXTURES / "sample-ordinary-law-laip-official.txt")

    try:
        render_markdown(blocks)
    except ValueError as error:
        assert "identifier is required" in str(error)
    else:
        raise AssertionError(
            "Expected ValueError when rendering without metadata or identifier")
