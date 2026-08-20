# 🌿 Grihine Soap

Pure. Handcrafted. From the Hills of Kurseong.

The official website of **Grihine Soap** — handcrafted organic soaps made by the
**Shree Ganesh Self Help Group**, Ambootia Tea Estate, Darjeeling Hills,
West Bengal, India.

**Live site:** https://shadowgreen9371.github.io/grihine-soap/

## Stack

Pure static HTML + CSS + JavaScript. No frameworks, no build step, no cookies,
no trackers. All product art is hand-drawn CSS; fonts are self-hosted.

```
index.html      landing page
products.html   catalogue
about.html      the committee's story
contact.html    order form (opens WhatsApp pre-filled)
privacy.html    DPDP Act 2023 privacy policy
style.css       all styles + self-hosted @font-face
script.js       menu, cart (localStorage only), WhatsApp ordering
fonts/          Playfair Display + Lato (woff2, latin subset)
images/         real product photos (optional — CSS art used meanwhile)
```

## Privacy & security

- Registered-conscious design for India's **Digital Personal Data Protection Act, 2023**:
  the site itself collects **zero personal data** — no cookies, no analytics,
  no third-party requests. Orders travel device → WhatsApp only.
- Content-Security-Policy + strict referrer policy on every page.
- Vulnerability reports: see `.well-known/security.txt`.

## Deploying

**Primary — GitHub Pages:** push to `main`; Pages serves the repo root.
(`.nojekyll` included.)

**Fallback — Hostinger FTP:** `cp .deploy.env.example .deploy.env`, fill in the
FTP credentials from hPanel, then `./deploy.sh`. See `README-HOSTINGER.md`.

## Before going to market

Search-and-replace these placeholders:

- `91XXXXXXXXXX` — real WhatsApp number (in `script.js` and all HTML files)
- Grievance Officer name in `privacy.html` (DPDP requirement)
- Google Maps embed in `contact.html` (marked `REPLACE`)

---

Made with ♥ in the Darjeeling Hills.
