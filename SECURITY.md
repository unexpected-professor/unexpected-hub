# Security policy

## Current status

The project is in pre-release planning. There is no supported production
version and no public service deployed from this repository yet.

Security still matters during this phase because repository history is public
and difficult to retract completely.

## Reporting a vulnerability

Do not publish credentials, personal information, working exploits, or other
sensitive details in a public issue.

GitHub private vulnerability reporting should be enabled before the first
production release. Once enabled, use the repository's **Security** tab to
report vulnerabilities privately. Until a private reporting channel is
available, open a minimal public issue asking the maintainer to establish a
private contact channel without including sensitive details.

The project does not currently promise a formal response time. Production
response expectations will be documented before launch.

## Secrets and personal information

- Never commit `.env` files, tokens, private keys, passwords, cookies, or
  provider credentials.
- Use repository or deployment-platform secrets for automation.
- Use synthetic data in examples and tests.
- Do not include student names, email addresses, identifiers, submissions,
  grades, availability, or private Moodle data.
- If a secret is committed, treat it as compromised, rotate it immediately,
  and then remove it from current source and, where justified, history.

## Production security baseline

Before the first public deployment, the project must verify the security
requirements recorded in
[`unexpected_professor_hub.md`](unexpected_professor_hub.md), including
non-root containers, disabled debug mode, restricted ports, HTTPS, secret
management, dependency review, backups, monitoring, and rollback.
