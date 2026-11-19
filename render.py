#!/usr/bin/env python3
"""Front page for Wednesday 18 November 2026 — 38 sourced stories, one image.

A single deterministic 1024x1024 PNG: masthead, photo hero, three feature
cards, a photo mini-card, a 22-story dense list, a dotted world map built
from Natural Earth coastline data, a seven-story "more" band, a day-in-numbers
bar, a UTC timeline of the day, and a footer ticker. Fixed fonts, fixed
geometry, no clock, no randomness — running the script twice yields a
byte-identical file, and the file stays under the 1 MiB cap.

Usage: python3 render.py
"""

import json
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
BYTE_CAP = 1024 * 1024

INK = (30, 30, 30)
FAINT = (80, 80, 80)
PAPER = (255, 255, 255)
BAND = (245, 245, 245)
RED = (220, 50, 50)
DARK = (25, 25, 25)
TICKER_GREY = (220, 220, 220)


def font(name, size):
    return ImageFont.truetype(str(HERE / "fonts" / name), size)


# ---------------------------------------------------------------------------
# The day's news. One dict per story: n = printed number, h = headline,
# d = one-line explainer, s = big stat, p = photo asset or None,
# k = map-marker key (see PLACES). Every story is sourced in NEWS-SOURCES.md.
# ---------------------------------------------------------------------------

STORIES = [
    {"n": 1, "h": "TRUMP LANDS IN MANILA", "d": "Trump meets Quad allies in Manila, then heads to APEC in Shenzhen", "s": "QUAD ×4", "p": "earth-night.jpg", "k": 1},
    {"n": 2, "h": "CRIMEAN BRIDGE PARTLY COLLAPSES", "d": "Ukraine's missile-and-drone strike took weeks to plan, Zelensky says", "s": "2 BRIDGES HIT", "p": None, "k": 2},
    {"n": 3, "h": "NVIDIA Q3 REVENUE +103%", "d": "Bumper results — but Huang will NOT return as CEO", "s": "HUANG OUT", "p": None, "k": 3},
    {"n": 4, "h": "TANKER HIT AGAIN IN HORMUZ", "d": "Panama-flagged LPG tanker attacked twice; 1 Indian seafarer missing", "s": "1 MISSING", "p": None, "k": 4},
    {"n": 5, "h": "CYCLONE AKVAN BEARS DOWN", "d": "Severe storm in the Bay of Bengal heads for Andhra Pradesh", "s": "145 km/h", "p": "cyclone.jpg", "k": 5},
    {"n": 6, "h": "CANADA–CHINA TRADE THAW", "d": "China cuts tariffs on pork and seafood; Canada extends steel remission", "s": "$280M", "p": None, "k": 6},
    {"n": 7, "h": "UK SANCTIONS 8 ISRAELI FIRMS", "d": "Asset freezes over West Bank settlements, plus Tzav 9, accused of blocking Gaza aid", "s": "8 FIRMS", "p": None, "k": 7},
    {"n": 8, "h": "DHONI BOWS OUT", "d": "IPL legend retires at 45, becomes CSK mentor; five titles, 5439 runs in 278 matches", "s": "5 TITLES", "p": None, "k": 8},
    {"n": 9, "h": "INDIA 2–1 PAKISTAN", "d": "SAFF final: Mandi's 88th-minute header seals it; record 10th SAFF title, third in a row", "s": "10th TITLE", "p": None, "k": 9},
    {"n": 10, "h": "AMAZON'S $7B GREEN BET", "d": "Four new wind and solar projects, 934 MW; portfolio past 2 GW — power for 3.5M homes", "s": "$7B", "p": None, "k": 10},
    {"n": 11, "h": "US LOSES MEASLES-FREE STATUS", "d": "More than 5400 cases and 10 measles-related deaths across US states", "s": "5400+ CASES", "p": None, "k": 11},
    {"n": 12, "h": "RUSSIAN PLANE CRASH KILLS 19", "d": "All 19 on board killed; defence ministry blames suspected technical malfunction", "s": "19 DEAD", "p": None, "k": 12},
    {"n": 13, "h": "US SOLDIER HELD IN UK", "d": "Met Police arrested Lt Col Brandon Carroll Tyner on 10 Nov; now in US military custody", "s": "10 NOV ARREST", "p": None, "k": 13},
    {"n": 14, "h": "ISRAEL PICKS NEW SPEAKER", "d": "Knesset elects Matan Kahana, Gadi Eisenkot ally, as coalition talks continue", "s": "NEW SPEAKER", "p": None, "k": 14},
    {"n": 15, "h": "SPAIN TO VOTE 29 NOV", "d": "Snap election after eight years of Socialist-led rule; polls put right ahead", "s": "29 NOV", "p": None, "k": 15},
    {"n": 16, "h": "TRUMP OPEN TO PUTIN ONE-ON-ONE", "d": "US president says he would meet Putin alone ahead of APEC trilateral", "s": "1-ON-1?", "p": None, "k": 16},
    {"n": 17, "h": "ASEAN SUMMIT WRAPS", "d": "Modi meets Marcos in Manila; leaders adopt AI-powered growth declaration for micro firms", "s": "23rd SUMMIT", "p": None, "k": 6},
    {"n": 18, "h": "INDIA BACK ON ITU COUNCIL", "d": "India re-elected for 2027–2030 on the International Telecommunication Union council", "s": "2027–30", "p": None, "k": 10},
    {"n": 19, "h": "BAIDU CHIEF WARNS OF AI 'BUBBLE'", "d": "Head of China's Baidu warns the AI boom looks bubbly as leaders gather in Shenzhen", "s": "AI BUBBLE?", "p": None, "k": 6},
    {"n": 20, "h": "EARTHSHOT IN MUMBAI", "d": "Earthshot Prize ceremony comes to Mumbai, hosted by William and Kate", "s": "MUMBAI", "p": None, "k": 10},
    {"n": 21, "h": "NATIONS LEAGUE", "d": "Northern Ireland reach the top tier; ten-man Portugal beat Wales in Cardiff", "s": "TOP TIER", "p": None, "k": 7},
    {"n": 22, "h": "INTEL SUED AFTER 29% PLUNGE", "d": "Shareholders sue Intel after a 29% stock plunge", "s": "−29%", "p": None, "k": 13},
    {"n": 23, "h": "DRUG LORD FELIX GALLARDO DIES, 80", "d": "Miguel Angel Felix Gallardo, once Mexico's most powerful drug lord, dies aged 80", "s": "AGE 80", "p": None, "k": 14},
    {"n": 24, "h": "THOMAS MARKLE CHARGED", "d": "Charged over child sex abuse material in the Philippines; held in US on separate charge", "s": "CHARGED", "p": None, "k": 1},
    {"n": 25, "h": "US–IRAN GULF STRIKES", "d": "US jets struck a Revolutionary Guard missile site on Qeshm Island; Iran fired drones at Bahrain and Kuwait", "s": "QESHM STRUCK", "p": None, "k": 4},
    {"n": 26, "h": "BANGLADESH UNREST GROWS", "d": "Paramilitary deployed nationwide; bomb blasts and arson blamed on Awami League supporters", "s": "71 ARRESTED", "p": None, "k": 9},
    {"n": 27, "h": "ETHIOPIA–ERITREA BUILD-UP", "d": "Both armies massed along the shared border; artillery clashes reported near Badme", "s": "BADME CLASHES", "p": None, "k": 15},
    {"n": 28, "h": "ERASMUS BANNED SIX TESTS", "d": "World Rugby suspends Springbok coach Rassie Erasmus for six Tests over match-fixing comments", "s": "6 TESTS", "p": None, "k": 16},
    {"n": 29, "h": "GULF MARKETS SLIDE", "d": "Gulf bourses down in early trade; Brent crude $91.69, down 1.6%, as shipping through Hormuz disrupted", "s": "BRENT $91.69", "p": None, "k": 4},
    {"n": 30, "h": "VOYAGER 1: ONE LIGHT-DAY", "d": "Voyager 1 reaches one light-day from Earth; NASA marks it with a 'Shine Bright' public tribute", "s": "1 LIGHT-DAY", "p": None, "k": 11},
    {"n": 31, "h": "PATTINSON IS THE NEW BOND", "d": "Robert Pattinson named the new James Bond, replacing Daniel Craig", "s": "7TH BOND", "p": None, "k": 7},
    {"n": 32, "h": "FORD'S FIRST CATL-TECH CELLS", "d": "First LFP cells ship in Michigan for the Fathom EV truck", "s": "40/MIN", "p": None, "k": 11},
    {"n": 33, "h": "ANTHROPIC IPO PRICED", "d": "Shares priced today; trading starts tomorrow as ANT", "s": "TICKER ANT", "p": None, "k": 11},
    {"n": 34, "h": "DOW −560; GOLD, BITCOIN SLIDE", "d": "Dow −560, S&P falls 5th day; gold $3,730, BTC $62,300", "s": "DOW −560", "p": None, "k": 11},
    {"n": 35, "h": "FED'S WALLER: 'SHOCK' HIKE", "d": "Waller: Fed may need a half-point hike; Dec odds 96%", "s": "96% ODDS", "p": None, "k": 11},
    {"n": 36, "h": "GTA VI SCORES 99/100", "d": "Reviews land at 99/100; NZ plays first at 11:00 UTC", "s": "99/100", "p": None, "k": 11},
    {"n": 37, "h": "BLAVATNIK'S $5B SPACEX STAKE", "d": "Billionaire builds a $5B stake in SpaceX, Bloomberg says", "s": "$5B STAKE", "p": None, "k": 11},
    {"n": 38, "h": "VULCAN FAILURE: FUEL STARVED", "d": "ULA: fuel shortage, not engines, doomed 40 Leo sats", "s": "40 LOST", "p": None, "k": 11},
]

# Map places keyed by the marker number printed on the map. Key 8 is
# deliberately absent (no story maps there); 15 places are drawn.
PLACES = {
    1: (121.0, 14.6), 2: (34.0, 45.3), 3: (30.5, 50.4), 4: (56.3, 26.5),
    5: (85.7, 12.2), 6: (114.1, 22.5), 7: (-0.1, 51.5), 9: (90.4, 23.8),
    10: (77.2, 28.6), 11: (-77.0, 38.9), 12: (86.1, 55.4), 13: (35.2, 31.8),
    14: (-3.7, 40.4), 15: (37.9, 14.7), 16: (28.2, -25.7),
}

# Display-only nudges for the two tightest marker pairs (Kyiv/Crimea and
# Shenzhen/Manila sit ~12-19 px apart on this map; the nudge separates the
# circles so their numbers stay readable). Geography underneath is unchanged.
NUDGE = {2: (0, 8), 3: (0, -8), 1: (0, 4), 6: (0, -4)}

# The day, hour by hour (UTC). Times are approximate except the two GTA VI
# unlocks and the Reuters timestamp; the strip says so on the image.
DAY_EVENTS = [
    (6.0, "06:00 GULF SLIDE", "down"),
    (11.0, "11:00 GTA VI NZ", "down"),
    (16.0, "16:00 GTA VI SG", "up"),
    (19.0, "19:00 FOMC MINUTES", "down"),
    (20.9, "20:54 SPACEX $5B", "up"),
]

# Vertical plan for the page (pixels from the top).
Y_MASTHEAD = (0, 50)
Y_HERO = (50, 190)
Y_FEATURES = (190, 320)
Y_MINI = (320, 370)
Y_LOWER = 370
X_SPLIT = 500          # dense list left of this, map right of it
Y_MAP_END = 740
Y_MORE = (748, 896)
Y_COUNTS = (904, 948)
Y_CLOCK = (956, 996)
Y_TICKER = (996, 1024)


def text_w(d, s, f):
    return d.textlength(s, font=f)


def text_h(d, s, f):
    box = d.textbbox((0, 0), s, font=f)
    return box[3] - box[1]


def wrap(d, s, f, width, limit=None):
    """Greedy wrap; every returned line fits inside width."""
    out, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if text_w(d, trial, f) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out[:limit] if limit is not None else out


def rect(d, x, y, w, h, fill):
    d.rectangle([x, y, x + w, y + h], fill=fill)


def put(d, x, y, s, f, fill=INK):
    d.text((x, y), s, font=f, fill=fill)


def put_centre(d, cx, y, s, f, fill=INK):
    d.text((cx, y), s, font=f, fill=fill, anchor="ma")


def fit_size(d, s, sizes, width, name="Inter.ttf"):
    """Largest size from sizes whose rendering of s fits width."""
    for size in sizes:
        f = font(name, size)
        if text_w(d, s, f) <= width:
            return f
    return font(name, sizes[-1])


def project(lon, lat, x0, y0, w, h):
    """Equirectangular projection of lon/lat into the map rectangle."""
    return x0 + (lon + 180.0) / 360.0 * w, y0 + (90.0 - lat) / 180.0 * h


# ---------------------------------------------------------------------------
# Sections. Each draws one band of the page and returns nothing; the caller
# owns the vertical plan above, so no section may paint outside its band.
# ---------------------------------------------------------------------------

def draw_masthead(d):
    y0, y1 = Y_MASTHEAD
    rect(d, 0, y0, W, y1 - y0, BAND)
    line = "WEDNESDAY, 18 NOVEMBER 2026 • 38 STORIES • 6 CONTINENTS"
    f = font("PlayfairDisplay.ttf", 34)
    assert text_w(d, line, f) <= W - 20, "masthead too wide"
    put_centre(d, W // 2, y0 + 8, line, f)


def draw_hero(im, d):
    y0, y1 = Y_HERO
    photo = HERE / "assets" / "earth-night.jpg"
    if photo.exists():
        shot = Image.open(photo).resize((W, y1 - y0), Image.LANCZOS).convert("RGB")
        im.paste(shot, (0, y0))
    else:
        rect(d, 0, y0, W, y1 - y0, (20, 20, 50))
    top = STORIES[0]
    rect(d, 0, y1 - 40, W, 40, (0, 0, 0))
    put(d, 20, y1 - 39, top["h"], font("Archivo.ttf", 24), (255, 255, 255))
    put(d, 20, y1 - 15, top["d"], font("Inter.ttf", 12), (200, 230, 255))


def draw_features(d):
    y0, y1 = Y_FEATURES
    card_w, gap = 310, 20
    total = 3 * card_w + 2 * gap
    x = (W - total) // 2
    for story in STORIES[1:4]:
        rect(d, x, y0, card_w, y1 - y0, PAPER)
        inner = card_w - 16
        cy = y0 + 6
        head = f"{story['n']}. {story['h']}"
        hf = fit_size(d, head, (18, 16, 14, 12), inner)
        for ln in wrap(d, head, hf, inner, limit=2):
            put(d, x + 8, cy, ln, hf)
            cy += text_h(d, ln, hf) + 2
        ef = font("Inter.ttf", 12)
        for ln in wrap(d, story["d"], ef, inner, limit=2):
            put(d, x + 8, cy, ln, ef, FAINT)
            cy += text_h(d, ln, ef) + 2
        put(d, x + 8, cy + 2, story["s"], font("Inter.ttf", 13), RED)
        x += card_w + gap


def draw_mini(im, d):
    y0, y1 = Y_MINI
    photo = HERE / "assets" / "cyclone.jpg"
    if photo.exists():
        shot = Image.open(photo).resize((80, 40), Image.LANCZOS).convert("RGB")
        im.paste(shot, (20, y0 + 5))
    else:
        rect(d, 20, y0 + 5, 80, 40, (180, 180, 220))
    story = STORIES[4]
    put(d, 110, y0 + 5, f"5. {story['h']}", font("Archivo.ttf", 20))
    put(d, 110, y0 + 27, story["d"], font("Inter.ttf", 12), FAINT)
    put(d, 110, y0 + 41, story["s"], font("Inter.ttf", 13), RED)


def draw_dense_list(d):
    """Stories 6-27 in the left column: headline, then one explainer line.
    Rows are 24 px so all 22 fit above the count bar (which starts at 904)."""
    y = Y_LOWER + 2
    head_f = font("Inter.ttf", 12)
    expl_f = font("Inter.ttf", 9)
    for story in STORIES[5:27]:
        head = f"{story['n']}. {story['h']}"
        if text_w(d, head, head_f) <= X_SPLIT - 24:
            put(d, 8, y, head, head_f)
            y += 12
        else:
            for ln in wrap(d, head, head_f, X_SPLIT - 24, limit=2):
                put(d, 8, y, ln, head_f)
                y += 12
        put(d, 8, y + 3, story["d"], expl_f, FAINT)
        y += 12
    return y


def draw_map(d):
    """Dotted continents from Natural Earth, then numbered place markers."""
    x0, y0, x1, y1 = X_SPLIT, Y_LOWER, W, Y_MAP_END
    geo = HERE / "ne_110m_land.geojson"
    land = json.loads(geo.read_text())
    for feat in land["features"]:
        rings = feat["geometry"]["coordinates"]
        for ring in rings:
            pts = [(project(lon, lat, x0, y0, x1 - x0, y1 - y0))
                   for lon, lat in ring]
            for j in range(0, len(pts), 4):
                px, py = pts[j]
                d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=INK)
    num_f = font("Inter.ttf", 10)
    for key in sorted(PLACES):
        lon, lat = PLACES[key]
        px, py = project(lon, lat, x0, y0, x1 - x0, y1 - y0)
        dx, dy = NUDGE.get(key, (0, 0))
        px, py = px + dx, py + dy
        r = 9
        d.ellipse([px - r, py - r, px + r, py + r], fill=BAND,
                  outline=INK, width=2)
        d.text((px, py), str(key), font=num_f, fill=INK, anchor="mm")


def draw_more(d):
    """Stories 32-38: two columns under the map, headline + explainer each."""
    y0, y1 = Y_MORE
    head_f = font("Archivo.ttf", 12)
    put(d, X_SPLIT + 8, y0 + 2, "MORE FROM THE DAY — EVERY STORY SOURCED",
        head_f)
    cols = [(X_SPLIT + 8, STORIES[31:35]), (X_SPLIT + 256, STORIES[35:38])]
    hf = font("Inter.ttf", 11)
    ef = font("Inter.ttf", 9)
    for cx, group in cols:
        ry = y0 + 24
        for story in group:
            head = f"{story['n']}. {story['h']}"
            assert text_w(d, head, hf) <= 248, head
            assert text_w(d, story["d"], ef) <= 248, story["d"]
            put(d, cx, ry, head, hf)
            put(d, cx, ry + 13, story["d"], ef, FAINT)
            ry += 27
    return y1


def draw_counts(d):
    y0, y1 = Y_COUNTS
    rect(d, 0, y0, W, y1 - y0, DARK)
    line = "38 STORIES  •  6 CONTINENTS  •  15 PLACES MAPPED  •  2 PHOTOS  •  ALL SOURCED"
    f = font("Inter.ttf", 13)
    assert text_w(d, line, f) <= W - 20, "count bar too wide"
    put_centre(d, W // 2, y0 + 13, line, f, (255, 255, 255))


def draw_clock(d):
    """UTC timeline of the day across the right column, times approximate."""
    y0, y1 = Y_CLOCK
    x0, x1 = X_SPLIT + 16, W - 16
    axis_y = y0 + 22
    put(d, x0, y0 + 2, "THE DAY IN UTC — TIMES APPROXIMATE",
        font("Archivo.ttf", 10), FAINT)
    d.line([x0, axis_y, x1, axis_y], fill=INK, width=2)
    small = font("Inter.ttf", 8)
    d.text((x0, axis_y + 4), "00", font=small, fill=FAINT)
    d.text((x1 - 12, axis_y + 4), "24", font=small, fill=FAINT)
    for hour, label, side in DAY_EVENTS:
        ex = x0 + hour / 24.0 * (x1 - x0)
        d.ellipse([ex - 4, axis_y - 4, ex + 4, axis_y + 4], fill=RED)
        lw = text_w(d, label, small)
        lx = max(x0, min(ex - lw / 2, x1 - lw))
        if side == "up":
            d.text((lx, axis_y - 16), label, font=small, fill=INK)
        else:
            d.text((lx, axis_y + 6), label, font=small, fill=INK)


def draw_ticker(d):
    y0, y1 = Y_TICKER
    rect(d, 0, y0, W, y1 - y0, TICKER_GREY)
    items = ["28 ERASMUS BANNED", "29 GULF MARKETS SLIDE",
             "30 VOYAGER 1: ONE LIGHT-DAY", "31 PATTINSON IS THE NEW BOND"]
    tf = font("Inter.ttf", 11)
    slot = W / 4
    for i, item in enumerate(items):
        assert text_w(d, item, tf) <= slot - 20, item
        put(d, i * slot + 10, y0 + 7, item, tf)


# ---------------------------------------------------------------------------
# Assembly, PNG validation, entry point
# ---------------------------------------------------------------------------

def build():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    draw_masthead(d)
    draw_hero(im, d)
    draw_features(d)
    draw_mini(im, d)
    draw_dense_list(d)
    draw_map(d)
    draw_more(d)
    draw_counts(d)
    draw_clock(d)
    draw_ticker(d)
    out = HERE / "entry.png"
    im.save(str(out), "PNG")
    variant = HERE / "variants" / "v1-entry.png"
    variant.parent.mkdir(parents=True, exist_ok=True)
    im.save(str(variant), "PNG")
    print(f"rendered {out} ({W}x{H})")
    return im


def check_png(path):
    """PNG magic, IHDR size, trailing IEND, byte cap — all must hold."""
    raw = Path(path).read_bytes()
    if len(raw) > BYTE_CAP:
        raise SystemExit(f"PNG is {len(raw)} bytes, over the 1 MiB cap")
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("bad PNG signature")
    if len(raw) < 33 or raw[12:16] != b"IHDR":
        raise SystemExit("missing IHDR chunk")
    w, h = struct.unpack(">II", raw[16:24])
    if (w, h) != (W, H):
        raise SystemExit(f"PNG is {w}x{h}, expected {W}x{H}")
    if raw[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        raise SystemExit("missing IEND chunk")
    return raw


if __name__ == "__main__":
    build()
    check_png(HERE / "entry.png")
    print("entry.png valid: 1024x1024, under 1 MiB, IEND present")
