#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261118.

Draws a one-page newspaper front page summing up world news of
Wednesday 18 November 2026. Everything is drawn from scratch with
Pillow primitives (rectangles, polygons, arcs, text) -- no photos,
no copied artwork, no network. Run: python3 tools/generate_image.py
writes ../entry.png (1024x1024, deterministic).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

BG = (10, 26, 47)          # deep navy page
PANEL = (19, 46, 82)       # panel fill
PANEL_BORDER = (46, 78, 120)
GOLD = (232, 185, 15)      # masthead date / accents
WHITE = (255, 255, 255)
MUTED = (185, 201, 220)    # body text
FAINT = (140, 160, 185)    # footer text
TICKER_BG = (16, 38, 66)

def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def chip(draw, x, y, label, color):
    """Small rounded tag, e.g. MIDDLE EAST. Returns its width."""
    fnt = font(True, 16)
    tw = draw.textlength(label, font=fnt)
    w = int(tw) + 20
    draw.rounded_rectangle([x, y, x + w, y + 26], radius=6, fill=color)
    draw.text((x + 10, y + 4), label, font=fnt, fill=WHITE)
    return w

def star4(draw, cx, cy, r, fill):
    draw.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28),
                  (cx + r, cy), (cx + r * 0.28, cy + r * 0.28),
                  (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
                  (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)], fill=fill)

# ---------------------------------------------------------------- icons
# Each draws inside a 112x112 box whose top-left is (x, y).

def icon_gulf(d, x, y):
    # Strait of Hormuz: sea waves, a jet, an explosion burst.
    for i, wy in enumerate((y + 88, y + 98)):
        d.line([(x, wy), (x + 18, wy - 6), (x + 36, wy), (x + 54, wy - 6),
                (x + 72, wy), (x + 90, wy - 6), (x + 112, wy)],
               fill=(70, 140, 200), width=3)
    # explosion starburst over the water
    cx, cy = x + 78, y + 58
    pts = []
    import math
    for k in range(12):
        ang = math.pi * k / 6
        r = 26 if k % 2 == 0 else 12
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(240, 140, 30))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 210, 60))
    # jet flying in from the upper left: fuselage, swept wings, tail
    d.polygon([(x + 4, y + 22), (x + 46, y + 28), (x + 52, y + 32),
               (x + 46, y + 36), (x + 4, y + 34)], fill=(220, 225, 232))
    d.polygon([(x + 22, y + 28), (x + 34, y + 12), (x + 40, y + 28)],
              fill=(190, 196, 206))
    d.polygon([(x + 8, y + 24), (x + 16, y + 12), (x + 20, y + 26)],
              fill=(190, 196, 206))
    d.line([(x + 52, y + 32), (x + 62, y + 40)], fill=(255, 210, 60), width=3)

def icon_summit(d, x, y):
    # Globe with three leader pins: Shenzhen summit.
    cx, cy = x + 56, y + 56
    d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], outline=(90, 170, 230),
              width=4)
    d.ellipse([cx - 20, cy - 44, cx + 20, cy + 44], outline=(90, 170, 230),
              width=2)
    d.line([(cx - 44, cy), (cx + 44, cy)], fill=(90, 170, 230), width=2)
    d.arc([cx - 44, cy - 22, cx + 44, cy + 22], 0, 360,
          fill=(90, 170, 230), width=2)
    for px, py, col in ((cx - 26, cy - 18, (200, 60, 60)),
                        (cx + 8, cy - 30, (232, 185, 15)),
                        (cx + 28, cy + 6, (70, 140, 220))):
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=WHITE)

def icon_bridge(d, x, y):
    # Kerch bridge: deck broken in the middle, a span falling, water below.
    # Left and right deck segments with a jagged gap between them.
    d.line([(x + 6, y + 44), (x + 46, y + 44)], fill=(210, 215, 225),
           width=5)
    d.line([(x + 66, y + 44), (x + 106, y + 44)], fill=(210, 215, 225),
           width=5)
    d.line([(x + 14, y + 44), (x + 14, y + 78)], fill=(160, 168, 180),
           width=4)
    d.line([(x + 98, y + 44), (x + 98, y + 78)], fill=(160, 168, 180),
           width=4)
    d.arc([x + 18, y + 30, x + 46, y + 78], 180, 360, fill=(240, 140, 30),
          width=4)
    d.arc([x + 66, y + 30, x + 94, y + 78], 180, 360, fill=(240, 140, 30),
          width=4)
    # the collapsed middle span, tilted as it falls toward the water
    d.polygon([(x + 46, y + 46), (x + 64, y + 52), (x + 60, y + 62),
               (x + 44, y + 56)], fill=(240, 140, 30))
    d.ellipse([x + 50, y + 68, x + 56, y + 74], fill=(255, 210, 60))
    d.ellipse([x + 60, y + 74, x + 65, y + 79], fill=(255, 210, 60))
    for wy in (y + 92, y + 102):
        d.line([(x, wy), (x + 18, wy - 5), (x + 36, wy), (x + 54, wy - 5),
                (x + 72, wy), (x + 90, wy - 5), (x + 112, wy)],
               fill=(70, 140, 200), width=3)

def icon_senate(d, x, y):
    # U.S. Capitol dome over a ballot box with a check mark.
    cx = x + 56
    d.pieslice([cx - 30, y + 12, cx + 30, y + 62], 180, 360,
               fill=(220, 225, 232))
    d.rectangle([cx - 34, y + 58, cx + 34, y + 66], fill=(220, 225, 232))
    for i in range(5):
        bx = cx - 28 + i * 14
        d.rectangle([bx, y + 66, bx + 7, y + 84], fill=(180, 188, 200))
    d.rectangle([cx - 38, y + 84, cx + 38, y + 90], fill=(220, 225, 232))
    d.line([(cx, y + 12), (cx, y + 2)], fill=(232, 185, 15), width=3)
    star4(d, cx, y + 2, 6, (232, 185, 15))
    # ballot check
    d.line([(x + 78, y + 92), (x + 88, y + 102), (x + 106, y + 78)],
           fill=(80, 200, 120), width=5)

def icon_health(d, x, y):
    # Medical cross in a ring, plus a spiky virus roundel.
    cx, cy = x + 40, y + 44
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=(80, 200, 120),
              width=4)
    d.rectangle([cx - 8, cy - 22, cx + 8, cy + 22], fill=(80, 200, 120))
    d.rectangle([cx - 22, cy - 8, cx + 22, cy + 8], fill=(80, 200, 120))
    vx, vy = x + 84, y + 78
    import math
    for k in range(8):
        ang = math.pi * k / 4
        d.line([(vx + 12 * math.cos(ang), vy + 12 * math.sin(ang)),
                (vx + 20 * math.cos(ang), vy + 20 * math.sin(ang))],
               fill=(240, 140, 30), width=3)
    d.ellipse([vx - 12, vy - 12, vx + 12, vy + 12], fill=(240, 140, 30))
    d.ellipse([vx - 4, vy - 4, vx + 4, vy + 4], fill=(255, 210, 60))

def icon_voyager(d, x, y):
    # Voyager probe: dish, body, boom, stars, and a dashed path.
    for i in range(14):
        px = x + 6 + i * 8
        py = y + 96 - i * 5
        if i % 2 == 0:
            d.line([(px, py), (px + 4, py - 3)], fill=(232, 185, 15), width=2)
    d.polygon([(x + 52, y + 34), (x + 92, y + 22), (x + 92, y + 46)],
              fill=(220, 225, 232))
    d.line([(x + 52, y + 34), (x + 30, y + 44)], fill=(160, 168, 180),
           width=4)
    d.rectangle([x + 18, y + 38, x + 32, y + 52], fill=(120, 200, 240))
    d.line([(x + 32, y + 45), (x + 52, y + 34)], fill=(160, 168, 180),
           width=3)
    star4(d, x + 14, y + 14, 7, WHITE)
    star4(d, x + 100, y + 66, 5, WHITE)
    star4(d, x + 88, y + 8, 4, (232, 185, 15))

# ---------------------------------------------------------------- stories
# Each story: (tag, tag colour, headline, summary, icon function).
# Facts as reported on 18 November 2026 by Reuters / AP / AFP via the
# day's briefings (Open Chronicle, The Daily Short, US Brief, Horizon,
# Zark News). The Qeshm strike itself was Tuesday; Iran's answer and
# the first reports landed on Wednesday 18 November.

STORIES = [
    ("MIDDLE EAST", (192, 57, 43),
     "U.S. strikes Iran site as drones hit Gulf bases",
     "U.S. jets hit a Revolutionary Guards missile site on Qeshm "
     "Island. Iran answered with drone attacks on U.S. bases in "
     "Bahrain and Kuwait.",
     icon_gulf),
    ("DIPLOMACY", (36, 113, 163),
     "Xi hosts Putin in Shenzhen; Trump talks set for Thursday",
     "The two leaders opened the APEC summit and denounced "
     "protectionism and sanctions, ahead of a rare three-way meeting "
     "with Donald Trump.",
     icon_summit),
    ("UKRAINE", (183, 149, 11),
     "Ukraine strike brings down an arch of the Kerch bridge",
     "Kyiv says a road arch and span fell after a second day of "
     "strikes on the bridge to Crimea. Moscow confirmed damage and "
     "vowed to rebuild.",
     icon_bridge),
    ("U.S. POLITICS", (30, 132, 73),
     "Peltola flips Alaska; Democrats take Senate 56\u201344",
     "Democrat Mary Peltola beat Republican Dan Sullivan \u2014 the "
     "party's ninth Senate flip \u2014 for its largest majority "
     "since 2009.",
     icon_senate),
    ("HEALTH", (202, 111, 30),
     "U.S. loses measles-free status after 26 years",
     "Measles has spread continuously for over a year, with 5,412 "
     "cases in 2026, the most since 1991. Ebola in Congo has passed "
     "11,000 cases.",
     icon_health),
    ("SPACE", (125, 60, 152),
     "Voyager 1 reaches one light-day from Earth",
     "NASA's probe crossed 16 billion miles at 5:16 a.m. ET \u2014 a "
     "distance light needs a full day to travel. No human-made "
     "object has gone farther.",
     icon_voyager),
]

TICKER = ("ALSO TODAY  \u2014  Cyclone Akvan bears down on Andhra Pradesh  "
          "\u00b7  Nvidia revenue doubles to $115.8bn  \u00b7  COP31 climate "
          "talks open in Turkey  \u00b7  Russia\u2013Ukraine agree largest "
          "prisoner swap")

# ---------------------------------------------------------------- page

def draw_panel(d, px, py, pw, ph, story):
    tag, color, headline, summary, icon = story
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=10, fill=PANEL,
                        outline=PANEL_BORDER, width=2)
    chip(d, px + 16, py + 13, tag, color)
    icon(d, px + 16, py + 52)
    hfnt = font(True, 25)
    lines = wrap(d, headline, hfnt, pw - 164)[:4]
    draw_text_block(d, px + 140, py + 54, lines, hfnt, WHITE, 30)
    sfnt = font(False, 18)
    slines = wrap(d, summary, sfnt, pw - 32)[:3]
    draw_text_block(d, px + 16, py + 168, slines, sfnt, MUTED, 23)

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Masthead
    d.line([(24, 14), (W - 24, 14)], fill=GOLD, width=3)
    tfnt = font(True, 58)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=tfnt)) / 2, 26), title,
           font=tfnt, fill=WHITE)
    dfnt = font(True, 33)
    date = "WEDNESDAY  \u00b7  18 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=dfnt)) / 2, 96), date,
           font=dfnt, fill=GOLD)
    sfnt = font(False, 20)
    sub = "Six stories that defined the day \u2014 from the Gulf to the edge of the Solar System"
    d.text(((W - d.textlength(sub, font=sfnt)) / 2, 140), sub,
           font=sfnt, fill=MUTED)
    # Story grid: 2 columns x 3 rows
    margin, gap = 24, 16
    pw = (W - 2 * margin - gap) // 2
    ph = 236
    top = 178
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        px = margin + col * (pw + gap)
        py = top + row * (ph + 14)
        draw_panel(d, px, py, pw, ph, story)
    # Ticker strip
    ty = top + 3 * ph + 2 * 14 + 12
    d.rounded_rectangle([margin, ty, W - margin, ty + 44], radius=8,
                        fill=TICKER_BG, outline=PANEL_BORDER, width=1)
    tfnt2 = font(False, 17)
    tlines = wrap(d, TICKER, tfnt2, W - 2 * margin - 28)
    draw_text_block(d, margin + 14, ty + 5, tlines[:2], tfnt2, WHITE, 20)
    # Footer
    ffnt = font(False, 15)
    foot = "Drawn from news reports of 18 November 2026  \u00b7  One image, one day"
    d.text(((W - d.textlength(foot, font=ffnt)) / 2, H - 26), foot,
           font=ffnt, fill=FAINT)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
