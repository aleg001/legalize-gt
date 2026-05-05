# RESEARCH-GT.md

# Guatemala (`gt`) Research Notes

## Status

Initial research document for adding Guatemala (`gt`) to Legalize.

This document follows the Legalize new-country playbook. It documents official sources, available formats, metadata, formatting structures, historical-version strategy, scope estimates, and known limitations before implementing a country fetcher.

## Executive summary

Guatemala does not currently appear to expose a Spain-style consolidated legislative API with embedded historical versions. The initial strategy is therefore conservative:

1. Use official sources only.
2. Start with a small set of representative laws and decrees.
3. Preserve source fidelity before attempting large-scale bootstrap.
4. Treat historical reconstruction as a documented research gate.
5. Do not claim full consolidated legal history until the version-history spike passes.

Primary sources under evaluation:

- Congreso de la República de Guatemala
- Diario de Centro América, edición legal
- Official institutional compilations where necessary, marked as secondary sources

---

## 0.1 Identify source(s)

### Source A: Congreso de la República de Guatemala

**Base URL:** `https://www.congreso.gob.gt`

**Relevant sections:**

- Legislative decrees search/listing
- PDF assets under `/assets/uploads/info_legislativo/decretos/`
- Institutional legal framework pages
- Initiative and reform PDFs under `/assets/uploads/info_legislativo/iniciativas/`

**Observed data:**

The Congreso website exposes decree listings and PDF assets. Some entries identify reforms, summaries, decree numbers and download/detail links.

**Known examples:**

- Decreto 57-2008, Ley de Acceso a la Información Pública
- Decreto 12-2002, Código Municipal
- Decreto 101-97, Ley Orgánica del Presupuesto
- Decreto 114-97, Ley del Organismo Ejecutivo

**Strengths:**

- Official legislative source
- Provides decree PDFs
- Provides issue/decree metadata in listings
- Useful for original laws and reform decrees

**Weaknesses / risks:**

- Not confirmed to expose consolidated historical versions
- Many documents are PDFs
- PDF quality may vary
- Reform detection may require parsing decree text, not only metadata
- Some documents may be scans or have OCR artifacts
- Need to distinguish law text, reform text, initiatives, and non-enacted documents

**Access pattern:**

- HTML listing pages
- PDF downloads
- No authentication observed
- Rate limits unknown
- Robots.txt and crawl-delay still need to be checked before bootstrap

**Source classification:**

`official_primary` for enacted decree PDFs and official decree listing.

---

### Source B: Diario de Centro América, edición legal

**Base URL:** `https://legal.dca.gob.gt` / `https://dca.gob.gt`

**Relevant sections:**

- Edición legal
- Decretos
- Acuerdos gubernativos
- Acuerdos ministeriales
- Resoluciones
- Actas municipales
- Acuerdos municipales
- Avisos and other legal notices

**Observed data:**

The Diario de Centro América is the official publication channel for laws and other legal instruments. The DCA website identifies itself as a publishing organ for laws and other regulations.

**Strengths:**

- Official publication source
- Useful for publication dates
- Useful for daily monitoring
- Useful for decrees, agreements, resolutions, and other legal instruments

**Weaknesses / risks:**

- Search interface may be dynamic
- Historical depth must be confirmed
- PDF/HTML availability may vary
- Need to determine whether entries expose stable IDs, document type, publication date, edition number, and downloadable text

**Access pattern:**

- Web search / legal search interface
- Details to be confirmed
- Rate limits unknown
- Robots.txt and crawl-delay still need to be checked

**Source classification:**

`official_primary_publication`.

---

### Source C: Institutional compilations

Potential institutional sources:

- Organismo Judicial
- Tribunal Supremo Electoral
- Ministerio de Finanzas Públicas
- Contraloría General de Cuentas
- ONSEC
- SEGEPLAN
- Relevant ministries depending on subject matter

**Use policy:**

Institutional compilations may be used only as secondary references unless they clearly reproduce official published law text. They must not override official publication sources.

**Source classification:**

`official_secondary` or `institutional_compilation`.

---

## 0.2 Save 5 representative fixtures

Fixtures should be stored under:

```text
engine/tests/fixtures/gt/
```

Initial fixture candidates:

| Fixture file | Norm | Type | Source | Format | Purpose |
|---|---|---|---|---|---|
| `sample-constitution.pdf` | Constitución Política de la República de Guatemala | Constitution | Congreso / official compilation | PDF | Highest-rank norm |
| `sample-ordinary-law-laip.pdf` | Decreto 57-2008, Ley de Acceso a la Información Pública | Ordinary law | Congreso | PDF | Clean ordinary law sample |
| `sample-code-codigo-municipal.pdf` | Decreto 12-2002, Código Municipal | Code / framework law | Congreso | PDF | Structured law with titles/chapters/articles |
| `sample-budget-law.pdf` | Decreto 101-97, Ley Orgánica del Presupuesto | Ordinary law | Congreso / MINFIN | PDF | Public finance/legal metadata |
| `sample-with-tables.pdf` | Law or regulation with tables, tariff schedule, fees, annexes, or forms | Regulation/annex | DCA/Congreso | PDF/HTML | Table and annex parser test |

Minimum fixture requirements:

- At least one law with titles, chapters, and articles.
- At least one law with enumerated lists.
- At least one document with tables or annexes.
- At least one reform decree, if available.
- At least one document with publication metadata from DCA, if available.

Notes:

- If no table-heavy law is found in the first search, continue searching in tax, tariff, budget, procurement, municipal, or administrative fee regulations.
- Do not proceed to quality gate without a table/annex sample unless the absence is explicitly documented.

### Fixture source warning

`sample-ordinary-law-laip.pdf` appears to come from INFILE, S.A. or an institutional/legal compilation rather than a clean official source PDF. The rendered Markdown contains repeated proprietary/access notices such as:

- `Queda rigurosamente prohibida... INFILE, S.A.`
- `El documento fue generado para el uso exclusivo de...`

This fixture is useful for parser stress-testing, but should not be treated as an official primary source for Legalize bootstrap.

Action required:

- Replace `sample-ordinary-law-laip.pdf` with a clean official Congreso or Diario de Centro América source PDF.
- Until replaced, mark this fixture as `source_type: institutional_or_third_party_compilation`.
- Do not use this file for final quality-gate review.

### LAIP fixture replacement

The original `sample-ordinary-law-laip.pdf` was identified as a third-party/institutional compilation containing INFILE notices and access restrictions. It was replaced with:

`sample-ordinary-law-laip-official.pdf`

This official-source fixture should be used for parser validation and quality-gate review. The previous INFILE-based fixture, if retained, must be treated only as a stress-test document and excluded from official quality-gate evidence.

---

## 0.3 Metadata inventory

### Generic metadata fields to capture

| Source field | Type | Example | Maps to | Notes |
|---|---|---|---|---|
| Country | string | `gt` | `NormMetadata.country` | ISO 3166-1 alpha-2 |
| Title | string | `Ley de Acceso a la Información Pública` | `NormMetadata.title` | Official title |
| Short title | string | `LAIP` | `NormMetadata.short_title` | Only if official/common |
| Identifier | string | `DECRETO-57-2008` | `NormMetadata.identifier` | Must be filesystem-safe |
| Rank/type | string | `decreto`, `ley`, `codigo`, `acuerdo_gubernativo` | `NormMetadata.rank` | Use source-native rank |
| Publication date | date | `2008-10-23` | `NormMetadata.publication_date` | Prefer DCA publication date |
| Effective date | date | `2009-04-20` | `extra.effective_date` or version date | Only if source provides it |
| Status | enum | `in_force`, `repealed`, `unknown` | `NormMetadata.status` | Do not infer unless verified |
| Department/body | string | `Congreso de la República` | `NormMetadata.department` | Issuing body |
| Source URL | URL | Congreso/DCA URL | `NormMetadata.source` | Official URL |
| PDF URL | URL | PDF asset URL | `NormMetadata.pdf_url` | If available |
| Jurisdiction | string | `GT` | `NormMetadata.jurisdiction` | National unless subnational |
| Last modified | date | unknown | `NormMetadata.last_modified` | If exposed |
| Subjects | list | `transparencia`, `contrataciones` | `NormMetadata.subjects` | If source exposes or controlled taxonomy exists |
| Summary | string | Listing summary | `NormMetadata.summary` | Use official summary only |

### Guatemala-specific metadata fields for `extra`

| Source field | Type | Example | Maps to | Notes |
|---|---|---|---|---|
| Decree number | string | `57-2008` | `extra.decree_number` | Keep original number |
| Gazette name | string | `Diario de Centro América` | `extra.gazette_name` | Publication source |
| Gazette edition | string | TBD | `extra.gazette_edition` | If DCA exposes |
| Emission date | date | `2008-09-23` | `extra.emission_date` | Congreso listing may expose |
| Sanction date | date | TBD | `extra.sanction_date` | If available |
| Promulgation date | date | TBD | `extra.promulgation_date` | If available |
| Entry into force text | string | `ocho días después...` | `extra.entry_into_force_text` | Preserve raw text |
| Source type | string | `official_primary` | `extra.source_type` | Important for trust |
| Source SHA-256 | string | hash | `extra.source_sha256` | Hash original PDF/HTML |
| Parser version | string | `gt-pdf-0.1.0` | `extra.parser_version` | For reproducibility |
| Extraction method | string | `pymupdf`, `pdfplumber`, `ocr` | `extra.extraction_method` | Distinguish OCR |
| OCR required | boolean | `false` | `extra.ocr_required` | If scanned |
| Images dropped | integer | `0` | `extra.images_dropped` | Required if images skipped |
| Tables detected | integer | `0` | `extra.tables_detected` | Useful quality flag |
| Confidence | string | `low`, `medium`, `high` | `extra.confidence` | Parser confidence |

### Metadata policy

- Capture every field exposed by official sources.
- Do not invent status, dates, publication number, or effective date.
- If a field is uncertain, set it to `null` or omit it and document the gap.
- Use English snake_case keys in `extra`.
- Preserve original Spanish legal terms in title/body.
- Dates must be ISO-8601.

---

## 0.4 Formatting inventory

Initial expected formatting structures in Guatemalan legal documents:

| Construct | Expected? | Parser strategy | Notes |
|---|---:|---|---|
| Titles | yes | `titulo_tit` / Markdown `##` | e.g. `TÍTULO PRIMERO` |
| Chapters | yes | `capitulo_tit` / Markdown `###` | e.g. `CAPÍTULO PRIMERO` |
| Sections | possible | `seccion` / Markdown `####` | verify in fixtures |
| Articles | yes | `articulo` / Markdown `#####` | e.g. `Artículo 1. Objeto` |
| Numbered lists | yes | Markdown ordered or preserved numbered paragraphs | Common in articles |
| Lettered clauses | yes | Preserve `a)`, `b)`, `c)` | Do not flatten |
| Roman numerals | possible | Preserve as source text | Common in titles/chapters |
| Tables | likely | Markdown pipe tables | Search in tax/tariff/budget/procurement docs |
| Annexes | likely | `Block(block_type="annex")` | Must not be dropped |
| Footnotes | possible | Markdown footnotes or preserved parenthetical notes | verify |
| Bold | possible | `**text**` | PDF extraction may not preserve |
| Italic | possible | `*text*` | PDF extraction may not preserve |
| Cross-references | yes | Plain text first, links later if reliable | Do not invent links |
| Quotations/amending text | yes | Markdown blockquote | Especially in reform decrees |
| Signatories | yes | bold paragraph or signature block | Preserve names/titles |
| Page headers/footers | yes | strip | Must not leak into Markdown |
| Page numbers | yes | strip | Common PDF artifact |
| Stamps/seals/images | possible | drop with `[image omitted]` if meaningful | Count in metadata |

### Formatting risks

- PDF line breaks may split sentences.
- Accents and special characters may be corrupted.
- OCR may confuse `Artículo`, `Articulo`, `Artlculo`, `ArtícuIo`.
- Headers and footers may appear on every page.
- Tables may be flattened into unreadable text.
- Reform decrees may quote replacement article text that must be preserved exactly.

### Parser rules

- Preserve article order exactly.
- Do not deduplicate paragraphs unless exact PDF artifact is confirmed.
- Do not modernize spelling.
- Do not add accents or correct OCR errors silently.
- Do not convert legal text into summaries.
- No leftover PDF artifacts, HTML/XML tags, control characters, or mojibake.

---

## 0.5 Version history spike

### Goal

Validate whether Guatemala can support Legalize-style historical commits:

```text
One law file.
Each reform becomes one git commit.
Each commit is dated with the reform/effective/publication date.
```

### Candidate law for spike

Primary candidate:

```text
Ley de Acceso a la Información Pública
Decreto 57-2008
```

Reason:

- Official source PDF exists.
- Reform initiatives and reform-related documents are discoverable.
- The law has clear article structure.
- It is important for civic tech and public accountability.

Alternative candidates:

```text
Ley de Contrataciones del Estado, Decreto 57-92
Código Municipal, Decreto 12-2002
Código de Comercio, Decreto 2-70
Ley Orgánica del Presupuesto, Decreto 101-97
```

### Evidence to collect

Create:

```text
engine/tests/fixtures/gt/version-spike.txt
```

Expected content:

```text
Law: Ley de Acceso a la Información Pública
Base identifier: DECRETO-57-2008

Version 1:
  source_type: official_primary
  source: Congreso PDF / DCA publication
  date_type: publication_date or emission_date
  date: YYYY-MM-DD
  text_available: yes
  stable_identifier: DECRETO-57-2008
  notes: Original law text.

Version 2:
  source_type: official_primary
  source: reform decree PDF / DCA publication
  reform_decree: XX-YYYY
  date_type: publication_date or emission_date
  date: YYYY-MM-DD
  affected_articles:
    - Article X
    - Article Y
  replacement_text_available: yes/no
  stable_identifier: DECRETO-57-2008
  notes: Reform text quotes replacement article or requires reconstruction.

Conclusion:
  historical_versions_available: yes / partial / no
  strategy: consolidated API / reform-decree reconstruction / snapshot only
  blocker: if any
```

### Pass condition

The spike passes only if:

- At least 2 versions of the same law can be identified.
- Each version has a usable date.
- The affected law can be linked to a stable identifier.
- The reform text or consolidated text can be obtained.

### If the spike fails

Document:

```text
Guatemala sources reviewed do not expose consolidated historical versions in an API or version table.
Initial implementation must be snapshot/decree-based.
Historical reconstruction requires a follow-up task using reform decrees and manual/legal validation.
```

Do not implement full historical bootstrap until this is resolved.

### Reform-note extraction from budget law

A first reform-note extraction was run against:

`tmp/extracted/gt/sample-budget-law.txt`

Command:

    grep -niE "Reformado|Reformada|Reformadas|Adicionado|Adicionada|Adicionadas|Derogado|Derogada|Derogadas" tmp/extracted/gt/sample-budget-law.txt > tmp/extracted/gt/budget-reform-notes.txt

The extracted notes show repeated references to several reform decrees.

Reform decree frequency:

| Reform decree | Count |
|---|---:|
| Decreto Número 13-2013 | 44 |
| Decreto Número 71-98 | 6 |
| Decreto Número 9-2014 | 3 |
| DECRETO NÚMERO 101-97 | 1 |

Examples:

    *Reformado por el Artículo 1, del Decreto Número 13-2013 el 20-11-2013
    *Reformadas literales c) y d), y adicionadas e), f) y g), por el Artículo 2, del Decreto Número 13-2013
    *Adicionado por el Artículo 5, del Decreto Número 13-2013 el 20-11-2013
    *Reformado por el Artículo 1, del Decreto Número 9-2014 el 03-03-2014
    *Reformado por el Artículo 1 del Decreto Número 71-98 del Congreso de la República

Initial conclusion:

`sample-budget-law.pdf` contains enough reform annotations to support a partial historical-version strategy. The strongest first spike target is Decreto Número 13-2013 because it appears 44 times in the extracted budget-law text.

However, this does not yet fully pass the Legalize version-history gate. The next required step is to obtain the official Decreto 13-2013 PDF, extract its text, and verify the affected articles and replacement text against Decreto 101-97.

### Version-history spike update: Decreto 13-2013

The first reform-decree spike was run against:

- Base law: `sample-budget-law.pdf`
- Reform decree: `reform-decree-13-2013.pdf`
- Base extracted text: `tmp/extracted/gt/sample-budget-law.txt`
- Reform extracted text: `tmp/extracted/gt/reform-decree-13-2013.txt`

Extraction result:

| Document | Pages | Extracted characters | Extraction method | Status |
|---|---:|---:|---|---|
| `sample-budget-law.pdf` | 37 | 107,926 | PyMuPDF `page.get_text("text")` | pass |
| `reform-decree-13-2013.pdf` | 16 | 126,775 | PyMuPDF `page.get_text("text")` | pass |

The extracted reform decree explicitly references the base law:

    REFORMAS AL DECRETO NÚMERO 101-97 DEL CONGRESO DE LA REPÚBLICA, LEY ORGÁNICA DEL PRESUPUESTO

It also exposes article-level reform operations such as:

    ARTÍCULO 1. Se reforma el artículo 1 del Decreto Número 101-97...
    ARTÍCULO 2. Se reforman las literales ... y se adicionan ...
    ARTÍCULO 5. Se adiciona el artículo 7 Bis...
    ARTÍCULO 7. Se reforma el artículo 12...
    ARTÍCULO 24. Se reforma el artículo 38...

The reform decree includes replacement text using patterns such as:

    el cual queda así:
    Artículo 1. Objeto...
    Artículo 7 Bis. Proceso Presupuestario...

This means Guatemala does not appear to have a Spain-style embedded historical XML API, but reform-decree reconstruction is feasible for at least this sample.

Current gate status:

    preliminary_pass

Reason:

- At least two relevant legal states can be identified:
  - Base law: Decreto 101-97.
  - Reform event: Decreto 13-2013.
- The reform decree has a usable date from the consolidated note: 2013-11-20.
- The reform decree explicitly identifies affected articles.
- The reform decree contains replacement text.

Remaining blockers:

- Confirm official publication/effective dates from DCA or official decree metadata.
- Extract article-level replacement bodies reliably.
- Compare extracted reform bodies against the consolidated base-law sample.
- Decide whether the first bootstrap can reconstruct history fully or ship with a documented partial-history strategy.

### Reform operation extractor result

A first operation extractor was tested on:

`tmp/extracted/gt/reform-decree-13-2013.txt`

Command:

    python scripts/extract_reform_operations.py

Output:

    tmp/extracted/gt/reform-operations-13-2013.txt

Result:

| Metric | Value |
|---|---:|
| Extracted operation chunks | 47 |
| Missing target count | 2 |
| Preliminary quality | usable for spike |

Examples of extracted operations:

| Decree article | Operation | Target article | Replacement detected |
|---:|---|---|---|
| 1 | reforma | 1 | yes |
| 5 | adiciona | 7 Bis | yes |
| 8 | adiciona | 17 Bis | yes |
| 9 | adiciona | 17 Ter | yes |
| 10 | adiciona | 17 Quáter | yes |
| 13 | adiciona | 26 Bis | yes |
| 15 | adiciona | 29 Bis | yes |
| 17 | adiciona | 30 Bis | yes |

Updated spike conclusion:

The Guatemala version-history spike preliminarily passes for a reconstruction-based strategy. Guatemala does not currently appear to expose a Spain-style embedded historical XML API, but Decreto 13-2013 provides article-level operations and replacement text sufficient to reconstruct at least one reform commit for Decreto 101-97.

Remaining work:

- Fix the remaining 2 missing targets.
- Extract replacement bodies cleanly.
- Compare extracted replacement bodies against the consolidated budget-law text.
- Confirm official publication/effective dates from DCA or official decree metadata.


### Replacement body extraction result

A first replacement-body extractor was tested on:

`tmp/extracted/gt/reform-decree-13-2013.txt`

Command:

    python scripts/extract_replacement_bodies.py

Output:

    tmp/extracted/gt/replacement-bodies-13-2013.txt

Result:

| Metric | Value |
|---|---:|
| Reform operation chunks available | 47 |
| Replacement bodies extracted | 34 |
| Operations without extracted body | 13 |
| Preliminary quality | viable for reconstruction spike |

Observed replacement examples:

| Decree article | Replacement preview |
|---:|---|
| 1 | `Artículo 1. Objeto...` |
| 4 | `Artículo 4. Rendición de Cuentas...` |
| 5 | `Artículo 7 Bis. Proceso Presupuestario...` |
| 6 | Replacement paragraphs for article 8 |
| 7 | `Artículo 12. Presupuestos de Egresos...` |

Known extraction issues:

- Some DCA/Congreso page artifacts still leak into replacement bodies.
- Some operations affect only literals or paragraphs, not entire articles.
- 13 operation chunks did not produce replacement bodies with the current heuristic.
- Some PDF/OCR artifacts remain in extracted text.

Updated conclusion:

The version-history spike is strong enough to justify a Guatemala parser with a reconstruction-based historical strategy. It does not yet prove complete automated historical fidelity, but it demonstrates that at least one official reform decree, Decreto 13-2013, provides article-level operations and extractable replacement text for Decreto 101-97.

Additional cleanup note:

The first page-artifact cleanup removed most DCA/Congreso headers and page numbers, but one OCR-like artifact remained: `NÚMER029`. A stricter line-level skip pattern is needed for malformed page headers such as `NÚMER029`, while preserving legitimate legal references such as `Decreto Número 101-97`.

### Replacement cleanup result

After adding stricter line-level cleanup patterns, malformed page artifacts such as `NÚMER029`, `DIARIO de CENTRO AMÉRICA`, and `Departamento de Información Legislativa` no longer appear in replacement-body output.

The remaining `Número` matches are legitimate legal references, for example:

- `Decreto Número 101-97`
- `Número de beneficiarios`
- `Número y fecha del convenio`

Current replacement extraction result:

| Metric | Value |
|---|---:|
| Replacement bodies extracted | 34 |
| Page-artifact grep hits | 0 problematic hits |
| Remaining `Número` hits | legitimate legal references |

Conclusion:

The replacement-body extraction is sufficiently clean for the version-history spike. Further cleanup should move into the production parser rather than continue as ad hoc research scripts.

### Preliminary structural parser result

A first structural parser was tested with `scripts/parse_gt_pdf.py`.

The parser reads PyMuPDF-extracted text from official PDF fixtures and emits preliminary JSON blocks with the following block types:

- `preamble`
- `title`
- `chapter`
- `section`
- `article`
- `reform_note`

The parser was corrected to process only source texts extracted from PDF fixtures, excluding intermediate research artifacts such as `budget-reform-notes.txt`, `structure-diagnosis.txt`, `reform-operations-13-2013.txt`, and `replacement-bodies-13-2013.txt`.

| Source text | Total blocks | Articles | Titles | Chapters | Sections | Reform notes |
|---|---:|---:|---:|---:|---:|---:|
| `reform-decree-13-2013.txt` | 86 | 83 | 0 | 2 | 0 | 0 |
| `sample-budget-law.txt` | 178 | 103 | 10 | 4 | 5 | 55 |
| `sample-civic-service.txt` | 68 | 54 | 0 | 8 | 5 | 0 |
| `sample-code-codigo-municipal.txt` | 211 | 178 | 8 | 24 | 0 | 0 |
| `sample-constitution.txt` | 376 | 311 | 16 | 29 | 19 | 0 |
| `sample-ordinary-law-laip.txt` | 91 | 72 | 5 | 13 | 0 | 0 |

Initial conclusion:

The parser can detect legal structure across all selected Guatemala fixtures. Results are promising enough to proceed to Markdown rendering, but still require manual review for false positives, table-of-contents artifacts, duplicated article detections, and PDF extraction noise.

---

## 0.6 Estimate total scope

### Initial MVP scope

Target: 5 to 10 laws.

Candidate laws:

| Identifier | Title | Priority | Reason |
|---|---|---:|---|
| CONSTITUCION-GT | Constitución Política de la República de Guatemala | 1 | Highest-rank norm |
| DECRETO-57-2008 | Ley de Acceso a la Información Pública | 1 | Civic tech/transparency |
| DECRETO-57-92 | Ley de Contrataciones del Estado | 1 | Public procurement |
| DECRETO-101-97 | Ley Orgánica del Presupuesto | 1 | Public finance |
| DECRETO-114-97 | Ley del Organismo Ejecutivo | 1 | Executive branch structure |
| DECRETO-12-2002 | Código Municipal | 2 | Municipal governance |
| DECRETO-1-85 | Ley Electoral y de Partidos Políticos | 2 | Democracy/elections |
| DECRETO-1748 | Ley de Servicio Civil | 2 | Public employment |
| DECRETO-89-2002 | Ley de Probidad | 2 | Public integrity |
| ORGANISMO-LEGISLATIVO | Ley Orgánica del Organismo Legislativo | 2 | Legislative branch |

### Estimated full scope

Unknown at this stage.

Research tasks:

- Count all decrees listed by Congreso.
- Count all DCA legal publications by category and year.
- Identify whether official sources expose a machine-readable catalog.
- Identify how many documents are PDF, HTML, XML, DOCX, or image scans.
- Identify how many are base laws versus reform decrees, agreements, resolutions, notices, or municipal acts.

### Expected fetch cost

Initial MVP:

```text
5 to 10 documents
10 to 30 HTTP requests
Manual verification required
```

Expanded corpus:

```text
Unknown until discovery endpoint/catalog is mapped.
If only HTML/PDF scraping is available, use max_workers=1 or 2 initially.
```

### Known blockers

- No confirmed consolidated historical API.
- PDF-heavy sources.
- Possible OCR/scanned PDFs.
- Need to distinguish enacted laws from initiatives.
- Need official publication dates from DCA.
- Need licensing/redistribution confirmation.
- Need robots.txt/crawl-delay review.

---

## 0.7 Format-coverage table

### Initial observation

Guatemala appears to expose much of the legislative corpus through PDF and HTML listing pages. A structured XML/JSON bulk API has not yet been confirmed.

### Format coverage, preliminary

| Format | Source | Total laws with ≥1 version | Unique coverage | % catalogue | Covered in fetcher? | Notes |
|---|---|---:|---:|---:|---|---|
| PDF | Congreso / DCA | TBD | TBD | TBD | yes, initial | Primary likely format |
| HTML listing | Congreso / DCA | TBD | TBD | TBD | yes, discovery only | Used for metadata/discovery |
| HTML full text | DCA / others | TBD | TBD | TBD | TBD | Verify availability |
| XML | Unknown | 0/TBD | TBD | TBD | no | No official XML source found yet |
| JSON API | Unknown | 0/TBD | TBD | TBD | no | No official JSON API found yet |
| DOC/DOCX | Institutional compilations | TBD | TBD | TBD | no initially | Use only if >1% unique or needed |
| Scanned image PDF | Historical sources | TBD | TBD | TBD | no initially | OCR only if justified |

### Coverage decision

Initial fetcher should support:

1. HTML discovery
2. PDF download
3. PDF text extraction
4. PDF metadata hashing

Do not support OCR in the first parser unless a selected fixture requires it. If OCR is required, mark confidence as `low` and document the extraction method.

### Cross-format fidelity check

Pending.

Required only if the same law has adjacent versions across multiple formats, e.g.:

```text
Version N: PDF from Congreso
Version N+1: HTML or PDF from DCA
```

If found, render both and verify that format differences do not create artificial structural diffs.

---

## Proposed implementation strategy

### Initial country code

```text
gt
```

### Initial fetcher package

```text
src/legalize/fetcher/gt/
  __init__.py
  client.py
  discovery.py
  parser.py
```

### Initial parser strategy

1. Download official PDF.
2. Compute SHA-256.
3. Extract text using PyMuPDF and pdfplumber.
4. Compare extraction quality.
5. Normalize UTF-8.
6. Strip repeated headers/footers and page numbers.
7. Detect structural headings:
   - `TÍTULO`
   - `CAPÍTULO`
   - `SECCIÓN`
   - `Artículo`
8. Preserve lists and quoted reform text.
9. Detect tables if text layout allows.
10. Emit Legalize `Block`, `Version`, `Paragraph`, and `NormMetadata`.

### Initial limitations

- No claim of complete national corpus.
- No claim of fully consolidated historical versions until spike passes.
- No legal advice.
- No silent OCR correction.
- No use of unofficial legal websites as authoritative sources.

---

## Quality gate plan

Before bootstrap, render 5 laws and review:

1. Text correctness
2. Metadata completeness
3. Structure preservation
4. Rich formatting
5. Encoding and hygiene

Do not proceed until:

```text
SUMMARY: 5/5 laws fully PASS
```

---

## Open questions

1. Does Congreso expose a machine-readable catalog of all decrees?
2. Does DCA expose stable URLs and metadata for legal publications?
3. Does DCA search cover all historical legal publications or only recent years?
4. Are publication dates available in structured form?
5. Can historical consolidated versions be obtained anywhere officially?
6. Are reform decrees sufficient to reconstruct article-level history?
7. What is the legal status/licensing of republishing official legal text?
8. How many PDFs are scanned versus text-based?
9. Which source should be considered authoritative when Congreso and DCA differ?
10. Should Guatemala initially ship as `snapshot`, `decree-based`, or `consolidated-history`?

---

## Current recommendation

Proceed only with Step 0 until the following artifacts exist:

- `RESEARCH-GT.md`
- 5 fixture files
- `version-spike.txt`
- metadata inventory
- formatting inventory
- preliminary format coverage table

Do not implement `fetcher/gt` until the version-history spike has been attempted and documented.
