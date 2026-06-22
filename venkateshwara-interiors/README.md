# Venkateshwara Interiors — Website

A fully responsive, animated, multi-page interior-design website built with **plain HTML, CSS and JavaScript** (no build step, no framework). Designed to be reused for multiple clients by editing a single configuration file / sheet.

---

## 1. Quick start

- **To preview:** double-click `index.html` (it opens straight in the browser).
- **To publish:** upload the whole folder to any web host (Hostinger, GoDaddy, Netlify, cPanel, etc.). No server-side code is required.

> Internet is needed the first time a visitor loads the site, because the fonts (Google Fonts) and the optional Excel reader load from the web. The site still works without them — it simply falls back to system fonts.

---

## 2. Folder structure

```
venkateshwara-interiors/
├── index.html                     ← Home
├── about.html
├── services.html
├── service-modular-kitchen.html   ← 12 individual service pages
├── service-false-ceiling.html
│   …(living-room, bedroom, pooja-room, study-room, tv-showcase,
│      dining-room, cupboards-wardrobes, kids-room, toilet-bathroom, commercial)
├── gallery-images.html
├── gallery-videos.html
├── contact.html
├── privacy.html
├── terms.html
├── sitemap.html
├── 404.html
├── config.xlsx                    ← editable business details (see §3)
├── assets/
│   ├── css/style.css              ← all styling
│   ├── js/config.js               ← business details (offline-safe source)
│   ├── js/site.js                 ← builds header/footer/menus + animations
│   ├── images/                    ← ALL images in ONE folder (1.svg … 36.svg + logo, favicon, geometric)
│   └── videos/                    ← drop your .mp4 clips here (see §5)
├── gen_images.py                  ← (optional) regenerates the room images
├── gen_config_xlsx.py             ← (optional) regenerates config.xlsx
└── build_pages.py                 ← (optional) regenerates the HTML pages
```

---

## 3. Changing the business details (reuse for any client)

All business information — name, address, phone, email, GSTIN, social links, Google Map, etc. — lives in **two places that mirror each other**:

| File | Role |
|------|------|
| `assets/js/config.js` | The **always-on source**. Works even when the site is opened locally by double-click. |
| `config.xlsx` → **Settings** sheet | The **easy-to-edit spreadsheet**. When the site is hosted on a web server, it automatically overrides `config.js`. |

### The simplest workflow
1. Open **`config.xlsx`**, go to the **Settings** sheet.
2. Edit only the **Value** column (leave the **Key** column unchanged).
3. Open **`assets/js/config.js`** and update the same values so the offline copy matches.
4. Save. Done — every page updates automatically (header, footer, contact page, map, click-to-call, WhatsApp, copyright year, etc.).

> **Why both?** Browsers block spreadsheet reading when a page is opened directly from disk (`file://`). `config.js` guarantees the site always shows correct details; `config.xlsx` makes editing friendly and takes over once the site is on a real web address.

The `config.xlsx` file also has a **Guidelines** sheet — a reference list of standard website sections and best practices.

---

## 4. The images (naming + watermark system)

- Every image lives in the single folder **`assets/images/`**.
- Files are numbered **`1.svg`, `2.svg`, `3.svg` …** for easy identification.
- Each image carries a **mild watermark that matches its file number** (a large faint number plus a small `VENKATESHWARA • N` tag), so you can instantly tell which file an on-screen image came from.

### Image map (which number is used where)

| # | Used for | # | Used for |
|---|----------|---|----------|
| 1 | Home hero (living) | 19–27 | Gallery variations |
| 2 | About / villa | 28 | Home stats backdrop |
| 3 | Modular Kitchen | 29 | About process |
| 4 | False Ceiling | 30 | Testimonials backdrop |
| 5 | Living Room | 31 | Video poster — Kitchen |
| 6 | Bedroom | 32 | Video poster — Living |
| 7 | Pooja Room | 33 | Video poster — Bedroom |
| 8 | Study Room | 34 | Video poster — Pooja |
| 9 | TV Showcase | 35 | Video poster — Ceiling |
| 10 | Dining Room | 36 | Video poster — Commercial |
| 11 | Cupboards & Wardrobes | | |
| 12 | Kids Room | `logo.svg` | Brand logo (header + footer) |
| 13 | Toilet / Bathroom | `favicon.svg` | Browser tab icon |
| 14 | Commercial | `geometric.svg` | Geometric background pattern |
| 15 | Contact | | |
| 16–18 | Gallery variations | | |

### Swapping in your own photos
The supplied images are **clean vector illustrations** styled to match each room. To use your **real photographs**:
1. Save your photo with the **same number and a common image extension**, e.g. `3.jpg` for the modular-kitchen image.
2. In the page(s) that use it, change the reference from `3.svg` to `3.jpg` (a quick find-and-replace), **or** simply re-save your photo as `3.svg` is not needed — just keep the numbering consistent.
3. Keep all images in the `assets/images/` folder.

> Tip: keep your photos roughly **16:10** (e.g. 1600×1000) for the best fit.

---

## 5. The videos

- Video posters on **Video Gallery** are numbered `31.svg`–`36.svg`.
- To make them play real clips, drop your `.mp4` files into **`assets/videos/`** named **`31.mp4`, `32.mp4`, …** matching the poster numbers.
- The lightbox player is already wired to those filenames.

---

## 6. Pages & menu

Menu and footer links are generated from one list inside `assets/js/site.js`, so they stay consistent everywhere:

- **Home, About Us**
- **Services** (dropdown: all 12 specialities)
- **Gallery** (dropdown: Image Gallery, Video Gallery)
- **Contact Us** (dropdown: Privacy Policy, Terms & Conditions, Sitemap)

The **fixed footer action bar** (mobile) has the required animated icons: **Home, Call, Google Map, WhatsApp, Social**.

---

## 7. Features included

Fixed/sticky header **and** footer · shrinking glass header on scroll · animated preloader · 3D card tilt & perspective media · scroll-reveal animations · animated counters · Ken-Burns hero · mega-menu + mobile slide-in drawer · filterable image gallery with lightbox · cinematic video gallery · accordions (FAQ) · testimonials · contact form (front-end demo) · Google Map embed · breadcrumbs · back-to-top · geometric backgrounds throughout · SEO meta tags · favicon · 404 page · fully responsive (laptop / tablet / mobile) · keyboard-accessible focus states · reduced-motion support.

---

## 8. Regenerating assets (optional, advanced)

These Python scripts were used to build the project and are included for convenience:

```bash
python3 gen_images.py        # rebuilds the room illustrations
python3 gen_config_xlsx.py   # rebuilds config.xlsx
python3 build_pages.py       # rebuilds all HTML pages
```

You do **not** need Python to run or edit the website — only if you want to regenerate these assets.

---

*Built with care for Indian homes. Palette: Midnight Peacock teal · Brass gold · Ivory silk · Kumkum maroon.*
