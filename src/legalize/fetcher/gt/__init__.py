"""Guatemala (`gt`) parser utilities."""

from legalize.fetcher.gt.parser import (
    ParsedBlock,
    blocks_to_dicts,
    classify_line,
    clean_line,
    count_blocks,
    is_page_artifact,
    normalize_for_matching,
    parse_text,
    parse_text_file,
    write_blocks_json,
)

__all__ = [
    "ParsedBlock",
    "blocks_to_dicts",
    "classify_line",
    "clean_line",
    "count_blocks",
    "is_page_artifact",
    "normalize_for_matching",
    "parse_text",
    "parse_text_file",
    "write_blocks_json",
]
