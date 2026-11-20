"""Render entry.png — a one-image newspaper front page for Thursday
19 November 2026, drawn entirely with Pillow primitives. This is the
full-day edition: it carries the day's later developments, including the
Shenzhen summit declaration, the World Court verdict on Myanmar, and
the second wave of mine strikes in the Strait of Hormuz.

The submitted entry point (main.py) never runs this file; it ships the
finished PNG. This script is kept in the repository so the artwork can be
reproduced and audited: `python3 generate_image.py` redraws the same page.
"""
import math

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PALETTE = {
    "paper": (248, 245, 238),
    "ink": (18, 18, 18),
    "accent": (168, 0, 27),
    "muted": (92, 88, 80),
    "panel": (238, 233, 221),
    "rule": (30, 30, 30),
    "water": (196, 208, 214),
    "fire": (224, 110, 20),
    "ash": (120, 116, 108),
    "white": (255, 255, 255),
}
FONT_DIR = "/usr/share/fonts/truetype/liberation"
TYPEFACES = {
    "headline": FONT_DIR + "/LiberationSerif-Bold.ttf",
    "italic": FONT_DIR + "/LiberationSerif-Italic.ttf",
    "bold": FONT_DIR + "/LiberationSans-Bold.ttf",
    "body": FONT_DIR + "/LiberationSans-Regular.ttf",
}

canvas = Image.new("RGB", (PAGE, PAGE), PALETTE["paper"])
pen = ImageDraw.Draw(canvas)


def face(kind, size):
    return ImageFont.truetype(TYPEFACES[kind], size)


def wrapped_lines(text, font, width):
    """Greedy word wrap: extend the current line while it still fits."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if pen.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(x, y, text, kind, size, width, colour="ink", gap=5):
    font = face(kind, size)
    for line in wrapped_lines(text, font, width):
        pen.text((x, y), line, font=font, fill=PALETTE[colour])
        y += size + gap
    return y


def section_label(x, y, text):
    pen.text((x, y), text, font=face("bold", 19), fill=PALETTE["accent"])
    return y + 27


def star_points(cx, cy, outer, inner):
    pts = []
    for step in range(10):
        angle = -math.pi / 2 + step * math.pi / 5
        radius = outer if step % 2 == 0 else inner
        pts.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return pts


def masthead():
    pen.rectangle([0, 0, PAGE, 10], fill=PALETTE["ink"])
    pen.text((PAGE // 2, 30), "THE WORLD TODAY", font=face("headline", 66),
             fill=PALETTE["ink"], anchor="ma")
    pen.text((PAGE // 2, 112),
             "THURSDAY  ·  19 NOVEMBER 2026  ·  THE DAY IN ONE IMAGE",
             font=face("bold", 21), fill=PALETTE["muted"], anchor="ma")
    pen.rectangle([36, 148, PAGE - 36, 151], fill=PALETTE["ink"])
    pen.rectangle([36, 155, PAGE - 36, 156], fill=PALETTE["ink"])


def flag_panel(x, y, width, colours, label, emblem=None):
    height = 56
    band = height // len(colours)
    for i, colour in enumerate(colours):
        pen.rectangle([x, y + i * band, x + width, y + (i + 1) * band], fill=colour)
    if emblem == "stars-and-stripes":
        pen.rectangle([x, y, x + width // 2, y + band * 2], fill=(38, 54, 120))
    if emblem == "lone-star":
        pen.polygon(star_points(x + 28, y + 16, 13, 5.2), fill=(255, 222, 0))
    pen.text((x + width // 2, y + height + 10), label, font=face("bold", 17),
             fill=PALETTE["ink"], anchor="ma")


def lead_story():
    x, w = 36, 612
    y = section_label(x, 172, "APEC SUMMIT  ·  SHENZHEN, CHINA")
    y = paragraph(x, y, "Trump, Xi and Putin end summit with nuclear pledge",
                  "headline", 41, w, gap=4) + 6
    box_h = 150
    pen.rectangle([x, y, x + w, y + box_h], fill=PALETTE["white"],
                  outline=PALETTE["rule"], width=2)
    flag_w = (w - 64) // 3
    specs = [
        ([(178, 34, 52), (255, 255, 255), (178, 34, 52)], "USA", "stripes"),
        ([(222, 41, 16)], "CHINA", "lone-star"),
        ([(255, 255, 255), (38, 74, 160), (200, 30, 40)], "RUSSIA", None),
    ]
    for i, (colours, label, emblem) in enumerate(specs):
        fx = x + 16 + i * (flag_w + 8)
        fy = y + 18
        if emblem == "stripes":
            for s in range(5):
                top = fy + s * 11
                pen.rectangle([fx, top, fx + flag_w, top + 11],
                              fill=(178, 34, 52) if s % 2 == 0 else (255, 255, 255))
            pen.rectangle([fx, fy, fx + flag_w // 2, fy + 28], fill=(38, 54, 120))
        elif emblem == "lone-star":
            pen.rectangle([fx, fy, fx + flag_w, fy + 56], fill=colours[0])
            pen.polygon(star_points(fx + 28, fy + 16, 13, 5.2), fill=(255, 222, 0))
        else:
            third = 56 // 3
            for j, colour in enumerate(colours):
                pen.rectangle([fx, fy + j * third, fx + flag_w, fy + (j + 1) * third],
                              fill=colour)
        pen.text((fx + flag_w // 2, fy + 66), label, font=face("bold", 17),
                 fill=PALETTE["ink"], anchor="ma")
    pen.rectangle([x + 16, y + 116, x + w - 16, y + 124], fill=PALETTE["ink"])
    pen.text((x + w // 2, y + 128), "FIRST TRILATERAL SUMMIT  ·  APEC",
             font=face("bold", 15), fill=PALETTE["muted"], anchor="ma")
    y += box_h + 12
    pen.text((x, y), "JOINT DECLARATION: UN REFORM, MORE OIL, NUCLEAR TALKS",
             font=face("bold", 16), fill=PALETTE["accent"])
    y += 30
    paragraph(x, y,
              "After a 90-minute meeting, the three leaders issued a joint "
              "declaration vowing talks to cut nuclear risks — 'a nuclear "
              "war cannot be won and must never be fought' — plus UN reform "
              "and more oil supply.",
              "body", 20, w, gap=5)


def side_column():
    x, w = 684, 304
    y = section_label(x, 172, "STRAIT OF HORMUZ  ·  ESCALATION")
    y = paragraph(x, y, "Two more supertankers hit mines in Hormuz",
                  "headline", 27, w, gap=3) + 4
    pen.rectangle([x, y, x + w, y + 62], fill=PALETTE["white"],
                  outline=PALETTE["rule"], width=2)
    hull_y = y + 62
    pen.polygon([x + 30, hull_y - 18, x + 250, hull_y - 18,
                 x + 232, hull_y - 4, x + 48, hull_y - 4], fill=PALETTE["ink"])
    pen.rectangle([x + 120, hull_y - 30, x + 170, hull_y - 18], fill=PALETTE["ink"])
    for fx in (x + 84, x + 140, x + 196):
        pen.polygon([fx, hull_y - 20, fx + 9, hull_y - 40, fx + 18, hull_y - 20],
                    fill=PALETTE["fire"])
        pen.ellipse([fx + 2, hull_y - 56, fx + 20, hull_y - 38], fill=PALETTE["ash"])
    pen.line([x + 6, hull_y - 2, x + w - 6, hull_y - 2], fill=PALETTE["water"], width=3)
    y += 70
    y = paragraph(x, y,
                  "Two more supertankers carrying 4 million barrels of crude "
                  "hit mines and exploded, Iran says — the fifth vessels "
                  "struck in a day.",
                  "body", 18, w, gap=4) + 10
    pen.line([x, y, x + w, y], fill=PALETTE["rule"], width=2)
    y += 12
    y = section_label(x, y, "WORLD COURT  ·  THE HAGUE")
    y = paragraph(x, y, "Court finds Myanmar guilty of genocide",
                  "headline", 25, w, gap=3) + 4
    paragraph(x, y,
              "The World Court finds Myanmar guilty of genocide and orders "
              "compensation — the first time it has held a state responsible.",
              "body", 18, w, gap=4)


def story_boxes():
    top, height = 634, 170
    width = (PAGE - 72 - 24) // 3
    stories = [
        ("GAMING", "GTA VI scores 99 and breaks launch records",
         "GTA VI scores 99 on Metacritic and sells an estimated 24.6m "
         "copies worth $2.36bn on day one — a record launch."),
        ("ART MARKET", "Van Gogh sells for a record $190.4m",
         "A Van Gogh fetches $190.4 million at auction, a record for the "
         "artist, after a row over its Nazi-era history. Buyer: Bill "
         "Acquavella."),
        ("SPACE", "Voyager 1 reaches one light-day",
         "NASA confirms Voyager 1, launched in 1977, crossed one light-day "
         "from Earth — 16.1 billion miles out, its signals now take 24 "
         "hours to arrive."),
    ]
    for i, (label, headline, body) in enumerate(stories):
        bx = 36 + i * (width + 12)
        pen.rectangle([bx, top, bx + width, top + height], fill=PALETTE["panel"])
        pen.rectangle([bx, top, bx + width, top + 5], fill=PALETTE["accent"])
        by = section_label(bx + 14, top + 14, label)
        by = paragraph(bx + 14, by, headline, "headline", 23, width - 28, gap=3) + 3
        paragraph(bx + 14, by, body, "body", 17, width - 28, gap=4)


def briefs():
    top = 634 + 170 + 22
    pen.line([36, top - 8, PAGE - 36, top - 8], fill=PALETTE["rule"], width=2)
    items = [
        ("MARKETS JOLTED",
         "Copper steadies after a 5.7% plunge; gold holds near a 14-month "
         "low as a December Fed hike is priced in."),
        ("CYCLONE AKVAN",
         "Cyclone Akvan nears India's east coast, with landfall due Friday "
         "near Gopalpur; over 120,000 people evacuated."),
        ("US–VENEZUELA PACT",
         "Hegseth calls Venezuela a 'compliant security partner' as "
         "Washington restores military ties; full terms undisclosed."),
        ("ALSO TODAY",
         "Crimean Bridge hit a third time in a week, halting trains; Trump "
         "plays down US tech outages."),
    ]
    width = (PAGE - 72 - 24) // 2
    for i, (headline, body) in enumerate(items):
        bx = 36 + (i % 2) * (width + 24)
        by = top + (i // 2) * 66
        pen.text((bx, by), headline, font=face("bold", 18), fill=PALETTE["ink"])
        paragraph(bx, by + 26, body, "body", 17, width, gap=3)


def footer():
    pen.rectangle([36, PAGE - 52, PAGE - 36, PAGE - 49], fill=PALETTE["ink"])
    pen.text((PAGE // 2, PAGE - 40),
             "One image, one day: the stories moving Thursday 19 November 2026.",
             font=face("italic", 17), fill=PALETTE["muted"], anchor="ma")


masthead()
lead_story()
side_column()
story_boxes()
briefs()
footer()

canvas.save("/home/hatch/workspace/makefun/news19-entry/entry.png", optimize=True)
print("saved entry.png", canvas.size)
