"""Poster renderer for the 25 November 2026 world-news image.

Builds a single 1024x1024 PNG from a fixed story list. Everything is
hard-coded and deterministic: same input bytes, same output bytes, no
network access and no clock reads anywhere in the rendering path.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024

NAVY = (13, 27, 62)
SLATE = (38, 52, 74)
DEEP = (18, 30, 56)
PAPER = (250, 248, 242)
AMBER = (232, 150, 33)
CRIMSON = (198, 47, 38)
BODY = (28, 28, 30)
FADED = (110, 110, 118)
RULE = (214, 210, 200)
LAND = (72, 100, 140)
SEA = (16, 42, 74)
FLAME = (244, 130, 32)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

LEAD_KICKER = "LEAD STORY"
LEAD_HEAD = "Putin vows payback as Ukraine's sea war goes global"
LEAD_DECK = (
    "Moscow calls retaliation inevitable after Kyiv's drones sank a "
    "warship off Libya and hit a cargo vessel in the Gulf of Finland. "
    "Lukashenko offers to fly Zelensky to Moscow; Zelensky says bring "
    "Putin to Kyiv instead."
)

SPOTLIGHT_TAG = "ALSO TODAY"
SPOTLIGHT_HEAD = "Grand Theft Auto VI launches worldwide for PS5 and Xbox"
SPOTLIGHT_BODY = (
    "Rockstar's long-awaited sequel arrived on 19 November, drawing "
    "record crowds across the games industry."
)

CELL_STORIES = [
    "Kyiv confirms drone hit on Russian cargo ship in Gulf of Finland",
    "Sea drones sank the corvette Merkury off Benghazi, Libya",
    "Leaked Russian records point to 720,000 soldiers killed",
    "Medvedev floats a \"preventive nuclear attack\" in a journal",
    "Moscow tells Estonia it is \"on the verge of open war\"",
    "Russian strike on flats near Kyiv kills at least 11 people",
    "Kyiv and Moscow trade accusations at the UN over shipping",
    "NATO to station early-warning aircraft in Poland",
    "EU rolls out another round of sanctions against Russia",
    "US envoy Kushner hints at NATO-style guarantees for Kyiv",
    "Zelenskyy to turn to Congress if Trump cannot force a deal",
    "Houthis hit Riyadh's tallest tower again; 11 people wounded",
    "Iran's Guards say three tankers struck mines in Hormuz",
    "Houthis now 60 km from Aden, but army says city will hold",
    "Gaza death toll reaches 74,746, health officials report",
    "Oxfam: pollution now threatens more than 99% of Gaza",
    "UN warns Gaza's humanitarian crisis keeps getting worse",
    "WFP: 266 million people now face acute food insecurity",
    "US envoy \"not certain\" Israel military aid ends this year",
    "Iran rations electricity as war damage deepens energy crisis",
    "US and Qatar hold strategic talks on regional security",
    "COP31 ends with no deal \u2014 first climate collapse since 2009",
    "Focus shifts to COP32 in Addis Ababa after Antalya failure",
    "Trump pardons turkeys Freedom and Feathers for Thanksgiving",
    "Giuliani receives the Presidential Medal of Freedom",
    "Fort Hood gunman Hasan asks court to halt his execution",
    "CIA and spy chief's office hit by cyber breach, sources say",
    "US Army to blast toxic lead explosive in Iowa despite court",
    "US prepares new tariffs on trading partners worldwide",
    "Microsoft declares \"Code Red\" after its worst outage ever",
    "Nvidia slides 6% as Huang comeback rally loses steam",
    "Huawei convicted on 10 of 12 counts in US criminal trial",
    "Dell raises outlook after record quarter for AI servers",
    "Anthropic shares briefly dip below their IPO price",
    "Sarkozy and Carla Bruni ordered to stand trial in Paris",
    "Sarkozy appeal verdict due on 30 November in Libya case",
    "UK asks the public about changing the age of consent",
    "UK to open inquiry into nuclear test veterans' health",
    "Indonesia factory fire toll hits 26 as search goes on",
    "England crush Australia by 8 wickets to level T20 series",
    "Gukesh and Sindarov draw the world title opener in Geneva",
    "BJP and Akali Dal reunite ahead of 2027 Punjab elections",
    "Nepal PM Shah makes first state visit to India",
    "RFE/RL returns to shortwave radio for Afghan girls",
    "Radar fault delays flights at Chicago's O'Hare airport",
]

TALLY = [
    ("720,000", "Russian soldiers killed, leaked records suggest"),
    ("74,746", "deaths reported in Gaza since October 2023"),
    ("26", "killed in the Indonesia candy factory fire"),
    ("11", "wounded in the Riyadh tower strike"),
]

# (label, latitude, longitude) for the globe strip.
PINS = [
    ("Kyiv", 50.45, 30.52),
    ("Benghazi", 32.12, 20.07),
    ("Gulf of Finland", 60.0, 27.0),
    ("Moscow", 55.75, 37.62),
    ("Tallinn", 59.44, 24.75),
    ("Riyadh", 24.71, 46.68),
    ("Hormuz", 26.5, 56.5),
    ("Gaza", 31.5, 34.47),
    ("Antalya", 36.9, 30.7),
    ("Paris", 48.85, 2.35),
    ("Jakarta", -6.2, 106.8),
    ("Washington", 38.9, -77.04),
    ("Brooklyn", 40.7, -73.99),
    ("Geneva", 46.2, 6.14),
    ("Gold Coast", -28.0, 153.4),
]

# Rough continent outlines as (longitude, latitude) pairs.
NORTH_AMERICA = [
    (-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68),
    (-105, 68), (-95, 69), (-88, 68), (-82, 66), (-80, 73),
    (-75, 62), (-68, 58), (-65, 60), (-60, 52), (-55, 47),
    (-60, 45), (-70, 42), (-75, 35), (-80, 32), (-81, 26),
    (-85, 30), (-90, 29), (-97, 26), (-105, 22), (-110, 24),
    (-115, 30), (-122, 37), (-124, 48), (-130, 55), (-140, 60),
    (-152, 58), (-162, 58), (-168, 66),
]
GREENLAND = [
    (-55, 60), (-45, 60), (-40, 64), (-32, 68), (-22, 70),
    (-30, 74), (-45, 76), (-58, 74), (-58, 68), (-55, 60),
]
SOUTH_AMERICA = [
    (-79, 9), (-72, 12), (-64, 10), (-58, 6), (-52, 4), (-50, 0),
    (-44, -3), (-37, -6), (-35, -9), (-39, -15), (-41, -23),
    (-48, -28), (-55, -35), (-62, -41), (-66, -47), (-69, -52),
    (-71, -54), (-73, -48), (-73, -38), (-72, -28), (-70, -20),
    (-76, -14), (-80, -5), (-81, 1), (-79, 9),
]
EUROPE = [
    (-10, 36), (-9, 43), (-2, 44), (-2, 48), (-4, 48), (-1, 50),
    (2, 51), (5, 53), (8, 55), (8, 57), (10, 59), (13, 56),
    (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (28, 65),
    (24, 68), (20, 70), (16, 69), (12, 67), (6, 62), (5, 58),
    (0, 57), (-4, 58), (-8, 55), (-10, 52), (-10, 48), (-10, 36),
]
AFRICA = [
    (-6, 35), (-10, 31), (-16, 27), (-17, 21), (-17, 15), (-15, 11),
    (-12, 8), (-8, 5), (-3, 5), (3, 6), (7, 4), (9, 4), (9, 0),
    (12, -5), (13, -10), (12, -17), (14, -22), (16, -28), (19, -34),
    (25, -34), (31, -29), (34, -26), (38, -18), (40, -12), (41, -6),
    (44, -1), (48, 2), (51, 5), (51, 11), (47, 11), (44, 11),
    (41, 13), (39, 16), (38, 20), (36, 24), (35, 28), (34, 31),
    (32, 31), (30, 32), (26, 33), (22, 33), (18, 33), (14, 32),
    (11, 34), (10, 37), (-6, 35),
]
ASIA = [
    (28, 36), (36, 36), (36, 33), (40, 32), (43, 38), (44, 42),
    (40, 45), (34, 45), (30, 46), (28, 44), (24, 40), (23, 37),
    (27, 39), (30, 42), (36, 42), (42, 41), (46, 39), (50, 37),
    (54, 37), (54, 40), (58, 39), (60, 41), (57, 45), (53, 47),
    (50, 50), (52, 55), (56, 60), (60, 64), (65, 68), (70, 72),
    (78, 73), (86, 74), (95, 76), (105, 76), (113, 74), (122, 73),
    (132, 72), (142, 72), (152, 70), (160, 66), (162, 60),
    (158, 55), (155, 51), (150, 59), (143, 59), (141, 52),
    (138, 45), (135, 42), (130, 38), (127, 35), (127, 40),
    (130, 43), (133, 47), (136, 51), (140, 55), (143, 59),
    (147, 60), (152, 59), (156, 52), (160, 56), (163, 60),
    (170, 66), (178, 65), (178, 62), (170, 60), (162, 58),
    (156, 52), (150, 59), (143, 59), (140, 50), (137, 44),
    (133, 40), (130, 37), (127, 35), (124, 38), (121, 37),
    (119, 32), (116, 27), (112, 22), (109, 17), (107, 11),
    (104, 8), (101, 7), (99, 10), (97, 15), (94, 18), (91, 22),
    (88, 22), (85, 19), (82, 16), (80, 12), (77, 8), (75, 12),
    (73, 18), (70, 21), (67, 24), (64, 25), (61, 25), (58, 26),
    (55, 27), (52, 27), (50, 29), (48, 30), (46, 29), (43, 30),
    (40, 31), (37, 32), (35, 34), (32, 35), (28, 36),
]
AUSTRALIA = [
    (113, -22), (114, -30), (115, -34), (118, -35), (124, -33),
    (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
    (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
    (146, -19), (142, -15), (142, -11), (140, -17), (136, -15),
    (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
    (118, -20), (114, -22), (113, -22),
]
LANDMASSES = [
    NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EUROPE, AFRICA, ASIA,
    AUSTRALIA,
]

# Fixed star positions inside the lead illustration (no randomness).
STARS = [
    (18, 14), (52, 30), (88, 10), (120, 26), (150, 8), (186, 22),
    (214, 12), (248, 28), (282, 10), (312, 24), (336, 14), (66, 44),
    (140, 48), (230, 46), (300, 44), (36, 58), (168, 60), (262, 58),
]


def grab_font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


def wrap_caption(draw, text, font, max_w):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_masthead(draw):
    draw.rectangle([0, 0, CANVAS_W, 76], fill=NAVY)
    draw.rectangle([0, 72, CANVAS_W, 76], fill=AMBER)
    title_font = grab_font(True, 46)
    draw.text((16, 12), "THE WORLD TODAY", font=title_font, fill=(255, 255, 255))
    date_font = grab_font(True, 20)
    draw.text((700, 14), "25 NOVEMBER 2026", font=date_font, fill=AMBER)
    sub_font = grab_font(False, 13)
    draw.text((700, 42), "47 STORIES  \u00b7  ONE IMAGE", font=sub_font,
              fill=(220, 222, 230))


def paint_illustration(draw, x0, y0, x1, y1):
    """Night sea scene: refinery silhouette, flames, drone, ship."""
    w = x1 - x0
    h = y1 - y0
    horizon = y0 + int(h * 0.62)
    # Sky bands, dark to less dark.
    for i in range(horizon - y0):
        shade = 10 + int(18 * i / max(1, horizon - y0))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=(shade, shade + 8, shade + 30))
    for sx, sy in STARS:
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                     fill=(235, 235, 240))
    # Sea.
    draw.rectangle([x0, horizon, x1, y1], fill=(14, 44, 70))
    for gy in range(horizon + 8, y1, 14):
        draw.line([(x0 + 12, gy), (x1 - 12, gy)], fill=(28, 66, 96))
    # Refinery silhouette on the left of the panel.
    base = horizon
    draw.rectangle([x0 + 18, base - 52, x0 + 150, base], fill=(8, 12, 22))
    draw.rectangle([x0 + 34, base - 84, x0 + 46, base - 52], fill=(8, 12, 22))
    draw.rectangle([x0 + 62, base - 96, x0 + 74, base - 52], fill=(8, 12, 22))
    draw.rectangle([x0 + 96, base - 72, x0 + 108, base - 52], fill=(8, 12, 22))
    draw.rectangle([x0 + 118, base - 60, x0 + 138, base - 52], fill=(8, 12, 22))
    # Flame tongues above the three stacks, each rooted on its own top.
    for fx, ftop, fh in ((40, 84, 30), (68, 96, 38), (102, 72, 24)):
        draw.polygon([
            (x0 + fx - 9, base - ftop),
            (x0 + fx, base - ftop - fh),
            (x0 + fx + 9, base - ftop),
        ], fill=FLAME)
    # Glow wash over the water.
    draw.ellipse([x0 + 30, base - 6, x0 + 150, base + 26], fill=(120, 60, 16))
    draw.ellipse([x0 + 46, base - 2, x0 + 134, base + 18], fill=(190, 90, 20))
    # Ship hull on the right, low in the water.
    draw.polygon([
        (x0 + 190, base + 2), (x0 + 320, base + 2),
        (x0 + 300, base + 22), (x0 + 210, base + 22),
    ], fill=(6, 10, 18))
    draw.rectangle([x0 + 228, base - 14, x0 + 282, base + 2], fill=(6, 10, 18))
    draw.polygon([
        (x0 + 244, base - 14), (x0 + 252, base - 34), (x0 + 260, base - 14),
    ], fill=FLAME)
    # Drone above the ship: small body, four rotor arms, one red light.
    dx, dy = x0 + 268, y0 + 46
    draw.ellipse([dx - 7, dy - 5, dx + 7, dy + 5], fill=(20, 22, 30))
    draw.line([(dx - 22, dy - 8), (dx + 22, dy - 8)], fill=(200, 200, 210))
    draw.line([(dx - 22, dy + 8), (dx + 22, dy + 8)], fill=(200, 200, 210))
    draw.ellipse([dx - 26, dy - 11, dx - 18, dy - 5], fill=(160, 160, 170))
    draw.ellipse([dx + 18, dy - 11, dx + 26, dy - 5], fill=(160, 160, 170))
    draw.ellipse([dx - 26, dy + 5, dx - 18, dy + 11], fill=(160, 160, 170))
    draw.ellipse([dx + 18, dy + 5, dx + 26, dy + 11], fill=(160, 160, 170))
    draw.ellipse([dx - 2, dy + 8, dx + 2, dy + 12], fill=(255, 60, 50))


def paint_lead(draw):
    draw.rectangle([0, 76, CANVAS_W, 300], fill=PAPER)
    kicker_font = grab_font(True, 13)
    draw.text((16, 90), LEAD_KICKER, font=kicker_font, fill=CRIMSON)
    head_font = grab_font(True, 30)
    head_lines = wrap_caption(draw, LEAD_HEAD, head_font, 610)
    hy = 112
    for line in head_lines:
        draw.text((16, hy), line, font=head_font, fill=NAVY)
        hy += 36
    deck_font = grab_font(False, 15)
    deck_lines = wrap_caption(draw, LEAD_DECK, deck_font, 610)
    dy = hy + 6
    for line in deck_lines:
        draw.text((16, dy), line, font=deck_font, fill=(52, 52, 58))
        dy += 20
    tag_font = grab_font(True, 12)
    draw.text((16, 272), "UKRAINE  \u00b7  RUSSIA  \u00b7  BLACK SEA",
              font=tag_font, fill=FADED)
    paint_illustration(draw, 656, 76, 1008, 300)


def project(lon, lat):
    mx = 16 + (lon + 170) * 684 / 360.0
    my = 306 + (75 - lat) * 108 / 130.0
    return int(mx), int(my)


def paint_globe(draw):
    draw.rectangle([0, 300, 700, 448], fill=DEEP)
    for shape in LANDMASSES:
        pts = [project(lon, lat) for lon, lat in shape]
        draw.polygon(pts, fill=LAND)
    label_font = grab_font(True, 11)
    draw.text((16, 304), "WHERE IT HAPPENED", font=label_font, fill=AMBER)
    dot_font = grab_font(True, 9)
    drawn = []
    for idx, (name, lat, lon) in enumerate(PINS, start=1):
        px, py = project(lon, lat)
        ox, oy = px, py
        for _ in range(3):
            clash = any(
                abs(px - qx) < 14 and abs(py - qy) < 14 for qx, qy in drawn
            )
            if not clash:
                break
            px, py = px + 13, py - 11
        if (px, py) != (ox, oy):
            draw.line([(ox, oy), (px, py)], fill=(200, 208, 220))
        drawn.append((px, py))
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=AMBER)
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], outline=(255, 255, 255))
        draw.text((px - 3, py - 5), str(idx), font=dot_font, fill=NAVY)
    legend_font = grab_font(False, 10)
    legend = "  \u00b7  ".join(
        "%d %s" % (i, name) for i, (name, _lat, _lon) in enumerate(PINS, start=1)
    )
    leg_lines = wrap_caption(draw, legend, legend_font, 668)
    ly = 416
    for line in leg_lines[:2]:
        draw.text((16, ly), line, font=legend_font, fill=(200, 208, 220))
        ly += 13


def paint_spotlight(draw):
    draw.rectangle([716, 300, 1008, 448], fill=(238, 232, 218))
    draw.rectangle([716, 300, 1008, 304], fill=AMBER)
    tag_font = grab_font(True, 12)
    draw.text((732, 314), SPOTLIGHT_TAG, font=tag_font, fill=CRIMSON)
    head_font = grab_font(True, 19)
    head_lines = wrap_caption(draw, SPOTLIGHT_HEAD, head_font, 260)
    hy = 338
    for line in head_lines:
        draw.text((732, hy), line, font=head_font, fill=NAVY)
        hy += 23
    body_font = grab_font(False, 13)
    body_lines = wrap_caption(draw, SPOTLIGHT_BODY, body_font, 260)
    by = hy + 4
    for line in body_lines:
        draw.text((732, by), line, font=body_font, fill=(52, 52, 58))
        by += 17


def paint_cells(draw):
    draw.rectangle([0, 448, CANVAS_W, 898], fill=PAPER)
    grid_x0, grid_y0 = 16, 448
    col_w = 322
    gap = 13
    row_h = 30
    num_font = grab_font(True, 13)
    cell_font = grab_font(False, 12)
    for pos, story in enumerate(CELL_STORIES):
        row, col = divmod(pos, 3)
        cx = grid_x0 + col * (col_w + gap)
        cy = grid_y0 + row * row_h
        draw.text((cx, cy + 2), "%02d" % (pos + 1), font=num_font, fill=AMBER)
        text_lines = wrap_caption(draw, story, cell_font, col_w - 30)
        ly = cy + 2
        for line in text_lines[:2]:
            draw.text((cx + 30, ly), line, font=cell_font, fill=BODY)
            ly += 14
        if row < 14:
            draw.line([(cx, cy + row_h - 1), (cx + col_w, cy + row_h - 1)],
                      fill=RULE)
    for col in (1, 2):
        vx = grid_x0 + col * (col_w + gap) - 7
        draw.line([(vx, grid_y0 + 4), (vx, grid_y0 + 14 * row_h)],
                  fill=RULE)


def paint_numbers(draw):
    draw.rectangle([0, 898, CANVAS_W, 958], fill=SLATE)
    col_w = CANVAS_W // 4
    big_font = grab_font(True, 24)
    small_font = grab_font(False, 11)
    for i, (figure, caption) in enumerate(TALLY):
        cx = i * col_w + 16
        draw.text((cx, 906), figure, font=big_font, fill=AMBER)
        cap_lines = wrap_caption(draw, caption, small_font, col_w - 32)
        ly = 934
        for line in cap_lines[:1]:
            draw.text((cx, ly), line, font=small_font, fill=(225, 228, 235))
            ly += 13


def paint_footer(draw):
    draw.rectangle([0, 958, CANVAS_W, CANVAS_H], fill=PAPER)
    draw.rectangle([0, 958, CANVAS_W, 961], fill=AMBER)
    foot_font = grab_font(False, 11)
    draw.text(
        (16, 972),
        "Sources: Reuters, AP, CNN, RFE/RL, The Independent, BBC, DOJ, Xinhua",
        font=foot_font, fill=FADED,
    )
    draw.text(
        (16, 990),
        "47 verified stories  \u00b7  Rendered 25 November 2026  \u00b7  Deterministic build, no network",
        font=foot_font, fill=FADED,
    )


def render(out_path):
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    pen = ImageDraw.Draw(canvas)
    paint_masthead(pen)
    paint_lead(pen)
    paint_globe(pen)
    paint_spotlight(pen)
    paint_cells(pen)
    paint_numbers(pen)
    paint_footer(pen)
    canvas.save(out_path, format="PNG")
    return out_path


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(target)
    sys.stderr.write("rendered %s (%d stories)\n"
                     % (target, 2 + len(CELL_STORIES)))
