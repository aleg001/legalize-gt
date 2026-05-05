from pathlib import Path
import shutil

from legalize.fetcher.gt.metadata import FIXTURE_METADATA, metadata_for_fixture
from legalize.fetcher.gt.parser import parse_text_file, write_blocks_json
from legalize.fetcher.gt.renderer import render_markdown


EXTRACTED_DIR = Path("tmp/extracted/gt")
PARSED_DIR = Path("tmp/parsed/gt")
RENDERED_DIR = Path("tmp/rendered/gt")


def reset_output_dirs() -> None:
    for directory in [PARSED_DIR, RENDERED_DIR]:
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)


def main() -> None:
    reset_output_dirs()

    for fixture_name in sorted(FIXTURE_METADATA):
        txt_path = EXTRACTED_DIR / f"{fixture_name}.txt"

        if not txt_path.exists():
            print(f"SKIP {fixture_name}: missing {txt_path}")
            continue

        metadata = metadata_for_fixture(fixture_name)
        blocks = parse_text_file(txt_path)

        json_path = PARSED_DIR / f"{metadata.identifier}.json"
        md_path = RENDERED_DIR / f"{metadata.identifier}.md"

        write_blocks_json(blocks, json_path)

        markdown = render_markdown(blocks, metadata=metadata)
        md_path.write_text(markdown, encoding="utf-8")

        print(f"BUILT {fixture_name}")
        print(f"  json: {json_path}")
        print(f"  md:   {md_path}")
        print(f"  blocks: {len(blocks)}")
        print()


if __name__ == "__main__":
    main()
