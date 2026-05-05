# SOURCE-INVENTORY-GT.md

# Guatemala (`gt`) Source Inventory

This document summarizes the current source inventory for the Guatemala (`gt`) Legalize prototype.

The machine-readable source metadata lives in:

```text
data/gt/sources.yaml
```

This document is a human-readable companion for reviewing source quality, source type, pending publication dates, and fixture coverage.

## Current source status

| Fixture key | Identifier | Title | Source type | Source PDF | Publication date | Issuing body | Confidence |
|---|---|---|---|---|---|---|---|
| `sample-budget-law` | `decreto-101-97` | Ley Orgánica del Presupuesto | `official_primary` | `sample-budget-law.pdf` | pending | Congreso de la República de Guatemala | medium |
| `sample-civic-service` | `decreto-20-2003` | Ley del Servicio Cívico | `official_primary` | `sample-civic-service.pdf` | pending | Congreso de la República de Guatemala | medium |
| `sample-code-codigo-municipal` | `decreto-12-2002` | Código Municipal | `official_primary` | `sample-code-codigo-municipal.pdf` | pending | Congreso de la República de Guatemala | medium |
| `sample-constitution` | `constitucion-politica-republica-guatemala` | Constitución Política de la República de Guatemala | `official_primary` | `sample-constitution.pdf` | `1985-05-31` | Asamblea Nacional Constituyente | medium |
| `sample-ordinary-law-laip-official` | `decreto-57-2008` | Ley de Acceso a la Información Pública | `official_primary` | `sample-ordinary-law-laip-official.pdf` | pending | Congreso de la República de Guatemala | high |
| `reform-decree-13-2013` | `decreto-13-2013` | Reformas al Decreto 101-97, Ley Orgánica del Presupuesto | `official_primary` | `reform-decree-13-2013.pdf` | `2013-11-12` | Congreso de la República de Guatemala | medium |

## Official source URLs

| Identifier | URL |
|---|---|
| `decreto-101-97` | `https://www.congreso.gob.gt/assets/uploads/info_legislativo/decretos/1997/gtdcx101-1997.pdf` |
| `decreto-20-2003` | `https://www.congreso.gob.gt/assets/uploads/info_legislativo/decretos/2003/gtdcx20-2003.pdf` |
| `decreto-12-2002` | `https://www.congreso.gob.gt/assets/uploads/info_legislativo/decretos/2002/gtdcx12-2002.pdf` |
| `constitucion-politica-republica-guatemala` | `https://www.congreso.gob.gt/assets/uploads/secciones/pdf/16e67-constitucion-politica-de-la-republica-de-guatemala.pdf` |
| `decreto-57-2008` | `https://www.congreso.gob.gt/assets/uploads/info_legislativo/decretos/2008/57-2008.pdf` |
| `decreto-13-2013` | `https://www.congreso.gob.gt/assets/uploads/info_legislativo/decretos/2013/13-2013.pdf` |

## Hashes

Canonical SHA-256 hashes are stored in:

```text
engine/tests/fixtures/gt/SHA256SUMS.txt
```

The runtime metadata parser computes `source_sha256` directly from each local PDF fixture.

## Coverage notes

### Covered

- Constitution-level document.
- Ordinary law.
- Code/framework law.
- Budget/public-finance law.
- Public-service law.
- Reform decree for version-history spike.

### Not yet covered

- Table-heavy or annex-heavy official fixture.
- Municipal act or local regulation.
- Agreement issued by Executive branch.
- DCA publication-page metadata.
- Official publication dates for all decrees.
- Effective dates for all decrees.
- Repeal/status metadata.

## Publication-date status

Only one fixture currently has a non-null publication/emission date:

| Identifier | Date | Notes |
|---|---|---|
| `constitucion-politica-republica-guatemala` | `1985-05-31` | Date currently recorded from institutional source context. |

Pending dates:

- `decreto-101-97`
- `decreto-20-2003`
- `decreto-12-2002`
- `decreto-57-2008`

Required next step:

Resolve publication dates through Diario de Centro América or another official publication reference.

## Source-quality notes

All current fixtures are treated as `official_primary`.

However, before upstream PR, each fixture should be manually checked for:

1. Direct official source URL.
2. Stable URL.
3. Matching local SHA-256.
4. Publication date.
5. Issuing body.
6. Whether the file is an original decree, consolidated compilation, or institutional copy.
7. Whether the text contains non-official page artifacts.
8. Whether republication in the corpus is legally acceptable.

## Fixture replacement notes

The original LAIP fixture was replaced because it contained INFILE/proprietary access notices.

Current official LAIP fixture:

```text
sample-ordinary-law-laip-official.pdf
```

The old INFILE-based fixture must not be used for quality-gate review or upstream PR evidence.

## Next actions

1. Resolve official publication dates.
2. Add date evidence to `RESEARCH-GT.md`.
3. Add `publication_date` values to `data/gt/sources.yaml`.
4. Add metadata tests requiring publication dates once verified.
5. Add one table/annex-heavy fixture.
6. Run formal 5-law quality review.
