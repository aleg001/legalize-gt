from pathlib import Path

from legalize.fetcher.gt.cli import main


def test_cli_build_fixtures(tmp_path, capsys):
    output_json_dir = tmp_path / "parsed"
    output_markdown_dir = tmp_path / "rendered"

    exit_code = main(
        [
            "build-fixtures",
            "--extracted-dir",
            "tmp/extracted/gt",
            "--output-json-dir",
            str(output_json_dir),
            "--output-markdown-dir",
            str(output_markdown_dir),
            "--clean",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Built" in captured.out
    assert "decreto-57-2008" in captured.out

    assert (output_json_dir / "decreto-57-2008.json").exists()
    assert (output_markdown_dir / "decreto-57-2008.md").exists()

    markdown = (output_markdown_dir /
                "decreto-57-2008.md").read_text(encoding="utf-8")

    assert 'identifier: "decreto-57-2008"' in markdown
    assert 'title: "Ley de Acceso a la Información Pública"' in markdown
    assert "##### Artículo 1. Objeto de la Ley." in markdown


def test_cli_returns_error_when_no_documents(tmp_path, capsys):
    empty_extracted_dir = tmp_path / "empty"
    empty_extracted_dir.mkdir()

    exit_code = main(
        [
            "build-fixtures",
            "--extracted-dir",
            str(empty_extracted_dir),
            "--output-json-dir",
            str(tmp_path / "parsed"),
            "--output-markdown-dir",
            str(tmp_path / "rendered"),
            "--clean",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "No Guatemala fixture documents were built." in captured.out
