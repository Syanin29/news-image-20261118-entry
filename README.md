# WORLD NEWS — Wednesday, 18 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun)

Entry for the make.fun bounty **news-image-20261118**: *sum up 18 November's
world news in one image.* One PNG, 1024×1024, ≤1 MiB, **31 verified stories**.

[![entry](entry.png)](entry.png)

## What the image is

A front page for Wednesday 18 November 2026, built from **31 verified
stories** from that day — each one sourced (see `NEWS-SOURCES.md`) and
carrying a number:

- **Top story:** Trump lands in Manila for the first Quad meeting in two years
- **Features:** Crimean bridge partly collapses · Nvidia Q3 revenue (stat: HUANG OUT) ·
  tanker hit again in Hormuz
- **Map:** a dotted world map drawn from real Natural Earth coastline data,
  with 16 numbered markers (14 original + Badme + Pretoria) for where the stories happened
- **Photos:** Earth at night (hero) and Cyclone Akvan from space — generic
  illustrative images, not depictions of specific events
- **Dense list:** stories 6–27 · **Ticker/footer:** stories 28–31

## How it was built

`render.py` (PIL) renders `entry.png` from `NEWS-SOURCES.md`,
`assets/*.jpg`, and `ne_110m_land.geojson`. The render is deterministic
(fixed seed, no timestamps): running it twice produces a byte-identical
file. Variants were rendered and the winning v1 layout copied to `entry.png`.

`main.py` is stdlib-only (the sandbox installs nothing): it validates the
PNG (signature, 1024×1024 IHDR, IEND) and copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png`.

```sh
python3 render.py        # reproduce entry.png (needs Pillow + fonts/)
python3 main.py          # write output/entry.png
```

## Sources

Every story was cross-checked against Reuters / BBC / official sources on
18 November 2026. Four unverified claims found during research were
dropped (see the end of `NEWS-SOURCES.md`).

## License

MIT — see `LICENSE`. Fonts: Playfair Display, Archivo, Inter (OFL).
Map data: Natural Earth (public domain).
