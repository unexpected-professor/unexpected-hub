# Domain and hosting options (UPH-002, UPH-010)

Research date: 2026-09-01. Prices and availability change frequently — reconfirm
at the registrar and provider before purchase. This document informs the two
open Phase 0 decisions; it does not itself register or provision anything.

Constraints carried in from earlier decisions:

- Public name **The Unexpected Professor**, YouTube handle
  `@TheUnexpectedProfessor` (ADR-011).
- French-first, personal / non-professional project (ADR-012, ADR-013).
- Deployment: Docker Compose + Caddy on one small EU VPS (ADR-010).
- Monthly hosting budget ceiling EUR 5-10, 2 vCPU / 4 GB class (ADR-016).

## 1. Domain

### 1.1 Availability check

Checked via RDAP on 2026-09-01 (registry responses; a registrar may still
apply premium pricing or a hold). **All of the following were unregistered:**

| Candidate | TLD | Notes |
|---|---|---|
| `theunexpectedprofessor.com` | .com | Exact match to the YouTube handle |
| `unexpectedprofessor.com` | .com | Shorter; drops the leading "the" |
| `unexpected-professor.com` | .com | Matches the GitHub org; hyphen hurts verbal sharing |
| `theunexpectedprof.com` | .com | Abbreviated |
| `unexpectedprof.com` | .com | Abbreviated |
| `unexpectedprofessor.net` / `theunexpectedprofessor.org` | .net/.org | Fallbacks only |
| `theunexpectedprofessor.fr` | .fr | Exact match, French TLD |
| `unexpectedprofessor.fr` | .fr | Shorter |
| `unexpected-professor.fr` | .fr | Matches the GitHub org |
| `professeurinattendu.fr` / `leprofesseurinattendu.fr` | .fr | French-language variants |

### 1.2 `.fr` and the pseudonym

The `.fr` registry (AFNIC) redacts the personal data of natural-person
registrants from public WHOIS/RDAP by default, which suits the pseudonym
posture. `.fr` registration requires a registrant in the EU/EEA/Switzerland.
The registrant identity is still held by AFNIC and the registrar; this is not
legal anonymity (see `legal-and-privacy-baseline.md`). Post-GDPR `.com` WHOIS
is also redacted by default, with registrar privacy services widely available
and now standard rather than a paid add-on.

### 1.3 Recommendation

- **Canonical hostname: `theunexpectedprofessor.com`.** It matches the YouTube
  handle exactly, which is the single most important discovery signal, and it
  does not commit the project to a French-only identity if the audience later
  broadens.
- **Also register `unexpectedprofessor.com`** and redirect it (and `www`) to
  the canonical apex, to prevent a near-name being taken by someone else.
- **`.fr` is optional and can wait.** Add `theunexpectedprofessor.fr` later if
  a French-facing identity becomes useful; managing one domain is simpler for
  the pilot. If the LCEN non-professional-publisher posture makes a `.fr`
  preferable, register `theunexpectedprofessor.fr` as canonical instead and
  redirect the `.com`.
- Keep the GitHub org name `unexpected-professor` as it is; do not adopt the
  hyphenated domain.

### 1.4 Registrar options

| Registrar | Base | .fr | WHOIS privacy | Position |
|---|---|---|---|---|
| **OVHcloud** | France, EU | Yes (AFNIC) | Free, default | Recommended: one EU account can hold the domain, DNS, and the future VPS; clear French legal footing |
| Gandi | France, EU | Yes | Free, default | Solid DNS and API; renewal prices have risen in recent years |
| Cloudflare Registrar | US | No | Free redaction | At-cost `.com` pricing and free DNS, but forces Cloudflare nameservers and no `.fr` |
| Porkbun | US | Yes | Free | Cheap, good UX; not EU-based |
| Netim | France, EU | Yes | Free | EU alternative to OVH/Gandi |

**Recommendation: OVHcloud**, with account 2FA enabled and registrar-lock on.
Cloudflare Registrar is a reasonable alternative if the project stays `.com`
only and wants Cloudflare's free authoritative DNS.

## 2. VPS

Target: 2 vCPU / 4 GB / >=40 GB SSD, EU region, provider snapshots available,
within EUR 5-10/month, leaving headroom for backups.

### 2.1 Options (2026, reconfirm before purchase)

| Provider | Representative plan | Approx. price/mo | Region(s) | Notes |
|---|---|---|---|---|
| **Hetzner** | CX22 — 2 vCPU x86, 4 GB, 40 GB, 20 TB traffic | ~EUR 4.5-5 | DE, FI | Best price/performance; very large self-hosting community; Cloud Firewall included; Backups add-on = 20% of server price. Hetzner raised cloud prices several times in 2026 — treat pricing as volatile. |
| Hetzner | CAX11 — 2 vCPU ARM (Ampere), 4 GB, 40 GB | ~EUR 3.5-4 | DE, FI | Cheaper; fine because Dash/Python/Caddy all ship arm64 images. Small risk: a Python wheel without an arm64 build. |
| netcup | VPS 1000 ARM G11 — 6 vCPU, 8 GB, 256 GB NVMe | ~EUR 6.5 + VAT | DE, AT | More resources per euro; ARM stock has been intermittent; historically 12-month minimum terms. |
| **OVHcloud** | **VPS-1** — 2 vCore, 4 GB, 40 GB NVMe | ~EUR 4.6/mo TTC | EU (GRA, SBG, DE) | French/EU; single account with the domain; daily automated backup and anti-DDoS included; slightly lower raw performance than Hetzner. VPS-2 (4 vCore / 8 GB) ~EUR 8.7 is the upgrade path. |
| Contabo | ~4 vCPU, 6 GB, large disk | ~EUR 6 | DE and others | Lots of resources; more variable disk I/O and slower support. |
| Scaleway | DEV1 range | Higher for equal specs | FR, NL, PL | French sovereignty option; pricier per unit of compute. |

### 2.1a Not a VPS: OVH shared web hosting

OVH also sells *hébergement web mutualisé* (Perso, Pro, Startup, Starter,
"Hébergement gratuit"). **These are not suitable.** Shared hosting serves only
static files and PHP, with no root, no Docker, and no way to run a persistent
Gunicorn process — so it cannot host the Dash laboratory, which is half of the
pilot. The bundled "1 nom de domaine offert" is not a reason to buy one.

### 2.2 Recommendation

- **Hetzner CX22** (x86, 4 GB) in Falkenstein or Helsinki, ~EUR 5/month. This
  keeps roughly half the budget ceiling free for the Backups add-on and a small
  volume if the image cache needs it. x86 avoids any arm64 packaging surprises
  during the pilot.
- **If a French/EU-company registrar and host on one invoice is preferred:**
  **OVHcloud VPS-1** (2 vCore / 4 GB / 40 GB NVMe, ~EUR 4.6/month TTC, daily
  automated backup included) in Gravelines or Strasbourg, with Ubuntu LTS.
  Same OVH account as the domain. This is the current chosen direction.
- Either way: enable provider snapshots/backups **and** configure an
  independent off-site backup (UPH-028) — provider snapshots alone are not the
  independent copy the plan requires. Candidates for the off-site copy: Hetzner
  Storage Box, Backblaze B2, or rsync.net.

### 2.3 Initial sizing note

4 GB RAM is adequate for one Astro static site behind Caddy plus one
Gunicorn-served Dash app during the pilot. Worker count and memory per worker
are set in UPH-020 and confirmed by the UPH-026 load test before any assessed
class depends on the service. If the load test shows headroom problems, the
first step is resizing the Hetzner/OVH instance, not re-architecting.

## 3. What still needs a human decision

Decided 2026-09-01: **OVHcloud** for both the registrar and the VPS, on one
account (ADR-018).

Still to confirm:

1. Canonical TLD: `.com` (recommended) or `.fr`.
2. Exact domain string to register (recommended: `theunexpectedprofessor.com`
   canonical + `unexpectedprofessor.com` redirect).
3. VPS plan and region: **OVHcloud VPS-1**, Gravelines or Strasbourg
   (recommended).
4. Recurring cost owner and payment method (for the operations record).

Once chosen, record the registrar, the domain, the provider, the region, the
plan, the monthly cost, and the account owner in the tracker (UPH-002,
UPH-003, UPH-010) and the decision log, then provision (UPH-011) and configure
DNS/TLS (UPH-012).
