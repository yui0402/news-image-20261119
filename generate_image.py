# Generates entry.png: a newspaper front page summing up Thursday 19 November
# 2026 (morning edition; a fuller edition follows before the deadline).
# Run locally with Pillow; the submitted main.py only copies the finished PNG.
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 245, 238)
INK = (18, 18, 18)
RED = (168, 0, 27)
GREY = (92, 88, 80)
BOX = (238, 233, 221)
LINE = (30, 30, 30)
SEA = (196, 208, 214)
FLAME = (224, 110, 20)
SMOKE = (120, 116, 108)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, text, font, fill=INK, max_w=300, leading=6):
    for ln in wrap(text, font, max_w):
        d.text((x, y), ln, font=font, fill=fill)
        y += font.size + leading
    return y


def kicker(x, y, s):
    d.text((x, y), s, font=F(SANS_B, 19), fill=RED)
    return y + 27


# ---------- masthead ----------
d.rectangle([0, 0, W, 10], fill=INK)
d.text((W // 2, 30), "THE WORLD TODAY", font=F(SERIF_B, 66), fill=INK, anchor="ma")
d.text((W // 2, 112), "THURSDAY  ·  19 NOVEMBER 2026  ·  THE DAY IN ONE IMAGE",
       font=F(SANS_B, 21), fill=GREY, anchor="ma")
d.rectangle([36, 148, W - 36, 151], fill=INK)
d.rectangle([36, 155, W - 36, 156], fill=INK)

# ---------- lead story: Shenzhen trilateral summit ----------
LX, LW = 36, 612
y = kicker(LX, 172, "APEC SUMMIT  ·  SHENZHEN, CHINA")
y = text_block(LX, y, "Trump, Xi and Putin meet face to face in Shenzhen",
               F(SERIF_B, 41), max_w=LW, leading=4)
y += 6
# drawing: three flags over a summit table
CH = 150
d.rectangle([LX, y, LX + LW, y + CH], fill=(255, 255, 255), outline=LINE, width=2)
flags = [((178, 34, 52), "USA"), ((222, 41, 16), "CHINA"), ((38, 74, 160), "RUSSIA")]
fw = (LW - 64) // 3
for i, (col, name) in enumerate(flags):
    fx = LX + 16 + i * (fw + 8)
    d.rectangle([fx, y + 18, fx + fw, y + 74], fill=col)
    if name == "USA":
        for s in range(4):
            d.line([fx, y + 26 + s * 12, fx + fw, y + 26 + s * 12], fill=(255, 255, 255), width=4)
        d.rectangle([fx, y + 18, fx + fw // 2, y + 46], fill=(38, 54, 120))
    if name == "CHINA":
        import math
        cx, cy, ro, ri = fx + 28, y + 34, 13, 5.2
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rad = ro if i % 2 == 0 else ri
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        d.polygon(pts, fill=(255, 222, 0))
    if name == "RUSSIA":
        d.rectangle([fx, y + 18, fx + fw, y + 37], fill=(255, 255, 255))
        d.rectangle([fx, y + 55, fx + fw, y + 74], fill=(200, 30, 40))
    d.text((fx + fw // 2, y + 84), name, font=F(SANS_B, 17), fill=INK, anchor="ma")
d.rectangle([LX + 16, y + 116, LX + LW - 16, y + 124], fill=INK)  # summit table
d.text((LX + LW // 2, y + 128), "FIRST TRILATERAL SUMMIT  ·  APEC",
       font=F(SANS_B, 15), fill=GREY, anchor="ma")
y += CH + 12
d.text((LX, y), "XI HUGS TRUMP ON THE TARMAC  ·  KYIV URGES PRESSURE ON PUTIN",
       font=F(SANS_B, 16), fill=RED)
y += 30
y = text_block(LX, y,
               "Xi Jinping gave Donald Trump a rare airport welcome and hailed "
               "ties with Russia as a source of stability, before the three "
               "presidents sat down together at the APEC summit — a meeting "
               "Beijing calls of groundbreaking significance.",
               F(SANS_R, 20), max_w=LW, leading=5)

# ---------- right column ----------
RX, RW = 684, 304
ry = kicker(RX, 172, "STRAIT OF HORMUZ  ·  ESCALATION")
ry = text_block(RX, ry, "Three tankers ablaze after hitting mines", F(SERIF_B, 27),
                max_w=RW, leading=3)
ry += 4
# small drawing: tanker silhouette with flames
d.rectangle([RX, ry, RX + RW, ry + 62], fill=(255, 255, 255), outline=LINE, width=2)
sy = ry + 62
d.polygon([RX + 30, sy - 18, RX + 250, sy - 18, RX + 232, sy - 4, RX + 48, sy - 4], fill=INK)
d.rectangle([RX + 120, sy - 30, RX + 170, sy - 18], fill=INK)
for fx in (RX + 84, RX + 140, RX + 196):
    d.polygon([fx, sy - 20, fx + 9, sy - 40, fx + 18, sy - 20], fill=FLAME)
    d.ellipse([fx + 2, sy - 56, fx + 20, sy - 38], fill=SMOKE)
d.line([RX + 6, sy - 2, RX + RW - 6, sy - 2], fill=SEA, width=3)
ry += 70
ry = text_block(RX, ry,
                "Iran says three oil tankers caught fire after striking mines "
                "east of Hormuz, as Gulf states repel Iranian drone attacks.",
                F(SANS_R, 18), max_w=RW, leading=4)
ry += 10
d.line([RX, ry, RX + RW, ry], fill=LINE, width=2)
ry += 12
ry = kicker(RX, ry, "WORLD COURT  ·  THE HAGUE")
ry = text_block(RX, ry, "Court rules on Myanmar genocide case", F(SERIF_B, 25),
                max_w=RW, leading=3)
ry += 4
ry = text_block(RX, ry,
                "The World Court delivers its judgment on Myanmar's alleged "
                "genocide of the Rohingya, watched by 1.2 million refugees in "
                "Bangladesh.",
                F(SANS_R, 18), max_w=RW, leading=4)

# ---------- middle band: three boxes ----------
BY = 634
BH = 170
BW = (W - 72 - 24) // 3
boxes = [
    ("GAMING", "GTA VI launches worldwide",
     "Grand Theft Auto VI goes on sale around the world after a 13-year wait, "
     "to near-perfect reviews — the biggest entertainment release of the year."),
    ("ART MARKET", "Van Gogh sells for a record $190.4m",
     "A Van Gogh fetches $190.4 million at auction, a record for the artist, "
     "after a row over its Nazi-era history."),
    ("SPACE", "Voyager 1 reaches one light-day",
     "NASA's Voyager 1, launched in 1977, is now a full light-day from Earth — "
     "its radio signals take 24 hours to arrive."),
]
for i, (k, h, b) in enumerate(boxes):
    bx = 36 + i * (BW + 12)
    d.rectangle([bx, BY, bx + BW, BY + BH], fill=BOX)
    d.rectangle([bx, BY, bx + BW, BY + 5], fill=RED)
    yy = kicker(bx + 14, BY + 14, k)
    yy = text_block(bx + 14, yy, h, F(SERIF_B, 23), max_w=BW - 28, leading=3)
    yy += 3
    text_block(bx + 14, yy, b, F(SANS_R, 17), max_w=BW - 28, leading=4)

# ---------- bottom briefs ----------
YY = BY + BH + 22
d.line([36, YY - 8, W - 36, YY - 8], fill=LINE, width=2)
briefs = [
    ("MARKETS JOLTED", "Copper plunges over 5% as tech jitters hit metals; gold sinks to a 14-month low."),
    ("CYCLONE AKVAN", "Severe cyclone Akvan closes on India's east coast; red warning for Andhra and Odisha."),
    ("US–VENEZUELA PACT", "Washington restores military ties with Venezuela; Hegseth signs a defence deal."),
    ("ALSO TODAY", "Crimean Bridge attacked again, Russia says. US tech outages put old infrastructure under scrutiny."),
]
CW = (W - 72 - 24) // 2
for i, (h, b) in enumerate(briefs):
    bx = 36 + (i % 2) * (CW + 24)
    by = YY + (i // 2) * 66
    d.text((bx, by), h, font=F(SANS_B, 18), fill=INK)
    text_block(bx, by + 26, b, F(SANS_R, 17), max_w=CW, leading=3)

# ---------- footer ----------
d.rectangle([36, H - 52, W - 36, H - 49], fill=INK)
d.text((W // 2, H - 40), "One image, one day: the stories moving Thursday 19 November 2026.",
       font=F(SERIF_I, 17), fill=GREY, anchor="ma")

img.save("/home/hatch/workspace/makefun/news19-entry/entry.png", optimize=True)
print("saved entry.png", img.size)
