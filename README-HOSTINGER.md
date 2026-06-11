# 🌿 Grihine Soap — Hostinger Deployment Guide

This folder contains the complete, ready-to-upload Grihine Soap website:

```
index.html        ← landing page
products.html     ← product catalogue
about.html        ← story of the women's committee
contact.html      ← order form + contact details
style.css         ← all styles
script.js         ← menu, cart, WhatsApp ordering
images/           ← put real product photos here later (site works without them)
```

> ⚠️ **Before uploading**, replace the placeholders:
> 1. WhatsApp number — search for `91XXXXXXXXXX` in **script.js** and in **every .html file** and replace with the real number (e.g. `919812345678` — country code, no `+`, no spaces). Also replace the visible `+91-XXXXXXXXXX` text on contact.html and index.html.
> 2. Email — `grihinesoap@gmail.com` is already in place; change it if the real address differs.
> 3. Instagram — `@grihinesoap` / `instagram.com/grihinesoap`; change if the real handle differs.
> 4. Google Map — in **contact.html**, follow the comment marked `REPLACE` to paste the real map embed iframe.

---

## Step 1 — Log into Hostinger hPanel

1. Go to **https://hpanel.hostinger.com**
2. Sign in with the email and password used when buying the hosting plan.
3. From the dashboard, find your hosting plan and click **Manage**.

## Step 2 — Open File Manager → public_html

1. In hPanel, scroll to the **Files** section.
2. Click **File Manager**.
3. In the file tree, double-click the **`public_html`** folder — this is your website's root. Everything inside it is what visitors see.
4. If there is a default `default.php` or "Coming Soon" `index.html` inside, **delete it** first.

## Step 3 — Upload all files

1. With `public_html` open, click the **Upload** icon (top-right, arrow pointing up).
2. Select **all** the files from this folder:
   `index.html`, `products.html`, `about.html`, `contact.html`, `style.css`, `script.js`
3. Upload the `images/` folder too (use **Upload folder**, or create a folder named `images` and upload its contents into it).
4. Wait for every upload to show a green tick.

> Tip: you can also zip this whole folder, upload the single `.zip`, then right-click → **Extract** in File Manager — faster for many files.

## Step 4 — Make sure index.html is the default page

Hostinger serves `index.html` automatically when someone visits your domain — no setting needed, **as long as the file sits directly inside `public_html`** (not inside a subfolder like `public_html/grihine/`).

✅ Correct: `public_html/index.html`
❌ Wrong: `public_html/hostinger-deploy/index.html`

If you accidentally uploaded the folder itself, move the files up: select all → right-click → **Move** → `public_html`.

## Step 5 — Connect a custom domain

**If you bought the domain from Hostinger:** it's usually connected automatically — skip to Step 6.

**If the domain is from elsewhere (GoDaddy, Namecheap, etc.):**
1. In hPanel go to **Domains → Add Domain** (or **Hosting → Manage → Domains**) and add your domain (e.g. `grihinesoap.com`).
2. Hostinger will show two nameservers, normally:
   - `ns1.dns-parking.com`
   - `ns2.dns-parking.com`
3. Log in at your domain registrar, find **Nameservers / DNS settings**, and replace the existing nameservers with the two above.
4. Wait for DNS propagation — usually 1–4 hours, can take up to 24.

## Step 6 — Enable free SSL (Let's Encrypt / HTTPS)

1. In hPanel go to **Security → SSL** (or search "SSL" in the hPanel search bar).
2. Select your domain and click **Install SSL** — Hostinger's free lifetime SSL (Let's Encrypt-based) installs in a few minutes.
3. After it shows **Active**, turn ON **Force HTTPS** on the same page so all visitors get the secure `https://` version automatically.

## Step 7 — Test the live site

1. Open `https://yourdomain.com` in a normal browser window **and** an incognito window.
2. Check each page: Home, Products, Our Story, Contact.
3. Click test:
   - 🟢 **WhatsApp floating button** (bottom-right) opens a chat with the right number.
   - 🟢 **Add to Cart** increases the basket counter in the navbar.
   - 🟢 Basket icon opens WhatsApp with your cart pre-typed.
   - 🟢 Contact form opens WhatsApp with the order details filled in.
4. Test on a phone: the menu should collapse into a ☰ hamburger, and everything should fit without sideways scrolling.
5. Check the padlock icon in the address bar — it confirms SSL is working.

### Troubleshooting

| Problem | Fix |
|---|---|
| "Index of /" or file list shows instead of the site | `index.html` is not directly in `public_html` — move it there |
| Old "Coming Soon" page still shows | Delete Hostinger's default page, then hard-refresh (Ctrl+Shift+R) |
| Domain doesn't load | DNS still propagating — wait, check at https://dnschecker.org |
| "Not secure" warning | Install SSL (Step 6) and enable Force HTTPS |
| WhatsApp button opens wrong chat | You missed a `91XXXXXXXXXX` placeholder — search all files again |

---

Made with ♥ in the Darjeeling Hills 🌿
