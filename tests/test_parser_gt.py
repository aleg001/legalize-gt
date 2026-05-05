from pathlib import Path

from legalize.fetcher.gt.parser import count_blocks, parse_text_file


FIXTURES = Path("tmp/extracted/gt")


def test_parse_official_laip_structure():
    blocks = parse_text_file(
        FIXTURES / "sample-ordinary-law-laip-official.txt")
    counts = count_blocks(blocks)

    assert counts.get("article", 0) >= 70
    assert counts.get("title", 0) >= 5
    assert counts.get("chapter", 0) >= 10


def test_parse_budget_law_structure_and_reforms():
    blocks = parse_text_file(FIXTURES / "sample-budget-law.txt")
    counts = count_blocks(blocks)

    assert counts.get("article", 0) >= 100
    assert counts.get("reform_note", 0) >= 50


def test_parse_constitution_structure():
    blocks = parse_text_file(FIXTURES / "sample-constitution.txt")
    counts = count_blocks(blocks)

    assert counts.get("article", 0) >= 280
    assert counts.get("title", 0) >= 8
    assert counts.get("chapter", 0) >= 20


def test_no_mojibake_in_parsed_blocks():
    files = [
        "sample-ordinary-law-laip-official.txt",
        "sample-budget-law.txt",
        "sample-civic-service.txt",
        "sample-code-codigo-municipal.txt",
        "sample-constitution.txt",
    ]

    bad_markers = ("Ã", "�", "â")

    for filename in files:
        blocks = parse_text_file(FIXTURES / filename)

        for block in blocks:
            assert not any(
                marker in block.text for marker in bad_markers), filename
            assert not any(
                marker in block.title for marker in bad_markers), filename


def test_page_artifacts_removed_from_laip():
    blocks = parse_text_file(
        FIXTURES / "sample-ordinary-law-laip-official.txt")
    joined = "\n".join(block.text for block in blocks)

    forbidden = [
        "INFILE",
        "Queda rigurosamente prohibida",
        "uso exclusivo",
        "Página 1/24",
    ]

    for marker in forbidden:
        assert marker not in joined
