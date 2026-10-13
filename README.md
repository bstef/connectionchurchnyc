# Connection Church NYC

A legacy website for **Connection Church NYC** — a church rooted in Astoria, Queens from 2011 to 2024. Built as a polished static page honoring the community, mission, and story of Connection Church NYC, whose legacy continues through [Queens Church](https://www.qns.church).

---

![Connection Church NYC — Hero](assets/screenshot-hero.png)

---

## About

Connection Church NYC was founded in 2011 by the McGhee and Mayberry families in Astoria, Queens — one of the most diverse neighborhoods in the world. For over 13 years the church built lasting faith, community, and mission in the heart of New York City.

In 2024, Connection Church NYC officially merged with Queens Church, continuing the same mission under a new name.

This site serves as a permanent archive and tribute to that legacy.

---

## What's on the site

| Section | Description |
|---|---|
| **Hero** | Labeled Astoria map with the former church location and core message |
| **A Church for the City** | Who Connection Church NYC was and what it stood for |
| **Important Update** | The 2024 announcement of the merge with Queens Church |
| **Our Story** | A visual timeline from 2011 founding through 2024 |
| **Find Us at Queens Church** | Service times, address, and directions |
| **Social Media** | Links to YouTube, Instagram, Facebook, Blog, and Podcast |
| **Church Partners** | Organizations that supported the mission |
| **Leadership** | The Mayberrys, McGhees, and ISI Ministry team |
| **Footer** | Full archive links and legacy credit |

---

## Social & Media

- YouTube: [@connectionchurchnyc](https://www.youtube.com/@connectionchurchnyc)
- Instagram: [@connectionnyc](https://www.instagram.com/connectionnyc/)
- Facebook: [connectionnyc](https://www.facebook.com/connectionnyc/)
- Blog: [connectionnyc.blogspot.com](https://connectionnyc.blogspot.com/)
- Podcast: [Connection Church NYC Sermons](https://podcast.app/connection-church-nyc-sermons-p282311)

---

## Tech

- Pure HTML + CSS — no frameworks, no build tools, no dependencies
- All styling inline in `index.html`
- Responsive layout with mobile breakpoints
- SVG logo (`assets/logo-icon.svg`) for crisp rendering at any size
- Hero street map © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), served as a local WebP with no runtime map service or API key
- Original terracotta map in the About section created with [terraink](https://github.com/bstef/terraink)

---

## Local preview

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` — or just open `index.html` directly in your browser.

---

## File structure

```
connectionchurchnyc/
├── index.html                          # Main site
├── assets/
│   ├── logo-icon.svg                   # SVG church logo
│   ├── Website+Logo.png                # Full logo lockup
│   ├── astoria_terracotta_20260406_145101.png   # Astoria map (terraink)
│   ├── astoria-location-map.webp       # Georeferenced hero street map
│   └── screenshot-hero.png             # Site preview
├── scripts/
│   └── build-astoria-map.py             # Optional map regeneration
└── archive/
    └── connection-church.html          # Archived alternate page
```

## Hero map

The blue pin marks the former Connection Church location provided in Google Maps
(**40.7567285, -73.9053766**), not the current Queens Church meeting location.
The neighborhood map includes Astoria Park and Ditmars Boulevard to the north.
The image and pin share a Web Mercator projection; their alignment is preserved
on desktop and mobile by scaling the whole map without cropping.

To regenerate the checked-in map, run `python3 scripts/build-astoria-map.py`
with Pillow installed. This is an optional maintenance step; the website itself
has no build or Python dependency. The script downloads only the tiles needed
for this one map. Keep the visible OpenStreetMap attribution when reusing it.

## Appearance

The site follows the device’s light or dark appearance until a visitor uses the
moon/sun button in the navigation. Their choice is saved locally for future visits.
The toggle supports keyboard activation and exposes its state to screen readers.
Storage restrictions do not prevent switching themes. Dark mode adjusts the hero,
map, navigation, cards, and light sections while retaining the warm Queens Church
section and dark announcement, social, and footer treatments.

## Connection Echo sermon archive

`/sermons/` adds a Connection-branded version of Skyline Echo’s library, calendar,
keyword search, optional contextual search, themes, and timestamp links to this
existing website. The homepage navigation and podcast links open the archive.
The original church page is preserved.

The catalog snapshot contains **438 episodes (2014–2024)** from the supplied
[podcast.app listing](https://podcast.app/connection-church-nyc-sermons-p282311).
Its original Buzzsprout feed currently has no episodes; the checked newest MP3
returns 404. Saved descriptions are metadata, never transcript passages.
Twenty-eight exact normalized-title matches link to the church’s surviving
YouTube videos. Matching titles identifies candidate equivalents; it does not
establish that video and podcast edits or timestamps are identical.

A pilot imports English automatic YouTube captions for **I Believe #11 — Repent
and Believe**: 934 segments grouped into 41 overlapping search passages.
Caption wording is unreviewed and retained as exported. Search links use the
**YouTube video timeline**, never the broken podcast MP3 timeline. Verify names,
Scripture references, wording, and timing against the recording before quoting.

Catalog search works from a checked-in JSON snapshot even without a backend.
Spoken-word search uses Cloudflare Pages Functions and a separate D1 database,
`connection-sermons`; it never queries or modifies the Skyline database.
No paid AI calls, transcription jobs, or schedules run during builds/deployment.

### Develop and deploy

```sh
npm ci
npm run db:local
npm run dev
```

Open the printed local URL followed by `/sermons/`. `npm test` checks actual D1
search, timestamped results, transcript replacement, protected publishing,
validation, and retries. `npm run check` checks Pages/Worker types.

For the existing Cloudflare Pages project `connectionchurchnyc`, set the build
command to `npm run build` and the output directory to `dist`. The checked-in
Wrangler config supplies the D1 binding. Apply migrations before deployment:

```sh
npx wrangler d1 migrations apply DB --remote
npm run build
npx wrangler pages deploy dist --project-name connectionchurchnyc
```

`dist/_routes.json` limits Functions to `/api/sermons/*`; the rest of the church
site continues to serve as static files. Preview branches use the same catalog
D1 binding; avoid testing writable publishing against that database.

### Add captions and recovered recordings

`scripts/import-podcast-catalog.py` refreshes metadata from public listing pages
and preserves existing video-source annotations. It does not fetch audio.
For another verified matching video, add its `youtube_url` to the relevant
catalog record, then import a timestamped browser-exported caption file:

```sh
python3 scripts/import-youtube-captions.py EPISODE_ID VIDEO_ID captions.txt migrations/0007_next_caption_import.sql
```

The importer verifies the video ID and matching catalog source, retains original
caption words, validates ordering, and creates an idempotent per-episode import.
Commit new numbered migrations rather than editing applied migrations.

The inherited protected endpoint `POST /api/sermons/admin/transcripts` can accept
real timestamped JSON from a future Groq/n8n runner or reviewed transcript. It is
closed until a server-side `TRANSCRIPT_PUBLISH_TOKEN` is configured. Payloads
include `episode` metadata, `segments` (`start`, `end`, `text`), and optional
`dry_run` (defaults to true). Synthetic samples can only be validated. Publication
is transactional and retry-safe. Keep credentials out of Git and frontend code.

Meaning search requires a separately configured Vectorize index, indexed
embeddings, and a server-side OpenAI key. Until configured, the app explicitly
falls back to keyword search. These resources are not enabled in this version.
