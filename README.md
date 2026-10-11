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
