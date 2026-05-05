from pathlib import Path

from legalize.fetcher.gt.parser import parse_text_file
from legalize.fetcher.gt.renderer import render_markdown


FIXTURES = Path("tmp/extracted/gt")


def test_render_official_laip_markdown_headings():
    blocks = parse_text_file(
        FIXTURES / "sample-ordinary-law-laip-official.txt")
    markdown = render_markdown(
        blocks,
        identifier="sample-ordinary-law-laip-official",
        title="Ley de Acceso a la Información Pública",
    )

    assert "---" in markdown
    assert "country: gt" in markdown
    assert "identifier: sample-ordinary-law-laip-official" in markdown
    assert '# Ley de Acceso a la Información Pública' in markdown
    assert "## TÍTULO PRIMERO" in markdown
    assert "### CAPÍTULO PRIMERO" in markdown
    assert "##### Artículo 1. Objeto de la Ley." in markdown


def test_render_budget_law_reform_notes_as_blockquotes():
    blocks = parse_text_file(FIXTURES / "sample-budget-law.txt")
    markdown = render_markdown(
        blocks,
        identifier="sample-budget-law",
        title="Ley Orgánica del Presupuesto",
    )

    assert "##### ARTICULO 1.- Objeto." in markdown
    assert "> *Reformado por el Artículo 1, del Decreto Número 13-2013" in markdown


def test_render_no_known_artifacts():
    files = [
        "sample-ordinary-law-laip-official.txt",
        "sample-budget-law.txt",
        "sample-civic-service.txt",
        "sample-code-codigo-municipal.txt",
        "sample-constitution.txt",
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

    for filename in files:
        blocks = parse_text_file(FIXTURES / filename)
        markdown = render_markdown(
            blocks, identifier=filename.removesuffix(".txt"))

        for marker in forbidden:
            assert marker not in markdown, f"{marker} found in {filename}"


def test_render_has_expected_article_counts():
    expected_minimums = {
        "sample-ordinary-law-laip-official.txt": 70,
        "sample-budget-law.txt": 100,
        "sample-civic-service.txt": 50,
        "sample-code-codigo-municipal.txt": 170,
        "sample-constitution.txt": 280,
    }

    for filename, minimum in expected_minimums.items():
        blocks = parse_text_file(FIXTURES / filename)
        markdown = render_markdown(
            blocks, identifier=filename.removesuffix(".txt"))

        assert markdown.count("\n##### ") >= minimum
