# Guatemala fixtures

These files are representative official legal documents used for the initial Guatemala (`gt`) research and parser validation.

## Fixtures

| File | Norm | Type | Expected parser coverage |
|---|---|---|---|
| `sample-constitution.pdf` | Constitución Política de la República de Guatemala | Constitution | highest-rank norm, titles, chapters, articles |
| `sample-ordinary-law-laip.pdf` | Decreto 57-2008, Ley de Acceso a la Información Pública | Ordinary law | articles, chapters, definitions, public-law structure |
| `sample-code-codigo-municipal.pdf` | Decreto 12-2002, Código Municipal | Code / framework law | titles, chapters, articles, numerals |
| `sample-budget-law.pdf` | Decreto 101-97, Ley Orgánica del Presupuesto | Ordinary law / public finance | structured articles, budget/legal terminology |
| `sample-civic-service.pdf` | Ley de Servicio Cívico / civic service-related law | Public employment / civic service | administrative-law structure, public employment terminology |

## Notes

- All files must come from official or institutional sources.
- Original source URLs must be added to `RESEARCH-GT.md`.
- SHA-256 hashes must be generated for every fixture.
- If none of these files contains tables or annexes, a sixth fixture should be added as `sample-with-tables.pdf`.

### Fixture hashes

| Fixture | SHA-256 |
|---|---|
| `sample-budget-law.pdf` | `d491d52282d37271d9803d461125f5d6d98ee3926ae2ab9b19449c373d1c25c6` |
| `sample-civic-service.pdf` | `e07588e40dd31d32ced019398de8d1cf2117fee3119a128f3b118adc09eab18e` |
| `sample-code-codigo-municipal.pdf` | `e4ee12b68d0263f7b07d55bf5b719e335af4ab84f2df39b972b8e216c767c1c0` |
| `sample-constitution.pdf` | `499db915d59dbaa8a5176920722ee4659e4596f19d3d5943fb56d375d75bad4f` |
| `sample-ordinary-law-laip.pdf` | `3e4d1f5d0763b8bf46ba6057a241501496868464b22c96bab2f91cc91e22f529` |

### Initial text extraction results

Text extraction was tested with PyMuPDF using `page.get_text("text")`.

| Fixture | Pages | Extracted characters | Extraction status | Notes |
|---|---:|---:|---|---|
| `sample-budget-law.pdf` | 37 | 107,926 | pass | Text is extractable. Manual structure review pending. |
| `sample-civic-service.pdf` | 12 | 31,091 | pass | Text is extractable. Manual structure review pending. |
| `sample-code-codigo-municipal.pdf` | 46 | 134,583 | pass | Text is extractable. Manual structure review pending. |
| `sample-constitution.pdf` | 83 | 196,983 | pass | Text is extractable. Manual structure review pending. |
| `sample-ordinary-law-laip.pdf` | 24 | 69,688 | pass | Text is extractable. Manual structure review pending. |

Initial conclusion: the selected fixtures are not image-only scans. A first parser can start with PyMuPDF text extraction. OCR is not required for these five samples, but remains a fallback for older or scanned PDFs.

### Initial structure detection

Basic grep-based inspection confirms that PyMuPDF extraction preserves key legal-structure markers in the sample corpus.

Observed markers:

| Marker | Evidence | Notes |
|---|---|---|
| `Artículo` | Found in Constitution, Budget Law, and other samples | Article-level parsing appears feasible. |
| `CAPÍTULO` | Found repeatedly in `sample-constitution.txt` | Chapter-level parsing appears feasible. |
| `TÍTULO` | Found in `sample-constitution.txt` and `sample-ordinary-law-laip.txt` | Title-level parsing appears feasible. |
| Reform notes | Found repeatedly in `sample-budget-law.txt` | Reform metadata may be extractable from consolidated institutional text. |
| Mojibake markers | No hits observed in initial `grep "Ã\\|�\\|â"` output | Encoding still requires full hygiene check. |

Examples:

- `sample-constitution.txt` contains `Artículo 1º. Protección a la persona.`
- `sample-constitution.txt` contains repeated chapter headings such as `CAPÍTULO I`, `CAPÍTULO II`, etc.
- `sample-constitution.txt` contains title headings such as `TÍTULO I`, `TÍTULO II`, etc.
- `sample-ordinary-law-laip.txt` contains headings such as `TÍTULO PRIMERO`, `TÍTULO SEGUNDO`, etc.
- `sample-budget-law.txt` contains reform annotations such as `Reformado por el Artículo 1, del Decreto Número 13-2013`.

Initial conclusion: the first parser can rely on regex-based structural detection for `TÍTULO`, `CAPÍTULO`, `SECCIÓN`, and `Artículo`, with additional logic for reform annotations.

### Structural marker counts

Initial regex counts were run against PyMuPDF-extracted text.

| Fixture | `Artículo` count | `TÍTULO` count | `CAPÍTULO` count | Reform notes | Mojibake hits |
|---|---:|---:|---:|---:|---:|
| `sample-budget-law.txt` | 57 | 0 | 0 | 54 | 0 |
| `sample-civic-service.txt` | 0 | 0 | 0 | 0 | 0 |
| `sample-code-codigo-municipal.txt` | 0 | 0 | 0 | 0 | 0 |
| `sample-constitution.txt` | 309 | 15 | 27 | 1 | 0 |
| `sample-ordinary-law-laip.txt` | 0 | 5 | 13 | 0 | 0 |

### Interpretation

The extraction is text-rich and shows no initial mojibake markers. However, structural markers vary significantly across PDFs. The parser must not rely only on exact accented markers such as `Artículo`, `TÍTULO`, and `CAPÍTULO`.

The first parser should support case-insensitive and accent-tolerant variants, including:

- `Artículo`
- `ARTÍCULO`
- `ARTICULO`
- `Articulo`
- `Art.`
- `ART.`
- `TÍTULO`
- `TITULO`
- `CAPÍTULO`
- `CAPITULO`

The `sample-budget-law.txt` file is the strongest candidate for reform extraction because it contains 54 reform notes.

### Accent-insensitive structural marker inspection

A second grep inspection was run with accent-insensitive and case-insensitive patterns.

Command used:

    grep -niE "art[ií]culo|articulo|art\.|cap[ií]tulo|capitulo|t[ií]tulo|titulo" tmp/extracted/gt/*.txt

This confirmed that all five fixtures contain parseable legal-structure markers.

| Fixture | Observed markers | Notes |
|---|---|---|
| `sample-budget-law.txt` | `TITULO`, `CAPITULO`, `ARTICULO`, reform notes | Strong candidate for reform extraction. Uses uppercase unaccented `ARTICULO`. |
| `sample-civic-service.txt` | `CAPITULO`, `ARTICULO` | Structure is parseable. Uses uppercase unaccented `ARTICULO`. |
| `sample-code-codigo-municipal.txt` | `TITULO`, `CAPITULO`, `ARTICULO` | Structure is parseable. Some article headings have extra spaces, e.g. `ARTICULO  1.` |
| `sample-constitution.txt` | `TÍTULO`, `TITULO`, `Capítulo`, `Artículo` | Structure is parseable, but table of contents appears at the beginning and must be ignored or handled separately. |
| `sample-ordinary-law-laip.txt` | `TÍTULO`, `CAPÍTULO`, `ARTICULO` | Structure is parseable. Some article headings have leading whitespace. |

### Parser implication

The Guatemala parser must use accent-insensitive matching for structure detection while preserving the original legal text in the rendered Markdown.

Required heading patterns:

- `Artículo`
- `ARTÍCULO`
- `ARTICULO`
- `Articulo`
- `Art.`
- `ART.`
- `TÍTULO`
- `TITULO`
- `Título`
- `Titulo`
- `CAPÍTULO`
- `CAPITULO`
- `Capítulo`
- `Capitulo`

Required article-heading tolerance:

- Extra spaces after `ARTICULO`, e.g. `ARTICULO  1.`
- Optional punctuation after article number, e.g. `ARTICULO 1.`, `ARTICULO 1.-`, `ARTICULO 4.*`
- Article suffixes, e.g. `ARTICULO 7 Bis.`
- Reform markers attached to headings, e.g. `ARTICULO 3.- * Desconcentración...`

### Structural marker examples

Examples found in the extracted fixtures:

    sample-budget-law.txt:23:TITULO I
    sample-budget-law.txt:25:ARTICULO 1.- Objeto.
    sample-budget-law.txt:135:CAPITULO I
    sample-budget-law.txt:143:ARTICULO 7 Bis.* Proceso Presupuestario.

    sample-civic-service.txt:27:CAPITULO I
    sample-civic-service.txt:29:ARTICULO 1.
    sample-civic-service.txt:90:CAPITULO II

    sample-code-codigo-municipal.txt:30:TITULO I
    sample-code-codigo-municipal.txt:32:ARTICULO  1.
    sample-code-codigo-municipal.txt:172:CAPITULO I

    sample-constitution.txt:10:TÍTULO I     La persona humana fines y deberes del Estado
    sample-constitution.txt:13:Capítulo I     Derechos Individuales
    sample-constitution.txt:94:Artículo 1º. Protección a la persona.

    sample-ordinary-law-laip.txt:49:TÍTULO PRIMERO
    sample-ordinary-law-laip.txt:50:CAPÍTULO PRIMERO
    sample-ordinary-law-laip.txt:52:  ARTICULO 1. Objeto de la Ley.

### Initial parser conclusion

The initial parser can be regex-based for structural detection. PyMuPDF extraction preserves enough text structure to detect titles, chapters, and articles in all five fixtures. OCR is not required for these selected samples.

The parser must handle:

- accent-insensitive legal headings,
- uppercase and lowercase variants,
- extra spaces,
- article suffixes such as `Bis`,
- table of contents lines in the Constitution,
- reform annotations embedded in consolidated texts.

### Structural marker counts

Initial regex counts were run against PyMuPDF-extracted text.

| Fixture | `Artículo` exact count | `TÍTULO` exact count | `CAPÍTULO` exact count | Reform notes | Mojibake hits |
|---|---:|---:|---:|---:|---:|
| `sample-budget-law.txt` | 57 | 0 | 0 | 54 | 0 |
| `sample-civic-service.txt` | 0 | 0 | 0 | 0 | 0 |
| `sample-code-codigo-municipal.txt` | 0 | 0 | 0 | 0 | 0 |
| `sample-constitution.txt` | 309 | 15 | 27 | 1 | 0 |
| `sample-ordinary-law-laip.txt` | 0 | 5 | 13 | 0 | 0 |

### Interpretation of exact-count results

The first exact-count diagnostic undercounted several documents because many Guatemalan PDFs use uppercase unaccented headings such as `ARTICULO`, `TITULO`, and `CAPITULO`. Therefore, exact accented matching is insufficient.

Parser matching must normalize accents and case for detection only. The original extracted text must still be preserved in the rendered Markdown.

Recommended matching approach:

    import unicodedata

    def normalize_for_matching(text: str) -> str:
        text = unicodedata.normalize("NFD", text)
        text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
        return text.lower()

Detection should run against normalized text, while output should keep the original text.