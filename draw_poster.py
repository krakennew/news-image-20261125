#!/usr/bin/env python3
"""Draw 'The World Today - 25 November 2026' front page, 1024x1024.

47 verified stories: lead on Putin's retaliation vow + Lukashenko's
Moscow flight offer, a world map with markers, and a 45-story grid.
Run: python3 draw_poster.py  -> writes entry.png beside this file.
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
MUTED = (74, 74, 74)
NAVY = (20, 38, 74)
RED = (179, 35, 27)
SEA = (220, 235, 245)
LAND = (203, 190, 162)
LAND_LINE = (138, 127, 102)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = font("DejaVuSerif-Bold.ttf", 40)
F_SERIF_SMALL = font("DejaVuSerif-Bold.ttf", 31)
F_BOLD_13 = font("DejaVuSans-Bold.ttf", 13)
F_BOLD_12 = font("DejaVuSans-Bold.ttf", 12)
F_BOLD_11 = font("DejaVuSans-Bold.ttf", 11)
F_BOLD_10 = font("DejaVuSans-Bold.ttf", 10)
F_REG_13 = font("DejaVuSans.ttf", 13)
F_REG_11 = font("DejaVuSans.ttf", 11)
F_REG_10 = font("DejaVuSans.ttf", 10)
F_NUM = font("DejaVuSans-Bold.ttf", 9)
F_NUM_S = font("DejaVuSans-Bold.ttf", 8)

SECTION_COLORS = {
    "WAR": (179, 35, 27),
    "CLIMATE": (30, 107, 58),
    "DISASTER": (107, 58, 30),
    "MARKETS": (122, 77, 0),
    "ASIA": (91, 45, 142),
    "RIGHTS": (142, 42, 91),
    "WORLD": (51, 51, 51),
    "SPORT": (29, 78, 137),
}

# (number, section, headline, summary) -- grid cells, stories 3..47
STORIES = [
    (3, "WAR", "RUSSIAN STRIKE KILLS 2 IN ODESA",
     "Drone strike kills two in Odesa; Kyiv flats hit, two hurt in night attacks."),
    (4, "WAR", "720,000 RUSSIAN SOLDIERS DEAD",
     "Leaked Rosstat data: 720,000 dead since 2022 - one every four minutes."),
    (5, "WAR", "MEDVEDEV WARNS OF NUCLEAR STRIKE",
     "Ex-president says a 'preventive nuclear attack' is now possible."),
    (6, "WAR", "RUSSIA RAGES AT ESTONIA",
     "Moscow calls border closure 'on the verge of open war'; envoy summoned."),
    (7, "WAR", "ESTONIA TO SHUT RUSSIA BORDER",
     "Crossings close 1 Dec for six months over an alleged arson plot."),
    (8, "WAR", "RUSSIAN MISSILES LAND IN POLAND",
     "Three Kh-101 cruise missiles crash; NATO sends AWACS jets."),
    (9, "WAR", "RUSSIAN DRONE VIOLATES POLISH AIRSPACE",
     "Drone strays during a night attack on Ukraine; Poland scrambles."),
    (10, "WAR", "POLAND FOILS 'FALSE FLAG' PLOT",
     "Security services stop alleged Russian provocation near Kaliningrad."),
    (11, "WAR", "HOUTHIS HIT RIYADH TOWER AGAIN",
     "Drone strike on PIF HQ wounds 11; second hit on the tower in a week."),
    (12, "WAR", "IRAN: 3 TANKERS HIT MINES",
     "Ships catch fire in Hormuz despite US escort; Tehran sets 7 talk terms."),
    (13, "WAR", "GAZA TOLL 74,746",
     "Nine killed in overnight strikes; toll passes 74,700 in three-year war."),
    (14, "WAR", "SUDAN DRONES KILL 4 IN KHARTOUM",
     "Strikes hit homes and a UN building; US demands an arms embargo."),
    (15, "WAR", "UKRAINE CUTS REFINING 30%",
     "Strikes slash Russian output; Novoshakhtinsk refinery still burning."),
    (16, "WAR", "MOSSAD CHIEF PUSHED US TO HIT IRAN",
     "Spy chief lobbied Washington despite his analysts' objections."),
    (17, "CLIMATE", "COP31 COLLAPSES IN ANTALYA",
     "No climate pact after two weeks; first breakdown since 2009."),
    (18, "CLIMATE", "COP32 SET FOR ADDIS ABABA",
     "Next summit runs 8-19 November 2027 in Ethiopia after Antalya failure."),
    (19, "CLIMATE", "90+ NATIONS BACK CLEAN-POWER PLEDGE",
     "Electrification pledge survives; Guterres 'deeply disappointed'."),
    (20, "CLIMATE", "US ARMY TO DETONATE TOXIC LEAD",
     "Army to blast 68 barrels of toxic lead explosive in Iowa this week."),
    (21, "DISASTER", "INDONESIA FACTORY FIRE TOLL 26",
     "Blaze rips through a candy factory in Cikande; dozens still missing."),
    (22, "DISASTER", "NIGERIA FUNERAL BOAT SINKS, 24 DEAD",
     "Overloaded boat capsizes in Bayelsa; 24 rescued after mechanical fault."),
    (23, "MARKETS", "NVIDIA SLIPS 6% AFTER +31% DAY",
     "Comeback rally fades as investors weigh governance and political risk."),
    (24, "MARKETS", "NVIDIA SOARS 31% IN A DAY",
     "Shares add about $952bn in value - the best day since 2003."),
    (25, "MARKETS", "S&P +4.8%, NASDAQ +6.5%",
     "Global tech rally follows Nvidia's comeback; Dow up 1,448 points."),
    (26, "MARKETS", "MICROSOFT DECLARES 'CODE RED'",
     "After worst outage in its history; one-hour fix target set."),
    (27, "MARKETS", "HUAWEI FOUND GUILTY IN US TRIAL",
     "Jury convicts on trade-secret conspiracy and bank fraud."),
    (28, "MARKETS", "TRUMP EYES NEW TARIFFS",
     "Duties on 16 trading partners after Supreme Court setback."),
    (29, "ASIA", "INDIA GIVES NEPAL $1.62BN",
     "Flood-rebuild package agreed as Modi hosts Nepal's PM Balendra Shah."),
    (30, "ASIA", "NEW AYODHYA-JANAKPUR TRAIN RUNS",
     "Saryu-Kamala Express flagged off; eight India-Nepal deals signed."),
    (31, "ASIA", "LOWER ARUN DAM WORK BEGINS",
     "Foundation laid for 669 MW hydro project in Nepal."),
    (32, "ASIA", "MYANMAR JUNTA SLAMS ASEAN",
     "Army-backed government calls summit decision 'unfair and imbalanced'."),
    (33, "RIGHTS", "IRAN FLOGS SINGER 74 LASHES",
     "Parastoo Ahmadi punished over a 2024 concert without hijab."),
    (34, "RIGHTS", "LISBON MARCHES OVER LIVING COSTS",
     "Tens of thousands in 30+ cities protest housing prices."),
    (35, "RIGHTS", "DENMARK BACKS \"GHETTO LAW\" EVICTIONS",
     "Top court says ending 91 leases in Helsingor is not discrimination."),
    (36, "WORLD", "SARKOZY ORDERED TO TRIAL",
     "Ex-president and wife Carla Bruni face trial; hearing 1 Apr 2027."),
    (37, "WORLD", "TRUMP PARDONS TURKEYS",
     "Freedom and Feathers spared; Feathers hides in the bushes."),
    (38, "WORLD", "GIULIANI GETS MEDAL OF FREEDOM",
     "Trump honours ex-mayor in private Oval Office ceremony."),
    (39, "WORLD", "TURKISH MP QUITS AMID PROBE",
     "AK Party founder Yazici resigns as fund probe widens to his son."),
    (40, "WORLD", "TURKISH HELICOPTER CRASH KILLS 5",
     "Military chopper down in western Turkiye; five aboard killed."),
    (41, "SPORT", "ENGLAND CRUSH AUSTRALIA IN T20",
     "Donald 85 off 32, Salt 58; England chase 185 in 13.1 overs."),
    (42, "SPORT", "GUKESH DRAWS CHESS OPENER",
     "World title defence starts with 38-move draw vs Sindarov in Geneva."),
    (43, "SPORT", "ALCARAZ WINS FIRST ATP FINALS",
     "Spaniard beats Zverev in Turin; joins Federer, Agassi, Djokovic."),
    (44, "SPORT", "VERSTAPPEN WINS LAS VEGAS GP",
     "75th career win after 35 lead changes; Norris second, Piastri third."),
    (45, "SPORT", "INDIA-NZ TEST ENDS IN DRAW",
     "India declare 720/9 with Pant's 128; NZ hold on at 239/5."),
    (46, "SPORT", "2031 WOMEN'S WORLD CUP HOSTS",
     "USA, Mexico, Costa Rica and Jamaica to stage first 48-team edition."),
    (47, "SPORT", "2035 WOMEN'S WORLD CUP TO UK",
     "England, Northern Ireland, Scotland and Wales to host."),
]

# (story number, label, lat, lon, badge dx, badge dy) for the map.
MARKERS = [
    (1, "1", 55.7, 37.6, 10, -12),
    (3, "3", 46.5, 30.7, -12, 10),
    (4, "", 60.0, 100.0, 0, 0),
    (6, "6", 58.5, 25.5, 20, 12),
    (8, "8", 52.0, 19.0, -20, -8),
    (11, "11", 24.7, 46.7, 10, -10),
    (12, "12", 26.5, 56.2, 12, 10),
    (13, "13", 31.5, 34.5, -20, 12),
    (14, "14", 15.6, 32.5, -16, -12),
    (17, "17", 36.9, 30.7, 10, 14),
    (21, "21", -6.3, 106.3, 10, -10),
    (23, "23", 37.4, -122.0, -12, -10),
    (26, "", 47.6, -122.1, 0, 0),
    (29, "29", 28.6, 77.2, 10, 10),
    (34, "34", 38.7, -9.1, -12, -10),
    (36, "36", 48.9, 2.3, -14, 12),
    (41, "41", -28.0, 153.4, -12, -10),
    (42, "", 46.2, 6.1, 0, 0),
]

# Rough continent outlines in (lon, lat)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 62),
     (-80, 45), (-75, 35), (-80, 25), (-90, 20), (-97, 16), (-105, 20),
     (-115, 30), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-168, 66)],
    [(-58, 64), (-45, 60), (-30, 68), (-40, 76), (-58, 76), (-58, 64)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-50, -30), (-60, -35), (-70, -50), (-75, -40), (-75, -20),
     (-80, -5), (-80, 10)],
    [(-10, 36), (-10, 43), (-5, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (25, 66), (20, 70),
     (15, 70), (5, 60), (-5, 58), (-10, 50), (-10, 36)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 12), (44, 0), (40, -10), (35, -20), (32, -28),
     (25, -35), (18, -35), (15, -25), (12, -10), (8, 4), (-8, 5), (-17, 15)],
    [(30, 62), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (150, 45),
     (140, 40), (130, 35), (127, 35), (120, 30), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (80, 20), (75, 10), (70, 20), (60, 25),
     (55, 27), (50, 29), (45, 30), (40, 35), (35, 36), (30, 36), (30, 62)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (147, -39),
     (150, -37), (153, -27), (150, -22), (146, -19), (142, -11), (136, -12),
     (132, -11), (126, -14), (122, -17), (113, -22)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 53), (1, 51),
     (-3, 50), (-5, 50)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (143, 43), (145, 44), (143, 42), (141, 39), (139, 36),
     (136, 34), (133, 34), (131, 32), (130, 31)],
]


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_header(d):
    d.rectangle([0, 0, W, 72], fill=NAVY)
    d.text((20, 12), "THE WORLD TODAY", font=F_SERIF, fill=(246, 241, 231))
    d.text((W - 20, 10), "WEDNESDAY", font=F_BOLD_13, fill=(246, 241, 231),
           anchor="ra")
    d.text((W - 20, 28), "25 NOVEMBER 2026", font=F_BOLD_13,
           fill=(255, 205, 80), anchor="ra")
    d.text((W - 20, 48), "47 STORIES", font=F_BOLD_11, fill=(246, 241, 231),
           anchor="ra")
    d.rectangle([0, 72, W, 76], fill=RED)
    d.text((20, 82), "ONE DAY  ·  ONE IMAGE  ·  EVERY STORY VERIFIED",
           font=F_BOLD_11, fill=MUTED)
    d.text((W - 20, 82), "make.fun  ·  $100", font=F_BOLD_11, fill=MUTED,
           anchor="ra")


def draw_lead(d):
    d.text((20, 100), "PUTIN: RETALIATION IS INEVITABLE",
           font=F_BOLD_13, fill=RED)
    head = "PUTIN VOWS REVENGE\nFOR REFINERY STRIKES"
    d.multiline_text((20, 120), head, font=F_SERIF_SMALL, fill=INK,
                     spacing=2)
    summary = ("Putin vows to hit back at Ukraine's refinery strikes, citing "
               "Trump's plea to stop - as Lukashenko offers to fly Zelensky "
               "to Moscow, and Zelensky tells him to bring Putin to Kyiv.")
    lines = wrap(d, summary, F_REG_13, 600)
    d.multiline_text((20, 196), "\n".join(lines), font=F_REG_13, fill=INK,
                     spacing=3)
    # illustration: burning refinery at night, missile trail overhead
    x0, y0, x1, y1 = 640, 100, 1004, 252
    d.rectangle([x0, y0, x1, y1], fill=(16, 32, 64))
    for yy in range(y0 + 26, y1, 14):
        d.line([(x0, yy), (x1, yy)], fill=(28, 52, 96), width=2)
    # refinery towers and tanks, silhouetted
    d.rectangle([668, 168, 700, 236], fill=(40, 44, 52))
    d.rectangle([712, 150, 748, 236], fill=(48, 52, 62))
    d.rectangle([760, 178, 812, 236], fill=(40, 44, 52))
    d.rectangle([824, 158, 858, 236], fill=(48, 52, 62))
    d.polygon([(700, 168), (712, 150), (712, 168)], fill=(40, 44, 52))
    d.polygon([(858, 158), (872, 158), (872, 236), (858, 236)],
              fill=(48, 52, 62))
    # lit windows on the towers so the refinery reads against the night sky
    for wx in (676, 688, 722, 734, 772, 788, 804, 834, 848):
        for wy in (196, 212, 226):
            d.rectangle([wx, wy, wx + 3, wy + 3], fill=(255, 205, 80))
    # flames licking from two towers
    for cx, cy, r in ((730, 146, 16), (730, 132, 10), (841, 154, 14),
                      (841, 142, 9), (690, 164, 11)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 170, 40))
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                  fill=(255, 220, 120))
    # smoke rising
    for sx, sy, sr in ((742, 116, 9), (756, 104, 11), (770, 94, 8),
                       (852, 122, 9), (864, 110, 10)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 110, 110))
    # missile trail arcing across the sky
    d.line([(660, 118), (760, 106), (860, 112), (960, 128)],
           fill=(255, 205, 80), width=2)
    d.ellipse([956, 122, 970, 136], fill=(255, 205, 80))
    d.text((x0 + 10, y1 - 22), "REFINERIES BURN AS MOSCOW THREATENS",
           font=F_BOLD_10, fill=(255, 205, 80))


def draw_map(d):
    d.text((20, 262), "WHERE IT HAPPENED", font=F_BOLD_12, fill=INK)
    mx0, my0, mw, mh = 20, 278, 984, 100
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=SEA,
                outline=(180, 190, 200))
    lat_top, lat_bot = 78.0, -58.0

    def proj(lon, lat):
        x = mx0 + (lon + 180.0) / 360.0 * mw
        y = my0 + (lat_top - lat) / (lat_top - lat_bot) * mh
        return x, y

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for _num, label, lat, lon, dx, dy in MARKERS:
        x, y = proj(lon, lat)
        d.ellipse([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=RED)
        if not label:
            continue
        bx, by = x + dx, y + dy
        d.line([(x, y), (bx, by)], fill=RED, width=1)
        r = 8 if len(label) > 2 else 7
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((bx, by), label, font=F_NUM_S, fill=(255, 255, 255),
               anchor="mm")


def draw_grid(d):
    y0 = 382
    row_h = 40
    col_x = [20, 352, 684]
    col_w = 320
    for i, (num, section, headline, summary) in enumerate(STORIES):
        row, col = divmod(i, 3)
        x = col_x[col]
        y = y0 + row * row_h
        color = SECTION_COLORS[section]
        d.rectangle([x, y + 2, x + 3, y + 38], fill=color)
        tx = x + 10
        num_txt = f"{num}."
        d.text((tx, y), num_txt, font=F_BOLD_12, fill=RED)
        nw = d.textlength(num_txt, font=F_BOLD_12)
        d.text((tx + nw + 4, y), headline, font=F_BOLD_12, fill=INK)
        lines = wrap(d, summary, F_REG_11, col_w - 10)[:2]
        d.multiline_text((tx, y + 16), "\n".join(lines), font=F_REG_11,
                         fill=MUTED, spacing=1)


def draw_footer(d):
    d.line([(20, 990), (W - 20, 990)], fill=(150, 140, 120), width=1)
    d.text((20, 996),
           "Sources: Reuters - CNN - AP - The Guardian - WRI - Xinhua - OCHA. "
           "Every story verified against two or more independent reports.",
           font=F_REG_10, fill=MUTED)
    lx = 20
    for section in ("WAR", "CLIMATE", "DISASTER", "MARKETS", "ASIA",
                    "RIGHTS", "WORLD", "SPORT"):
        d.text((lx, 1012), section, font=F_BOLD_10,
               fill=SECTION_COLORS[section])
        lx += d.textlength(section, font=F_BOLD_10) + 10
    d.text((W - 20, 1012), "Built by an AI agent for make.fun",
           font=F_REG_10, fill=MUTED, anchor="ra")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_lead(d)
    draw_map(d)
    draw_grid(d)
    draw_footer(d)
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
