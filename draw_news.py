#!/usr/bin/env python3
"""Render the 26 November 2026 world-news front page as a 1024x1024 PNG.

Everything here is drawn from scratch with Pillow: masthead, lead cards,
a UTC timeline, a schematic world map, a markets panel and six region
columns. Story data is embedded below and comes only from the verified
list for this midday edition (news to about 09:00 WIB, 26 Nov 2026).
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (251, 247, 239)
INK = (20, 20, 22)
NAVY = (22, 40, 63)
NAVY_SOFT = (38, 62, 92)
RED = (178, 34, 34)
GOLD = (184, 134, 11)
GREY = (110, 108, 100)
LIGHT_LINE = (205, 198, 184)
PANEL = (255, 255, 255)
SEA = (214, 228, 238)
LAND = (196, 205, 170)
GREEN_UP = (27, 120, 62)
RED_DOWN = (178, 34, 34)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: load_font("DejaVuSans.ttf", s)
SANS_B = lambda s: load_font("DejaVuSans-Bold.ttf", s)

F_TITLE = SERIF_B(46)
F_DATE = SANS_B(13)
F_KICK = SANS_B(11)
F_LEAD_H = SERIF_B(21)
F_LEAD_H2 = SERIF_B(17)
F_BODY = SANS(12)
F_SMALL = SANS(10)
F_SMALL_B = SANS_B(10)
F_TINY = SANS(9)
F_TINY_B = SANS_B(9)
F_TAG = SANS_B(8)
F_MAP = SANS_B(9)


def wrap_words(draw, text, font, max_w):
    """Split text into lines that fit max_w; returns a list of strings."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_w, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    lh = leading if leading is not None else int(font.size * 1.25)
    for line in wrap_words(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def measure_block(draw, text, font, max_w, leading=None):
    lh = leading if leading is not None else int(font.size * 1.25)
    return len(wrap_words(draw, text, font, max_w)) * lh


def rule(draw, x0, y, x1, colour=LIGHT_LINE, width=1):
    draw.line([(x0, y), (x1, y)], fill=colour, width=width)


# ---------------------------------------------------------------- stories
LEADS = [
    {
        "kicker": "TRADE WAR",
        "colour": RED,
        "head": "Trump hits 14 partners with new tariffs",
        "body": ("China faces 20% on top of roughly 25% already in place; the EU, "
                 "Japan and South Korea are capped at 15%; Vietnam up to 35%. "
                 "Hearings open from 25 January."),
        "src": "REUTERS  ·  25 NOV",
        "bars": [("China", 20), ("EU · Japan · S. Korea", 15), ("Vietnam", 35)],
    },
    {
        "kicker": "AI ROUT",
        "colour": NAVY_SOFT,
        "head": "Nvidia slides 3.9% to $149.30",
        "body": ("The Nasdaq plunged 4.6% intraday before clawing back to -0.6%; "
                 "the Dow edged up 0.3% as the AI sell-off deepened."),
        "src": "REUTERS  ·  25 NOV",
    },
    {
        "kicker": "OIL SHOCK",
        "colour": GOLD,
        "head": "Houthis claim Ras Tanura hit",
        "body": ("Brent jumps 3.5% to $94.61; WTI $83.68. Saudis say four "
                 "drones downed; claim unconfirmed."),
        "src": "REUTERS  ·  25 NOV",
    },
]

TIMELINE = [
    ("25 NOV  13:30 UTC", "Tariffs proposed on 14 partners"),
    ("25 NOV  16:00 UTC", "Nasdaq -4.6% intraday, closes -0.6%"),
    ("25 NOV  EVENING", "Houthis claim Ras Tanura; Brent +3.5%"),
    ("25 NOV  EVENING", "Pope Leo: COP31 \u201ctroubling\u201d"),
    ("26 NOV  00:00 UTC", "Kim orders nuclear deployment"),
]

NUMBERS = [
    ("$94.61", "BRENT  +3.5%"),
    ("$149.30", "NVIDIA  -3.9%"),
    ("490,334", "RUSSIAN WAR DEAD"),
    ("31", "KILLED, CAIRO FIRE"),
    ("20%", "TOP CHINA TARIFF"),
    ("-1,927", "TAIWAN POINTS LOST"),
]

REGIONS = [
    ("AMERICAS", [
        ("Second judge blocks Trump's birthright citizenship order", "REUTERS · 25 NOV"),
        ("Fed Beige Book: modest growth, wage gains, price pressure persists", "FED · 25 NOV"),
        ("US markets shut today for Thanksgiving; early close Fri 1pm ET", "NASDAQ · 26 NOV"),
        ("Melania Trump reunites 9 Ukrainian and Russian children with families", "AP · 25 NOV"),
        ("Ecuador minister: US talks focus on reviewing operations", "REUTERS · 25 NOV"),
        ("US proposes 10% tariff on Brazil's Embraer jets, higher sugar duties", "REUTERS · 25 NOV"),
    ]),
    ("EUROPE", [
        ("Ukraine hits Savasleyka air base; 3 MiG-31 and 2 Su-34 out", "REUTERS · 25 NOV"),
        ("Leaked data puts Russian war dead near 490,000", "BBC · 25 NOV"),
        ("Russia oil refining at 20-year low after 18 refineries hit", "REUTERS · 25 NOV"),
        ("Murmansk governor held in pre-trial detention on graft charges", "REUTERS · 25 NOV"),
        ("Norway top court voids climate-disputed oil licences", "AP · 26 NOV"),
        ("EU hunts new ECB chief as Lagarde resigns", "AP · 25 NOV"),
        ("Pope Leo calls COP31 failure \u201ctroubling\u201d", "REUTERS · 25 NOV"),
    ]),
    ("MIDDLE EAST", [
        ("Israeli strike kills senior Hamas security official and family in Gaza City", "BBC · 25 NOV"),
        ("Cairo fuel tanker fire kills at least 31, injures 21", "GUARDIAN · 25 NOV"),
        ("Iran says ships hit mines in Hormuz, warns vessels to coordinate", "REUTERS · 25 NOV"),
        ("Lebanon to open second international airport next month", "REUTERS · 25 NOV"),
        ("Israeli judges urge dropping most serious charges against Netanyahu", "AP · 26 NOV"),
    ]),
    ("AFRICA", [
        ("RSF drone strikes kill 19 civilians in Sudan's Blue Nile (Damazin)", "REUTERS · 26 NOV"),
        ("Kenya discharges last Ebola patient; DRC toll passes 5,300", "AP · 26 NOV"),
        ("S. African court backs Ramaphosa in cash-theft probe", "REUTERS · 26 NOV"),
        ("ECOWAS approves regional force plan by end-2027", "AP · 25 NOV"),
        ("Ghana unveils heritage banknotes honouring Nkrumah, Annan", "AP · 26 NOV"),
    ]),
    ("ASIA-PACIFIC", [
        ("Kim Jong Un orders wider tactical nuclear deployment", "KCNA · 26 NOV"),
        ("N. Korea orders Swiss office in Pyongyang shut", "AP · 26 NOV"),
        ("Taiwan shares plunge 1,927 points; NT$ past 33", "CNA · 25 NOV"),
        ("How China got Nvidia AI chips despite US rules", "REUTERS · 26 NOV"),
        ("Pakistan's first astronaut reaches Tiangong aboard Shenzhou-24", "REUTERS · 25 NOV"),
        ("India marks Constitution Day; 6,000 new IIT seats in AI, robotics, space", "PTI · 26 NOV"),
        ("Bangladesh raises garment minimum wage 36%", "AP · 26 NOV"),
    ]),
    ("TECH · SCIENCE · SPORT", [
        ("Hera images show stadium-sized asteroid crater", "ESA · 26 NOV"),
        ("Gukesh faces Sindarov in World Chess Championship, Geneva", "PTI · 26 NOV"),
        ("IPL 2027 auction draws 1,220 players", "PTI · 26 NOV"),
        ("Sooryavanshi smashes 204 off 53 balls vs UAE", "PTI · 26 NOV"),
        ("Flipkart CEO Kalyan Krishnamurthy to step down in December", "REUTERS · 26 NOV"),
    ]),
]

MARKETS = [
    ("Brent crude", "+3.5%", 3.5),
    ("Nvidia", "-3.9%", -3.9),
    ("Nasdaq", "-0.6%", -0.6),
    ("Dow", "+0.3%", 0.3),
]

# Rough continent outlines as (lon, lat) rings, drawn on a plain grid.
CONTINENTS = [
    [(-168, 66), (-150, 71), (-128, 71), (-110, 73), (-95, 80), (-82, 73),
     (-65, 60), (-55, 47), (-65, 44), (-75, 35), (-81, 26), (-90, 21),
     (-97, 16), (-105, 20), (-114, 29), (-125, 40), (-125, 49), (-140, 60),
     (-158, 58), (-168, 66)],
    [(-79, 9), (-62, 10), (-52, 5), (-35, -6), (-40, -20), (-48, -28),
     (-58, -35), (-65, -41), (-70, -54), (-73, -44), (-73, -30), (-77, -12),
     (-81, -3), (-79, 9)],
    [(-10, 36), (-9, 43), (-2, 48), (3, 51), (8, 57), (10, 59), (18, 56),
     (21, 55), (28, 60), (30, 65), (32, 70), (25, 71), (15, 70), (5, 62),
     (-5, 58), (-10, 50), (-10, 36)],
    [(-17, 15), (-16, 27), (-10, 31), (-5, 35), (10, 37), (20, 32),
     (32, 31), (34, 28), (43, 12), (51, 11), (48, 2), (40, -5), (40, -15),
     (35, -25), (32, -29), (20, -35), (16, -28), (12, -18), (9, -1),
     (9, 4), (-8, 5), (-13, 8), (-17, 15)],
    [(40, 68), (55, 68), (70, 72), (90, 75), (110, 74), (130, 72),
     (150, 70), (170, 66), (178, 65), (162, 60), (156, 51), (142, 45),
     (140, 39), (127, 35), (122, 31), (120, 23), (110, 20), (105, 9),
     (100, 7), (97, 10), (92, 16), (88, 22), (80, 8), (77, 8), (73, 16),
     (66, 25), (58, 25), (52, 26), (48, 29), (43, 12), (40, 68)],
    [(113, -22), (122, -14), (130, -12), (136, -12), (142, -11), (146, -19),
     (150, -22), (153, -27), (150, -37), (140, -38), (132, -32), (124, -33),
     (115, -35), (113, -22)],
]

HOTSPOTS = [
    (-77, 39, "US TARIFFS", -4, -16),
    (47, 25, "RAS TANURA", -8, -16),
    (30, 50, "KYIV STRIKES", -6, -16),
    (34, 31, "GAZA", -2, 14),
    (34, 11, "SUDAN", -2, 14),
    (126, 39, "PYONGYANG", -62, -16),
    (121, 25, "TAIPEI", -10, 14),
]


def lonlat_to_xy(lon, lat, x0, y0, w, h):
    px = x0 + (lon + 170.0) / 360.0 * w
    py = y0 + (75.0 - lat) / 130.0 * h
    return (px, py)


def paint_masthead(d):
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.rectangle([0, 92, W, 95], fill=GOLD)
    d.text((24, 12), "THE WORLD TODAY", font=F_TITLE, fill=(250, 247, 239))
    d.text((24, 66), "THURSDAY  26  NOVEMBER  2026", font=F_DATE, fill=(232, 196, 90))
    right = "WORLD NEWS IN ONE PAGE  ·  MIDDAY EDITION"
    d.text((W - 24 - d.textlength(right, font=F_SMALL_B), 70),
           right, font=F_SMALL_B, fill=(200, 210, 224))
    d.text((W - 24 - d.textlength("News to ~09:00 WIB", font=F_TINY), 16),
           "News to ~09:00 WIB", font=F_TINY, fill=(200, 210, 224))


def paint_numbers(d):
    x0, y0, gap = 24, 100, 8
    cw = (W - 48 - gap * 5) // 6
    for i, (val, lab) in enumerate(NUMBERS):
        x = x0 + i * (cw + gap)
        d.rectangle([x, y0, x + cw, y0 + 40], outline=LIGHT_LINE, width=1, fill=PANEL)
        d.rectangle([x, y0, x + cw, y0 + 3], fill=NAVY)
        d.text((x + 8, y0 + 7), val, font=SANS_B(15), fill=INK)
        d.text((x + 8, y0 + 25), lab, font=F_TAG, fill=GREY)


def paint_lead_card(d, x, y, w, h, lead, big):
    d.rectangle([x, y, x + w, y + h], outline=LIGHT_LINE, width=1, fill=PANEL)
    d.rectangle([x, y, x + w, y + 4], fill=lead["colour"])
    cx, cy = x + 12, y + 12
    d.text((cx, cy), lead["kicker"], font=F_KICK, fill=lead["colour"])
    sw = d.textlength(lead["src"], font=F_TAG)
    d.text((x + w - 12 - sw, cy + 2), lead["src"], font=F_TAG, fill=GREY)
    hy = cy + 18
    hfont = F_LEAD_H if big else F_LEAD_H2
    hy = draw_wrapped(d, cx, hy, lead["head"], hfont, w - 24, leading=24 if big else 21)
    by = hy + 4
    if lead.get("bars"):
        by = draw_wrapped(d, cx, by, lead["body"], F_BODY, w - 24, leading=15)
        # Horizontal tariff bars: name, bar, percent — one row per partner.
        ry = by + 10
        d.text((cx, ry), "NEW TARIFF RATES — PROPOSED", font=F_TAG, fill=GREY)
        ry += 16
        for name, pct in lead["bars"]:
            d.text((cx, ry), name, font=F_TINY_B, fill=INK)
            bar_x = cx + 150
            d.rectangle([bar_x, ry + 1, bar_x + pct * 6, ry + 11],
                        fill=lead["colour"])
            d.text((bar_x + pct * 6 + 6, ry), f"{pct}%", font=F_TINY_B,
                   fill=lead["colour"])
            ry += 20
        rule(d, cx, y + h - 22, x + w - 12)
        d.text((cx, y + h - 18),
               "Proposals only — hearings open 25 January; rates may change.",
               font=F_TINY, fill=GREY)
        return
    draw_wrapped(d, cx, by, lead["body"], F_BODY, w - 24, leading=15)


def paint_leads(d):
    paint_lead_card(d, 24, 148, 560, 196, LEADS[0], big=True)
    paint_lead_card(d, 600, 148, 400, 94, LEADS[1], big=False)
    paint_lead_card(d, 600, 250, 400, 94, LEADS[2], big=False)


def paint_timeline(d):
    y0, y1 = 352, 404
    d.rectangle([24, y0, W - 24, y1], outline=LIGHT_LINE, width=1, fill=PANEL)
    axis_y = y0 + 28
    d.line([(48, axis_y), (W - 48, axis_y)], fill=NAVY, width=2)
    n = len(TIMELINE)
    span = W - 48 - 96
    for i, (when, what) in enumerate(TIMELINE):
        cx = 48 + 48 + i * span // (n - 1) if n > 1 else 48
        d.ellipse([cx - 5, axis_y - 5, cx + 5, axis_y + 5], fill=RED,
                  outline=(255, 255, 255), width=1)
        tw = d.textlength(when, font=F_TINY_B)
        tx = min(max(cx - tw / 2, 30), W - 30 - tw)
        d.text((tx, axis_y - 22), when, font=F_TINY_B, fill=NAVY)
        # One short line per event, clamped inside the panel.
        line = wrap_words(d, what, F_TINY, 205)[0]
        lw = d.textlength(line, font=F_TINY)
        lx = min(max(cx - lw / 2, 28), W - 28 - lw)
        d.text((lx, axis_y + 9), line, font=F_TINY, fill=INK)


def paint_map(d):
    x0, y0, w, h = 24, 412, 600, 188
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=LIGHT_LINE, width=1, fill=SEA)
    d.text((x0 + 10, y0 + 6), "WHERE IT HAPPENED", font=F_TAG, fill=NAVY)
    mx, my, mw, mh = x0 + 6, y0 + 22, w - 12, h - 30
    for ring in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, mx, my, mw, mh) for lon, lat in ring]
        d.polygon(pts, fill=LAND, outline=(140, 148, 120))
    for lon, lat, label, dx, dy in HOTSPOTS:
        px, py = lonlat_to_xy(lon, lat, mx, my, mw, mh)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px + dx, py + dy), label, font=F_MAP, fill=NAVY)


def paint_markets(d):
    x0, y0, w, h = 640, 412, 360, 188
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=LIGHT_LINE, width=1, fill=PANEL)
    d.text((x0 + 10, y0 + 6), "MARKETS  —  25 NOV", font=F_TAG, fill=NAVY)
    zero_y = y0 + 84
    d.line([(x0 + 10, zero_y), (x0 + w - 10, zero_y)], fill=INK, width=1)
    bw, gap = 62, 16
    bx = x0 + 18
    for name, val, pct in MARKETS:
        bh = max(abs(pct) * 12, 3)
        col = GREEN_UP if pct > 0 else RED_DOWN
        if pct > 0:
            d.rectangle([bx, zero_y - bh, bx + bw, zero_y], fill=col)
            d.text((bx, zero_y - bh - 13), val, font=F_TINY_B, fill=col)
        else:
            d.rectangle([bx, zero_y, bx + bw, zero_y + bh], fill=col)
            d.text((bx, zero_y + bh + 3), val, font=F_TINY_B, fill=col)
        nw = d.textlength(name, font=F_TINY)
        d.text((bx + (bw - nw) / 2, y0 + h - 38), name, font=F_TINY, fill=INK)
        bx += bw + gap
    d.text((x0 + 10, y0 + h - 20),
           "Taiwan index -1,927 pts  ·  US markets shut Thu for Thanksgiving",
           font=F_TINY, fill=GREY)


def paint_region(d, x, y, w, h, title, items):
    d.rectangle([x, y, x + w, y + h], outline=LIGHT_LINE, width=1, fill=PANEL)
    d.rectangle([x, y, x + w, y + 20], fill=NAVY)
    d.text((x + 8, y + 4), title, font=F_SMALL_B, fill=(250, 247, 239))
    count = f"{len(items)} STORIES"
    d.text((x + w - 8 - d.textlength(count, font=F_TAG), y + 5),
           count, font=F_TAG, fill=(200, 210, 224))
    iy = y + 26
    for head, src in items:
        if iy + 26 > y + h - 4:
            break
        d.text((x + 8, iy), "\u2022", font=F_SMALL_B, fill=RED)
        tx = x + 18
        tw = w - 26
        lines = wrap_words(d, head, F_SMALL, tw)[:2]
        ly = iy
        for ln in lines:
            d.text((tx, ly), ln, font=F_SMALL, fill=INK)
            ly += 12
        tag = "— " + src
        tag_w = d.textlength(tag, font=F_TINY)
        last = lines[-1]
        last_w = d.textlength(last, font=F_SMALL)
        if last_w + 6 + tag_w <= tw and len(lines) == 1:
            d.text((tx + last_w + 6, ly - 12), tag, font=F_TINY, fill=GREY)
            iy = ly + 3
        elif last_w + 6 + tag_w <= tw:
            d.text((tx + last_w + 6, ly - 12), tag, font=F_TINY, fill=GREY)
            iy = ly + 3
        else:
            d.text((tx, ly), tag, font=F_TINY, fill=GREY)
            iy = ly + 12 + 2
    return iy


def paint_regions(d):
    col_w = (W - 48 - 24) // 3
    row_h = 184
    for idx, (title, items) in enumerate(REGIONS):
        col, row = idx % 3, idx // 3
        x = 24 + col * (col_w + 12)
        y = 608 + row * (row_h + 8)
        paint_region(d, x, y, col_w, row_h, title, items)


def paint_footer(d):
    rule(d, 24, 992, W - 24, width=2)
    d.text((24, 999),
           "All stories first reported 25\u201326 November 2026  ·  Sources: Reuters, AP, BBC, Guardian, PTI, CNA, KCNA, ESA, Fed, Nasdaq",
           font=F_TINY, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    paint_masthead(d)
    paint_numbers(d)
    paint_leads(d)
    paint_timeline(d)
    paint_map(d)
    paint_markets(d)
    paint_regions(d)
    paint_footer(d)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
