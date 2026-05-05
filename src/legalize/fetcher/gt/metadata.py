from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import hashlib


FIXTURE_DIR = Path("engine/tests/fixtures/gt")


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
    source_sha256: str
    extraction_method: str
    confidence: str
    status: str = "parsed"
    parser_version: str = "gt-structural-0.1.0"


FIXTURE_METADATA: dict[str, dict[str, str | None]] = {
    "sample-budget-law": {
        "identifier": "decreto-101-97",
        "title": "Ley Orgánica del Presupuesto",
        "short_title": "Ley Orgánica del Presupuesto",
        "rank": "decreto",
        "decree_number": "101-97",
        "source_type": "official_or_institutional_compilation",
        "source_pdf": "sample-budget-law.pdf",
        "extraction_method": "pymupdf",
        "confidence": "medium",
    },
    "sample-civic-service": {
        "identifier": "sample-civic-service",
        "title": "Ley de Servicio Cívico",
        "short_title": "Ley de Servicio Cívico",
        "rank": "decreto",
        "decree_number": None,
        "source_type": "official_or_institutional_compilation",
        "source_pdf": "sample-civic-service.pdf",
        "extraction_method": "pymupdf",
        "confidence": "medium",
    },
    "sample-code-codigo-municipal": {
        "identifier": "decreto-12-2002",
        "title": "Código Municipal",
        "short_title": "Código Municipal",
        "rank": "codigo",
        "decree_number": "12-2002",
        "source_type": "official_or_institutional_compilation",
        "source_pdf": "sample-code-codigo-municipal.pdf",
        "extraction_method": "pymupdf",
        "confidence": "medium",
    },
    "sample-constitution": {
        "identifier": "constitucion-politica-republica-guatemala",
        "title": "Constitución Política de la República de Guatemala",
        "short_title": "Constitución Política",
        "rank": "constitution",
        "decree_number": None,
        "source_type": "official_or_institutional_compilation",
        "source_pdf": "sample-constitution.pdf",
        "extraction_method": "pymupdf",
        "confidence": "medium",
    },
    "sample-ordinary-law-laip-official": {
        "identifier": "decreto-57-2008",
        "title": "Ley de Acceso a la Información Pública",
        "short_title": "LAIP",
        "rank": "decreto",
        "decree_number": "57-2008",
        "source_type": "official_primary",
        "source_pdf": "sample-ordinary-law-laip-official.pdf",
        "extraction_method": "pymupdf",
        "confidence": "high",
    },
    "reform-decree-13-2013": {
        "identifier": "decreto-13-2013",
        "title": "Reformas al Decreto 101-97, Ley Orgánica del Presupuesto",
        "short_title": "Decreto 13-2013",
        "rank": "reform_decree",
        "decree_number": "13-2013",
        "source_type": "official_primary",
        "source_pdf": "reform-decree-13-2013.pdf",
        "extraction_method": "pymupdf",
        "confidence": "medium",
    },
}


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
        source_sha256=sha256_file(source_path),
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
