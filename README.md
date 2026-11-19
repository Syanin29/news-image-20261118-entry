# Wednesday 18 November 2026: 38 stories, 6 continents, one front page and a map

[![make.fun](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun)

Entry for the make.fun bounty **news-image-20261118**: *sum up 18 November's
world news in one image.* One PNG, 1024×1024, 359,978 bytes, **38 verified
stories** — every one sourced in `NEWS-SOURCES.md`.

[![entry](entry.png)](entry.png)

## What the image holds

A front page for Wednesday 18 November 2026, built from **38 verified
stories** from that day — each one sourced and carrying a number:

- **Top story:** Trump lands in Manila for the first Quad meeting in two years
- **Features:** Crimean bridge partly collapses · Nvidia Q3 revenue (stat:
  HUANG OUT) · tanker hit again in Hormuz
- **Photo mini-card:** Cyclone Akvan bears down on the Bay of Bengal
- **Dense list:** stories 6–27 (22 stories, headline + one-line explainer each)
- **Map:** a dotted world map drawn from real Natural Earth coastline data,
  with 15 numbered place markers for where the stories happened
- **More from the day:** stories 32–38 — Ford's first CATL-tech battery
  cells, the Anthropic IPO pricing, the Dow/gold/Bitcoin slide, the Fed's
  "shock" hike warning, GTA VI at 99/100, Blavatnik's $5B SpaceX stake,
  and the Vulcan fuel-starvation finding
- **Day in numbers:** 38 stories · 6 continents · 15 places mapped ·
  2 photos · all sourced
- **The day in UTC:** a timeline strip (Gulf slide ~06:00, GTA VI live in
  New Zealand 11:00 and Singapore 16:00, FOMC minutes 19:00, SpaceX stake
  20:54; times approximate)
- **Ticker/footer:** stories 28–31

## How it was built

`render.py` (PIL) renders `entry.png` from the story table inside the
script, `assets/*.jpg`, and `ne_110m_land.geojson`. The render is
deterministic (fixed fonts, fixed geometry, no timestamps, no randomness):
running it twice produces a byte-identical file — verified, sha256
`695fe044346c4c6885bd5827fbf857214c71f374536ac703954e1bd5a1e07793`.

`main.py` is stdlib-only (the sandbox installs nothing): it validates the
PNG (signature, 1024×1024 IHDR, IEND tail, 1 MiB cap) and copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png`.

```sh
python3 render.py        # reproduce entry.png (needs Pillow + fonts/)
python3 main.py          # write output/entry.png
```

## Sources

Every story was cross-checked against Reuters / BBC / Investopedia /
official sources on 18–19 November 2026. Four unverified claims found
during the first research pass were dropped (see `NEWS-SOURCES.md`).

## License

MIT — see `LICENSE`. Fonts: Playfair Display, Archivo, Inter (OFL).
Map data: Natural Earth (public domain). Photos: Earth at night (hero)
and Cyclone Akvan from space — generic illustrative images, not
depictions of specific events.
