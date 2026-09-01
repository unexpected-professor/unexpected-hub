# The Unexpected Professor

The Unexpected Professor is a personal, French-first educational publishing
project combining structured web lessons, YouTube videos, and interactive
browser laboratories.

The project is currently in **Phase 0: decisions and safe project boundary**.
No website, dashboard, domain, or production infrastructure has been deployed
from this repository yet.

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
[`unexpected_professor_hub.md`](unexpected_professor_hub.md). The name, licence,
legal status, dedicated GitHub SSH identity, deployment model (Docker Compose +
Caddy), budget ceiling, and first vertical slice are decided. The next work is
to audit the first candidate Dash laboratory (`cm1_dash`) for public release,
then select a domain, registrar, and EU VPS provider.
