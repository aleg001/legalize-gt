from __future__ import annotations

import argparse
from pathlib import Path

from legalize.fetcher.gt.builder import build_all_fixture_documents


def build_fixtures(args: argparse.Namespace) -> int:
    results = build_all_fixture_documents(
        extracted_dir=Path(args.extracted_dir),
        output_json_dir=Path(args.output_json_dir),
        output_markdown_dir=Path(args.output_markdown_dir),
        clean=args.clean,
    )

    if not results:
        print("No Guatemala fixture documents were built.")
        return 1

    for result in results:
        print(f"BUILT {result.identifier}")
        print(f"  title: {result.title}")
        print(f"  json:  {result.json_path}")
        print(f"  md:    {result.markdown_path}")
        print(f"  blocks: {result.block_count}")
        print()

    print(f"Built {len(results)} Guatemala fixture document(s).")
    return 0


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m legalize.fetcher.gt.cli",
        description="Guatemala (`gt`) local fixture builder for Legalize-style research.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser(
        "build-fixtures",
        help="Build parsed JSON and rendered Markdown from extracted Guatemala fixture text.",
    )
    build_parser.add_argument(
        "--extracted-dir",
        default="tmp/extracted/gt",
        help="Directory containing extracted Guatemala fixture .txt files.",
    )
    build_parser.add_argument(
        "--output-json-dir",
        default="tmp/parsed/gt",
        help="Directory where parsed JSON files will be written.",
    )
    build_parser.add_argument(
        "--output-markdown-dir",
        default="tmp/rendered/gt",
        help="Directory where rendered Markdown files will be written.",
    )
    build_parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean output directories before building.",
    )
    build_parser.set_defaults(func=build_fixtures)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
