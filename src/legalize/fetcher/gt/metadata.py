from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import hashlib

import yaml


FIXTURE_DIR = Path("engine/tests/fixtures/gt")
SOURCES_YAML = Path("data/gt/sources.yaml")


@dataclass(frozen=True)
class GTMetadata:
    country: str
    identifier: str
    title: str
    short_title: str
    rank: str
    decree_number: str | None
    source_type: str
    source_pdf: str
    source_url: str | None
    source_sha256: str
    publication_date: str | None
    issuing_body: str | None
    extraction_method: str
    confidence: str
    status: str = "parsed"
    parser_version: str = "gt-structural-0.1.0"


def load_fixture_metadata(path: Path = SOURCES_YAML) -> dict[str, dict[str, str | None]]:
    if not path.exists():
        raise FileNotFoundError(f"GT sources YAML not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if not isinstance(data, dict):
        raise ValueError(f"GT sources YAML must contain a mapping: {path}")

    return data


FIXTURE_METADATA: dict[str, dict[str, str | None]] = load_fixture_metadata()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def metadata_for_fixture(stem: str, fixture_dir: Path = FIXTURE_DIR) -> GTMetadata:
    if stem not in FIXTURE_METADATA:
        raise KeyError(f"No GT fixture metadata registered for: {stem}")

    raw = FIXTURE_METADATA[stem]
    source_pdf = raw["source_pdf"]

    if not isinstance(source_pdf, str):
        raise ValueError(f"Invalid source_pdf for fixture: {stem}")

    source_path = fixture_dir / source_pdf

    if not source_path.exists():
        raise FileNotFoundError(f"Source PDF not found: {source_path}")

    return GTMetadata(
        country="gt",
        identifier=str(raw["identifier"]),
        title=str(raw["title"]),
        short_title=str(raw["short_title"]),
        rank=str(raw["rank"]),
        decree_number=str(raw["decree_number"]
                          ) if raw["decree_number"] else None,
        source_type=str(raw["source_type"]),
        source_pdf=str(source_pdf),
        source_url=str(raw["source_url"]) if raw["source_url"] else None,
        source_sha256=sha256_file(source_path),
        publication_date=str(raw["publication_date"]
                             ) if raw["publication_date"] else None,
        issuing_body=str(raw["issuing_body"]) if raw["issuing_body"] else None,
        extraction_method=str(raw["extraction_method"]),
        confidence=str(raw["confidence"]),
    )


def metadata_to_dict(metadata: GTMetadata) -> dict[str, str | None]:
    return asdict(metadata)


def metadata_for_identifier(identifier: str, fixture_dir: Path = FIXTURE_DIR) -> GTMetadata:
    for stem, raw in FIXTURE_METADATA.items():
        if raw["identifier"] == identifier:
            return metadata_for_fixture(stem, fixture_dir)

    raise KeyError(f"No GT metadata registered for identifier: {identifier}")
