# The Unexpected Professor

The Unexpected Professor is a personal, French-first educational publishing
project combining structured web lessons, YouTube videos, and interactive
browser laboratories.

The **Phase 1 local vertical slice is complete**. Phase 0 decisions are done
and `theunexpectedprofessor.com` is registered. The Astro site is in
[`apps/site/`](apps/site/) and the first laboratory in
[`apps/labs/converter-foundations/`](apps/labs/converter-foundations/); both
build and run locally. No production infrastructure is deployed yet — Phase 2
provisions the OVHcloud VPS.

## Project channels

- YouTube: [@TheUnexpectedProfessor](https://www.youtube.com/@TheUnexpectedProfessor)
- Website: domain not selected
- Interactive labs: not deployed
- Canonical plan and tracker: [`unexpected_professor_hub.md`](unexpected_professor_hub.md)

The intended division of responsibilities is:

- YouTube for video discovery and delivery;
- the website for canonical lessons, transcripts, references, and downloads;
- self-hosted Dash applications for interactive laboratories;
- Moodle for enrolled students, assignments, grades, and private material.

## Repository boundary

This is a clean public repository. Material from private or institutional
course repositories must pass the review in
[`documentation/public-boundary.md`](documentation/public-boundary.md) before
being copied here. In particular, do not commit student information, private
course administration, credentials, unreviewed third-party assets, or inherited
Git history.

## Licensing

This is a mixed-licence repository:

- original educational content is licensed under
  [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt);
- source code is licensed under
  [GNU GPL version 3 only](LICENSES/GPL-3.0-only.txt).

See [`LICENSE.md`](LICENSE.md) for the exact scope and exceptions.

## Current resume point

Use the tracker and the **Resume from here** section in
[`unexpected_professor_hub.md`](unexpected_professor_hub.md). Phases 0 and 1 are
complete: decisions recorded, `theunexpectedprofessor.com` registered, and the
site + first laboratory build and run locally. The next work is Phase 2 —
provision the OVHcloud VPS-1 (owner action), then Commit 5 (Compose + Caddy
deployment stack) and DNS + HTTPS.
