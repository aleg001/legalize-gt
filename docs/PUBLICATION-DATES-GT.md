# PUBLICATION-DATES-GT.md

# Guatemala (`gt`) Publication Date Research

This document tracks publication-date and effective-date research for Guatemala fixtures.

## Date status

| Identifier | Decree | Date candidate | Date type | Source | Confidence | Notes |
|---|---|---:|---|---|---|---|
| `decreto-13-2013` | 13-2013 | `2013-11-12` | `publication_date` | DCA header inside official PDF extraction | high | The extracted official PDF repeatedly shows `Guatemala, MARTES 12 de noviembre 2013` and `DIARIO de CENTRO AMÉRICA`. |
| `decreto-57-2008` | 57-2008 | pending | `publication_date` | pending | pending | LAIP. Need DCA publication evidence. |
| `decreto-101-97` | 101-97 | `1997-11-20` | `publication_date_candidate` | Congreso PDF / DCA header in PDF | medium | PDF text/search result indicates `DIARIO DE CENTRO AMERICA, Noviembre 20 de 1997`. Needs manual confirmation from local fixture or PDF header. |
| `decreto-12-2002` | 12-2002 | `2002-05-13` | `publication_date_candidate` | Congreso PDF / DCA header in PDF | medium | PDF text/search result indicates `DIARIO DE CENTRO AMERICA, 13 de mayo de 2002`. Needs manual confirmation from local fixture or PDF header. |
| `decreto-20-2003` | 20-2003 | pending | `publication_date` | pending | pending | Ley del Servicio Cívico. Need DCA publication evidence. |
| `constitucion-politica-republica-guatemala` | n/a | `1985-05-31` | `emission_date` | Congreso institutional context | medium | Already in metadata as constitutional date, not necessarily DCA publication date. |

## Research rules

- Prefer Diario de Centro América publication date.
- If DCA date is unavailable, use Congreso emission date only as `emission_date`, not `publication_date`.
- Do not infer dates from filename or decree number.
- If source is not official, mark confidence as low.
- Effective date must be separately captured if available.
- Use `publication_date_candidate` until a DCA header, DCA page, or official metadata field is manually verified.

## Evidence log

### Decreto 101-97

Candidate:

```text
1997-11-20
```

Evidence:

The Congreso PDF for Decreto 101-97 contains or is indexed with the DCA header:

```text
DIARIO DE CENTRO AMERICA, Noviembre 20 de 1997
```

Current status:

```text
publication_date_candidate
```

Next action:

Confirm this date from the local extracted text or from the PDF header/page image.

### Decreto 12-2002

Candidate:

```text
2002-05-13
```

Evidence:

The Congreso PDF for Decreto 12-2002 contains or is indexed with the DCA header:

```text
DIARIO DE CENTRO AMERICA, 13 de mayo de 2002
```

Current status:

```text
publication_date_candidate
```

Next action:

Confirm this date from the local extracted text or from the PDF header/page image.

### Decreto 13-2013

### Decreto 13-2013

Publication date:

```text
2013-11-12

Evidence:

The consolidated Decreto 101-97 fixture contains repeated reform notes such as:

```text
Reformado por el Artículo 1, del Decreto Número 13-2013 el 20-11-2013
```

Current status:

```text
reform_note_date
```

Next action:

Confirm this date against the official Decreto 13-2013 PDF header or Diario de Centro América publication record.

### Decreto 57-2008

Candidate:

```text
pending
```

Next action:

Search DCA/Congreso PDF header for publication date.

### Decreto 20-2003

Candidate:

```text
pending
```

Next action:

Search DCA/Congreso PDF header for publication date.

## Pending dates

- `decreto-57-2008`
- `decreto-20-2003`

## Next commands

Run local searches in extracted fixture text:

```bash
grep -niE "DIARIO|CENTRO AMERICA|CENTRO AMÉRICA|Guatemala,|mayo|noviembre|2008|2003|2013|1997|2002" tmp/extracted/gt/decreto-*.txt tmp/extracted/gt/sample-*.txt | head -80
```

More targeted:

```bash
grep -niE "DIARIO|CENTRO AMERICA|CENTRO AMÉRICA|Noviembre|noviembre|1997" tmp/extracted/gt/sample-budget-law.txt | head -40

grep -niE "DIARIO|CENTRO AMERICA|CENTRO AMÉRICA|mayo|2002" tmp/extracted/gt/sample-code-codigo-municipal.txt | head -40

grep -niE "DIARIO|CENTRO AMERICA|CENTRO AMÉRICA|2013|noviembre|20-11-2013" tmp/extracted/gt/reform-decree-13-2013.txt tmp/extracted/gt/sample-budget-law.txt | head -60

grep -niE "DIARIO|CENTRO AMERICA|CENTRO AMÉRICA|2008|octubre|noviembre|57-2008" tmp/extracted/gt/sample-ordinary-law-laip-official.txt | head -60

grep -niE "DIARIO|CENTRO AMERICA|CENTRO AMÉRICA|2003|Servicio Cívico|20-2003" tmp/extracted/gt/sample-civic-service.txt | head -60
```

## Update policy for `data/gt/sources.yaml`

Only update `publication_date` in `sources.yaml` when the date is verified from one of:

1. DCA publication page.
2. DCA header inside official PDF.
3. Official Congreso metadata field clearly indicating publication date.
4. Another official source with explicit publication date.

Until then, keep dates as `null` or mark them only in this research document as candidates.
