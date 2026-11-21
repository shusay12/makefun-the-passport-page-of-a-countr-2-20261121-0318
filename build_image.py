#!/usr/bin/env python3
"""Build entry.png: an open passport spread for the invented Republic of
Talveria. Drawn programmatically with Pillow; the portrait is a generated
photo (portrait.png) cropped to passport size.

Travel history (all dates agree; passport issued 02 JUN 2026 in Miren):
  02 JUN 2026  passport issued, Miren (valid to 02 JUN 2036)
  12 JUN 2026  Ostavia visa issued in Miren, valid 18 JUN - 17 JUL 2026
  18 JUN 2026  depart Talveria (Miren Airport) / arrive Ostavia (Kalden)
  25 JUN 2026  depart Ostavia (Kalden)
  26 JUN 2026  arrive Belmar (Velgrad)
  09 JUL 2026  depart Belmar (Velgrad) / arrive Talveria (Miren)
Telling paperwork detail: the Ostavia visa condition
"NO EMPLOYMENT - TOURIST ONLY" plus the fee stamp "FEE PAID - 40 TALER",
and bilingual (Talverian / English) field labels on the data page.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024

# ---- fonts ---------------------------------------------------------------
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---- colours ---------------------------------------------------------------
INK = (32, 32, 34)
MUTED = (110, 104, 92)
PAGE = (246, 241, 228)
PAGE_EDGE = (214, 205, 188)
NAVY = (24, 48, 96)
GOLD = (150, 118, 52)
BLUE_INK = (28, 62, 140)
PURPLE_INK = (112, 42, 108)
RED_INK = (158, 32, 32)
GREEN_INK = (28, 104, 62)


# ---- MRZ (ICAO 9303 TD3, check digits 7-3-1) ------------------------------
def check_digit(s):
    vals = {c: i for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
    total = 0
    for i, ch in enumerate(s):
        v = 0 if ch == "<" else vals[ch]
        total += v * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<TALVELDEN<<MARA<ILSA"
    line1 = line1 + "<" * (44 - len(line1))
    doc = "TV4829167"
    dob = "980314"   # 14 MAR 1998
    exp = "360602"   # 02 JUN 2036
    personal = "<" * 14
    line2 = (
        doc + check_digit(doc)
        + "TAL" + dob + check_digit(dob)
        + "F" + exp + check_digit(exp)
        + personal + check_digit(personal)
    )
    composite_src = line2[:10] + line2[13:20] + line2[21:28] + line2[28:43]
    line2 = line2 + check_digit(composite_src)
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2


# ---- helpers ---------------------------------------------------------------
def text_c(draw, cx, y, s, f, fill=INK):
    draw.text((cx - draw.textlength(s, font=f) / 2, y), s, font=f, fill=fill)


def text_l(draw, x, y, s, f, fill=INK):
    draw.text((x, y), s, font=f, fill=fill)


def guilloche(draw, x0, y0, x1, y1, step=26, alpha=14):
    """Faint diagonal security lines across a page."""
    layer = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w, h = x1 - x0, y1 - y0
    for k in range(-h, w + h, step):
        d.line([(k, 0), (k + h, h)], fill=(120, 100, 60, alpha), width=1)
    return layer


def coat_of_arms(draw, cx, cy, r, colour=NAVY):
    """Simple emblem: ring, three mountain peaks, a star above."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=3)
    draw.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5],
                 outline=colour, width=1)
    # mountains
    base = cy + r * 0.45
    draw.polygon([(cx - r * 0.62, base), (cx - r * 0.18, cy - r * 0.25),
                  (cx + r * 0.12, base)], fill=colour)
    draw.polygon([(cx - r * 0.28, base), (cx + r * 0.12, cy - r * 0.45),
                  (cx + r * 0.62, base)], fill=colour)
    # star
    sx, sy, sr = cx, cy - r * 0.62, r * 0.16
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = sr if i % 2 == 0 else sr * 0.45
        pts.append((sx + rr * math.cos(ang), sy + rr * math.sin(ang)))
    draw.polygon(pts, fill=GOLD)


def stamp(base, cx, cy, w, h, lines, colour, angle, fonts):
    """One ink entry/exit stamp, drawn on its own layer and rotated."""
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = 20, 20, 20 + w, 20 + h
    d.rounded_rectangle([x0, y0, x1, y1], radius=8,
                        outline=colour + (255,), width=3)
    d.rounded_rectangle([x0 + 5, y0 + 5, x1 - 5, y1 - 5], radius=5,
                        outline=colour + (200,), width=1)
    total = sum(f.getbbox(t)[3] + 4 for t, f in lines)
    y = y0 + (h - total) / 2 + 2
    for t, f in lines:
        text_c(d, x0 + w / 2, y, t, f, fill=colour + (235,))
        y += f.getbbox(t)[3] + 4
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    base.alpha_composite(layer, (int(cx - w / 2 - 20), int(cy - h / 2 - 20)))


# ---- build -----------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), (38, 33, 28))
    d = ImageDraw.Draw(img, "RGBA")
    # desk: soft vertical gradient + vignette
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)],
               fill=(int(52 - 22 * t), int(46 - 20 * t), int(40 - 18 * t)))
    # page shadows
    for (x0, y0, x1, y1) in [(36, 130, 506, 870), (518, 130, 988, 870)]:
        d.rectangle([x0 + 6, y0 + 8, x1 + 6, y1 + 8], fill=(0, 0, 0, 160))

    pages = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pages)

    # ---- page bodies ------------------------------------------------------
    for (x0, y0, x1, y1) in [(36, 130, 506, 870), (518, 130, 988, 870)]:
        pd.rectangle([x0, y0, x1, y1], fill=PAGE + (255,),
                     outline=PAGE_EDGE + (255,), width=2)
        g = guilloche(pd, x0 + 2, y0 + 2, x1 - 2, y1 - 2)
        pages.alpha_composite(g, (x0 + 2, y0 + 2))
    # centre gutter shadow
    pd.rectangle([504, 130, 520, 870], fill=(0, 0, 0, 60))

    # ================= LEFT PAGE: data page ===============================
    lx, ly, lw = 36, 130, 470
    cx = lx + lw // 2

    coat_of_arms(pd, cx, ly + 46, 27)
    text_c(pd, cx, ly + 82, "REPUBLIC OF TALVERIA", font(SERIF_B, 22))
    text_c(pd, cx, ly + 110, "REPUBLIKA TALVERIJA  ·  PASSPORT — PUTOVNICA",
           font(SANS, 11), fill=MUTED)
    pd.line([(lx + 26, ly + 134), (lx + lw - 26, ly + 134)],
            fill=NAVY + (255,), width=2)

    # portrait
    portrait = Image.open(HERE / "portrait.png").convert("RGB")
    crop = portrait.crop((450, 60, 1150, 970)).resize((148, 192),
                                                     Image.LANCZOS)
    px, py = lx + 26, ly + 152
    pd.rectangle([px - 2, py - 2, px + 150, py + 194],
                 outline=NAVY + (255,), width=2)
    pages.paste(crop, (px, py))
    # signature under portrait
    text_c(pd, px + 74, py + 204, "Mara Ilsa Velden", font(SERIF_I, 17))
    pd.line([(px, py + 228), (px + 148, py + 228)], fill=INK + (255,), width=1)
    text_c(pd, px + 74, py + 234, "HOLDER'S SIGNATURE / POTPIS",
           font(SANS, 9), fill=MUTED)

    # data fields, right of portrait
    fx = lx + 198
    fields = [
        ("SURNAME / PREZIME", "VELDEN"),
        ("GIVEN NAMES / IMENA", "MARA ILSA"),
        ("NATIONALITY / DRŽAVLJANSTVO", "TALVERIAN"),
        ("DATE OF BIRTH / DATUM ROĐENJA", "14 MAR 1998"),
        ("PLACE OF BIRTH / MJESTO ROĐENJA", "MIREN"),
        ("SEX / SPOL", "F"),
    ]
    y = ly + 152
    for label, value in fields:
        text_l(pd, fx, y, label, font(SANS, 10), fill=MUTED)
        text_l(pd, fx, y + 13, value, font(SANS_B, 16))
        y += 36

    pd.line([(lx + 26, ly + 400), (lx + lw - 26, ly + 400)],
            fill=PAGE_EDGE + (255,), width=1)

    # lower block: two columns
    y0 = ly + 416
    col2 = lx + 252
    left_rows = [
        ("DATE OF ISSUE / DATUM IZDAVANJA", "02 JUN 2026"),
        ("DATE OF EXPIRY / DATUM ISTEKA", "02 JUN 2036"),
        ("AUTHORITY / TIJELO", "MINISTRY OF THE INTERIOR"),
        ("", "MIREN"),
    ]
    right_rows = [
        ("PLACE OF ISSUE / MJESTO", "MIREN"),
        ("PASSPORT No. / BROJ", "TV 4829167"),
        ("TYPE / VRSTA", "P"),
        ("CODE / KOD", "TAL"),
    ]
    for rows, x in ((left_rows, lx + 26), (right_rows, col2)):
        y = y0
        for label, value in rows:
            if label:
                text_l(pd, x, y, label, font(SANS, 10), fill=MUTED)
            text_l(pd, x, y + 13, value, font(SANS_B, 15))
            y += 36

    text_c(pd, cx, ly + 566,
           "The holder is a citizen of the Republic of Talveria.",
           font(SERIF_I, 12), fill=MUTED)
    text_c(pd, cx, ly + 586, "THIS PASSPORT CONTAINS 32 PAGES",
           font(SANS, 9), fill=MUTED)

    # MRZ
    l1, l2 = mrz_lines()
    pd.line([(lx + 26, ly + 616), (lx + lw - 26, ly + 616)],
            fill=NAVY + (255,), width=1)
    mrz = font(MONO, 15)
    text_l(pd, lx + 26, ly + 626, l1, mrz)
    text_l(pd, lx + 26, ly + 648, l2, mrz)

    # ================= RIGHT PAGE: visas & stamps =========================
    rx, ry, rw = 518, 130, 470
    rcx = rx + rw // 2
    text_c(pd, rcx, ry + 24, "VISAS", font(SERIF_B, 19))
    text_c(pd, rcx, ry + 50, "VIZE  ·  ENDORSEMENTS", font(SANS, 10),
           fill=MUTED)
    pd.line([(rx + 26, ry + 72), (rx + rw - 26, ry + 72)],
            fill=NAVY + (255,), width=2)

    # --- Ostavia visa sticker ---------------------------------------------
    vx0, vy0, vx1, vy1 = rx + 24, ry + 88, rx + rw - 24, ry + 308
    pd.rounded_rectangle([vx0, vy0, vx1, vy1], radius=6,
                         fill=(223, 232, 242, 255),
                         outline=NAVY + (255,), width=2)
    pd.rectangle([vx0, vy0, vx1, vy0 + 30], fill=NAVY + (255,))
    text_c(pd, (vx0 + vx1) // 2, vy0 + 7, "VISA  ·  REPUBLIC OF OSTAVIA",
           font(SANS_B, 14), fill=(255, 255, 255))
    vfields = [
        ("Type / Vrsta", "C — TOURIST"),
        ("Entries / Ulazaka", "SINGLE"),
        ("Valid from / Od", "18 JUN 2026"),
        ("Valid until / Do", "17 JUL 2026"),
        ("Duration of stay", "30 DAYS"),
        ("Issued at / Izdano u", "MIREN, 12 JUN 2026"),
        ("Visa No.", "OSV-771204"),
    ]
    y = vy0 + 42
    for label, value in vfields:
        text_l(pd, vx0 + 14, y, label, font(SANS, 11), fill=MUTED)
        text_l(pd, vx0 + 168, y, value, font(SANS_B, 12))
        y += 19
    text_c(pd, (vx0 + vx1) // 2, vy0 + 176,
           "CONDITION: NO EMPLOYMENT — TOURIST ONLY",
           font(SANS_B, 12), fill=RED_INK)
    # fee stamp: small red-bordered box at the sticker's bottom right
    fee = "FEE PAID · 40 TALER"
    fw = pd.textlength(fee, font=font(SANS_B, 11))
    fx0, fy0 = vx1 - 16 - int(fw) - 16, vy0 + 198
    pd.rectangle([fx0, fy0, fx0 + int(fw) + 16, fy0 + 18],
                 outline=RED_INK + (255,), width=2)
    text_l(pd, fx0 + 8, fy0 + 3, fee, font(SANS_B, 11), fill=RED_INK)

    # --- border stamps ------------------------------------------------------
    f_big = font(SANS_B, 13)
    f_mid = font(SANS_B, 12)
    f_small = font(SANS, 9)
    stamps = [
        ("DEPARTURE", "TALVERIA — MIREN AIRPORT", "18 JUN 2026",
         BLUE_INK, -4),
        ("ARRIVAL", "OSTAVIA — PORT OF KALDEN", "18 JUN 2026",
         BLUE_INK, 3),
        ("DEPARTURE", "OSTAVIA — KALDEN", "25 JUN 2026",
         PURPLE_INK, 5),
        ("ARRIVAL", "BELMAR — VELGRAD", "26 JUN 2026",
         GREEN_INK, -3),
        ("DEPARTURE", "BELMAR — VELGRAD", "09 JUL 2026",
         PURPLE_INK, 4),
        ("ARRIVAL", "TALVERIA — MIREN", "09 JUL 2026",
         RED_INK, -5),
    ]
    sx0, sy0 = rx + 26, ry + 330
    sw, sh, gap = 200, 108, 18
    for i, (kind, place, date, colour, angle) in enumerate(stamps):
        col, row = i % 2, i // 2
        cxp = sx0 + col * (sw + gap) + sw // 2
        cyp = sy0 + row * (sh + gap) + sh // 2
        stamp(pages, cxp, cyp, sw, sh,
              [(kind, f_big), (place, f_mid), (date, f_mid),
               ("BORDER CONTROL", f_small)],
              colour, angle, None)

    text_c(pd, rcx, ry + 700, "— 12 —", font(SANS, 10), fill=MUTED)

    img.paste(pages, (0, 0), pages)
    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
