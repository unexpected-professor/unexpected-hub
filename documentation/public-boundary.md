# Public repository boundary

## Purpose

This repository is public and represents The Unexpected Professor pseudonym.
It must not become a direct publication of a private course workspace. Existing
course material is imported selectively only after ownership, privacy,
metadata, and pedagogical review.

The current private-source candidate is the Energie S3 working repository. Its
history and complete directory tree are outside the public project boundary.

## Allowed material

- Original code written for the public website and laboratories.
- Original educational content approved for `CC-BY-SA-4.0` publication.
- Original diagrams and media whose source files are retained and whose public
  licence is recorded.
- Third-party material whose licence permits the intended redistribution and
  for which complete attribution is recorded.
- Synthetic datasets and examples that contain no personal information.
- Deployment configuration containing placeholders rather than secrets.

## Prohibited material

- Student names, identifiers, email addresses, work, grades, attendance, or
  availability.
- Private Moodle exports, enrolment data, assessment records, or messages.
- Personal addresses, phone numbers, private email addresses, or credentials.
- Institution-only files or branding without publication authorisation.
- API keys, SSH keys, `.env` contents, cookies, access tokens, or provider
  configuration containing secrets.
- Unlicensed images, music, video, fonts, proprietary documents, or copied
  textbook material.
- Editor caches, backups, generated builds, virtual environments, and machine
  paths.
- Private repository history or bulk directory copies that have not been
  reviewed file by file.

## Export checklist

Complete this checklist for every import from a private or institutional
source:

- [ ] Identify the exact source paths and intended public destination.
- [ ] Confirm that the author has the right to publish every file.
- [ ] Inspect text, images, archives, PDFs, and office-document metadata.
- [ ] Search for names, email addresses, absolute paths, secrets, and local
      configuration.
- [ ] Record third-party provenance, licence, attribution, and modifications.
- [ ] Replace real student or operational data with synthetic examples.
- [ ] Confirm the destination licence in `LICENSE.md` applies.
- [ ] Copy content without importing private Git history.
- [ ] Run secret scanning and repository-wide text searches after import.
- [ ] Build and test the exported result independently of the private source.
- [ ] Review the staged diff before commit.
- [ ] Record the audit evidence in the progress tracker and work log.

## Pseudonymous Git metadata

Repository-local Git configuration must use:

```text
user.name = The Unexpected Professor
user.email = the ID-based no-reply address supplied by GitHub
```

Do not modify the machine-wide Git identity for this project. A dedicated SSH
key and SSH host alias should authenticate pushes as the `unexpected-professor`
account rather than another personal GitHub account.

Before pushing, verify the staged commit metadata and enable GitHub's option to
block command-line pushes that expose a personal email address.

## Asset attribution register

Create the register before the first public asset import. Each entry must
include:

| Asset | Creator/source | Original licence | Modifications | Public destination | Verified by/date |
|---|---|---|---|---|---|
| _No assets imported yet_ | — | — | — | — | — |

## Boundary review triggers

Repeat the boundary review when:

- importing a new course or a batch of existing material;
- adding a contributor;
- enabling uploads, comments, accounts, analytics, or contact forms;
- establishing formal institutional affiliation;
- monetising content or offering paid training;
- changing the public licences;
- moving private and public repositories into a shared build pipeline.
