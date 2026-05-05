# UPSTREAM-PR-CHECKLIST-GT.md

# Guatemala (`gt`) Upstream PR Checklist

This document tracks what remains before opening a PR to `legalize-dev/legalize-pipeline`.

## Current local status

- [x] Research document exists: `RESEARCH-GT.md`
- [x] Local quality gate exists: `docs/QUALITY-GATE-GT.md`
- [x] Parser prototype exists: `src/legalize/fetcher/gt/parser.py`
- [x] Renderer prototype exists: `src/legalize/fetcher/gt/renderer.py`
- [x] Metadata prototype exists: `src/legalize/fetcher/gt/metadata.py`
- [x] Discovery prototype exists: `src/legalize/fetcher/gt/discovery.py`
- [x] Fixture client exists: `src/legalize/fetcher/gt/client.py`
- [x] Build pipeline exists: `src/legalize/fetcher/gt/builder.py`
- [x] CLI exists: `src/legalize/fetcher/gt/cli.py`
- [x] Tests pass locally: `27 passed`
- [x] Version-history spike exists for Decreto 101-97 + Decreto 13-2013

## Required before upstream PR

### 1. Official source metadata

- [ ] Add official source URLs for every fixture.
- [ ] Add publication dates where available.
- [ ] Add issuing body for every fixture.
- [ ] Add source classification for every fixture.
- [ ] Add DCA publication reference when available.
- [ ] Add tests requiring non-empty source URLs.

### 2. Legalize interface alignment

- [ ] Inspect `legalize-dev/legalize-pipeline` expected parser interfaces.
- [ ] Rename/adapt `GTMetadata` to upstream metadata models if required.
- [ ] Rename/adapt `ParsedBlock` to upstream block/version models if required.
- [ ] Check expected country registry format.
- [ ] Check expected config format.
- [ ] Check expected CLI commands.

### 3. Fixtures

- [ ] Confirm all 5 primary fixtures are from official or acceptable institutional sources.
- [ ] Move fixtures to the exact upstream expected path.
- [ ] Include `SHA256SUMS.txt`.
- [ ] Keep INFILE/third-party LAIP fixture excluded from quality gate.
- [ ] Add one table/annex-heavy fixture if none of the current fixtures sufficiently tests tables.

### 4. Quality gate

- [ ] Review 5 rendered Markdown files manually.
- [ ] Mark each file PASS/FAIL/NEEDS REVIEW for text correctness.
- [ ] Mark metadata completeness.
- [ ] Mark structure preservation.
- [ ] Mark rich formatting.
- [ ] Mark encoding/hygiene.
- [ ] Produce final `SUMMARY: 5/5 laws fully PASS` before claiming official readiness.

### 5. Version-history spike

- [x] Identify base law: Decreto 101-97.
- [x] Identify reform decree: Decreto 13-2013.
- [x] Extract reform operations.
- [x] Extract replacement bodies.
- [ ] Confirm official publication date for Decreto 13-2013.
- [ ] Confirm effective date if different.
- [ ] Compare at least 3 replacement bodies against the consolidated Decreto 101-97 text.
- [ ] Document whether reconstruction is full, partial, or manual-assisted.

### 6. Live discovery

- [ ] Implement Congreso known-document discovery.
- [ ] Implement DCA publication-date lookup or resolver.
- [ ] Add HTTP client with rate limiting.
- [ ] Add source URL tests.
- [ ] Respect robots.txt / responsible crawling.
- [ ] Avoid bulk bootstrap until discovery is stable.

### 7. Documentation

- [ ] Update README with exact upstream migration instructions.
- [ ] Update `RESEARCH-GT.md` with final source URLs.
- [ ] Update `QUALITY-GATE-GT.md` after manual review.
- [ ] Add limitations clearly.
- [ ] Add disclaimer: not legal advice, not official consolidation.

## Suggested upstream PR title

`feat(gt): add Guatemala legislation fetcher`

## Suggested PR summary

This PR adds initial Guatemala (`gt`) support with:

- official-source research,
- representative fixtures,
- structural parser,
- metadata strategy,
- Markdown rendering,
- fixture discovery,
- parser tests,
- local quality-gate evidence,
- and a version-history reconstruction spike for Decreto 101-97 using Decreto 13-2013.

## Current recommended status

Do not open the upstream PR yet.

Recommended next step:

Complete official source URLs, publication dates, and metadata completeness tests.