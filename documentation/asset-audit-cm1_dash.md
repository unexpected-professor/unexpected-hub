# Asset audit — `cm1_dash` (UPH-007)

Audit date: 2026-09-01. Auditor: The Unexpected Professor (with Claude Code).

Source (private): `Energie S3` course repository,
`new_course/images/plotting_python/cm1_dash/`, plus the ported-from originals
`new_course/images/plotting_python/cm1_interactive.py` and `cm2_interactive.py`.

Public destination: `apps/labs/converter-foundations/` (first production Dash
laboratory, ADR-017).

This audit applies the checklist in [`public-boundary.md`](public-boundary.md).

## Verdict

**Cleared for export, with required changes.** No student data, credentials,
personal identifiers, or restricted institutional material is present. All code
and diagrams are the author's own work and can be published under the
repository licences. Three changes are required before the files are committed
to the public repository, and several production items are deferred to UPH-020.

## What was reviewed

| Path | Type | Result |
|---|---|---|
| `app.py` | Dash entry point | Clean. Dev-only `app.run(debug=True)`; hardcoded course title (change required). |
| `i18n.py` | FR/EN UI string catalogue | Clean. Pedagogical strings only; course identifiers `CM1`/`CM2` in titles (change required). |
| `models/converter_physics.py`, `models/cm2_physics.py` | Pure physics | Clean. Original analytic converter models, no third-party code, no plotting deps. |
| `layouts/*.py` | Declarative UI | Clean. |
| `callbacks/*.py` | Interactivity + Plotly figure builders | Clean. No I/O, no filesystem persistence, no user-input evaluation. |
| `assets/*.drawio.png` (11 files) | Circuit diagrams | Original draw.io diagrams. Editable `mxfile` XML embedded in each PNG (change required). |
| `requirements.txt` | Dependencies | Unpinned `>=`; pin/lock deferred to UPH-020. |
| `dash_development.md` | Internal dev log | **Do not export** — course-internal scaffolding notes, relative path references, no public value. |
| `cm1_interactive.py`, `cm2_interactive.py` | Matplotlib originals | Clean. Author's own; no licence headers, no third-party attribution, no copyright notices. |

## Checklist results

- **Source paths / destination**: identified (above).
- **Right to publish every file**: yes. Git history of the course repository
  attributes every `cm1_dash` file to a single author (`Luiz Villa
  <luiz.villa@laas.fr>`), who is the project owner. The `laas.fr` address
  appears only in the private repository's history, which is **not** exported
  (file copy only, per ADR-007).
- **Metadata inspection**: `.py` files carry no author metadata. The 11 PNGs
  each embed the full editable draw.io diagram (`mxfile` `tEXt` chunk) with
  internal diagram IDs; a `strings` scan found no names, emails, or paths.
- **Names / emails / absolute paths / secrets / local config**: none found in
  code. `dash_development.md` references relative paths (`../../../WORK_STATUS.md`,
  `Energie S3/venv`, `build.bat`) and is excluded from export.
- **Third-party provenance / licences**: no vendored third-party code.
  Runtime dependencies — `dash` (MIT), `dash-bootstrap-components` (Apache-2.0),
  `plotly` (MIT), `numpy` (BSD-3-Clause); the matplotlib originals also use
  `matplotlib` (PSF/BSD-style) and `Pillow` (HPND). All are permissive and
  compatible with distribution of `GPL-3.0-only` code. Bootstrap CSS is bundled
  by `dash-bootstrap-components`.
- **Replace real data with synthetic**: not applicable — the lab has no
  datasets; all values are user-driven slider parameters.
- **Destination licence applies**: yes. Code → `GPL-3.0-only`; circuit diagrams
  → `CC-BY-SA-4.0` (see register below).
- **Copy without private Git history**: required — export by file copy only.
- **Secret scan after import**: to be run on the staged export (UPH-019).
- **Build and test independently**: to be done in UPH-019/UPH-021.

## Required changes before commit

1. **Rebrand course identifiers.** `app.py` title `'Énergie S3 – CM1 / CM2'`
   and the `i18n.py` `title` / `title2` strings (`CM1 – …`, `CM2 – …`) must
   become subject-based names (hub section 5.1). Keep the IUT identifiers only
   as private cross-reference metadata, not in the public UI.
2. **Flatten the circuit PNGs.** Re-export each diagram from draw.io without
   "include a copy of my diagram", or strip the `mxfile` metadata chunk, so the
   published assets carry no editable source or internal IDs and are smaller
   (the Buck/Boost PNGs are ~130 KB each). Keep the editable `.drawio` sources
   privately.
3. **Do not export `dash_development.md`.** Write a fresh public README for the
   lab describing what it demonstrates and how to run it.

## Deferred to UPH-020 (productionisation, not export blockers)

- Pin/lock dependencies; add Gunicorn; replace `app.run(debug=True)`.
- Non-root Dockerfile; bind `0.0.0.0` on an internal port; logs to stdout/stderr.
- Add a health check route and a `server` import smoke test.
- Confirm no filesystem persistence is assumed (initial review: none).

## Owner confirmation

- 2026-09-01: the owner confirms the circuit diagrams were drawn entirely by
  them and trace no copyrighted textbook or datasheet figure. UPH-007 is
  therefore DONE.

## How to flatten the PNGs (change 2)

Renaming the files (dropping `.drawio` from the name) does **not** flatten
them — the editable diagram is a `tEXt`/`zTXt` chunk named `mxfile` inside the
PNG binary, independent of the filename. It must be removed:

- draw.io desktop: **Export as -> PNG** with **"Include a copy of my diagram"
  unchecked**; this is also the moment to re-export at higher resolution.
- or strip in place, e.g. `Image.open(f).save(out)` with Pillow (a plain
  re-save drops all text chunks), or `pngcrush -rem text`, or
  `convert in.png -strip out.png`.

Verified on `case_1.drawio.png`: a plain Pillow re-save removed the `mxfile`
chunk and reduced the file from 12 971 to 7 970 bytes.

## Asset attribution register entries

To be merged into the register in `public-boundary.md` on export:

| Asset | Creator/source | Original licence | Modifications | Public destination | Verified by/date |
|---|---|---|---|---|---|
| `case_1..5[_D].drawio.png` (7 files) | The Unexpected Professor (draw.io) | Author's own → `CC-BY-SA-4.0` | Flatten (remove embedded `mxfile`) | `apps/labs/converter-foundations/assets/` | Owner / 2026-09-01 |
| `Buck_chopper_1/2.drawio.png`, `Boost_chopper_1/2.drawio.png` (4 files) | The Unexpected Professor (draw.io) | Author's own → `CC-BY-SA-4.0` | Flatten (remove embedded `mxfile`) | `apps/labs/converter-foundations/assets/` | Owner / 2026-09-01 |
| `converter_physics.py`, `cm2_physics.py`, `callbacks/*`, `layouts/*`, `i18n.py`, `app.py` | The Unexpected Professor | Author's own → `GPL-3.0-only` | Rebrand course identifiers; productionise (UPH-020) | `apps/labs/converter-foundations/` | Owner / 2026-09-01 |
