# legalize-gt

Guatemala (`gt`) prototype for converting official Guatemalan legal documents into structured Markdown with metadata, parser tests, and a preliminary version-history reconstruction spike.

This repository is an experimental implementation inspired by the Legalize project. It is intended to research whether Guatemala can be added as a country integration to a Legalize-style pipeline where laws are represented as Markdown files and legal reforms can eventually be represented as Git commits.

## Current status

Current milestone:

- PDF fixture extraction with PyMuPDF.
- Structural parser for titles, chapters, sections, articles, and reform notes.
- Markdown renderer with metadata frontmatter.
- Fixture-based metadata parser.
- Fixture-based discovery client.
- Fixture-based build pipeline.
- Local quality gate documentation.
- Version-history spike using Decreto 101-97 and Decreto 13-2013.
- Automated tests for parser, renderer, metadata, discovery, and builder.

Current test result:

```bash
PYTHONPATH=src pytest tests -q
```

```text
25 passed
```

## Repository structure

```text
legalize-gt/
  README.md
  RESEARCH-GT.md
  docs/
    QUALITY-GATE-GT.md
  engine/
    tests/
      fixtures/
        gt/
          sample-budget-law.pdf
          sample-civic-service.pdf
          sample-code-codigo-municipal.pdf
          sample-constitution.pdf
          sample-ordinary-law-laip-official.pdf
          reform-decree-13-2013.pdf
          SHA256SUMS.txt
  scripts/
    build_gt_samples.py
    diagnose_structure.py
    extract_fixture_text.py
    extract_reform_operations.py
    extract_replacement_bodies.py
    parse_gt_pdf.py
    render_gt_markdown.py
  src/
    legalize/
      fetcher/
        gt/
          __init__.py
          builder.py
          client.py
          discovery.py
          metadata.py
          parser.py
          renderer.py
  tests/
    test_builder_gt.py
    test_discovery_gt.py
    test_metadata_gt.py
    test_parser_gt.py
    test_renderer_gt.py
```

## Main components

### `parser.py`

Parses extracted Guatemalan legal text into structural blocks.

Current block types:

- `preamble`
- `title`
- `chapter`
- `section`
- `article`
- `reform_note`

The parser uses accent-insensitive matching for legal headings while preserving the original legal text in the rendered output.

Supported heading variants include:

- `Artículo`
- `ARTÍCULO`
- `ARTICULO`
- `Articulo`
- `TÍTULO`
- `TITULO`
- `CAPÍTULO`
- `CAPITULO`

It also handles common article-heading variants such as:

```text
ARTICULO 1.
ARTICULO 1.-
ARTICULO 4.*
ARTICULO 7 Bis.
Artículo 1º.
```

### `renderer.py`

Converts parsed blocks into Markdown.

Current Markdown conventions:

```md
## Title

### Chapter

#### Section

##### Article

> Reform note
```

The renderer also emits YAML frontmatter with metadata.

Example frontmatter:

```yaml
---
country: "gt"
identifier: "decreto-57-2008"
title: "Ley de Acceso a la Información Pública"
short_title: "LAIP"
rank: "decreto"
decree_number: "57-2008"
source_type: "official_primary"
source_pdf: "sample-ordinary-law-laip-official.pdf"
source_sha256: "..."
extraction_method: "pymupdf"
confidence: "high"
status: "parsed"
parser_version: "gt-structural-0.1.0"
---
```

### `metadata.py`

Provides fixture-based metadata for the current research corpus.

Current metadata fields:

- `country`
- `identifier`
- `title`
- `short_title`
- `rank`
- `decree_number`
- `source_type`
- `source_pdf`
- `source_sha256`
- `extraction_method`
- `confidence`
- `status`
- `parser_version`

This is still fixture-based and must later be replaced or complemented by live metadata from official sources such as Congreso and Diario de Centro América.

### `discovery.py`

Discovers available fixture documents from the local extracted-text directory.

This is a temporary local discovery layer used to simulate the future country discovery process.

### `client.py`

Provides a fixture-based client for retrieving discovered documents and their extracted text.

### `builder.py`

Runs the local pipeline end to end:

```text
discover documents
→ read extracted text
→ parse structural blocks
→ render Markdown with metadata
→ write JSON and Markdown outputs
```

## Setup

Recommended Python version:

```text
Python 3.11+
```

Install development dependencies:

```bash
pip install pytest pymupdf
```

If using a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest pymupdf
```

## Extract fixture text

The current parser works from text extracted from PDF fixtures.

Run:

```bash
python scripts/extract_fixture_text.py
```

Expected outputs:

```text
tmp/extracted/gt/reform-decree-13-2013.txt
tmp/extracted/gt/sample-budget-law.txt
tmp/extracted/gt/sample-civic-service.txt
tmp/extracted/gt/sample-code-codigo-municipal.txt
tmp/extracted/gt/sample-constitution.txt
tmp/extracted/gt/sample-ordinary-law-laip-official.txt
```

## Build sample outputs

Run:

```bash
PYTHONPATH=src python scripts/build_gt_samples.py
```

Expected output directories:

```text
tmp/parsed/gt/
tmp/rendered/gt/
```

Current rendered Markdown outputs:

```text
tmp/rendered/gt/constitucion-politica-republica-guatemala.md
tmp/rendered/gt/decreto-101-97.md
tmp/rendered/gt/decreto-12-2002.md
tmp/rendered/gt/decreto-13-2013.md
tmp/rendered/gt/decreto-57-2008.md
tmp/rendered/gt/sample-civic-service.md
```

## Run tests

```bash
PYTHONPATH=src pytest tests -q
```

Current expected result:

```text
25 passed
```

## Current fixtures

### Primary local quality-gate fixtures

| Fixture | Norm | Purpose |
|---|---|---|
| `sample-constitution.pdf` | Constitución Política de la República de Guatemala | Highest-rank constitutional norm |
| `sample-ordinary-law-laip-official.pdf` | Decreto 57-2008, Ley de Acceso a la Información Pública | Official ordinary law fixture |
| `sample-budget-law.pdf` | Decreto 101-97, Ley Orgánica del Presupuesto | Budget law, reform-note extraction |
| `sample-code-codigo-municipal.pdf` | Decreto 12-2002, Código Municipal | Code/framework law |
| `sample-civic-service.pdf` | Ley de Servicio Cívico | Administrative/public-service law |

### Supplementary version-history fixture

| Fixture | Norm | Purpose |
|---|---|---|
| `reform-decree-13-2013.pdf` | Decreto 13-2013 | Reform-decree spike for Decreto 101-97 |

## Current parser results

Current structural diagnosis:

| Source text | Article headings | Title headings | Chapter headings | Reform notes | Mojibake |
|---|---:|---:|---:|---:|---:|
| `sample-budget-law.txt` | 103 | 10 | 4 | 57 | 0 |
| `sample-civic-service.txt` | 54 | 0 | 8 | 0 | 0 |
| `sample-code-codigo-municipal.txt` | 178 | 8 | 24 | 0 | 0 |
| `sample-constitution.txt` | 311 | 16 | 54 | 1 | 0 |
| `sample-ordinary-law-laip-official.txt` | 73 | 5 | 13 | 0 | 0 |
| `reform-decree-13-2013.txt` | 83 | 0 | 2 | 0 | 0 |

## Current rendered Markdown article counts

```bash
grep -c "^##### " tmp/rendered/gt/*.md
```

Current counts:

| Rendered Markdown | Article headings |
|---|---:|
| `constitucion-politica-republica-guatemala.md` | 311 |
| `decreto-101-97.md` | 103 |
| `decreto-12-2002.md` | 178 |
| `decreto-13-2013.md` | 83 |
| `decreto-57-2008.md` | 73 |
| `sample-civic-service.md` | 54 |

## Version-history spike

The current version-history spike tests whether Guatemala can support a Legalize-style reconstruction strategy.

Spike target:

- Base law: Decreto 101-97, Ley Orgánica del Presupuesto.
- Reform decree: Decreto 13-2013.

Current evidence:

- `sample-budget-law.txt` contains repeated reform annotations.
- `Decreto Número 13-2013` appears 44 times in the consolidated budget-law sample.
- `reform-decree-13-2013.txt` contains article-level reform operations.
- The operation extractor identified 47 operation chunks.
- Only 2 targets were missing in the first operation-extraction pass.
- The replacement-body extractor extracted 34 replacement bodies.

Current conclusion:

```text
The Guatemala version-history spike preliminarily passes for a reconstruction-based strategy.
```

This does not yet prove full automated historical fidelity, but it shows that at least one official reform decree provides article-level operations and replacement text sufficient to reconstruct at least one historical reform commit for Decreto 101-97.

## Local quality gate status

See:

```text
docs/QUALITY-GATE-GT.md
```

Current local decision:

```text
PARTIAL PASS
```

Meaning:

- Text extraction works on the selected fixtures.
- Structural parsing works across the 5 primary fixtures.
- Markdown rendering works with metadata frontmatter.
- Initial artifact cleanup works.
- Metadata is still fixture-based.
- Full source discovery, publication-date resolution, tables/annexes, and production bootstrap are still pending.

## Known limitations

1. This is not yet an official Legalize country integration.
2. Metadata is currently fixture-based.
3. Discovery is currently fixture-based.
4. No live Congreso scraper exists yet.
5. No live DCA publication-date resolver exists yet.
6. No official source URL resolver has been implemented.
7. Tables and annexes need further validation.
8. Historical reconstruction is proven only as a spike using Decreto 101-97 and Decreto 13-2013.
9. The parser still needs stronger handling for table-of-contents artifacts, especially in the Constitution.
10. The parser currently relies on pre-extracted `.txt` files generated from PDFs.
11. Not all fixtures have final source-classification confidence.
12. The output is not legal advice and must not be treated as an authoritative legal consolidation.

## Git hygiene

Generated outputs are intentionally ignored:

```text
tmp/
__pycache__/
.pytest_cache/
.DS_Store
```

Do not commit generated `tmp/parsed` or `tmp/rendered` outputs unless explicitly needed for a release artifact or review snapshot.

## Next milestones

### Milestone 1: complete metadata

- Add official source URLs.
- Add publication dates.
- Add issuing body.
- Add source classification for each fixture.
- Add DCA publication references where available.
- Add metadata tests for required fields.

### Milestone 2: live source discovery

Implement official-source discovery against:

- Congreso de la República.
- Diario de Centro América.

Initial target:

```text
discover official PDFs and metadata for a small set of known laws.
```

### Milestone 3: formal parser integration

Prepare a Legalize-style parser interface.

Expected files:

```text
src/legalize/fetcher/gt/parser.py
tests/test_parser_gt.py
```

The current implementation already exists locally, but must be adapted to the expected interfaces of `legalize-dev/legalize-pipeline`.

### Milestone 4: formal 5-law quality gate

Review 5 rendered Markdown outputs for:

1. Text correctness.
2. Metadata completeness.
3. Structure preservation.
4. Rich formatting.
5. Encoding and hygiene.

### Milestone 5: prepare upstream PR

Target repository:

```text
legalize-dev/legalize-pipeline
```

Potential PR title:

```text
feat(gt): add Guatemala legislation fetcher
```

PR should include:

- `RESEARCH-GT.md`
- Guatemala fixtures
- Parser implementation
- Metadata strategy
- Tests
- Quality-gate evidence
- Version-history spike evidence

## Development commands

Run extraction:

```bash
python scripts/extract_fixture_text.py
```

Run structural diagnosis:

```bash
python scripts/diagnose_structure.py > tmp/extracted/gt/structure-diagnosis.txt
```

Build samples:

```bash
PYTHONPATH=src python scripts/build_gt_samples.py
```

Run tests:

```bash
PYTHONPATH=src pytest tests -q
```

Check rendered article counts:

```bash
grep -c "^##### " tmp/rendered/gt/*.md
```

Check common artifacts:

```bash
grep -niE "INFILE|Queda rigurosamente|uso exclusivo|Página [0-9]+/[0-9]+|NÚMER029|Departamento de Información Legislativa|Ã|�|â|<[^>]+>" tmp/rendered/gt/*.md | head -30
```

## Disclaimer

This repository is a research prototype. It does not provide legal advice and does not claim to be an official or authoritative consolidation of Guatemalan law.

Official sources must always be consulted for legal interpretation, legal compliance, and authoritative text.
