#!/usr/bin/env python3
"""Render 'The World in One Page' — a dense 1024x1024 newspaper front page
summarising the world news of Thursday 26 November 2026.

Midday edition (09:00 WIB / 02:00 UTC): Trump's new tariffs on 14 trading
partners, Nvidia's slide as the AI rout deepens, the Houthis' Ras Tanura
claim pushing Brent to $94.61, Ukraine's strike on Savasleyka air base, and
Kim Jong Un's call for wider tactical nuclear deployment.

Run:  python3 draw_news.py        -> writes entry.png next to this script.
Only the Python standard library plus Pillow is used; fonts are the system
DejaVu faces. Everything on the page is drawn from the story tables below.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (250, 246, 238)
INK = (22, 26, 34)
BODY = (52, 56, 64)
NAVY = (18, 33, 62)
RED = (178, 34, 34)
GREY = (96, 100, 108)
CARD = (255, 255, 255)
EDGE = (203, 196, 184)
OCEAN = (172, 206, 224)
LAND = (233, 215, 165)
LEAF = (150, 184, 130)
GREEN = (39, 124, 74)


def fnt(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)


def wrap_text(draw, text, font, max_w):
    """Greedy word wrap measured with the real font; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Sheet:
    """The page plus the small drawing helpers every panel shares."""

    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def text(self, xy, s, size, bold=False, fill=INK):
        self.d.text(xy, s, font=fnt(size, bold), fill=fill)

    def centred(self, y, s, size, bold=False, fill=INK, cx=W // 2):
        w = self.d.textlength(s, font=fnt(size, bold))
        self.d.text((cx - w / 2, y), s, font=fnt(size, bold), fill=fill)

    def para(self, x, y, w, s, size, fill=BODY, leading=None, bold=False):
        """Draw a wrapped paragraph; return the y just below it."""
        font = fnt(size, bold)
        step = leading if leading is not None else size + 3
        for line in wrap_text(self.d, s, font, w):
            self.d.text((x, y), line, font=font, fill=fill)
            y += step
        return y

    def save(self):
        self.img.save(OUT)
        print(f"wrote {OUT} {W}x{H}")


class Column:
    """One vertical stack of region sections: coloured header bars with
    short headline + one-line body stories underneath."""

    def __init__(self, sheet, x, y, w, bottom):
        self.s = sheet
        self.x, self.y, self.w, self.bottom = x, y, w, bottom

    def header(self, title, colour):
        d = self.s.d
        d.rectangle([self.x, self.y, self.x + self.w, self.y + 20], fill=colour)
        d.text((self.x + 8, self.y + 4), title, font=fnt(11, True),
               fill=(255, 255, 255))
        self.y += 23

    def story(self, head, body, tag):
        d = self.s.d
        x, w = self.x + 2, self.w - 4
        for line in wrap_text(d, head, fnt(10, True), w):
            d.text((x, self.y), line, font=fnt(10, True), fill=INK)
            self.y += 12
        lines = wrap_text(d, body, fnt(9), w)
        tag_font = fnt(8, True)
        tag_w = d.textlength(" " + tag, font=tag_font)
        for i, line in enumerate(lines):
            d.text((x, self.y), line, font=fnt(9), fill=BODY)
            self.y += 11
            if i == len(lines) - 1:  # red source tag at the end of the story
                lw = d.textlength(line, font=fnt(9))
                if lw + tag_w <= w:
                    d.text((x + lw, self.y - 11), " " + tag,
                           font=tag_font, fill=RED)
                else:
                    d.text((x, self.y), tag, font=tag_font, fill=RED)
                    self.y += 10
        self.y += 2
        if self.y > self.bottom:
            print(f"WARNING: column overflow past y={self.bottom} "
                  f"(now {self.y})")


# ---------------------------------------------------------------- content
LEADS = [
    ("LEAD 1 \u2014 TRADE",
     "Trump hits 14 partners with new tariffs",
     "China faces 20% on top of ~25% from his first term; the EU, Japan "
     "and South Korea are capped at 15%; Vietnam up to 35%. Public "
     "hearings start 25 Jan. \u2014 REUTERS, 25 NOV"),
    ("LEAD 2 \u2014 MARKETS",
     "Nvidia slides 3.9% as the AI rout deepens",
     "Closed at $149.30 after falling to $141.17 intraday. The Nasdaq "
     "plunged 4.6% in the session before recovering to -0.6%; the Dow "
     "rose 0.3%. \u2014 REUTERS, 25 NOV"),
    ("LEAD 3 \u2014 ENERGY",
     "Houthis claim Ras Tanura hit; Brent jumps to $94.61",
     "Brent +3.5%, WTI $83.68. The Houthis say they hit Saudi Arabia's "
     "biggest refinery and Riyadh's financial district; Riyadh says it "
     "downed 4 drones. \u2014 REUTERS, 25 NOV"),
]

TIMELINE = [
    ("25 NOV 13:30", "US proposes new tariffs on 14 trading partners"),
    ("25 NOV 16:00", "Nasdaq plunges 4.6% intraday, recovers to -0.6%"),
    ("25 NOV EVENING", "Houthis claim Ras Tanura strike; Brent ends +3.5%"),
    ("25 NOV EVENING", "Pope Leo calls the COP31 failure \u2018troubling\u2019"),
    ("26 NOV 00:00", "Kim Jong Un orders wider tactical nuclear deployment"),
]

# (panel title, colour, [(headline, body, source tag), ...])
REGIONS_LEFT = [
    ("AMERICAS", (21, 101, 160), [
        ("Second judge blocks birthright citizenship order",
         "Trump's newest order curtailing birthright citizenship is halted.", "REUTERS"),
        ("Fed Beige Book: modest growth, price pressure",
         "Wage gains continue but price pressures persist, the Fed reports.", "FED"),
        ("US markets shut today for Thanksgiving",
         "NYSE and Nasdaq closed Thu 26 Nov; early close Fri at 1pm ET.", "NASDAQ"),
        ("Melania Trump reunites 9 children with families",
         "Nine Ukrainian and Russian children returned to their families.", "AP"),
        ("Ecuador minister: US talks review operations",
         "Quito says talks with Washington focus on US operations in Ecuador.", "REUTERS"),
        ("US proposes 10% tariff on Brazil's Embraer jets",
         "Plus higher sugar duties above quota in a new trade-probe move.", "REUTERS"),
    ]),
    ("EUROPE", (108, 52, 131), [
        ("Ukraine hits Savasleyka air base; 5 jets out",
         "Three MiG-31s and two Su-34s knocked out, Kyiv's General Staff says.", "REUTERS"),
        ("Leaked data puts Russian war dead near 490,000",
         "BBC analysis of leaked Russian mortality statistics gives the toll.", "BBC"),
        ("Russia's oil refining at a 20-year low",
         "Ukraine has hit at least 18 refineries, cutting output sharply.", "REUTERS"),
        ("Murmansk governor held on corruption charges",
         "Governor of the strategic Arctic region in pre-trial custody.", "REUTERS"),
        ("Norway top court voids disputed oil licences",
         "Supreme Court rules climate-disputed licences invalid.", "AP"),
        ("EU hunts new ECB chief as Lagarde resigns",
         "Search begins for Christine Lagarde's successor at the ECB.", "AP"),
        ("Pope Leo calls COP31 failure \u2018troubling\u2019",
         "Pontiff urges leaders to step up climate action at his audience.", "REUTERS"),
    ]),
    ("MIDDLE EAST", (185, 119, 14), [
        ("Israeli strike kills Hamas security chief in Gaza",
         "Senior official dies with his wife and children in Gaza City.", "BBC"),
        ("Cairo fuel tanker fire kills at least 31",
         "Blaze on the Ring Road injures 21 and chars dozens of vehicles.", "GUARDIAN"),
        ("Iran says ships hit mines in Hormuz",
         "Tehran warns vessels to coordinate passage through the strait.", "REUTERS"),
        ("Lebanon to open second airport next month",
         "Northern airport opens as Hezbollah's sway wanes, officials say.", "REUTERS"),
        ("Judges urge dropping top Netanyahu charges",
         "Israeli judges recommend dropping the most serious charges.", "AP"),
    ]),
]

REGIONS_RIGHT = [
    ("AFRICA", (30, 132, 73), [
        ("Drone strikes kill 19 civilians in Sudan",
         "RSF drones hit three residential areas in Damazin, Blue Nile.", "REUTERS"),
        ("Kenya discharges last Ebola patient",
         "DRC death toll passes 5,300 as the outbreak's end nears.", "AP"),
        ("S. African court backs Ramaphosa in cash probe",
         "Court victory for the president over the cash-theft inquiry.", "REUTERS"),
        ("ECOWAS approves regional force plan",
         "West African bloc sets a roadmap to deploy its force by end-2027.", "AP"),
        ("Ghana unveils heritage banknotes",
         "New series honours Nkrumah, Kofi Annan and Makola traders.", "AP"),
    ]),
    ("ASIA-PACIFIC", (202, 111, 30), [
        ("Kim orders wider tactical nuclear deployment",
         "North Korea to deploy tactical nuclear arms across more domains.", "KCNA"),
        ("N. Korea orders Swiss office in Pyongyang shut",
         "Pyongyang expels the Swiss diplomat in a sanctions row.", "AP"),
        ("Taiwan shares plunge 1,927 points",
         "Index falls as US tariff plan hits; NT dollar weakens past 33.", "CNA"),
        ("How China got Nvidia AI chips despite rules",
         "Reuters explainer traces the routes around US export controls.", "REUTERS"),
        ("Pakistan's first astronaut reaches Tiangong",
         "Shenzhou-24 docks; Zeeshan Ali is the first foreigner aboard.", "REUTERS"),
        ("India marks Constitution Day, adds IIT seats",
         "6,000 new seats in robotics, AI and space technology.", "PTI"),
        ("Bangladesh raises garment wage 36%",
         "Minimum monthly wage for entry-level garment workers rises.", "AP"),
    ]),
    ("TECH / SCIENCE / SPORT", (46, 64, 83), [
        ("Hera images show stadium-sized asteroid crater",
         "Spacecraft's pictures reveal the crater from the defence test.", "ESA"),
        ("Gukesh faces Sindarov in World Chess final",
         "India's champion meets Uzbekistan's Sindarov in Geneva.", "PTI"),
        ("IPL 2027 auction draws 1,220 players",
         "A record 1,220 cricketers register for the auction.", "PTI"),
        ("Sooryavanshi smashes 204 off 53 balls",
         "Teenager's double century powers India past the UAE.", "PTI"),
        ("Flipkart CEO to step down in December",
         "Kalyan Krishnamurthy leaves the top job at the e-commerce firm.", "REUTERS"),
    ]),
]

NUMBERS = [
    ("$94.61", "Brent crude, +3.5% on the day"),
    ("$149.30", "Nvidia close, -3.9% on Wed"),
    ("490,334", "Russian war dead in leaked data"),
    ("31", "killed in the Cairo tanker fire"),
    ("20%", "top tariff rate proposed on China"),
    ("1,927", "points lost by Taiwan's market"),
]

# (label, value %, colour) for the markets bars
BARS = [
    ("Brent Wed", 3.5, GREEN),
    ("Dow Wed", 0.33, GREEN),
    ("S&P 500 Wed", -0.25, RED),
    ("Nasdaq Wed", -0.62, RED),
    ("NVDA Wed", -3.91, RED),
]

# schematic map: (label, dot x, dot y, label dx, label dy) in panel coords
MAP_DOTS = [
    ("Washington", 78, 52, 8, -4),
    ("Kyiv", 288, 30, -8, -14),
    ("Gaza", 300, 52, -40, -4),
    ("Cairo", 296, 64, -62, 8),
    ("Riyadh", 332, 58, 8, -4),
    ("Damazin", 310, 86, 8, -4),
    ("Jiuquan", 400, 28, -56, -16),
    ("Pyongyang", 432, 34, 8, -4),
    ("Taipei", 448, 58, -50, 10),
]


def draw_masthead(s):
    d = s.d
    d.rectangle([0, 0, W, 62], fill=NAVY)
    s.centred(7, "THE WORLD IN ONE PAGE", 30, bold=True, fill=(255, 255, 255))
    s.centred(42, "THURSDAY 26 NOVEMBER 2026  \u2022  MIDDAY EDITION \u2014 "
              "NEWS TO 09:00 WIB / 02:00 UTC",
              11, fill=(205, 214, 228))
    d.rectangle([0, 62, W, 65], fill=RED)


def draw_leads(s):
    y, h, w, gap = 70, 112, 328, 12
    for i, (kicker, head, body) in enumerate(LEADS):
        x = 8 + i * (w + gap)
        s.d.rectangle([x, y, x + w, y + h], fill=CARD, outline=EDGE)
        s.d.rectangle([x, y, x + w, y + 3], fill=RED)
        yy = s.para(x + 10, y + 9, w - 20, kicker, 9, fill=RED, bold=True)
        yy = s.para(x + 10, yy + 1, w - 20, head, 13, fill=INK,
                    leading=16, bold=True)
        s.para(x + 10, yy + 2, w - 20, body, 10, leading=13)


def draw_timeline(s):
    d = s.d
    y = 188
    s.text((8, y), "25\u201326 NOV \u2014 AS THE DAY UNFOLDED (UTC)", 11,
           bold=True, fill=NAVY)
    d.line([8, y + 18, W - 8, y + 18], fill=RED, width=2)
    col_w = 199
    for i, (when, what) in enumerate(TIMELINE):
        x = 8 + i * col_w
        d.text((x, y + 22), when, font=fnt(10, True), fill=RED)
        s.para(x, y + 36, col_w - 8, what, 9, leading=11)


def draw_map(s):
    px, py, pw, ph = 8, 248, 548, 120
    d = s.d
    d.rectangle([px, py, px + pw, py + ph], fill=OCEAN, outline=EDGE)
    s.text((px + 8, py + 4), "WHERE THE NEWS HAPPENED", 10, bold=True, fill=NAVY)
    # rough continent blobs (schematic, not to scale)
    blobs = [
        (18, 26, 128, 62, LAND), (96, 66, 138, 104, LAND),
        (238, 20, 288, 44, LAND), (246, 48, 296, 92, LEAF),
        (300, 16, 470, 62, LAND), (428, 84, 486, 104, LAND),
    ]
    for (x0, y0, x1, y1, col) in blobs:
        d.ellipse([px + x0, py + y0, px + x1, py + y1], fill=col)
    for label, dx, dy, lx, ly in MAP_DOTS:
        cx, cy = px + dx, py + dy
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED,
                  outline=(255, 255, 255))
        tx, ty = cx + lx, cy + ly
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            d.text((tx + ox, ty + oy), label, font=fnt(9, True),
                   fill=(255, 255, 255))
        d.text((tx, ty), label, font=fnt(9, True), fill=INK)


def draw_markets(s):
    px, py, pw, ph = 564, 248, 452, 120
    d = s.d
    d.rectangle([px, py, px + pw, py + ph], fill=CARD, outline=EDGE)
    s.text((px + 10, py + 5), "MARKETS \u2014 AI ROUT, OIL SURGE",
           10, bold=True, fill=NAVY)
    axis = px + 112
    top = py + 26
    scale = 230.0 / 4.6
    for i, (label, val, col) in enumerate(BARS):
        yy = top + i * 15
        d.text((px + 10, yy), label, font=fnt(9), fill=BODY)
        d.line([axis, top - 4, axis, top + 5 * 15 - 6], fill=EDGE, width=1)
        bar = int(abs(val) * scale)
        if val >= 0:
            d.rectangle([axis, yy + 1, axis + bar, yy + 11], fill=col)
            d.text((axis + bar + 5, yy), f"+{val}%", font=fnt(9, True), fill=col)
        else:
            d.rectangle([axis - bar, yy + 1, axis, yy + 11], fill=col)
            d.text((axis + 6, yy), f"{val}%", font=fnt(9, True), fill=col)
    s.para(px + 10, top + 5 * 15, pw - 20,
           "Wed close: Nasdaq -0.6% after -4.6% intraday \u00b7 S&P -0.25% "
           "\u00b7 Dow +0.33%. US markets closed Thu for Thanksgiving. "
           "\u2014 REUTERS",
           8, fill=GREY, leading=10)


def draw_regions(s):
    left = Column(s, 8, 374, 496, 934)
    for title, colour, stories in REGIONS_LEFT:
        left.header(title, colour)
        for head, body, tag in stories:
            left.story(head, body, tag)
    right = Column(s, 520, 374, 496, 934)
    for title, colour, stories in REGIONS_RIGHT:
        right.header(title, colour)
        for head, body, tag in stories:
            right.story(head, body, tag)
    print(f"region columns end at y={left.y} (left) / {right.y} (right)")


def draw_numbers(s):
    d = s.d
    y = 940
    d.rectangle([8, y, W - 8, 1016], fill=CARD, outline=EDGE)
    s.text((16, y + 6), "BY THE NUMBERS", 11, bold=True, fill=NAVY)
    col_w = (W - 32) // 6
    for i, (val, label) in enumerate(NUMBERS):
        x = 16 + i * col_w
        d.text((x, y + 24), val, font=fnt(15, True), fill=RED)
        s.para(x, y + 44, col_w - 10, label, 8, fill=GREY, leading=10)


def main():
    s = Sheet()
    draw_masthead(s)
    draw_leads(s)
    draw_timeline(s)
    draw_map(s)
    draw_markets(s)
    draw_regions(s)
    draw_numbers(s)
    s.save()
    total = sum(len(stories) for _, _, stories in REGIONS_LEFT + REGIONS_RIGHT)
    print(f"stories: {len(LEADS)} leads + {total} region stories = "
          f"{len(LEADS) + total} total")


if __name__ == "__main__":
    main()
