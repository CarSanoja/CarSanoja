import math
import random
import sys
from PIL import Image, ImageDraw

W, H, S = 320, 122, 6
N = 60

C = {
    "wall": (28, 33, 62), "wall2": (34, 40, 74), "wallsh": (22, 26, 50),
    "floor": (18, 20, 38), "desk": (112, 74, 58), "desk2": (84, 54, 44), "deskhi": (146, 100, 78),
    "frame": (52, 60, 98), "frame2": (70, 80, 124), "screen": (12, 18, 30), "screen2": (16, 26, 42),
    "cyan": (94, 234, 212), "cyandim": (40, 110, 110), "amber": (255, 196, 92), "pink": (255, 92, 170),
    "white": (232, 236, 245), "grey": (120, 128, 160), "dark": (10, 12, 24),
    "board": (30, 64, 52), "boardfr": (120, 86, 60), "chalk": (214, 226, 214),
    "sky": (20, 30, 70), "sky2": (30, 44, 96), "moon": (250, 236, 190), "mount": (24, 52, 58), "mount2": (34, 70, 70),
    "rack": (40, 44, 70), "rack2": (56, 62, 96), "ledg": (110, 255, 140), "ledo": (255, 170, 60), "ledoff": (30, 40, 50),
    "hair": (30, 22, 20), "skin": (196, 136, 104), "skin2": (160, 104, 80), "shirt": (60, 92, 160), "shirt2": (46, 70, 126),
    "chair": (24, 26, 44), "chair2": (36, 38, 62), "plant": (70, 160, 90), "plant2": (44, 110, 64), "pot": (180, 96, 70),
    "mug": (220, 224, 236), "steam": (140, 150, 190), "metal": (150, 160, 190), "metal2": (100, 110, 140),
    "book1": (180, 70, 80), "book2": (70, 120, 190), "book3": (220, 180, 80), "book4": (110, 80, 160),
}
ARC = [(0, 0, 0), (0, 116, 217), (255, 65, 54), (46, 204, 64), (255, 220, 0), (170, 170, 170), (240, 18, 190), (255, 133, 27), (127, 219, 255), (135, 12, 37)]

FONT = {
    "0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"], "3": ["111", "001", "011", "001", "111"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "111"],
    ".": ["000", "000", "000", "000", "010"], ":": ["000", "010", "000", "010", "000"],
    "#": ["101", "111", "101", "111", "101"], " ": ["000", "000", "000", "000", "000"],
    "/": ["001", "001", "010", "100", "100"], "-": ["000", "000", "111", "000", "000"],
    ">": ["100", "010", "001", "010", "100"], "_": ["000", "000", "000", "000", "111"],
    "=": ["000", "111", "000", "111", "000"], "+": ["000", "010", "111", "010", "000"],
    "A": ["010", "101", "111", "101", "101"], "B": ["110", "101", "110", "101", "110"],
    "C": ["011", "100", "100", "100", "011"], "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"], "F": ["111", "100", "110", "100", "100"],
    "G": ["011", "100", "101", "101", "011"], "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"], "K": ["101", "101", "110", "101", "101"],
    "L": ["100", "100", "100", "100", "111"], "M": ["101", "111", "111", "101", "101"],
    "N": ["110", "101", "101", "101", "101"], "O": ["010", "101", "101", "101", "010"],
    "P": ["110", "101", "110", "100", "100"], "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"], "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "111"], "V": ["101", "101", "101", "101", "010"],
    "W": ["101", "101", "111", "111", "101"], "X": ["101", "101", "010", "101", "101"],
    "Y": ["101", "101", "010", "010", "010"], "Q": ["010", "101", "101", "011", "001"],
}


def text(d, x, y, s, col):
    for ch in s:
        g = FONT.get(ch, FONT[" "])
        for j, row in enumerate(g):
            for i, b in enumerate(row):
                if b == "1":
                    d.point((x + i, y + j), fill=col)
        x += 4
    return x


def rect(d, x0, y0, x1, y1, col):
    d.rectangle((x0, y0, x1, y1), fill=col)


def window(d, f):
    x0, y0, x1, y1 = 248, 8, 306, 58
    rect(d, x0 - 2, y0 - 2, x1 + 2, y1 + 2, C["frame"])
    rect(d, x0, y0, x1, y1, C["sky"])
    rect(d, x0, y0 + 26, x1, y1, C["sky2"])
    rng = random.Random(7)
    for k in range(18):
        sx, sy = rng.randint(x0 + 1, x1 - 1), rng.randint(y0 + 1, y0 + 28)
        on = (f + k * 7) % 23 not in (0, 1)
        d.point((sx, sy), fill=C["white"] if on else C["sky2"])
    rect(d, 290, 13, 295, 18, C["moon"])
    d.point((290, 13), fill=C["sky"])
    d.point((295, 18), fill=C["sky"])
    prof = [44, 42, 40, 37, 34, 31, 29, 27, 26, 25, 24, 24, 25, 26, 27, 26, 25, 24, 23, 23, 24, 25, 27, 28, 29, 31, 33, 34, 35, 36, 37, 38, 38, 39, 40, 40, 41, 42, 43, 43, 44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 48, 49, 49, 50, 50, 50, 50, 51, 51]
    for i, x in enumerate(range(x0, x1 + 1)):
        top = y0 + prof[i % len(prof)] - 8
        rect(d, x, top, x, y1, C["mount"])
        if i % 9 < 4:
            d.point((x, top), fill=C["mount2"])
    rng2 = random.Random(3)
    for k in range(22):
        lx, ly = rng2.randint(x0, x1), rng2.randint(y1 - 6, y1)
        if (f // 4 + k) % 5:
            d.point((lx, ly), fill=C["amber"])
    rect(d, (x0 + x1) // 2, y0, (x0 + x1) // 2, y1, C["frame"])
    rect(d, x0, (y0 + y1) // 2 - 6, x1, (y0 + y1) // 2 - 6, C["frame"])
    rect(d, x0 - 4, y1 + 3, x1 + 4, y1 + 4, C["frame2"])


def board(d, f):
    x0, y0, x1, y1 = 46, 10, 112, 46
    rect(d, x0 - 2, y0 - 2, x1 + 2, y1 + 2, C["boardfr"])
    rect(d, x0, y0, x1, y1, C["board"])
    text(d, x0 + 3, y0 + 3, "L = -LOG P", C["chalk"])
    text(d, x0 + 3, y0 + 11, "BITS/BYTE", C["chalk"])
    for i in range(24):
        x = x0 + 4 + i
        y = y0 + 30 - int(10 * math.exp(-i / 7))
        d.point((x, y), fill=C["chalk"])
    rect(d, x0 + 4, y0 + 20, x0 + 4, y0 + 31, C["chalk"])
    rect(d, x0 + 4, y0 + 31, x0 + 30, y0 + 31, C["chalk"])
    text(d, x0 + 36, y0 + 21, "UMA", C["amber"])
    text(d, x0 + 36, y0 + 28, "USB", C["amber"])
    rect(d, x0 + 8, y1 + 3, x0 + 12, y1 + 4, C["white"])


def neon(d, f):
    on = f % 29 not in (11, 13) and f not in (40,)
    col = C["pink"] if on else (90, 40, 70)
    x, y = 122, 12
    for gx, gy in [(1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 6), (2, 6), (3, 6)]:
        rect(d, x + gx * 2, y + gy * 2, x + gx * 2 + 1, y + gy * 2 + 1, col)
    x = 134
    for gx, gy in [(1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (0, 6), (1, 6), (2, 6)]:
        rect(d, x + gx * 2, y + gy * 2, x + gx * 2 + 1, y + gy * 2 + 1, col)


def shelf(d, f):
    rect(d, 166, 44, 236, 45, C["desk"])
    rect(d, 166, 46, 236, 46, C["desk2"])
    rect(d, 170, 47, 171, 50, C["desk2"])
    rect(d, 231, 47, 232, 50, C["desk2"])
    for i, col in enumerate([C["book1"], C["book2"], C["book3"], C["book4"], C["book2"]]):
        h = [12, 10, 13, 9, 11][i]
        rect(d, 168 + i * 3, 44 - h, 169 + i * 3, 43, col)
    bx, by = 194, 43
    rect(d, bx - 3, by - 1, bx + 3, by, C["metal2"])
    a1 = math.radians(-70 + 25 * math.sin(f * 2 * math.pi / N))
    a2 = a1 + math.radians(60 + 30 * math.sin(f * 4 * math.pi / N + 1))
    j1 = (bx + 9 * math.cos(a1), by - 2 + 9 * math.sin(a1))
    j2 = (j1[0] + 7 * math.cos(a2), j1[1] + 7 * math.sin(a2))
    d.line([(bx, by - 2), j1], fill=C["amber"], width=2)
    d.line([j1, j2], fill=C["amber"], width=2)
    d.point((round(j1[0]), round(j1[1])), fill=C["dark"])
    gx, gy = round(j2[0]), round(j2[1])
    d.point((gx - 1, gy + 1), fill=C["metal"])
    d.point((gx + 1, gy + 1), fill=C["metal"])
    dy = round(1.5 * math.sin(f * 2 * math.pi / 20))
    dx0, dyy = 218, 26 + dy
    rect(d, dx0 - 2, dyy, dx0 + 2, dyy + 2, C["metal2"])
    d.point((dx0, dyy + 1), fill=C["ledg"] if f % 6 < 3 else C["ledoff"])
    d.line([(dx0 - 6, dyy - 1), (dx0 - 2, dyy)], fill=C["metal2"])
    d.line([(dx0 + 2, dyy), (dx0 + 6, dyy - 1)], fill=C["metal2"])
    pc = C["white"] if f % 2 else C["grey"]
    for px in (dx0 - 6, dx0 + 6):
        if f % 2:
            rect(d, px - 2, dyy - 2, px + 2, dyy - 2, pc)
        else:
            rect(d, px - 1, dyy - 2, px + 1, dyy - 2, pc)


def rack(d, f):
    x0, y0, x1, y1 = 6, 36, 38, 121
    rect(d, x0, y0, x1, y1, C["rack"])
    rect(d, x0 + 1, y0 + 1, x1 - 1, y0 + 1, C["rack2"])
    text(d, x0 + 4, y0 + 4, "TRN2", C["cyan"])
    rng = random.Random(f // 2)
    for u in range(8):
        uy = y0 + 13 + u * 9
        rect(d, x0 + 2, uy, x1 - 2, uy + 6, C["rack2"])
        rect(d, x0 + 3, uy + 1, x1 - 3, uy + 5, C["dark"])
        for k in range(6):
            on = rng.random() < 0.6
            col = (C["ledg"] if k < 4 else C["ledo"]) if on else C["ledoff"]
            d.point((x0 + 5 + k * 2, uy + 3), fill=col)
        for k in range(4):
            d.point((x1 - 12 + k * 2, uy + 2), fill=C["grey"])
            d.point((x1 - 12 + k * 2, uy + 4), fill=C["grey"])
    rect(d, x1 + 1, y0 + 6, x1 + 2, y1, C["wallsh"])


def curve_val(t):
    e = (math.exp(-4.2 * t) - math.exp(-4.2)) / (1 - math.exp(-4.2))
    return 0.947 + (1.40 - 0.947) * e + 0.012 * math.sin(37 * t) * (1 - t) * math.exp(-2 * t)


def monitor(d, f):
    x0, y0, x1, y1 = 108, 50, 192, 92
    rect(d, x0 - 2, y0 - 2, x1 + 2, y1 + 2, C["frame"])
    rect(d, x0 - 2, y0 - 2, x1 + 2, y0 - 2, C["frame2"])
    rect(d, x0, y0, x1, y1, C["screen"])
    rect(d, x0, y0, x1, y0 + 6, C["screen2"])
    for k, col in enumerate([C["pink"], C["amber"], C["ledg"]]):
        d.point((x0 + 2 + k * 3, y0 + 3), fill=col)
    text(d, x0 + 14, y0 + 1, "TRAIN.PY D24", C["grey"])
    cx0, cy0, cx1, cy1 = x0 + 4, y0 + 10, x1 - 22, y1 - 6
    for gy in range(cy0, cy1 + 1, 6):
        for gx in range(cx0, cx1 + 1, 3):
            d.point((gx, gy), fill=(24, 34, 52))
    phase = f % N
    reveal = min(1.0, phase / 40)
    pts = []
    n = cx1 - cx0
    for i in range(n + 1):
        t = i / n
        if t > reveal:
            break
        v = curve_val(t)
        y = cy1 - (v - 0.92) / (1.42 - 0.92) * (cy1 - cy0)
        pts.append((cx0 + i, round(y)))
    if len(pts) > 1:
        d.line(pts, fill=C["cyan"], width=1)
        hx, hy = pts[-1]
        rect(d, hx - 1, hy - 1, hx + 1, hy + 1, C["white"] if phase % 2 == 0 else C["cyan"])
    v = curve_val(reveal)
    tx = x1 - 20
    text(d, tx, y0 + 10, "BPB", C["grey"])
    text(d, tx, y0 + 17, f"{v:.3f}", C["cyan"] if reveal < 1 else C["amber"])
    text(d, tx, y0 + 26, "LB", C["grey"])
    if reveal >= 1:
        if phase >= 52 or phase % 4 < 3:
            text(d, tx, y0 + 33, "3RD", C["amber"])
    else:
        text(d, tx, y0 + 33, "..", C["grey"])
    rect(d, (x0 + x1) // 2 - 4, y1 + 3, (x0 + x1) // 2 + 4, 95, C["frame"])


TARGET = [
    [0, 1, 1, 1, 0],
    [1, 4, 4, 4, 1],
    [1, 4, 2, 4, 1],
    [1, 4, 4, 4, 1],
    [0, 1, 1, 1, 0],
]


def monitor2(d, f):
    x0, y0, x1, y1 = 198, 60, 240, 92
    rect(d, x0 - 2, y0 - 2, x1 + 2, y1 + 2, C["frame"])
    rect(d, x0, y0, x1, y1, C["screen"])
    text(d, x0 + 2, y0 + 2, "ARC", C["grey"])
    gx0, gy0 = x0 + 2, y0 + 9
    for j in range(5):
        for i in range(5):
            v = TARGET[j][i]
            rect(d, gx0 + i * 4, gy0 + j * 4, gx0 + i * 4 + 2, gy0 + j * 4 + 2, ARC[5] if v else (40, 40, 48))
    d.point((gx0 + 21, gy0 + 9), fill=C["grey"])
    d.point((gx0 + 22, gy0 + 9), fill=C["grey"])
    d.point((gx0 + 23, gy0 + 8), fill=C["grey"])
    d.point((gx0 + 23, gy0 + 10), fill=C["grey"])
    ox = x0 + 28
    phase = f % N
    k = min(25, max(0, (phase - 8) // 1 if phase < 34 else 25))
    for idx in range(25):
        j, i = divmod(idx, 5)
        col = ARC[TARGET[j][i]] if idx < k else (24, 24, 30)
        if TARGET[j][i] == 0 and idx < k:
            col = (40, 40, 48)
        rect(d, ox + (i * 25) // 10, gy0 + j * 4, ox + (i * 25) // 10 + 1, gy0 + j * 4 + 2, col)
    if k == 25 and phase % 6 < 4:
        text(d, x0 + 26, y1 - 5, "OK", C["ledg"])
    rect(d, (x0 + x1) // 2 - 2, y1 + 3, (x0 + x1) // 2 + 2, 95, C["frame"])


def desk(d, f):
    rect(d, 40, 95, 316, 98, C["desk"])
    rect(d, 40, 95, 316, 95, C["deskhi"])
    rect(d, 40, 99, 316, 100, C["desk2"])
    rect(d, 46, 101, 49, H, C["desk2"])
    rect(d, 308, 101, 311, H, C["desk2"])
    rect(d, 252, 87, 258, 94, C["mug"])
    rect(d, 259, 89, 260, 92, C["mug"])
    d.point((259, 90), fill=C["wall"])
    rect(d, 253, 88, 257, 88, (110, 60, 40))
    for k in range(3):
        sy = 85 - ((f + k * 5) % 15) // 2
        sx = 254 + k * 2 + (1 if ((f + k) // 3) % 2 else 0)
        if sy > 76:
            d.point((sx, sy), fill=C["steam"])
    rect(d, 288, 86, 296, 94, C["pot"])
    rect(d, 287, 86, 297, 87, (200, 116, 88))
    sway = 1 if (f // 10) % 2 else 0
    for lx, ly, col in [(292, 78, C["plant"]), (289, 81, C["plant2"]), (295, 80, C["plant"]), (291, 74, C["plant2"]), (294, 76, C["plant"])]:
        rect(d, lx + sway, ly, lx + 1 + sway, ly + 6, col)
    rect(d, 269, 82, 277, 82, C["amber"])
    rect(d, 270, 83, 276, 86, C["amber"])
    rect(d, 267, 83, 268, 83, C["amber"])
    rect(d, 278, 83, 279, 83, C["amber"])
    d.point((267, 84), fill=C["amber"])
    d.point((279, 84), fill=C["amber"])
    d.point((268, 85), fill=C["amber"])
    d.point((278, 85), fill=C["amber"])
    rect(d, 271, 87, 275, 87, C["amber"])
    rect(d, 272, 88, 274, 88, C["amber"])
    rect(d, 273, 89, 273, 90, C["amber"])
    rect(d, 270, 91, 276, 94, C["desk2"])
    rect(d, 271, 92, 275, 93, C["deskhi"])
    text(d, 272, 83, "3", C["desk2"])
    rect(d, 120, 93, 176, 94, C["metal2"])
    rect(d, 120, 93, 176, 93, C["metal"])


def person(d, f):
    cx = 150
    rect(d, cx - 13, 92, cx + 13, H, C["chair"])
    rect(d, cx - 13, 92, cx + 13, 93, C["chair2"])
    rect(d, cx - 10, 86, cx + 10, H, C["shirt"])
    rect(d, cx - 10, 86, cx + 10, 87, C["shirt2"])
    rect(d, cx - 2, 84, cx + 2, 86, C["skin2"])
    rect(d, cx - 6, 72, cx + 6, 84, C["hair"])
    rect(d, cx - 7, 74, cx + 7, 82, C["hair"])
    rect(d, cx - 8, 78, cx - 7, 81, C["skin"])
    rect(d, cx + 7, 78, cx + 8, 81, C["skin"])
    for hx in [(cx - 4, 72), (cx + 1, 71), (cx + 4, 72), (cx - 1, 71)]:
        d.point(hx, fill=C["hair"])
    tl = (f // 2) % 2
    tr = 1 - tl
    rect(d, cx - 13, 87, cx - 10, 93, C["shirt2"])
    rect(d, cx + 10, 87, cx + 13, 93, C["shirt2"])
    rect(d, cx - 15, 90, cx - 13, 93, C["shirt2"])
    rect(d, cx + 13, 90, cx + 15, 93, C["shirt2"])
    rect(d, cx - 17, 91 - tl, cx - 15, 92 - tl, C["skin"])
    rect(d, cx + 15, 91 - tr, cx + 17, 92 - tr, C["skin"])


def frame(f):
    im = Image.new("RGB", (W, H), C["wall"])
    d = ImageDraw.Draw(im)
    for y in range(0, 96, 8):
        rect(d, 0, y, W, y, C["wall2"])
    window(d, f)
    board(d, f)
    neon(d, f)
    shelf(d, f)
    rect(d, 0, 96, W, H, C["floor"])
    rack(d, f)
    desk(d, f)
    monitor(d, f)
    monitor2(d, f)
    person(d, f)
    return im.resize((W * S, H * S), Image.NEAREST)


if __name__ == "__main__":
    out = sys.argv[1]
    frames = [frame(f) for f in range(N)]
    cols = sorted({c for fr in frames for _, c in fr.resize((W, H), Image.NEAREST).getcolors(4096)})
    pal = Image.new("P", (1, 1))
    flat = [v for c in cols for v in c]
    pal.putpalette(flat + [0] * (768 - len(flat)))
    q = [fr.quantize(palette=pal, dither=Image.Dither.NONE) for fr in frames]
    durations = [90] * N
    durations[N - 1] = 1400
    for i in range(40, N - 1):
        durations[i] = 140
    q[0].save(out, save_all=True, append_images=q[1:], duration=durations, loop=0, optimize=True, disposal=1)
    frames[N - 1].save(out.replace(".gif", "_last.png"))
    frames[20].save(out.replace(".gif", "_mid.png"))
