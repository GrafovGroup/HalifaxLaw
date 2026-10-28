# HalifaxLaw.ca

Bilingual, static website for Kostyantyn Mykhalchenko, Barrister, Solicitor & Notary Public, at Pavel Boubnov – Barrister & Solicitor.

Live site: https://halifaxlaw.ca

## Build and validate

Requires Python 3.12 or newer. No Python dependencies or JavaScript build tooling are required.

```sh
python3 generate.py
python3 validate.py
node --check dist/app.js
```

`dist/` contains the deployable static website, including images and local fonts. A static host must serve directory `index.html` files and use `dist/404.html` for missing routes. For local development, any static server can serve `dist/`.

## Editing

- `generate.py`: page templates and bilingual content; stable route definitions.
- `expansion.py`, `criminal.py`: service and community content.
- `experience.py`: navigation improvements, appointment questions and linked JSON-LD entities.
- `contact_form.py`: accessible Formspree form markup.
- `dist/styles.css`, `dist/app.js`: maintained source assets; do not delete `dist/` before building.
- `image-placements.json`, `image_placements.py`: assigned photographs, attribution and alt text. Keep image licences and font licences with the project.
- `validate.py`: route, anchor, sitemap, heading, language alternate, image and structured-data checks.

The generator writes 86 route pages plus the host-level 404 fallback. The sitemap contains 82 indexable URLs. Canonicals and language alternates target `https://halifaxlaw.ca`. Robots, sitemap, social metadata and structured data are generated at build time; the site does not require JavaScript for its content or FAQs.

## Contact and privacy

The existing Formspree endpoint is a public form action, not a secret. Do not send test enquiries without the owner's authorization. Browser checks cover validation and topic selection, not delivery to the practice's inbox. No analytics, advertising tags or browser storage of form entries are introduced.

Appointment languages are English, Ukrainian and Russian. French content does not promise French-language representation. Do not add office addresses, prices, reviews, certifications, legal-review dates or service guarantees without confirmation. Legal information needs professional review when changed.

## Publication

OpenAI Sites remains the live host. `.openai/hosting.json` preserves the existing project identity. GitHub is the source repository copy; pushing to this repository alone does not deploy the live Site or configure GitHub Pages. Publish an exact validated source revision through Sites for subsequent releases.

Never commit credentials, environment secrets, access tokens or local preview state.

## October 27, 2026 improvements

- Clear appointment and phone actions; service shortcuts; smaller mobile hero.
- Sticky navigation, mobile contact actions, keyboard dismissal and JavaScript-free navigation fallback.
- Service-specific enquiry links, topic preselection in both languages and contextual language switching.
- Preparation and FAQ anchors, full breadcrumbs, contact expectations and accessible form validation.
- Linked Organization, Person, WebSite, WebPage, Service and BreadcrumbList entities; FAQ schema on the dedicated FAQ pages matches visible answers.
- Social images, locale metadata, image-preview directives and multilingual sitemap annotations.

These changes improve usability and discoverability; they do not establish search rankings, AI citations or FAQ rich-result eligibility. No search-engine ownership verification, sitemap submission or inbox delivery test is claimed.

## Practice imagery additions

Twenty original editorial photographs add relevant imagery to six bilingual service articles, four criminal-law cards, and bilingual contact/resources pages. The existing criminal-law article images and professional photographs are retained. New assets are `dist/assets/practice-*.webp`; each has a 600px responsive derivative, descriptive English/French alt text and lazy loading. The entire new image set including derivatives is approximately 1.92 MB.

`imagery-additions.json` records the complete built-in image-generation prompts and asset destinations. `image-placements.json` controls placements and provenance. `IMAGE-REVIEW-2026-10-27.json` records local uniqueness screening and its limits. Generated scenes illustrate service context; they do not depict actual clients, staff or premises.
