"""Guatemala (`gt`) parser and renderer utilities."""

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
from legalize.fetcher.gt.renderer import (
    blocks_from_json,
    normalize_blank_lines,
    render_block,
    render_json_file,
    render_markdown,
    render_reform_note,
    title_from_identifier,
    yaml_quote,
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
    "blocks_from_json",
    "normalize_blank_lines",
    "render_block",
    "render_json_file",
    "render_markdown",
    "render_reform_note",
    "title_from_identifier",
    "yaml_quote",
]
