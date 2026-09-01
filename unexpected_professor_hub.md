# The Unexpected Professor Hub

## Living plan, progress tracker, and work log

| Field | Current value |
|---|---|
| Document role | Canonical overview and resume point for The Unexpected Professor publishing platform |
| Status | Phase 0 — decisions and safe project boundary in progress |
| Created | 2026-09-01 |
| Last updated | 2026-09-01 |
| Confirmed public name | The Unexpected Professor |
| YouTube | `https://www.youtube.com/@TheUnexpectedProfessor` |
| Launch language | French-first |
| Current project status | Personal and non-professional; reassess before monetisation or institutional affiliation |
| Educational-content licence | Creative Commons Attribution-ShareAlike 4.0 International (`CC-BY-SA-4.0`) |
| Source-code licence | GNU General Public License version 3 only (`GPL-3.0-only`) |
| GitHub account | `unexpected-professor` (`https://github.com/unexpected-professor/`) |
| Canonical repository | `git@github.com:unexpected-professor/unexpected-hub.git` |
| Local canonical clone | A local working clone (path deliberately kept out of public history) |
| Canonical branch | `main` |
| Repository-local Git author | `The Unexpected Professor` with the account-scoped GitHub no-reply address |
| Remote publication state | Commit 0 (`0c5a043`) and Commit 1 (`5a71a77`) published on `origin/main`; later documentation-only commits may be pending local review before push |
| Deployment control plane | Docker Compose + Caddy (ADR-010, resolved 2026-09-01) |
| Monthly hosting budget ceiling | EUR 5-10 (small EU VPS, 2 vCPU / 4 GB class) |
| First vertical slice | Converter-foundations lesson reusing the `cm1_dash` Dash pilot |
| Current course repository | `Energie S3` |
| Current course branch | `dash` |
| Course baseline at project creation | `238f504` (`docs(status): reconcile progress trackers and record resume point`) |
| Existing pilot application | `new_course/images/plotting_python/cm1_dash/` |
| Domain | Not selected or registered |
| Hosting provider | Not selected |
| Production deployment | Not started |

This is the living source of truth for creating **The Unexpected Professor**
educational hub. It records the intended architecture, decisions, implementation
sequence, validation criteria, operational requirements, and the exact point
from which work should resume in a future session.

Update this file whenever a decision changes or a milestone is completed. Do
not silently rewrite past decisions: amend the relevant section and append a
dated entry to the work log.

## 1. Vision

The Unexpected Professor will be a public educational identity connecting three
complementary channels:

- **YouTube** provides discovery, subscriptions, playlists, comments, video
  encoding, and video delivery.
- **The public website** is the canonical learning library: lessons,
  transcripts, equations, references, downloads, and durable navigation.
- **Interactive laboratories** provide browser-based Dash simulations and
  visualisations linked to individual lessons.
- **Moodle** remains the institutional course gateway for enrolled students,
  schedules, assignments, submissions, grades, and private course material.

The website should remain useful without Moodle, while Moodle should link to
canonical public pages instead of duplicating material that will drift over
time.

```text
YouTube channel
  discovery, playlists, video delivery
                 <->
unexpectedprofessor.example
  lessons, transcripts, downloads, references
                  |
                  v
labs.unexpectedprofessor.example
  interactive Dash applications
                  ^
                  |
Moodle
  curated sequence, assignments, grades, restricted material
```

`unexpectedprofessor.example` is a placeholder. No domain availability has
been checked and no domain should be published in course material until its
registration and DNS control have been confirmed.

## 2. Guiding principles

1. **One canonical source per kind of information.** The site owns public
   lesson content, YouTube owns video playback, Moodle owns student activity,
   and Git owns source history.
2. **Start with one complete vertical slice.** Publish one lesson, one video
   integration, and one Dash laboratory before building the full catalogue.
3. **Separate public and private material.** Do not deploy the current course
   repository or expose its Git history directly.
4. **Prefer stateless public applications.** Student accounts, submissions,
   and grades stay in Moodle unless a later requirement justifies LTI or
   institutional authentication.
5. **Keep the platform portable.** Each application must build as a container
   so that it can move between VPS providers or institutional infrastructure.
6. **Privacy and accessibility are design requirements.** They are not launch
   clean-up tasks.
7. **Operational simplicity comes before maximum sovereignty.** Self-host the
   website and dashboards first; do not self-host video during the pilot.
8. **Every production change is documented and recoverable.** Deployment,
   backup, rollback, and verification instructions belong in version control.

## 3. Scope

### 3.1 Initial scope

- Establish The Unexpected Professor public identity and domain namespace.
- Create a clean public-platform repository with no inherited private history.
- Build a responsive educational website from Markdown/MDX content.
- Package the existing Dash application for production.
- Deploy the website and first lab on an EU-hosted VPS over HTTPS.
- Integrate one YouTube video or placeholder using privacy-aware loading.
- Link the resulting lesson and lab from Moodle.
- Add minimum viable security, backups, monitoring, documentation, and a
  repeatable publishing workflow.

### 3.2 Explicitly deferred

- Self-hosted video delivery or a PeerTube instance.
- Student accounts on the public website.
- Moodle grade return, deep linking, or LTI 1.3 integration.
- Payments, subscriptions, advertising, or a commercial training offer.
- A community forum, comments hosted on the website, or user uploads.
- High-availability clustering, Kubernetes, or multi-region deployment.
- A mobile application.
- Migration of the complete Energie S3 course before the pilot is validated.

## 4. Working architecture

### 4.1 Recommended baseline

The working recommendation is a rented EU VPS rather than a server at home.
The VPS remains self-hosted in the operational sense: the software, data,
configuration, deployment process, and backups remain under project control.
It avoids dependence on domestic power, residential upload bandwidth, dynamic
addressing, carrier-grade NAT, and exposing a home network to students.

Baseline capacity for the pilot:

- 2 to 4 vCPU;
- 4 GB RAM for a minimal Docker Compose installation;
- preferably 8 GB RAM when using Coolify and building several containers on
  the production host;
- 40 GB or more of SSD storage;
- an EU data-centre region;
- provider snapshots or backups plus an independent off-site backup;
- IPv4, with IPv6 enabled where the provider and DNS configuration support it.

This is a starting estimate, not a concurrency guarantee. Dash callback load
must be measured with representative student usage before an assessed class
depends on the service.

### 4.2 Hosting and deployment alternatives

| Alternative | Strengths | Costs and risks | Position |
|---|---|---|---|
| Docker Compose + Caddy on an EU VPS | Small stack, transparent configuration, easy portability, automatic HTTPS | More command-line administration and manual deployment work | Preferred when direct infrastructure understanding is a goal |
| Coolify on an EU VPS | Git-driven deployments, domains, logs, environment variables, and rollbacks through a UI | Extra RAM, extra attack surface, and Coolify itself must be maintained | Working recommendation for several evolving apps |
| Institution-managed VM or container service | Institutional governance, potential SSO, and clearer support for private student services | Provisioning may be slow and public pseudonymous branding may be constrained | Strong alternative for protected or assessed activities |
| Home server | Physical control and useful learning environment | Power, ISP, NAT, bandwidth, physical failure, and security burden | Development or mirror only; not the primary student endpoint |
| Managed application host | Very low server administration | Less self-hosting control and potentially higher per-service cost | Fallback if VPS operations become too burdensome |
| PeerTube or another self-hosted video platform | Greater control of video distribution | Storage, egress, transcoding, moderation, and availability burden | Reconsider only after the audience and archive justify it |

### 4.3 Decision gate: Coolify or plain Compose

**Resolved 2026-09-01 (ADR-010): Docker Compose + Caddy.** The pilot is a
single-maintainer deployment of one static site plus one Dash lab, on a small
EU VPS with a monthly budget ceiling of EUR 5-10 (2 vCPU / 4 GB class). A
minimal, auditable stack with automatic HTTPS fits that constraint; Coolify's
extra RAM and administrative surface are not justified yet. Reconsider Coolify
only if several evolving apps and frequent Git-driven deploys appear.

The application containers must still remain compatible with both approaches.
The choice of deployment control plane must not leak into application code, so
a later switch to Coolify remains possible without rewriting the labs.

### 4.4 Logical services

| Service | Technology | Public role | Persistent state |
|---|---|---|---|
| Main site | Astro static build | Lessons, transcripts, catalogue, downloads, legal pages | Git content and media only |
| Lab catalogue | Astro page initially | Searchable entry point for interactive tools | None |
| Dash lab(s) | Python, Dash, Plotly, Gunicorn | Interactive simulations | None during pilot |
| Reverse proxy | Caddy, or Coolify-managed proxy | HTTPS termination and routing | Certificates and configuration |
| Analytics | None initially; optionally self-hosted Umami later | Aggregate audience understanding | Database if enabled |
| Availability monitoring | External check or Uptime Kuma | Detect public outage | Small monitoring database if self-hosted |
| Source and deployment | Git plus container registry or on-host build | Reproducible releases and rollback | Repository and container images |

## 5. Public information architecture

### 5.1 Proposed site sections

```text
Home
About The Unexpected Professor
Courses
  Power electronics
  Future subject areas
Lessons
Videos
Interactive labs
Resources and downloads
Licence and attribution
Privacy
Legal notice
Contact
```

The navigation should be organised around subject matter rather than local
course identifiers such as `CM1` or `TD2`. Internal identifiers may still be
stored as metadata for cross-referencing the IUT course.

### 5.2 Canonical lesson page

Each lesson should be able to contain:

1. Title, summary, expected level, and estimated duration.
2. Learning objectives and prerequisites.
3. Consent-controlled YouTube player and a direct YouTube link.
4. Searchable transcript or structured written explanation.
5. Equations, diagrams, definitions, and worked examples.
6. An embedded laboratory when appropriate, plus a full-screen fallback link.
7. Exercises, datasets, code, slides, or printable resources.
8. Sources, image credits, content licence, publication date, and revision
   date.
9. Links to the previous and next lessons in the sequence.

A matching YouTube description should link back to the canonical lesson page
and the associated lab. YouTube playlists and website course names should use
the same taxonomy.

### 5.3 Proposed content metadata

The exact Astro schema will be decided during implementation, but the initial
content contract should cover at least:

```yaml
title: "Lesson title"
slug: "stable-public-slug"
summary: "Short description"
language: "fr"
level: "undergraduate"
topics: ["power-electronics", "buck-converter"]
course_sequence: "power-electronics-foundations"
sequence_index: 1
youtube_id: null
lab_url: null
published_at: null
updated_at: null
authors: ["The Unexpected Professor"]
licence: "TBD"
draft: true
```

French is the confirmed launch language. The current Dash interface already
supports French and English, but the public website will be French-first. Do
not duplicate every page in two languages until the maintenance cost and
intended audience have been evaluated. English content may be added later as a
separately planned extension.

## 6. Repository and source boundaries

### 6.1 Separation requirement

Create a fresh repository for the public hub rather than publishing the
existing Energie S3 repository. Before copying any asset, review:

- copyright and licence status;
- student, colleague, or institutional information;
- file metadata and embedded author information;
- Git author name and email configuration;
- absolute local paths, usernames, and machine-specific settings;
- API keys, deployment tokens, `.env` files, and cached credentials;
- whether the asset is pedagogically ready for a public audience.

Do not rewrite or sanitise the current course repository destructively. Export
only explicitly approved content into the new repository.

### 6.2 Proposed public repository layout

```text
unexpected-professor/
  apps/
    site/                       # Astro website and lesson content
    labs/
      converter-foundations/   # First production Dash application
  packages/
    content-schema/             # Optional shared schemas/utilities
    design-system/              # Optional shared styles/components
  infra/
    compose.yaml
    caddy/
    coolify/                    # Notes or manifests, if selected
    backup/
  documentation/
    architecture.md
    deployment.md
    publishing-workflow.md
    privacy-and-legal-checklist.md
    operations-runbook.md
  .env.example
  README.md
  LICENSE                       # Source-code licence, once selected
```

For the pilot, avoid creating packages that have only one consumer. The
directory structure may be simplified until duplication actually appears.

### 6.3 Version-control model

- `main` represents the deployable public state.
- Feature branches are reviewed and verified before merging.
- Content drafts use front matter such as `draft: true` and do not appear in
  production builds.
- Production is deployed from a tagged commit or an identifiable `main`
  commit.
- The deployment system records the deployed commit SHA.
- Secrets are configured on the server or deployment platform and never
  committed.
- Generated site output and local virtual environments are ignored.

## 7. Website technical specification

### 7.1 Astro baseline

- Static output for the main public pages.
- Markdown/MDX content collections with validated front matter.
- Responsive, keyboard-accessible navigation.
- KaTeX or an equivalent accessible mathematics pipeline, selected after a
  render comparison.
- Syntax highlighting only where code is actually used.
- Image optimisation with original sources retained separately.
- Atom/RSS feed and sitemap.
- Stable canonical URLs and metadata for search and link previews.
- No advertising or third-party analytics during the pilot.
- A useful page must remain readable when JavaScript is unavailable, except
  for the explicitly interactive laboratory.

### 7.2 Visual identity

Before visual implementation, define:

- exact public spelling and capitalisation of The Unexpected Professor;
- matching YouTube handle and preferred domain;
- logo or wordmark requirements;
- primary and secondary colours with accessible contrast;
- typography that supports French, mathematics, and code;
- illustration and thumbnail style;
- whether the public tone is French-only, bilingual, or language-selectable.

Brand work must not delay the functional pilot. A restrained temporary
wordmark and colour system are acceptable for the first release.

### 7.3 YouTube integration

- Do not load a YouTube iframe before the visitor makes the relevant consent
  choice.
- Display a local thumbnail or neutral placeholder with a clear action to load
  the video.
- Use YouTube privacy-enhanced embed URLs (`youtube-nocookie.com`) after
  consent.
- Provide a direct YouTube link for browsers, assistive technology, or network
  policies that block embedding.
- Prefer click-to-play; do not autoplay.
- Provide French captions and a transcript whenever possible.
- Keep the YouTube video ID in lesson metadata rather than hand-writing iframe
  markup on every page.
- If a video is unlisted, document that anyone with the URL can share it; it is
  not an access-control mechanism.

### 7.4 Dashboard integration

The initial site should link to a full-screen dashboard. An embedded iframe can
be added after responsive behaviour and browser policies have been tested.
Every embedded lab must also have a visible full-screen link.

Subdomains are preferred for the pilot because the current Dash application
runs at its URL root. Hosting several Dash applications under path prefixes
would require consistent `requests_pathname_prefix` and asset-path handling.

## 8. Dash production specification

The current pilot lives at
`new_course/images/plotting_python/cm1_dash/` and already exposes
`server = app.server`. Its development entry point uses `app.run(debug=True)`;
production must invoke the exported server through Gunicorn so that debug mode
is never exposed publicly.

Required production work:

- create a minimal, pinned or locked Python dependency set;
- add Gunicorn as the production WSGI server;
- add a Dockerfile with a supported Python version;
- copy all required Dash `assets/` into the container image;
- run as a non-root user;
- bind the application to `0.0.0.0` on an internal container port;
- emit logs to standard output and standard error;
- add a lightweight health check;
- make development and production configuration explicit;
- verify that no filesystem persistence is assumed;
- document worker, thread, and timeout settings rather than guessing them;
- test French and English layouts, callbacks, figures, and static assets;
- test narrow mobile layouts and provide a full-screen recommendation if the
  lab is not usable at phone width;
- add a smoke test that imports `server` and receives a successful HTTP
  response;
- load-test representative callback interactions before classroom use.

Illustrative production command, subject to load testing:

```bash
gunicorn app:server --bind 0.0.0.0:8050
```

Do not select a final worker count until memory per worker and callback latency
have been measured. Each Python worker can duplicate application memory.

## 9. Network, DNS, and TLS

### 9.1 Proposed DNS records

| Name | Purpose | Initial target |
|---|---|---|
| Apex domain | Main public website | VPS public address |
| `www` | Redirect to the canonical apex domain | Reverse proxy |
| `labs` | Lab catalogue or first lab | Reverse proxy |
| Lab-specific subdomain(s) | Individual Dash services, if used | Reverse proxy |
| `status` | Optional public status page | Monitoring service or external provider |

The final names depend on the registered domain. Choose one canonical website
hostname and redirect alternatives to prevent duplicate indexing.

### 9.2 Public ports

- TCP 80 for HTTP-to-HTTPS redirection and certificate challenges.
- TCP 443 for all public web traffic.
- SSH on a deliberately configured port, preferably restricted by source IP
  or a private administrative network where practical.
- Do not expose Dash, databases, Docker, Coolify internals, or monitoring
  administration ports directly to the internet.

### 9.3 TLS and proxy behaviour

- Obtain and renew public certificates automatically.
- Redirect HTTP to HTTPS.
- Preserve proxy headers required by Dash and Gunicorn.
- Set security headers deliberately, including a Content Security Policy that
  permits only the third-party resources actually used.
- Decide explicitly whether the website may embed the lab and whether Moodle
  may frame it; configure `frame-ancestors` accordingly.
- Apply upload and request-size limits even if the pilot has no upload forms.

## 10. Deployment and release process

### 10.1 Target workflow

```text
Edit source/content
  -> local lint, tests, and builds
  -> commit and review
  -> push selected branch
  -> build immutable container/static artifact
  -> deploy to staging or preview
  -> smoke and visual checks
  -> promote to production
  -> record deployed commit and verification
```

Minimum automated checks:

- Markdown and internal-link validation;
- Astro content-schema validation and production build;
- Python syntax and unit tests for physics models;
- Dash server import and HTTP smoke test;
- container image build;
- check that required static assets exist in the built image;
- `git diff --check`;
- dependency and image vulnerability review when tooling is selected.

Production releases must be reversible. Keep at least the current and previous
known-good images or deployment revisions and document the rollback command.

### 10.2 Environments

| Environment | Purpose | Publicly discoverable |
|---|---|---|
| Local | Development and rapid callback testing | No |
| Preview/staging | Validate a proposed release and Moodle framing | No, or access-restricted |
| Production | Stable public lessons and labs | Yes |

The pilot may initially combine staging and production, but only if rollback is
tested and no course assessment depends on uninterrupted access.

## 11. Moodle integration

During the pilot, Moodle should use ordinary URL resources:

- link to the canonical lesson page for the pedagogical sequence;
- link directly to a full-screen lab when students need maximum workspace;
- prefer a new tab until iframe behaviour is verified in desktop browsers and
  the Moodle mobile application;
- keep submissions, completion rules, grades, and private files in Moodle;
- do not pass student names, email addresses, IDs, or other personal data in
  URL query parameters;
- document that hiding the Moodle link does not protect a public URL.

If a future requirement needs Moodle identity, controlled access, or grade
return, evaluate LTI 1.3 or institution-managed authentication as a separate
project with the IUT's Moodle administrator and data-protection contact.

## 12. Privacy, legal, licensing, and pseudonym

The visible brand may be **The Unexpected Professor**, but a pseudonym must not be
treated as a technical or legal anonymity mechanism.

Before public launch:

- determine whether the project is personal, professional, institutional, or
  mixed, and obtain appropriate advice for the corresponding French legal
  notice requirements;
- decide what editor identity and hosting information must appear publicly;
- consult the institution or DPO before presenting the site as connected to
  the IUT or using institutional logos;
- publish a privacy page describing server logs, embedded media, analytics,
  contact forms, retention, and rights;
- minimise and rotate IP-containing server logs;
- do not enable analytics until its purpose and legal basis are documented;
- avoid a contact form initially if a dedicated email alias is sufficient;
- if a form is added, provide the required information at collection time;
- block third-party video loading until consent;
- select separate licences for original educational content and source code;
- maintain an attribution register for diagrams, fonts, photographs, music,
  clips, and reused source material;
- review YouTube music, image, and footage rights independently of website
  publication rights.

No student-specific data should be collected by the public pilot. If that
changes, stop implementation and perform a new privacy and security review.

## 13. Security baseline

### 13.1 Server

- Supported Ubuntu LTS or another explicitly supported distribution.
- SSH keys only; disable password authentication after recovery access is
  verified.
- Separate non-root administrative account.
- Host and provider firewall rules with only required ports open.
- Automatic security updates with a documented reboot process.
- Docker containers running as non-root wherever supported.
- No Docker socket exposed to application containers.
- Deployment dashboard protected by a strong unique credential and preferably
  a private administrative path or network.
- Secrets stored outside Git and rotated if accidentally disclosed.
- Resource limits and restart policies for application containers.
- Log rotation and disk-usage alerts.

### 13.2 Application

- Dash debug mode disabled in production.
- Dependencies reviewed and updated on a scheduled basis.
- No arbitrary code execution, file upload, or user-provided HTML.
- Validate all future query parameters and user inputs.
- Conservative Content Security Policy and frame policy.
- Generic error responses to students; detailed traces remain in protected
  logs.
- Health endpoints reveal no sensitive configuration.

### 13.3 Operational access

Document who can access:

- domain registrar and DNS;
- VPS provider console;
- Git repository and deployment keys;
- server SSH;
- deployment dashboard;
- YouTube channel;
- Moodle course;
- backups and recovery credentials.

Enable multi-factor authentication where available and store recovery codes in
an appropriate offline password manager or secure institutional location.

## 14. Backups, recovery, and continuity

Git is the primary recovery source for code and content, but it is not a backup
of DNS, provider configuration, secrets, certificates, analytics data, or
deployment state.

Minimum backup design:

- provider snapshot or automated VPS backup;
- independent encrypted off-site backup of persistent volumes and essential
  configuration;
- documented DNS records and server bootstrap steps;
- daily backups with an initial target of 7 daily and 4 weekly recovery
  points, to be reviewed after storage use is known;
- automated success/failure notification;
- quarterly restore exercise to a temporary environment;
- recovery runbook containing the order in which DNS, proxy, website, labs,
  and optional databases are restored.

Classroom fallback:

- keep static screenshots or a recorded demonstration of each critical lab;
- keep exercises usable without the live service;
- do not make the public service a single point of failure for assessment;
- provide Moodle with a temporary maintenance message or alternative resource
  when an outage is known.

## 15. Monitoring and capacity

Monitor at least:

- HTTPS reachability and certificate expiry;
- HTTP response time for the website and each lab;
- CPU, memory, disk use, load, and container restart count;
- failed deployments and failed backups;
- application error rate and callback duration;
- free disk space before container builds;
- synthetic completion of one representative Dash interaction when feasible.

Initial service objectives are intentionally modest:

- the site and lab should be available during announced teaching sessions;
- routine updates should be recoverable without data loss;
- the previous version should be restorable within one documented maintenance
  session;
- no formal uptime promise is made during the pilot.

Before classroom reliance, run a load test representing the expected class
size and interaction pattern. Record the test script, server size, container
settings, peak resource use, callback latency, failures, and the resulting
capacity decision in this document.

## 16. Publishing workflow

### 16.1 New lesson

1. Create a draft from the canonical lesson template.
2. Add objectives, prerequisites, explanation, sources, and accessibility
   text.
3. Associate a video ID only after the YouTube upload state is known.
4. Associate a lab URL only after its production health check passes.
5. Preview desktop, mobile, keyboard navigation, mathematics, and print view.
6. Review copyright, attribution, and public/private boundaries.
7. Publish the site page.
8. Add the canonical page URL to the YouTube description.
9. Add the canonical page or full-screen lab URL to Moodle.
10. Record the publication in the work log.

### 16.2 New or updated lab

1. Develop and test physics separately from the interface.
2. Verify callbacks locally with the documented virtual environment.
3. Build the production container without secrets or local-only files.
4. Run unit, smoke, asset, and visual tests.
5. Deploy to preview and test through the reverse proxy.
6. Load-test if the computational profile changed.
7. Deploy the immutable verified revision to production.
8. Confirm monitoring and rollback.
9. Update lesson links, Moodle, and this tracker.

### 16.3 New video

1. Use the website lesson outline as the content brief.
2. Verify visual and audio rights before editing.
3. Produce captions and a transcript.
4. Publish with the correct public, unlisted, or private visibility.
5. Add chapters and link to the canonical lesson and lab.
6. Update the lesson metadata and verify consent-controlled embedding.
7. Add the video to the matching playlist and record the release.

## 17. Progress tracker

Status values:

- `NOT STARTED`: no implementation work has begun.
- `IN PROGRESS`: actively being implemented in the current workstream.
- `BLOCKED`: cannot proceed without a named decision or external action.
- `VERIFY`: implementation exists but acceptance checks are incomplete.
- `DONE`: acceptance criteria passed and evidence is recorded.
- `DEFERRED`: intentionally outside the current phase.

Update `Status`, `Evidence / reference`, and `Last update` whenever work is
performed. A completed row must point to a commit, deployed URL, test record,
or documented decision.

| ID | Workstream | Deliverable / acceptance criterion | Status | Depends on | Evidence / reference | Last update |
|---|---|---|---|---|---|---|
| UPH-000 | Governance | Create this canonical hub plan and tracker | DONE | None | `unexpected_professor_hub.md`; Commit 0 subject below | 2026-09-01 |
| UPH-001 | Identity | Confirm exact public spelling, capitalisation, and YouTube handle | DONE | None | **The Unexpected Professor**; `https://www.youtube.com/@TheUnexpectedProfessor` | 2026-09-01 |
| UPH-002 | Identity | Shortlist domains and verify availability, trademark ambiguity, and handle consistency | NOT STARTED | UPH-001 | — | 2026-09-01 |
| UPH-003 | Identity | Register domain and enable registrar MFA/recovery | NOT STARTED | UPH-002 | — | 2026-09-01 |
| UPH-004 | Governance | Decide French-only versus bilingual launch | DONE | UPH-001 | French-first launch; English may be evaluated later | 2026-09-01 |
| UPH-005 | Governance | Select content, code, and asset licensing policy | DONE | None | Educational content: `CC-BY-SA-4.0`; code: `GPL-3.0-only`; third-party and brand assets require explicit notices; see `LICENSE.md` | 2026-09-01 |
| UPH-006 | Governance | Determine personal/professional/institutional status and legal-notice requirements | IN PROGRESS | UPH-001 | Personal/non-professional status confirmed; host identification and final legal/privacy notice must be reviewed before launch and status reassessed before monetisation or affiliation | 2026-09-01 |
| UPH-007 | Source control | Audit existing material for public export and metadata exposure | DONE | UPH-005, UPH-006 | `documentation/asset-audit-cm1_dash.md`: `cm1_dash` cleared for export with 3 required changes to apply during UPH-019 (rebrand course identifiers, flatten PNGs, drop the dev log); dependency licences all permissive/compatible; no student data, secrets, or personal identifiers. Owner confirmed 2026-09-01 that the circuit diagrams are entirely their own work | 2026-09-01 |
| UPH-008 | Source control | Create clean public-platform repository with protected secrets and correct author identity | DONE | UPH-001, UPH-005 | Commit 0 (`0c5a043`) and Commit 1 (`5a71a77`) published on `origin/main`; repository-local pseudonymous author and account-scoped no-reply email configured; dedicated `github-unexpected-professor` SSH alias verified; README, licences, security/contribution policies, ignore rules, and public-boundary checklist published. Note: earlier commits still contain the maintainer's local clone path in history | 2026-09-01 |
| UPH-009 | Architecture | Decide Coolify versus Docker Compose + Caddy | DONE | None | ADR-010 resolved 2026-09-01: **Docker Compose + Caddy**; see section 4.3 | 2026-09-01 |
| UPH-010 | Hosting | Select EU VPS provider, region, initial capacity, backup option, and budget ceiling | IN PROGRESS | UPH-009 | Budget ceiling set at EUR 5-10/month (2 vCPU / 4 GB class); EU provider, region, and backup option still to be selected | 2026-09-01 |
| UPH-011 | Hosting | Provision VPS, administrative account, SSH keys, firewall, and updates | NOT STARTED | UPH-003, UPH-010 | — | 2026-09-01 |
| UPH-012 | Hosting | Configure DNS and obtain HTTPS for canonical site and lab names | NOT STARTED | UPH-003, UPH-011 | — | 2026-09-01 |
| UPH-013 | Site | Scaffold Astro static site and validated content collections | NOT STARTED | UPH-004, UPH-008 | — | 2026-09-01 |
| UPH-014 | Site | Establish accessible temporary visual system and responsive navigation | NOT STARTED | UPH-001, UPH-013 | — | 2026-09-01 |
| UPH-015 | Site | Implement canonical lesson template and navigation between lessons | NOT STARTED | UPH-013 | — | 2026-09-01 |
| UPH-016 | Site | Add sitemap, feed, canonical metadata, error page, and basic SEO validation | NOT STARTED | UPH-013 | — | 2026-09-01 |
| UPH-017 | Privacy | Add legal, privacy, licence, attribution, and contact pages | NOT STARTED | UPH-005, UPH-006, UPH-013 | — | 2026-09-01 |
| UPH-018 | YouTube | Implement consent-controlled privacy-enhanced video component with direct-link fallback | NOT STARTED | UPH-013, UPH-017 | — | 2026-09-01 |
| UPH-019 | Labs | Select and export the first approved Dash lab into the public repository | NOT STARTED | UPH-007, UPH-008 | Selected 2026-09-01: `new_course/images/plotting_python/cm1_dash/` (converter-foundations slice); export blocked on the UPH-007 asset audit | 2026-09-01 |
| UPH-020 | Labs | Pin dependencies, add Gunicorn, Dockerfile, non-root runtime, and health check | NOT STARTED | UPH-019 | — | 2026-09-01 |
| UPH-021 | Labs | Add physics unit tests, server smoke test, asset verification, and responsive visual checks | NOT STARTED | UPH-020 | — | 2026-09-01 |
| UPH-022 | Deployment | Add production Compose/deployment definitions without secrets | NOT STARTED | UPH-009, UPH-013, UPH-020 | — | 2026-09-01 |
| UPH-023 | Deployment | Add automated build, validation, deployment, deployed-SHA record, and rollback | NOT STARTED | UPH-011, UPH-022 | — | 2026-09-01 |
| UPH-024 | Pilot content | Publish one complete lesson with text, sources, video or placeholder, and lab link | NOT STARTED | UPH-015, UPH-018, UPH-021 | — | 2026-09-01 |
| UPH-025 | Production | Deploy website and first lab over HTTPS and complete public smoke tests | NOT STARTED | UPH-012, UPH-023, UPH-024 | — | 2026-09-01 |
| UPH-026 | Performance | Load-test representative classroom use and record capacity decision | NOT STARTED | UPH-025 | — | 2026-09-01 |
| UPH-027 | Moodle | Add pilot lesson/lab URL resources and test desktop, mobile, and iframe behaviour | NOT STARTED | UPH-025 | — | 2026-09-01 |
| UPH-028 | Operations | Implement off-site backup, retention, alerting, and a successful restore exercise | NOT STARTED | UPH-011, UPH-023 | — | 2026-09-01 |
| UPH-029 | Operations | Implement availability/resource monitoring and log rotation | NOT STARTED | UPH-025 | — | 2026-09-01 |
| UPH-030 | Documentation | Complete deployment, recovery, publishing, and incident runbooks | NOT STARTED | UPH-023, UPH-028, UPH-029 | — | 2026-09-01 |
| UPH-031 | Pilot review | Review student/visitor feedback, operations burden, accessibility, and costs | NOT STARTED | UPH-026, UPH-027, UPH-030 | — | 2026-09-01 |
| UPH-032 | Scale decision | Decide whether to add more lessons/labs, resize/split services, or seek institutional hosting | NOT STARTED | UPH-031 | — | 2026-09-01 |
| UPH-033 | Analytics | Evaluate and, only if justified, deploy privacy-oriented aggregate analytics | DEFERRED | UPH-017, UPH-025 | Candidate: self-hosted Umami | 2026-09-01 |
| UPH-034 | Authentication | Evaluate institutional authentication or LTI 1.3 if protected student features are required | DEFERRED | Explicit new requirement | — | 2026-09-01 |
| UPH-035 | Video sovereignty | Re-evaluate PeerTube, mirroring, storage, transcoding, and bandwidth | DEFERRED | Sustained audience/archive requirement | — | 2026-09-01 |

## 18. Phase acceptance criteria

### Phase 0 — Decisions and safe project boundary

- Brand spelling and language scope recorded.
- Domain and hosting decision recorded with owner and recurring cost.
- Licence and legal review actions recorded.
- Public repository created without unintended history, identity, secrets, or
  restricted assets.

### Phase 1 — Local vertical slice

- Astro site builds locally from validated content.
- One lesson page renders correctly on desktop and mobile.
- YouTube component remains unloaded until consent and has a direct-link
  fallback.
- First Dash container builds and responds through Gunicorn.
- Site-to-lab navigation works locally.

### Phase 2 — Self-hosted pilot

- DNS and HTTPS work for the canonical website and lab URLs.
- Deployment is reproducible from the repository.
- Production does not expose debug mode, secrets, internal ports, or an
  unrestricted administration interface.
- Website and lab health checks pass.
- Previous release can be restored.

### Phase 3 — Teaching readiness

- Expected classroom interaction load has been tested.
- Moodle links work on desktop and mobile.
- Static fallback material exists.
- Backups, monitoring, and log rotation operate successfully.
- Legal, privacy, attribution, and contact pages are published.
- Operations and publishing runbooks have been followed once by the owner.

### Phase 4 — Repeatable publication

- A second lesson or lab can be published using the documented workflow
  without redesigning infrastructure.
- Content and application changes can be deployed independently.
- Costs, maintenance time, incidents, and feedback are reviewed.
- Scaling or institutional-hosting decisions use measured evidence.

## 19. Ordered atomic commit sequence

The implementation must use an ordered, atomic commit sequence. When this plan
is first committed, **Commit 0 contains only this document**. Implementation
does not begin in the same commit.

0. `docs(plan): add The Unexpected Professor hub roadmap`
   - Commit only `unexpected_professor_hub.md`.
1. `chore(hub): establish public repository boundaries`
   - Add repository scaffolding, ignore rules, licence placeholders, security
     policy, and contribution/author metadata decisions.
2. `feat(site): scaffold the educational website`
   - Add the Astro application, content schema, navigation, base styles, and
     local verification.
3. `feat(site): add privacy-aware lesson media`
   - Add the lesson template, consent-controlled YouTube component, legal-page
     structure, and accessibility checks.
4. `feat(labs): productionize the first Dash laboratory`
   - Export only approved code/assets; add locked dependencies, tests,
     Gunicorn, health check, and a non-root Docker image.
5. `chore(deploy): add self-hosted production stack`
   - Add Compose/Coolify-compatible deployment configuration, proxy routing,
     environment examples, security defaults, and rollback instructions.
6. `feat(content): publish the first integrated lesson`
   - Add one reviewed lesson linking its video and lab, with sources,
     transcript/placeholder, downloads, attribution, and responsive checks.
7. `chore(ops): add monitoring backup and recovery procedures`
   - Add monitoring definitions, backup scripts/configuration, retention,
     alerts, and a verified restore record.
8. `docs(release): record pilot deployment and Moodle handoff`
   - Record production URLs, deployed SHAs, load-test outcome, Moodle checks,
     known limitations, costs, and the exact resume point.

If the public hub is created in a new repository, Commit 0 and subsequent
commits belong there. The copy of this overview in the course repository should
then be replaced by or linked to the canonical public-project copy, without
allowing two independently edited trackers to develop.

Every implementation commit should update the relevant tracker row and append
one work-log entry when that update does not compromise the commit's atomic
scope.

## 20. Decision log

| Decision ID | Date | Decision | Status | Rationale / consequence |
|---|---|---|---|---|
| ADR-001 | 2026-09-01 | Use YouTube for video delivery during the pilot | ACCEPTED | Avoids early storage, transcoding, egress, and player operations |
| ADR-002 | 2026-09-01 | Self-host the website and Dash labs on controllable infrastructure | PROPOSED | Provides control and portability while retaining YouTube reach |
| ADR-003 | 2026-09-01 | Use an EU VPS rather than a home server for the primary endpoint | PROPOSED | Improves network availability and separates the public service from the home network |
| ADR-004 | 2026-09-01 | Use Astro with Markdown/MDX for the public educational site | PROPOSED | Suits durable, versioned, content-heavy pages with low runtime overhead |
| ADR-005 | 2026-09-01 | Containerise each Dash lab and serve it through Gunicorn | PROPOSED | Reproducible, portable production execution without Dash debug mode |
| ADR-006 | 2026-09-01 | Keep Moodle responsible for students, assessment, and restricted material | ACCEPTED | Avoids duplicating LMS functions and collecting student data publicly |
| ADR-007 | 2026-09-01 | Create a clean public repository rather than publishing the course repository | ACCEPTED | Protects private material, metadata, and unrelated history |
| ADR-008 | 2026-09-01 | Defer analytics until a purpose and privacy basis are documented | ACCEPTED | Reduces launch complexity and tracking exposure |
| ADR-009 | 2026-09-01 | Defer PeerTube and self-hosted video | ACCEPTED | Video operations are disproportionate to the initial need |
| ADR-010 | 2026-09-01 | Deploy the pilot with **Docker Compose + Caddy**, not Coolify | ACCEPTED | Minimal auditable stack with automatic HTTPS fits a single-maintainer pilot (one site + one lab) on a EUR 5-10/month VPS; containers stay Coolify-compatible so the control plane can change later without touching application code |
| ADR-016 | 2026-09-01 | Target a small EU VPS with a EUR 5-10/month ceiling (2 vCPU / 4 GB class) for the pilot | ACCEPTED | Sets the capacity envelope for sizing, worker counts, and load testing; revisit if callback load or a second lab exceeds it |
| ADR-017 | 2026-09-01 | Make the first vertical slice a converter-foundations lesson reusing the existing `cm1_dash` Dash pilot | ACCEPTED | Lowest new-work path to a complete lesson + lab + video slice; depends on the UPH-007 asset audit clearing the code and assets for public release |
| ADR-011 | 2026-09-01 | Use **The Unexpected Professor** as the exact public display name and `unexpected-professor/unexpected-hub` as the public GitHub namespace | ACCEPTED | Establishes the initial brand and clean public source boundary; YouTube handle and domain remain separate decisions |
| ADR-012 | 2026-09-01 | Launch in French first | ACCEPTED | Matches the immediate teaching audience and avoids maintaining premature bilingual duplication |
| ADR-013 | 2026-09-01 | Operate initially as a personal, non-professional project independent of formal IUT affiliation | ACCEPTED | Preserves a clear public boundary; legal and institutional status must be reassessed if funding, monetisation, branding, or official use changes |
| ADR-014 | 2026-09-01 | Licence original educational content under `CC-BY-SA-4.0` and source code under `GPL-3.0-only` | ACCEPTED | Supports reuse with attribution and share-alike obligations while keeping code under strong copyleft; third-party material remains under its original terms |
| ADR-015 | 2026-09-01 | Use a dedicated GitHub SSH identity for the `unexpected-professor` account | ACCEPTED | Existing key `id_ed25519_tup` authenticates as `unexpected-professor`; SSH alias `github-unexpected-professor` and the repository remote now select it explicitly |

## 21. Risk register

| Risk | Probability / impact | Mitigation | Trigger for review |
|---|---|---|---|
| Public repository exposes private or identifying material | Medium / High | Fresh repository, explicit export audit, secret scan, metadata review | Before first push and every bulk import |
| VPS is unavailable during class | Medium / High during pilot | Monitoring, load test, static fallback, rollback, no assessment dependency | Before Moodle launch and after capacity changes |
| Dash callbacks exhaust CPU or memory | Medium / Medium-High | Measure workers and memory, set limits, optimise or resize based on data | Before whole-class use |
| Website and Moodle content diverge | Medium / Medium | Website is canonical for public lessons; Moodle links rather than copies | Every course revision |
| YouTube embed creates privacy non-compliance | Medium / High | Consent-controlled loading, privacy-enhanced URL, privacy notice | Before video component release |
| Pseudonym is mistaken for legal anonymity | Medium / High | Determine status and disclosure obligations before launch | Before domain publication or monetisation |
| Copyright prevents public reuse of course assets | Medium / High | Asset register, licence review, replace or omit uncertain material | Before each public export |
| Self-hosting maintenance displaces teaching work | Medium / Medium | Keep stack small, automate routine tasks, track maintenance time | Pilot review |
| Backups exist but cannot be restored | Medium / High | Scheduled restore exercise and documented recovery order | Quarterly and after storage changes |
| Coolify/control plane consumes too many resources | Medium / Medium | Begin with adequate RAM, monitor builds, or fall back to plain Compose | First container builds and load test |
| Domain/brand inconsistency weakens discovery | Medium / Medium | Confirm exact spelling, handles, canonical domain, and redirects first | Before registration and branding work |

## 22. Research references

These are starting references, not frozen specifications. Re-check product
requirements, prices, and legal guidance at the time of implementation.

- [Astro content collections](https://docs.astro.build/en/guides/content-collections/)
- [Docker Compose in production](https://docs.docker.com/compose/how-tos/production/)
- [Caddy automatic HTTPS](https://caddyserver.com/docs/automatic-https)
- [Caddy reverse proxy](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy)
- [Coolify self-hosted installation](https://coolify.io/docs/get-started/installation)
- [Coolify application deployment](https://coolify.io/docs/applications/index)
- [YouTube video and playlist embedding](https://support.google.com/youtube/answer/171780)
- [Moodle URL resource settings](https://docs.moodle.org/404/en/URL_module_settings)
- [Moodle LTI external tools](https://docs.moodle.org/502/en/LTI_External_tools)
- [CNIL guidance for third-party embedded content and trackers](https://www.cnil.fr/fr/questions-reponses-lignes-directrices-modificatives-et-recommandation-cookies-traceurs)
- [CNIL practical web communication guidance](https://www.cnil.fr/fr/rgpd-en-pratique-communiquer-en-ligne)
- [French government guidance on website legal notices](https://www.economie.gouv.fr/entreprises/developper-son-entreprise/innover-et-numeriser-son-entreprise/mentions-sur-votre-site-internet-les-obligations-respecter)
- [PeerTube hardware guidance](https://joinpeertube.org/en_US/faq)

## 23. Work log

Append entries in chronological order. Do not delete an entry when later work
supersedes it; link to the new decision or correction.

| Date | Session / scope | Work completed | Verification / evidence | Commit or deployment | Next resume point |
|---|---|---|---|---|---|
| 2026-09-01 | Initial hosting study and hub plan | Defined the YouTube/site/Dash/Moodle roles; compared VPS deployment models; specified architecture, operational baseline, phased tracker, decision log, risks, and atomic commit sequence | Markdown structure inspected; `git diff --check` passes | Course-repository planning commit `1e680e6` | Establish the canonical plan in the clean public repository |
| 2026-09-01 | Phase 0 identity and repository boundary | Confirmed the display name **The Unexpected Professor**; audited the empty `unexpected-professor/unexpected-hub` clone and remote; prevented inheritance of the personal global Git email by setting repository-local pseudonymous author metadata | GitHub reports `unexpected-professor` as user ID `323542878`; local repository is empty on `main`; remote is `git@github.com:unexpected-professor/unexpected-hub.git` | Commit 0: `docs(plan): add The Unexpected Professor hub roadmap` | Confirm GitHub email-privacy settings and exact YouTube handle, then resolve language, licence, legal status, domain, and ADR-010 |
| 2026-09-01 | Phase 0 project choices | Recorded `@TheUnexpectedProfessor`, French-first publication, personal/non-professional status, `CC-BY-SA-4.0` educational content, and `GPL-3.0-only` code; attempted the authorised first push | Local tracker and licence boundary updated; GitHub rejected the push because SSH authenticated as `luizvilla`, leaving the remote empty and local Commit 0 intact | Commit 1: `chore(hub): establish public repository boundaries` (local) | Configure a dedicated GitHub SSH identity, push Commit 0, then request separate approval before pushing Commit 1 |
| 2026-09-01 | Phase 0 GitHub authentication recovery | Located the existing dedicated `id_ed25519_tup` key, verified it authenticates as `unexpected-professor`, published exactly Commit 0, added the `github-unexpected-professor` SSH alias, and made the repository remote use that alias | `origin/main` at `0c5a043`; local `main` one commit ahead at Commit 1; SSH authentication test returned `Hi unexpected-professor!` | Remote: `0c5a043`; local: `e82d958` before amendment | Review the amended local Commit 1 and obtain explicit approval before pushing it |
| 2026-09-01 | Phase 0 boundary publication and deployment decisions | Scanned Commit 1 for secrets/personal data, published Commit 1 to `origin/main` (UPH-008 DONE); resolved ADR-010 to Docker Compose + Caddy (UPH-009 DONE); set the EUR 5-10/month VPS budget ceiling (ADR-016); selected the `cm1_dash` converter-foundations first vertical slice (ADR-017); scrubbed the maintainer's local clone path from the working document | `origin/main` at `5a71a77`; `git rev-list` shows local and remote level; sensitive-string scan of Commit 1 clean apart from the already-public clone path | `docs(hub): record deployment model and pilot slice decisions` (follows Commit 1; not part of the numbered feature sequence) | Run the UPH-007 asset audit on `cm1_dash`, then shortlist a domain/registrar and an EU VPS provider |
| 2026-09-01 | UPH-007 asset audit of `cm1_dash` | Read every `cm1_dash` source file, the two matplotlib originals, all 11 circuit PNGs, and the dev log; checked dependency licences, git authorship, embedded metadata, and course identifiers against `public-boundary.md` | `documentation/asset-audit-cm1_dash.md`: cleared for export; required changes are rebranding the `Énergie S3 / CM1 / CM2` identifiers, flattening the PNGs (they embed editable `mxfile` XML), and dropping `dash_development.md`; deps (`dash`/`dbc`/`plotly`/`numpy`/`matplotlib`/`Pillow`) all permissive and GPL-compatible; no student data, secrets, or personal identifiers | `docs(hub): record the cm1_dash asset audit` (follows the decisions commit) | UPH-007 signed off (owner confirmed diagram authorship 2026-09-01). Next: shortlist a domain/registrar and an EU VPS provider, then start UPH-019 export |

## 24. Known open questions

1. Which matching `.fr`, `.com`, or other domain names are available?
2. Which EU VPS provider and region, and which backup option, within the
   EUR 5-10/month ceiling (ADR-016)?
3. What is the expected maximum simultaneous class size (needed for load
   testing and worker sizing)?
4. Should the first lab be publicly discoverable, public but unlisted, or
   protected through institutional infrastructure?
5. Does any `cm1_dash` asset or dependency contain third-party material that
   prevents release under `CC-BY-SA-4.0` / `GPL-3.0-only`? (UPH-007)
6. What exact legal notice is appropriate once the VPS provider and domain
   registrar are known?

Resolved: exact name and handle (ADR-011), launch language (ADR-012), legal
status (ADR-013), licensing (ADR-014), deployment control plane (ADR-010),
budget ceiling (ADR-016), first vertical slice (ADR-017).

## 25. Resume from here

Phase 0 is nearly complete. Commit 0 and Commit 1 are published on
`origin/main` through the dedicated `unexpected-professor` SSH identity. The
repository boundary, licensing, identity, deployment model (Docker Compose +
Caddy), budget ceiling, and first vertical slice (`cm1_dash` converter
foundations) are all decided. No domain, VPS, application scaffold, exported
course asset, or deployment exists yet.

Remaining Phase 0 work, in order:

1. **UPH-002 / UPH-003** — shortlist `.fr` / `.com` domains, verify
   availability and handle consistency, choose a registrar, register, enable
   MFA.
2. **UPH-010** — pick an EU VPS provider, region, and backup option within the
   EUR 5-10/month ceiling; record owner and recurring cost.

UPH-007 is DONE: the `cm1_dash` audit
(`documentation/asset-audit-cm1_dash.md`) cleared the pilot for export, and
the owner confirmed the circuit diagrams are their own work. The three
required changes (rebrand identifiers, flatten PNGs, drop the dev log) are
applied during UPH-019, not now.

GitHub email privacy was reviewed and judged not necessary for this project.

Then Phase 1 begins with the numbered feature sequence: Commit 2
(`feat(site): scaffold the educational website`), Commit 3 (privacy-aware
lesson media), Commit 4 (productionise the `cm1_dash` laboratory).

Do not begin broad site design or copy course assets until the UPH-007 audit
has cleared the pilot material.
