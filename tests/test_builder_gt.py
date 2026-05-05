from pathlib import Path

from legalize.fetcher.gt.builder import build_all_fixture_documents


def test_build_all_fixture_documents(tmp_path):
    output_json_dir = tmp_path / "parsed"
    output_markdown_dir = tmp_path / "rendered"

    results = build_all_fixture_documents(
        extracted_dir=Path("tmp/extracted/gt"),
        output_json_dir=output_json_dir,
        output_markdown_dir=output_markdown_dir,
        clean=True,
    )

    identifiers = {result.identifier for result in results}

    assert "decreto-57-2008" in identifiers
    assert "decreto-101-97" in identifiers
    assert "decreto-12-2002" in identifiers
    assert "constitucion-politica-republica-guatemala" in identifiers

    for result in results:
        assert result.json_path.exists()
        assert result.markdown_path.exists()
        assert result.block_count > 0

    laip_md = output_markdown_dir / "decreto-57-2008.md"
    content = laip_md.read_text(encoding="utf-8")

    assert 'identifier: "decreto-57-2008"' in content
    assert 'title: "Ley de Acceso a la Información Pública"' in content
    assert "##### Artículo 1. Objeto de la Ley." in content
