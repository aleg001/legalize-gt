from pathlib import Path

from legalize.fetcher.gt.builder import build_all_fixture_documents


def main() -> None:
    results = build_all_fixture_documents(
        extracted_dir=Path("tmp/extracted/gt"),
        output_json_dir=Path("tmp/parsed/gt"),
        output_markdown_dir=Path("tmp/rendered/gt"),
        clean=True,
    )

    for result in results:
        print(f"BUILT {result.identifier}")
        print(f"  title: {result.title}")
        print(f"  json:  {result.json_path}")
        print(f"  md:    {result.markdown_path}")
        print(f"  blocks: {result.block_count}")
        print()


if __name__ == "__main__":
    main()
