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
from legalize.fetcher.gt.metadata import (
    FIXTURE_METADATA,
    GTMetadata,
    metadata_for_fixture,
    metadata_for_identifier,
    metadata_to_dict,
    sha256_file,
)

from legalize.fetcher.gt.client import GuatemalaFixtureClient
from legalize.fetcher.gt.discovery import (
    GTDocument,
    discover_fixture_documents,
    get_fixture_document,
)

from legalize.fetcher.gt.builder import (
    BuildResult,
    build_all_fixture_documents,
    build_document,
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
    "FIXTURE_METADATA",
    "GTMetadata",
    "metadata_for_fixture",
    "metadata_for_identifier",
    "metadata_to_dict",
    "sha256_file",
    "GuatemalaFixtureClient",
    "GTDocument",
    "discover_fixture_documents",
    "get_fixture_document",
    "BuildResult",
    "build_all_fixture_documents",
    "build_document",
]
