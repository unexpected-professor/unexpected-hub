# The Unexpected Professor

The Unexpected Professor is a personal, French-first educational publishing
project combining structured web lessons, YouTube videos, and interactive
browser laboratories.

The project is currently in **Phase 1: local vertical slice**. Phase 0
decisions are complete and `theunexpectedprofessor.com` is registered. The
Astro site scaffold lives in [`apps/site/`](apps/site/); no dashboard or
production infrastructure has been deployed yet.

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
[`unexpected_professor_hub.md`](unexpected_professor_hub.md). Phase 0 is
complete: name, licence, legal status, GitHub SSH identity, deployment model
(Docker Compose + Caddy), budget ceiling, first vertical slice, registrar and
host (OVHcloud), and the `cm1_dash` asset audit are all done. The next work is
Commit 3 (canonical lesson template + consent-gated YouTube + legal pages),
then Commit 4 (export and productionise the `cm1_dash` laboratory), then
provisioning the OVHcloud VPS.
