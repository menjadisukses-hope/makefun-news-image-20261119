#!/usr/bin/env python3
"""Generate a 1024x1024 newspaper front-page image summing up 19 Nov 2026 world news.
Deterministic: no randomness, no timestamps, no network."""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
BG = (250, 247, 238)
INK = (18, 18, 18)
RED = (178, 24, 24)
BLUE = (20, 55, 110)
GREY = (90, 90, 90)
LIGHT = (232, 226, 210)

# Outlets consulted while researching the day's stories.
SOURCES = ("Reuters", "AP", "AFP", "Al Jazeera", "IAEA", "IMD")
EDITION_LINE = "Thursday 19 November 2026"

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)
    return d.textbbox((x, y), s, font=font, anchor=anchor)[3]

def wrap(s, font, width):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def block(x, y, w_, headline, body, hsize=20, bsize=14, hcolor=INK, blines_max=4):
    yy = y
    for ln in wrap(headline, F(SANS_B, hsize), w_):
        text(x, yy, ln, F(SANS_B, hsize), hcolor)
        yy += hsize + 3
    for ln in wrap(body, F(SANS, bsize), w_)[:blines_max]:
        text(x, yy, ln, F(SANS, bsize), (40, 40, 40))
        yy += bsize + 3
    return yy

def hline(x0, x1, y, color=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=color, width=width)

# Masthead
d.rectangle([0, 0, W, 92], fill=INK)
text(W // 2, 10, "THE  WORLD  TODAY", F(SERIF_B, 46), (255, 255, 255), "ma")
text(W // 2, 62, "Thursday 19 November 2026  •  15 stories  •  6 continents  •  One page",
     F(SANS_B, 16), (255, 210, 120), "ma")
hline(24, W - 24, 104, RED, 4)

# Lead story: GTA VI launch day
y = 114
text(24, y, "1  GAMES • LAUNCH DAY", F(SANS_B, 15), RED)
y += 22
y = block(24, y, 640, "GTA VI SMASHES EVERY STREAMING RECORD",
          "Rockstar's Grand Theft Auto VI launched in a rolling midnight rollout and drew a "
          "preliminary peak of 7.89 million concurrent viewers across Twitch, YouTube and Kick — "
          "4.5x the old launch record. Twitch alone hit 3.29m, a category record, and critics "
          "gave the game 99 on Metacritic. Sensor Tower counts about 17m copies pre-sold.",
          hsize=30, bsize=15, blines_max=5)
hline(24, 664, y + 4, GREY, 1)

# Right rail top: APEC trilateral
rx = 688
text(rx, 114, "2  APEC • SHENZHEN", F(SANS_B, 15), RED)
block(rx, 136, 312, "TRUMP, XI & PUTIN MEET: FIRST-EVER TRILATERAL",
      "The three presidents sat down together in Shenzhen on the APEC sidelines — a first. "
      "Nuclear arms, the Iran war and trade topped the agenda; Xi urged a ban on nuclear "
      "weapons, pledged $20m for APEC cooperation, and the US–China trade truce expires "
      "10 January.",
      hsize=19, bsize=13, blines_max=7)
hline(rx, W - 24, 330, GREY, 1)
text(rx, 340, "3  GULF • HORMUZ", F(SANS_B, 15), RED)
block(rx, 362, 312, "TWO SUPERTANKERS 'HIT MINES' IN THE STRAIT",
      "Iran's Revolutionary Guards said two supertankers carrying 4m barrels exploded after "
      "hitting mines on an unauthorised route. Crude flows are back near pre-war levels, "
      "but LNG is stuck at a third and Brent holds near $92.",
      hsize=17, bsize=13, blines_max=5)

# Map band
my = 352
d.rectangle([24, my, 664, 540], fill=(214, 228, 238), outline=BLUE, width=2)
text(36, my + 8, "THE DAY ON THE MAP", F(SANS_B, 16), BLUE)
land = (168, 188, 150)
continents = [
    [(60, 420), (150, 395), (210, 410), (205, 450), (160, 490), (120, 470), (70, 460)],
    [(185, 470), (220, 465), (225, 505), (200, 520), (180, 505)],
    [(330, 400), (390, 390), (420, 415), (400, 450), (350, 445), (325, 425)],
    [(340, 450), (410, 445), (430, 490), (395, 530), (355, 505)],
    [(425, 400), (540, 390), (610, 420), (590, 470), (500, 455), (440, 440)],
    [(545, 475), (600, 470), (615, 500), (575, 520), (550, 500)],
]
for poly in continents:
    d.polygon(poly, fill=land, outline=(120, 140, 110))
pins = [
    (470, 425, "3", "Hormuz"),
    (540, 412, "2", "Shenzhen"),
    (400, 406, "4", "Kerch Bridge"),
    (352, 418, "4", "Odesa"),
    (500, 465, "5", "Akvan"),
    (575, 395, "6", "Yongbyon"),
    (598, 425, "7", "Tokyo"),
]
for px, py, num, label in pins:
    d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED, outline=(255, 255, 255), width=2)
    text(px, py - 1, num, F(SANS_B, 12), (255, 255, 255), "ma")
text(36, 512, "2 Shenzhen  •  3 Hormuz  •  4 Ukraine  •  5 Cyclone Akvan  •  6 Korea  •  7 Tokyo",
     F(SANS_B, 12), BLUE)

# Middle grid, 3 columns x 2 rows
gy = 552
cols = [(24, 320), (352, 320), (680, 320)]
stories = [
    ("4  UKRAINE", "KERCH BRIDGE HIT A 3RD TIME IN 3 DAYS",
     "Ukraine struck the Crimean bridge again overnight, halting road and rail. Russia hit "
     "Odesa, killing four — the city declared 19 Nov a day of mourning. 30+ leaders meet in "
     "Berlin on security guarantees; the EU proposes a €45bn loan for 2027."),
    ("5  ASIA", "CYCLONE AKVAN NEARS INDIA'S EAST COAST",
     "Severe Cyclone Akvan is due to cross the Andhra–Odisha coast around noon Friday, "
     "winds 90–100 km/h gusting to 110. Odisha evacuated nearly 50,000 people and opened "
     "448 shelters; schools shut for three days."),
    ("6  KOREA", "IAEA: N. KOREA EXPANDS URANIUM PLANT",
     "The UN nuclear watchdog says North Korea extended its Yongbyon enrichment facility — "
     "construction since mid-September, externally complete by late October. Trump says he "
     "wants to meet Kim Jong Un during his Asia trip."),
    ("7  INDIA–JAPAN", "TOKYO 2+2: JAPANESE TROOPS TO TRAIN IN INDIA",
     "India and Japan held their 4th foreign-and-defence ministers' dialogue in Tokyo and "
     "agreed Japan's Self-Defence Forces will use an Indian firing range for the first time "
     "in 2027, deepening Quad security ties."),
    ("8  TECH", "US OUTAGES HIT BANKS, AIRLINES AND APPS",
     "Disruptions rippled through JPMorgan Chase, United Airlines, Apple and Microsoft "
     "services and air-traffic systems. Officials said cyberattacks were not the cause; "
     "Nvidia's record $115.8bn quarter still buoyed chip stocks."),
    ("9  MARKETS", "OIL STEADY, GAS JUMPS AS COLD SNAP NEARS",
     "Brent settled near $92 and WTI near $83 despite the Gulf fighting, as crude flows "
     "recovered. European gas rebounded to €86/MWh with a cold snap due from 20 Nov; "
     "stocks stayed nervous on war and trade headlines."),
]
for i, (kicker, head, body) in enumerate(stories):
    cx, cw = cols[i % 3]
    cy = gy if i < 3 else gy + 150
    text(cx, cy, kicker, F(SANS_B, 13), RED)
    block(cx, cy + 18, cw, head, body, hsize=16, bsize=12, blines_max=5)
    if i % 3 != 2:
        d.line([(cx + cw + 14, cy), (cx + cw + 14, cy + 132)], fill=(200, 195, 180), width=1)
hline(24, W - 24, gy + 142, GREY, 1)
hline(24, W - 24, gy + 292, GREY, 1)

# Bottom briefs
by = gy + 302
text(24, by, "IN BRIEF — THE REST OF THE WORLD IN ONE LINE EACH", F(SANS_B, 15), BLUE)
briefs = [
    "DELHI: The Prince and Princess of Wales met PM Narendra Modi on their India visit.",
    "SEOUL: President Lee Jae Myung renews his call for dialogue with Pyongyang.",
    "WASHINGTON: Trump tells Fox the US needs no help from China or Russia on Iran.",
    "GAZA: The ceasefire stays fragile as fighting and aid shortfalls continue.",
    "BERLIN: Coalition of the Willing leaders gather on Ukraine aid and guarantees.",
    "KYIV: Ukraine says its drone strikes have cut Russian oil refining output by 45%.",
]
yy = by + 24
for b in briefs:
    text(24, yy, "•  " + b, F(SANS, 12), (35, 35, 35))
    yy += 17

d.rectangle([0, H - 28, W, H], fill=INK)
footer = ("All the day's news, in one image — " + EDITION_LINE +
          "  •  Sources: " + ", ".join(SOURCES))
text(W // 2, H - 22, footer, F(SANS, 11), (255, 255, 255), "ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
img.save(out, optimize=True)
print(out, os.path.getsize(out))
