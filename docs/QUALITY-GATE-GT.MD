# QUALITY-GATE-GT.md

# Guatemala (`gt`) Local Quality Gate

This document records the local quality review for the first Guatemala parser/rendering prototype.

This is not yet the official Legalize Step 7 quality gate. It is a pre-gate review used to decide whether the Guatemala parser is ready to be migrated from exploratory scripts into `src/legalize/fetcher/gt/parser.py`.

## Scope

Reviewed rendered Markdown files:

| Rendered file | Source fixture | Included in local gate? | Notes |
|---|---|---:|---|
| `tmp/rendered/gt/sample-budget-law.md` | `sample-budget-law.pdf` | yes | Budget/public finance law, includes reform notes |
| `tmp/rendered/gt/sample-civic-service.md` | `sample-civic-service.pdf` | yes | Administrative/public-service law |
| `tmp/rendered/gt/sample-code-codigo-municipal.md` | `sample-code-codigo-municipal.pdf` | yes | Code/framework law |
| `tmp/rendered/gt/sample-constitution.md` | `sample-constitution.pdf` | yes | Highest-rank constitutional norm |
| `tmp/rendered/gt/sample-ordinary-law-laip-official.md` | `sample-ordinary-law-laip-official.pdf` | yes | Official LAIP fixture |
| `tmp/rendered/gt/reform-decree-13-2013.md` | `reform-decree-13-2013.pdf` | supplementary | Used for version-history spike, not part of the 5-law local gate |

## Current parser/rendering scripts

- `scripts/extract_fixture_text.py`
- `scripts/diagnose_structure.py`
- `scripts/parse_gt_pdf.py`
- `scripts/render_gt_markdown.py`
- `scripts/extract_reform_operations.py`
- `scripts/extract_replacement_bodies.py`

## Structure diagnosis summary

Generated with:

    python scripts/diagnose_structure.py > tmp/extracted/gt/structure-diagnosis.txt

Current structure-diagnosis result:

| Source text | Article headings | Title headings | Chapter headings | Reform notes | Mojibake |
|---|---:|---:|---:|---:|---:|
| `sample-budget-law.txt` | 103 | 10 | 4 | 57 | 0 |
| `sample-civic-service.txt` | 54 | 0 | 8 | 0 | 0 |
| `sample-code-codigo-municipal.txt` | 178 | 8 | 24 | 0 | 0 |
| `sample-constitution.txt` | 311 | 16 | 54 | 1 | 0 |
| `sample-ordinary-law-laip-official.txt` | 73 | 5 | 13 | 0 | 0 |
| `reform-decree-13-2013.txt` | 83 | 0 | 2 | 0 | 0 |

Initial diagnosis:

- All reviewed source texts are extractable with PyMuPDF.
- All five primary fixtures expose article-level structure.
- No initial mojibake markers were detected.
- The official LAIP fixture replaced the previous third-party/INFILE-based fixture.
- The Constitution includes table-of-contents-like chapter lines that still require special handling.
- The budget law includes many reform notes and remains the strongest source for the version-history spike.

## Rendered Markdown sanity checks

Commands:

    grep -c "^##### " tmp/rendered/gt/*.md

Observed article-heading counts:

| Rendered Markdown | Article headings |
|---|---:|
| `reform-decree-13-2013.md` | 83 |
| `sample-budget-law.md` | 103 |
| `sample-civic-service.md` | 54 |
| `sample-code-codigo-municipal.md` | 178 |
| `sample-constitution.md` | 311 |
| `sample-ordinary-law-laip-official.md` | 73 |

Artifact/encoding command:

    grep -niE "INFILE|Queda rigurosamente|uso exclusivo|Página [0-9]+/[0-9]+|NÚMER029|DIARIO de CENTRO AMÉRICA|Departamento de Información Legislativa|Ã|�|â|<[^>]+>" tmp/rendered/gt/*.md | head -30

Observed result:

- No INFILE notices.
- No proprietary access notices.
- No malformed `NÚMER029` artifact.
- No mojibake markers found.
- One `Diario de Centro América` match appears in the LAIP official rendered Markdown as legal body text, not as a page artifact.

## Five quality checks

Each primary file must be graded PASS / FAIL / NEEDS REVIEW.

### 1. Text correctness

Checks:

- No mojibake.
- No leftover HTML/XML tags.
- No obvious truncated sections.
- No duplicated page headers.
- No third-party notices.
- No page-number artifacts.
- Legal text remains in Spanish and is not summarized.

| File | Status | Notes |
|---|---|---|
| `sample-budget-law.md` | NEEDS REVIEW | Reform notes preserved. Requires manual review for PDF noise. |
| `sample-civic-service.md` | NEEDS REVIEW | Structure detected. Manual text review pending. |
| `sample-code-codigo-municipal.md` | NEEDS REVIEW | Structure detected. Manual text review pending. |
| `sample-constitution.md` | NEEDS REVIEW | Table-of-contents artifacts likely require handling. |
| `sample-ordinary-law-laip-official.md` | PASS | No INFILE artifacts; official fixture appears clean in initial checks. |

### 2. Metadata completeness

Current prototype metadata is minimal and fixture-based.

Current frontmatter includes:

- `country`
- `identifier`
- `title`
- `status`
- `source_type`
- `parser_version`

Required before official Legalize parser:

- official title
- official identifier/decree number
- rank/type
- source URL
- PDF URL
- source SHA-256
- publication date
- issuing body
- source type
- extraction method
- confidence/status

| File | Status | Notes |
|---|---|---|
| All rendered files | FAIL | Frontmatter is intentionally minimal in prototype. Full metadata parser is not implemented yet. |

### 3. Structure preservation

Checks:

- Titles render as `##`.
- Chapters render as `###`.
- Sections render as `####`.
- Articles render as `#####`.
- Reform notes render as blockquotes.
- Article order is preserved.
- No articles are skipped.
- No articles are duplicated.

| File | Status | Notes |
|---|---|---|
| `sample-budget-law.md` | NEEDS REVIEW | 103 article headings and 55 reform notes rendered. |
| `sample-civic-service.md` | NEEDS REVIEW | 54 article headings rendered. |
| `sample-code-codigo-municipal.md` | NEEDS REVIEW | 178 article headings rendered. |
| `sample-constitution.md` | NEEDS REVIEW | 311 article headings rendered; TOC requires careful review. |
| `sample-ordinary-law-laip-official.md` | NEEDS REVIEW | 73 article headings rendered. |

### 4. Rich formatting

Checks:

- Lists remain readable.
- Tables are preserved if present.
- Annexes are not silently dropped.
- Reform notes are preserved.
- Quoted replacement text is preserved.
- Signatories are preserved.

| File | Status | Notes |
|---|---|---|
| `sample-budget-law.md` | NEEDS REVIEW | Reform notes preserved; table handling not yet validated. |
| `sample-civic-service.md` | NEEDS REVIEW | Lists/signatories need review. |
| `sample-code-codigo-municipal.md` | NEEDS REVIEW | Lists and municipal structure need review. |
| `sample-constitution.md` | NEEDS REVIEW | Constitutional structure preserved; TOC and tables need review. |
| `sample-ordinary-law-laip-official.md` | NEEDS REVIEW | Lists appear readable; manual review pending. |

### 5. Encoding and hygiene

Checks:

- UTF-8.
- No C0/C1 control chars.
- No `Ã`, `�`, `â` mojibake.
- No HTML/XML tags.
- Unix line endings.
- Files end with a single newline.
- No obvious page artifacts.

Current status:

| File | Status | Notes |
|---|---|---|
| All rendered files | PASS preliminary | Initial grep found no mojibake or major artifacts. Full hygiene script still needed. |

## Known issues

1. Metadata is not production-ready.
2. Tables are not yet explicitly preserved as Markdown pipe tables.
3. Constitution table-of-contents lines may still be overcounted in `chapter_headings`.
4. Some PDF extraction artifacts remain possible even if not caught by grep.
5. The parser currently works from pre-extracted `.txt`, not directly from raw source bytes.
6. Reform reconstruction is proven only as a spike using Decreto 13-2013 and Decreto 101-97.
7. Official source URLs and publication/effective dates still need to be completed.
8. The previous INFILE-based LAIP fixture should not be used for official quality-gate review.

## Version-history spike status

Spike target:

- Base law: Decreto 101-97, Ley Orgánica del Presupuesto
- Reform decree: Decreto 13-2013

Current evidence:

| Metric | Value |
|---|---:|
| Reform operation chunks | 47 |
| Missing targets | 2 |
| Replacement bodies extracted | 34 |
| Preliminary status | reconstruction strategy viable |

Conclusion:

The Guatemala version-history spike preliminarily passes for a reconstruction-based strategy. Guatemala does not appear to expose a Spain-style embedded historical XML API, but Decreto 13-2013 provides article-level reform operations and extractable replacement text sufficient to reconstruct at least one historical reform commit for Decreto 101-97.

## Local gate decision

Current decision:

    PARTIAL PASS

Meaning:

- The text extraction, structural parsing, rendering, and reform spike are strong enough to proceed to a first Legalize-style parser implementation.
- The prototype is not yet ready for official bootstrap.
- The next milestone is to migrate the proven logic into `src/legalize/fetcher/gt/parser.py` with real metadata parsing and tests.

## Next actions

1. Implement `src/legalize/fetcher/gt/parser.py`.
2. Create `tests/test_parser_gt.py`.
3. Implement fixture-based tests for:
   - structure detection,
   - article counts,
   - mojibake absence,
   - metadata completeness,
   - reform operation extraction.
4. Add official source URLs and metadata fields to `RESEARCH-GT.md`.
5. Build a minimal sample Legalize output for 5 laws.
6. Run a formal AI review against the 5 rendered Markdown files.