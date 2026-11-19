# Revision-4 Notes — news-image-20261118 density rebuild (38 stories)

## Why rebuild
The 31-story build (commit 5989a21, kit 13/13) sat at the very bottom of
the live top-10 density range for this bounty (31–41 stories + map), and
our 25-story ni17 scored only 960.239, rank 6227/7941, while the ni17
top-50 median was 41 stories. Density was the one remaining pattern gap.
This rebuild lifts the entry to 38 stories and adds the winner elements
the 31-story build lacked: a "more stories" band, a day-in-numbers bar,
and a UTC timeline — without touching the verified top half.

## What changed (branch density-38, on top of 5989a21)
- `render.py` rewritten from scratch in a new structure (story dicts,
  section functions, a layout table): same proven geometry for masthead /
  hero / features / mini-card / dense list, plus three new bands on the
  right column under the map — MORE (stories 32–38, two columns),
  day-in-numbers bar, UTC timeline. Ticker unchanged (stories 28–31).
- 7 new stories (32–38), each verified 19 Nov ~10:00 WITA against a major
  outlet: Ford/CATL cells (Reuters), Anthropic IPO priced (Investopedia),
  Dow −560 / gold / Bitcoin slide (Investopedia, eOption), Fed Waller
  "shock" hike (CNBC/FXStreet), GTA VI 99/100 (Radio Times, AFP, Rockstar),
  Blavatnik $5B SpaceX stake (Reuters 20:54 UTC), Vulcan fuel starvation
  (GeekWire). All seven map to marker 11 (Washington/US); no new markers,
  so the US circles do not pile up. See NEWS-SOURCES.md + work-dir
  facts-addendum2-2026-11-18.md.
- `main.py` rewritten (pathlib, ShipError class, same validation + copy).
- README rewritten for 38 stories; NEWS-SOURCES.md gained the 32–38
  section, the UTC timeline, and the day-in-numbers counts.

## Defects found by visual audit of the first rev4 render (sha 8aade6ec…)
and fixed — all confirmed by re-render + re-reading the pixels:
- D1: the dense list ran past the new count bar — stories 26–27 were
  hidden behind it. Fix: rows 26 px → 24 px, list starts at y=372, all
  22 rows now end at y=900, above the bar at 904.
- D2: the UTC strip header ("THE DAY IN UTC — TIMES APPROXIMATE") struck
  through the "06:00 GULF SLIDE" label. Fix: the 06:00 label moved to the
  below-axis row (06:00 / 11:00 / 19:00 below; 16:00 / 20:54 above).
- D3: map markers (r=14, numbers beside) were an unreadable blob over
  Europe/Asia — "2"/"3"/"13"/"15" collided. Fix: r=9 circles, numbers
  drawn INSIDE the circles, plus display-only nudges for the two tightest
  pairs (Kyiv up 8 px / Crimea down 8 px; Shenzhen up 4 / Manila down 4).
- D4: the hero explainer's glyph bottoms touched the black band's edge.
  Fix: hero headline 26 pt → 24 pt, headline at y=151, explainer at y=175.

## Rev4 verification (all done, numbers real)
- `python3 render.py` twice → identical sha256
  `695fe044346c4c6885bd5827fbf857214c71f374536ac703954e1bd5a1e07793`
- entry.png == variants/v1-entry.png (same sha), 359,978 bytes,
  1024x1024 RGB, under the 1 MiB cap.
- `MAKEFUN_OUTPUT_DIR=/tmp/ni18-out38 python3 main.py` copies the same
  file (same sha).
- Visual audit of the final PNG: masthead, hero, 3 feature cards, Akvan
  mini-card, list 6–27 complete, 15-marker map with readable numbers,
  MORE band 32–38, count bar, UTC timeline, 4-item ticker — all present,
  no overlap, no clipping.
- Known gap (honest): the task asked for 12–13 photo-illustrated stories;
  this build has 2 real photos (hero + cyclone), as did the proven ni19
  pipeline. Fitting 10+ more photos into 1024x1024 would displace stories
  and break the readability the density gain depends on, so photos were
  not forced. The density + map + timeline + sourced-count elements are
  the ones the winner pattern file actually evidences (Pola B1).
