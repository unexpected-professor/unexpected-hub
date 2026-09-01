# Legal and privacy baseline

## Status and limits

The Unexpected Professor is currently defined as a **personal,
non-professional project** operating under a public pseudonym. This document is
an implementation checklist, not legal advice. It must be reviewed when the
domain and hosting provider are selected and before the public launch.

The project is not currently presented as an official IUT service. Do not use
institutional logos, imply institutional endorsement, or move protected
student activity outside Moodle without explicit authorisation and appropriate
data-protection review.

## Pseudonymous publication

Current French LCEN provisions allow a person publishing a non-professional
online public communication service to limit the publicly displayed identity
information to the hosting provider's name and address, provided the publisher
has supplied the required personal identification to that provider.

Before relying on this provision:

- verify that the activity remains non-professional;
- verify the current legal text and obtain advice if its application to the
  chosen VPS arrangement is unclear;
- confirm which entity is legally the hosting provider;
- confirm that the provider holds the required publisher identification;
- publish the provider information required by the applicable text;
- provide a working procedure for legal notices and rights of reply.

Reference:
[French LCEN provisions on non-professional online publishers](https://www.legifrance.gouv.fr/codes/section_lc/JORFTEXT000000801164/LEGISCTA000006117684/).

Reassess this position before advertising, sponsorship, paid subscriptions,
selling training, formal institutional affiliation, or other professional
activity.

## Pilot privacy posture

The initial public site and laboratories should collect no student-specific
data and provide no public accounts, comments, uploads, grades, or submissions.
Moodle remains responsible for student identity and assessed activity.

Before launch:

- document the hosting provider, server-log fields, purposes, access, and
  retention;
- minimise and rotate logs containing IP addresses;
- publish a privacy page and a contact method for exercising rights;
- do not enable analytics until purpose, configuration, retention, and legal
  basis have been documented;
- do not load YouTube or other third-party embeds before the relevant consent;
- use a local placeholder and direct external link when consent is refused;
- do not send Moodle user identifiers or names through URL parameters;
- review any contact or newsletter form before collecting personal data.

References:

- [CNIL practical guidance for websites and online communication](https://www.cnil.fr/fr/rgpd-en-pratique-communiquer-en-ligne)
- [CNIL guidance on third-party embedded content and trackers](https://www.cnil.fr/fr/questions-reponses-lignes-directrices-modificatives-et-recommandation-cookies-traceurs)

## Launch checklist

- [ ] Personal/non-professional status reconfirmed.
- [ ] Hosting provider legal identity and address recorded.
- [ ] Publisher identification supplied to the hosting provider where required.
- [ ] Legal notice reviewed for the selected hosting arrangement.
- [ ] Privacy page matches actual logs, embeds, forms, and analytics.
- [ ] YouTube remains blocked before consent and has a direct-link fallback.
- [ ] Contact method and rights-request process tested.
- [ ] No student data or institutional private material present.
- [ ] Content, source-code, asset, and brand licensing scopes published.
- [ ] Status-change triggers assigned for periodic review.
