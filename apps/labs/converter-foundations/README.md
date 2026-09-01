# Converter Foundations — interactive laboratory

A Dash (Plotly) application demonstrating power-conversion fundamentals and
continuous / discontinuous conduction (CCM / DCM) for Buck and Boost
converters. It is the first production laboratory for The Unexpected Professor
and is linked from the corresponding lesson on the website.

Two views, selected by the tab bar:

- **Fondamentaux** — from a direct source to a Buck converter with an output
  capacitor; average vs. RMS on pulsed quantities; the voltage-current plane.
- **Conduction CCM / DCM** — Buck and Boost, transistor vs. diode, the DCM
  zone, and `V_OUT = f(D)` real vs. ideal.

The interface is bilingual (French default, English toggle).

## Layout

- `app.py` — entry point; wires layouts + callbacks; exposes `server` for WSGI.
- `models/` — pure analytic physics, no plotting imports.
- `layouts/` — declarative UI (three-pane shell, sliders).
- `callbacks/` — interactivity and Plotly figure builders.
- `assets/` — circuit diagrams, served by Dash from `/assets/`.
- `tests/` — physics checks, a server smoke test, and asset verification.

## Local development

Requires Python 3.12 (see `.python-version`).

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
python app.py            # http://127.0.0.1:8050  (debug OFF)
DASH_DEBUG=1 python app.py   # opt in to the Dash debugger
pytest
```

## Production

The container runs the exported `server` through Gunicorn; Dash debug mode is
never enabled by a production process.

```bash
docker build -t converter-foundations .
docker run --rm -p 8050:8050 converter-foundations
curl -fsS localhost:8050/healthz     # -> ok
```

- Binds `0.0.0.0:8050` inside the container; runs as UID 10001 (non-root).
- Logs to stdout/stderr.
- `HEALTHCHECK` polls `/healthz`.
- Worker / thread / timeout settings live in `gunicorn.conf.py` and are
  **provisional** until the representative-classroom load test (hub UPH-026).
- No filesystem persistence is assumed; the container can run read-only.

## Dependencies

`requirements.txt` pins the direct dependencies; `requirements.lock` is the
full transitive lock used by the image. Regenerate both together — see the
comment at the top of `requirements.txt`.

## Responsive behaviour

The three-pane layout is designed for tablet width and above. On a narrow
phone the panes stack and the graphs become cramped; the lesson links to the
lab full-screen and recommends a larger screen. A dedicated compact layout is
out of scope for the pilot.

## Provenance and licence

Adapted from the author's existing power-electronics teaching materials.
Source code: `GPL-3.0-only`. Circuit diagrams: `CC-BY-SA-4.0` (original work).
See the repository `LICENSE.md`.
