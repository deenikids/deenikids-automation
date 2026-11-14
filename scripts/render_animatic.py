"""Render a 2D ANIMATIC (timing/layout test video) from storyboard.json + the mixed audio.

This is the Phase 2 renderer: it proves the timing, scenes, subtitles, Shorts cuts and
upload pipeline work. In Phase 3 the same storyboard drives Blender for the 3D version;
this file is kept as a fast preview / fallback renderer.

Usage:
  python scripts/render_animatic.py bismillah-before-we-begin --lang en
  python scripts/render_animatic.py bismillah-before-we-begin --lang hi --short chorus
"""
import argparse
import bisect
import math
import os
import subprocess
import sys
from multiprocessing import Pool

from PIL import Image, ImageDraw, ImageFont

from characters2d import DRAW, OUT
from common import (bar_seconds, load_settings, load_song, load_storyboard, note_events,
                    out_dir, path, song_length_sec)

SS = 2  # draw at 2x then shrink = smooth (anti-aliased) edges
G = {}  # per-process render context


# ----------------------------------------------------------------------------- helpers
def lerp(a, b, f):
    return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))


def ease_out_back(f):
    f = max(0.0, min(1.0, f))
    c = 1.70158
    return 1 + (c + 1) * (f - 1) ** 3 + c * (f - 1) ** 2


def ease_out_cubic(f):
    f = max(0.0, min(1.0, f))
    return 1 - (1 - f) ** 3


def font(size, arabic=False):
    key = (int(size), arabic)
    cache = G.setdefault("fonts", {})
    if key not in cache:
        if arabic:
            f = ImageFont.truetype(path("assets", "fonts", "NotoNaskhArabic.ttf"), int(size), layout_engine=ImageFont.Layout.RAQM)
            try:
                f.set_variation_by_axes([700])
            except Exception:
                pass
        else:
            f = ImageFont.truetype(path("assets", "fonts", "Baloo2.ttf"), int(size))
            try:
                f.set_variation_by_axes([800])
            except Exception:
                pass
        cache[key] = f
    return cache[key]


def text(d, xy, s, size, fill, stroke=None, arabic=False, anchor="mm"):
    size = round(size / 2) * 2  # even sizes only -> fewer cached fonts during pop-in animations
    if size < 8:  # too small to see (start of a pop-in) - nothing to draw
        return
    sw = max(2, int(size * 0.09)) if stroke else 0
    kw = {"direction": "rtl", "language": "ar"} if arabic else {}
    d.text(xy, s, font=font(size, arabic), fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor, **kw)


def gradient(d, W, H, top, bottom, y0=0, y1=None):
    y1 = H if y1 is None else y1
    for y in range(int(y0), int(y1)):
        d.line([(0, y), (W, y)], fill=lerp(top, bottom, (y - y0) / max(1, y1 - y0)))


def star(d, cx, cy, r, fill, points=5, inner=0.45, rot=-math.pi / 2):
    pts = []
    for k in range(points * 2):
        rr = r if k % 2 == 0 else r * inner
        a = rot + k * math.pi / points
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


# ----------------------------------------------------------------------------- backgrounds (drawn once, at 2x)
def bg_ocean(W, H):
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    gradient(d, W, H, (130, 220, 248), (24, 112, 190))
    for k in range(5):  # light rays
        x = W * (0.1 + k * 0.22)
        d.polygon([(x, 0), (x + W * 0.06, 0), (x + W * 0.16, H * 0.8), (x + W * 0.02, H * 0.8)], fill=lerp((130, 220, 248), (90, 180, 230), 0.4 + 0.1 * k))
    d.ellipse([-W * 0.2, H * 0.82, W * 1.2, H * 1.35], fill=(246, 223, 164))
    for k in range(9):  # seaweed
        x = W * (0.04 + k * 0.12)
        pts = [(x + math.sin(j * 0.8 + k) * W * 0.015, H * (0.95 - j * 0.04)) for j in range(9)]
        d.line(pts, fill=(52, 168, 96), width=int(W * 0.012), joint="curve")
    for x, c in ((0.18, (255, 120, 140)), (0.82, (255, 160, 90)), (0.6, (210, 120, 230))):
        for j in range(4):
            r = W * (0.025 - j * 0.004)
            d.ellipse([W * x - r + j * W * 0.012, H * 0.86 - j * H * 0.035 - r, W * x + r + j * W * 0.012, H * 0.86 - j * H * 0.035 + r], fill=c)
    return im


def bg_home(W, H):
    im = Image.new("RGB", (W, H), (255, 244, 214))
    d = ImageDraw.Draw(im)
    d.rectangle([0, H * 0.62, W, H * 0.66], fill=(240, 214, 160))
    d.rectangle([0, H * 0.66, W, H], fill=(242, 194, 123))
    for k in range(12):
        d.line([(W * k / 12, H * 0.66), (W * k / 12 - W * 0.05, H)], fill=(228, 178, 108), width=int(W * 0.003))
    wx, wy, ww, wh = W * 0.08, H * 0.12, W * 0.24, H * 0.36  # window
    d.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=W * 0.02, fill=(150, 215, 250), outline=(255, 255, 255), width=int(W * 0.01))
    d.ellipse([wx + ww * 0.6, wy + wh * 0.15, wx + ww * 0.85, wy + wh * 0.15 + ww * 0.25], fill=(255, 214, 80))
    d.line([(wx + ww / 2, wy), (wx + ww / 2, wy + wh)], fill=(255, 255, 255), width=int(W * 0.006))
    fx, fy, fs = W * 0.72, H * 0.24, W * 0.07  # framed 8-point star pattern
    d.rounded_rectangle([fx - fs, fy - fs, fx + fs, fy + fs], radius=W * 0.01, fill=(46, 158, 91), outline=(200, 150, 60), width=int(W * 0.008))
    star(d, fx, fy, fs * 0.7, (255, 214, 80), points=8, inner=0.75)
    star(d, fx, fy, fs * 0.35, (46, 158, 91), points=8, inner=0.75)
    d.ellipse([W * 0.25, H * 0.86, W * 0.75, H * 0.98], fill=(120, 190, 220))
    d.polygon([(W * 0.9, H * 0.66), (W * 0.96, H * 0.66), (W * 0.95, H * 0.58), (W * 0.91, H * 0.58)], fill=(200, 110, 70))
    for a in (-0.6, -0.2, 0.2, 0.6):
        d.ellipse([W * 0.93 + a * W * 0.03 - W * 0.015, H * 0.48, W * 0.93 + a * W * 0.03 + W * 0.015, H * 0.59], fill=(60, 170, 90))
    return im


def bg_kitchen(W, H):
    im = Image.new("RGB", (W, H), (222, 245, 232))
    d = ImageDraw.Draw(im)
    for k in range(0, 40):
        d.line([(W * k / 40, H * 0.3), (W * k / 40, H * 0.55)], fill=(200, 232, 214), width=int(W * 0.002))
    for k in range(6):
        d.line([(0, H * (0.3 + k * 0.05)), (W, H * (0.3 + k * 0.05))], fill=(200, 232, 214), width=int(W * 0.002))
    d.rectangle([0, H * 0.04, W, H * 0.24], fill=(255, 255, 255))
    for k in range(6):
        d.rounded_rectangle([W * (0.02 + k * 0.165), H * 0.06, W * (0.165 + k * 0.165), H * 0.22], radius=W * 0.008, fill=(186, 226, 205), outline=(140, 190, 165), width=int(W * 0.003))
    d.rectangle([0, H * 0.55, W, H * 0.6], fill=(240, 240, 240))
    d.rectangle([0, H * 0.6, W, H], fill=(250, 220, 170))
    d.line([(W * 0.5, 0), (W * 0.5, H * 0.08)], fill=OUT, width=int(W * 0.003))
    d.chord([W * 0.46, H * 0.06, W * 0.54, H * 0.14], 180, 360, fill=(255, 200, 60))
    return im


def bg_bathroom(W, H):
    im = Image.new("RGB", (W, H), (214, 238, 252))
    d = ImageDraw.Draw(im)
    for k in range(30):
        d.line([(W * k / 30, 0), (W * k / 30, H * 0.7)], fill=(190, 222, 245), width=int(W * 0.002))
    for k in range(12):
        d.line([(0, H * k / 17), (W, H * k / 17)], fill=(190, 222, 245), width=int(W * 0.002))
    d.rectangle([0, H * 0.7, W, H], fill=(170, 210, 235))
    d.rounded_rectangle([W * 0.32, H * 0.08, W * 0.68, H * 0.36], radius=W * 0.03, fill=(235, 250, 255), outline=(255, 255, 255), width=int(W * 0.008))
    d.rounded_rectangle([W * 0.82, H * 0.2, W * 0.9, H * 0.5], radius=W * 0.01, fill=(255, 190, 120))
    return im


def bg_stage(W, H, base, ray):
    im = Image.new("RGB", (W, H), base)
    d = ImageDraw.Draw(im)
    cx, cy = W * 0.5, H * 0.95
    for k in range(18):
        a0, a1 = math.pi * k / 9, math.pi * (k + 0.5) / 9
        R = max(W, H) * 1.5
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy - R * math.sin(a0)), (cx + R * math.cos(a1), cy - R * math.sin(a1))], fill=ray)
    d.ellipse([-W * 0.1, H * 0.86, W * 1.1, H * 1.3], fill=lerp(base, (255, 255, 255), 0.35))
    cols = [(255, 214, 80), (255, 255, 255), (242, 123, 168), (46, 158, 91), (38, 154, 214)]
    n = 14
    for k in range(n):  # bunting
        x0, x1 = W * k / n, W * (k + 1) / n
        d.polygon([(x0, H * 0.02), (x1, H * 0.02), ((x0 + x1) / 2, H * 0.09)], fill=cols[k % 5])
    for k in range(10):
        star(d, W * ((k * 0.137 + 0.05) % 1), H * (0.15 + (k * 0.29) % 0.55), W * 0.012, (255, 255, 255))
    return im


def bg_masjid(W, H):
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    gradient(d, W, H, (150, 215, 250), (225, 245, 255), 0, H * 0.7)
    d.rectangle([0, H * 0.7, W, H], fill=(236, 214, 170))
    gold, white, green = (232, 190, 80), (250, 250, 245), (46, 158, 91)
    cx = W * 0.5
    d.rectangle([cx - W * 0.22, H * 0.38, cx + W * 0.22, H * 0.7], fill=white)
    d.chord([cx - W * 0.12, H * 0.2, cx + W * 0.12, H * 0.56], 180, 360, fill=gold)
    d.polygon([(cx, H * 0.12), (cx - W * 0.006, H * 0.2), (cx + W * 0.006, H * 0.2)], fill=gold)
    for side in (-1, 1):
        mx = cx + side * W * 0.3
        d.rectangle([mx - W * 0.025, H * 0.2, mx + W * 0.025, H * 0.7], fill=white)
        d.chord([mx - W * 0.03, H * 0.13, mx + W * 0.03, H * 0.25], 180, 360, fill=green)
        d.chord([cx + side * W * 0.16 - W * 0.05, H * 0.32, cx + side * W * 0.16 + W * 0.05, H * 0.46], 180, 360, fill=gold)
    for k in range(5):
        x = cx - W * 0.16 + k * W * 0.08
        d.chord([x - W * 0.025, H * 0.5, x + W * 0.025, H * 0.6], 180, 360, fill=(120, 170, 210))
        d.rectangle([x - W * 0.025, H * 0.55, x + W * 0.025, H * 0.66], fill=(120, 170, 210))
    for k in range(9):
        d.ellipse([W * (0.06 + k * 0.11), H * 0.74, W * (0.1 + k * 0.11), H * 0.79], fill=(110, 190, 110))
    return im


def bg_night(W, H):
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    gradient(d, W, H, (18, 28, 70), (60, 60, 130))
    for k in range(40):
        x, y = W * ((k * 0.6180339) % 1), H * ((k * 0.3819660 * 1.7) % 0.65)
        star(d, x, y, W * (0.004 + 0.004 * (k % 3)), (255, 240, 180))
    d.ellipse([W * 0.75, H * 0.08, W * 0.85, H * 0.08 + W * 0.1], fill=(255, 236, 160))
    d.ellipse([W * 0.77, H * 0.07, W * 0.87, H * 0.07 + W * 0.1], fill=(28, 38, 84))
    d.ellipse([-W * 0.2, H * 0.82, W * 1.2, H * 1.4], fill=(40, 50, 100))
    return im


BACKGROUNDS = {
    "ocean": bg_ocean, "home": bg_home, "kitchen": bg_kitchen, "bathroom": bg_bathroom,
    "stage_green": lambda W, H: bg_stage(W, H, (60, 180, 110), (80, 196, 128)),
    "stage_pink": lambda W, H: bg_stage(W, H, (240, 120, 165), (248, 145, 185)),
    "masjid": bg_masjid, "night": bg_night,
}


def emoji_img(ch, size):
    """A colour emoji as an RGBA image (Noto Color Emoji, Apache-2.0). None if the font has no such picture."""
    cache = G.setdefault("emoji", {})
    key = (ch, int(size))
    if key not in cache:
        img = None
        try:
            f = ImageFont.truetype(path("assets", "fonts", "NotoColorEmoji.ttf"), 109)
            im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((8, 8), ch, font=f, embedded_color=True)
            bbox = im.getbbox()
            if bbox:
                im = im.crop(bbox)
                sc = size / max(im.size)
                img = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
        except Exception:
            img = None
        cache[key] = img
    return cache[key]


def draw_subject(frame, d, info, cx, cy, size, bounce):
    """White rounded card with the topic's emoji / Arabic glyph, bouncing gently."""
    cy -= bounce
    r = size / 2
    d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=size * 0.18, fill=(255, 255, 255), outline=(30, 42, 74), width=max(3, int(size * 0.025)))
    if info.get("arabic"):
        text(d, (cx, cy - size * 0.05), info["arabic"], size * 0.62, (46, 158, 91), arabic=True)
        return
    em = emoji_img(info["emoji"], size * 0.72) if info.get("emoji") else None
    if em:
        frame.paste(em, (int(cx - em.width / 2), int(cy - em.height / 2)), em)
    else:
        label = (info.get("text_hi") if G["lang"] == "hi" else info.get("text")) or ""
        sz = size * 0.3
        while sz > 10 and d.textlength(label, font=font(sz)) > size * 0.86:
            sz *= 0.9
        text(d, (cx, cy), label, sz, (30, 42, 74))


def background(name):
    cache = G.setdefault("bgs", {})
    if name not in cache:
        cache[name] = BACKGROUNDS[name](G["W"] * SS, G["H"] * SS)
    return cache[name]


# ----------------------------------------------------------------------------- props
def plate(d, x, y, r, scale=1.0):
    r *= scale
    d.ellipse([x - r, y - r * 0.38, x + r, y + r * 0.38], fill=(255, 255, 255), outline=OUT, width=max(2, int(r * 0.05)))
    d.ellipse([x - r * 0.7, y - r * 0.26, x + r * 0.7, y + r * 0.26], outline=(210, 220, 235), width=max(2, int(r * 0.03)))


def food(d, x, y, r, kind):
    if kind == "dates":
        for k in range(3):
            d.ellipse([x - r * 0.5 + k * r * 0.32, y - r * 0.28, x - r * 0.14 + k * r * 0.32, y], fill=(120, 60, 30), outline=OUT, width=2)
    elif kind == "bread":
        d.rounded_rectangle([x - r * 0.45, y - r * 0.4, x + r * 0.45, y], radius=r * 0.15, fill=(235, 180, 100), outline=OUT, width=2)
    elif kind == "apple":
        d.ellipse([x - r * 0.3, y - r * 0.55, x + r * 0.3, y], fill=(230, 60, 60), outline=OUT, width=2)
        d.ellipse([x, y - r * 0.68, x + r * 0.2, y - r * 0.55], fill=(60, 170, 90))
    elif kind == "banana":
        d.arc([x - r * 0.5, y - r * 0.7, x + r * 0.5, y + r * 0.1], 20, 160, fill=(255, 210, 60), width=int(r * 0.18))


def draw_table(d, W, H, ts, scene, props, bs):
    top = H * 0.73
    d.rounded_rectangle([W * 0.12, top, W * 0.88, top + H * 0.06], radius=W * 0.01, fill=(201, 139, 79), outline=OUT, width=int(W * 0.003))
    d.rectangle([W * 0.12, top + H * 0.06, W * 0.88, H], fill=(181, 119, 62))
    d.rectangle([W * 0.12, top - H * 0.005, W * 0.88, top + H * 0.012], fill=(255, 255, 255))
    xs = [0.3, 0.5, 0.7]
    kinds = [["dates", "apple"], ["bread"], ["banana", "dates"]]
    for k, x in enumerate(xs):
        sc = 1.0
        if "plates_appear" in props:
            sc = ease_out_back((ts - (0.3 + k * 0.45)) / 0.35)
            if sc <= 0:
                continue
        plate(d, W * x, top + H * 0.015, W * 0.07, sc)
        if "food" in props:
            for j, kind in enumerate(kinds[k]):
                food(d, W * x + (j - (len(kinds[k]) - 1) / 2) * W * 0.05, top + H * 0.01, W * 0.08, kind)
        if "empty_plates" in props:
            for j in range(3):
                d.ellipse([W * x - W * 0.02 + j * W * 0.017, top + H * 0.005, W * x - W * 0.014 + j * W * 0.017, top + H * 0.013], fill=(210, 160, 100))


def draw_sink(d, W, H, ts):
    d.rounded_rectangle([W * 0.2, H * 0.74, W * 0.8, H * 0.84], radius=W * 0.03, fill=(255, 255, 255), outline=OUT, width=int(W * 0.003))
    d.rectangle([W * 0.45, H * 0.84, W * 0.55, H], fill=(235, 240, 245))
    d.rounded_rectangle([W * 0.47, H * 0.62, W * 0.53, H * 0.66], radius=W * 0.01, fill=(190, 200, 210), outline=OUT, width=int(W * 0.002))
    d.line([(W * 0.5, H * 0.66), (W * 0.5, H * 0.74)], fill=(150, 210, 255), width=int(W * 0.006))


def bubbles(d, W, H, t, n=16, soap=False, region=(0, 1)):
    for k in range(n):
        seed = (k * 7919) % 997 / 997
        x = W * (region[0] + (region[1] - region[0]) * ((seed * 13.7) % 1))
        speed = 0.12 + seed * 0.15
        prog = (t * speed + seed) % 1.0
        y = H * (1.05 - prog * 1.15) if not soap else H * (0.7 - prog * 0.2)
        r = W * (0.006 + 0.012 * ((seed * 5.3) % 1)) * (1.4 if soap else 1)
        x += math.sin(t * 2 + k) * W * 0.01
        col = (255, 255, 255) if soap else (220, 245, 255)
        d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=max(2, int(r * 0.25)))
        d.ellipse([x - r * 0.45, y - r * 0.55, x - r * 0.1, y - r * 0.2], fill=col)


# ----------------------------------------------------------------------------- characters
def mouth_amount(t):
    starts = G["note_starts"]
    i = bisect.bisect_right(starts, t) - 1
    if i < 0:
        return 0.0
    start, dur, _m, bar = G["notes"][i]
    if not G["song"]["bars"][bar].get(G["lang"]):
        return 0.0
    f = (t - start) / dur
    if f > 1:
        return 0.0
    return math.sin(math.pi * min(1, f * 1.3)) ** 0.6


def place(x, y):
    if G["vertical"]:
        return 0.06 + x * 0.88, 0.3 + y * 0.55
    return x, y


def draw_character(d, ch, scene, t, ts, beat_phase, bar):
    W, H = G["W"] * SS, G["H"] * SS
    bs = G["bs"]
    x, y = place(ch["x"], ch["y"])
    act = ch.get("action", "idle")
    pose, dx, dy = "idle", 0.0, math.sin(t * 2.4 + x * 5) * 0.008
    if act == "bob":
        dy = math.sin(t * 2 * math.pi * 0.45 + x * 3) * 0.02
    elif act == "dance":
        pose = "dance"
        dy = -abs(math.sin(math.pi * beat_phase)) * 0.035
        dx = math.sin(t * math.pi * G["bps"] / 2) * 0.008
    elif act == "wave":
        pose = "wave"
    elif act == "happy":
        pose = "happy"
        dy = -abs(math.sin(math.pi * beat_phase)) * 0.012
    elif act == "wash_hands":
        pose = "wash"
    elif act == "juggle":
        pose = "dance"
        dy = math.sin(t * 6) * 0.01
    elif act == "swim_in":
        f = ease_out_cubic(ts / (bs * 1.6))
        x = -0.3 + (x + 0.3) * f
        dy = math.sin(t * 3) * 0.02
    elif act in ("walk_in_left", "walk_in_right"):
        f = ease_out_cubic(ts / (bs * 0.8))
        start = -0.15 if act == "walk_in_left" else 1.15
        x = start + (x - start) * f
        dy = -abs(math.sin(t * 10)) * 0.015 if f < 0.98 else 0.0
    sing_bars = ch.get("sing_bars")
    sings = act != "juggle" and (sing_bars is None or sing_bars[0] <= bar < sing_bars[1])
    blink = ((t + x * 1.7) % 3.3) < 0.13
    u = (0.34 * G["W"] if G["vertical"] else 0.33 * G["H"]) * SS
    st = {"t": t, "mouth": mouth_amount(t) if sings else 0.0, "blink": blink, "pose": pose, "bps": G["bps"]}
    DRAW[ch["name"]](d, (x + dx) * W, (y + dy) * H, u, st)
    if act == "juggle":
        cx, cy = (x + dx) * W, (y + dy) * H - u * 0.55
        for k, kind in enumerate(("apple", "banana", "dates")):
            a = t * 4 + k * 2 * math.pi / 3
            food(d, cx + math.cos(a) * u * 0.45, cy - abs(math.sin(a)) * u * 0.5, u * 0.5, kind)
    if act == "wash_hands":
        bubbles(d, W, H, t, n=8, soap=True, region=(x - 0.1, x + 0.1))


# ----------------------------------------------------------------------------- overlays (drawn at 1x after camera)
def draw_subtitle(d, t, bar):
    W, H = G["W"], G["H"]
    if bar >= len(G["song"]["bars"]):
        return
    line = G["song"]["bars"][bar].get(G["lang"])
    if not line:
        return
    size = (0.045 * H) if G["vertical"] else (0.065 * H)
    y = H * (0.76 if G["vertical"] else 0.9)
    tw = d.textlength(line, font=font(size))
    while tw > W * 0.9:
        size *= 0.92
        tw = d.textlength(line, font=font(size))
    pad = size * 0.45
    d.rounded_rectangle([W / 2 - tw / 2 - pad, y - size * 0.75, W / 2 + tw / 2 + pad, y + size * 0.7], radius=size * 0.5, fill=(30, 42, 74))
    text(d, (W / 2, y), line, size, (255, 255, 255))
    # bouncing progress ball over the line
    f = (t - bar * G["bs"]) / G["bs"]
    bx = W / 2 - tw / 2 + tw * f
    by = y - size * 0.95 - abs(math.sin(math.pi * 4 * f)) * size * 0.4
    d.ellipse([bx - size * 0.16, by - size * 0.16, bx + size * 0.16, by + size * 0.16], fill=(255, 214, 80), outline=(30, 42, 74), width=3)


def draw_words(d, scene, ts, beat_phase, bar, frame=None):
    W, H = G["W"], G["H"]
    props = scene.get("props", [])
    lang = G["lang"]
    bounce = abs(math.sin(math.pi * beat_phase)) * H * 0.012
    top = H * (0.16 if G["vertical"] else 0.0)
    if "word_bismillah" in props:
        text(d, (W / 2, top + H * 0.12 - bounce), "بِسْمِ اللَّهِ", H * (0.06 if G["vertical"] else 0.1), (255, 214, 80), (30, 42, 74), arabic=True)
        colours = [(255, 255, 255), (255, 214, 80), (255, 255, 255), (180, 240, 255)]
        text(d, (W / 2, top + H * 0.26 - bounce), "Bismillah!", H * (0.07 if G["vertical"] else 0.12), colours[bar % 4], (30, 42, 74))
    if scene.get("word"):
        w = scene["word"]
        label = w.get("text_hi") if lang == "hi" else w.get("text")
        size = H * (0.07 if G["vertical"] else 0.12)
        while d.textlength(label, font=font(size)) > W * 0.8:
            size *= 0.92
        if w.get("arabic"):
            text(d, (W / 2, top + H * 0.11 - bounce), w["arabic"], H * (0.07 if G["vertical"] else 0.12), (255, 214, 80), (30, 42, 74), arabic=True)
        elif w.get("emoji") and frame is not None:
            em = emoji_img(w["emoji"], H * (0.07 if G["vertical"] else 0.13))
            if em:
                frame.paste(em, (int(W / 2 - em.width / 2), int(top + H * 0.11 - bounce - em.height / 2)), em)
        colours = [(255, 255, 255), (255, 214, 80), (255, 255, 255), (180, 240, 255)]
        text(d, (W / 2, top + H * 0.26 - bounce), label, size, colours[bar % 4], (30, 42, 74))
    if scene.get("subject") and frame is not None:
        if G["vertical"]:
            draw_subject(frame, d, scene["subject"], W * 0.5, H * 0.3, W * 0.42, bounce)
        else:
            draw_subject(frame, d, scene["subject"], W * 0.5, H * 0.3, H * 0.34, bounce)
    if "word_alhamdulillah" in props:
        f = ease_out_back(ts / 0.5)
        if f > 0:
            text(d, (W / 2, top + H * 0.12), "الْحَمْدُ لِلَّهِ", H * (0.055 if G["vertical"] else 0.09) * f, (46, 158, 91), (255, 255, 255), arabic=True)
            text(d, (W / 2, top + H * 0.25), "Alhamdulillah!", H * (0.06 if G["vertical"] else 0.1) * f, (255, 214, 80), (30, 42, 74))
    if "question_mark" in props and bar == scene["bars"][0]:
        x, y = place(0.66, 0.2)
        text(d, (x * W, y * H - bounce * 2), "?", H * 0.14, (255, 214, 80), (30, 42, 74))
    if scene.get("title_card"):
        f = ease_out_back((ts - 0.6) / 0.6)
        if f > 0:
            title = G["song"]["title_en"] if lang == "en" else G["song"]["title_hi"]
            size = H * (0.05 if G["vertical"] else 0.1) * f
            while d.textlength(title, font=font(max(8, size))) > W * 0.9:
                size *= 0.92
            text(d, (W / 2, top + H * 0.2), title, max(8, size), (255, 255, 255), (30, 42, 74))
        text(d, (W / 2, top + H * 0.07), G["settings"]["brand"], H * (0.035 if G["vertical"] else 0.06), (255, 214, 80), (30, 42, 74))
    if scene.get("end_card"):
        f = ease_out_back(ts / 0.6)
        text(d, (W / 2, top + H * 0.15), G["settings"]["brand"], H * (0.07 if G["vertical"] else 0.13) * max(0.01, f), (255, 214, 80), (30, 42, 74))
        text(d, (W / 2, top + H * 0.29), G["settings"]["tagline"], H * (0.035 if G["vertical"] else 0.06) * max(0.01, f), (255, 255, 255), (30, 42, 74))


# ----------------------------------------------------------------------------- frame
def scene_at(bar):
    for sc in G["storyboard"]["scenes"]:
        if sc["bars"][0] <= bar < sc["bars"][1]:
            return sc
    return G["storyboard"]["scenes"][-1]


def render_frame(i):
    t = G["t0"] + i / G["fps"]
    bs = G["bs"]
    bar = int(t / bs)
    scene = scene_at(bar)
    ts = t - scene["bars"][0] * bs
    sd = (scene["bars"][1] - scene["bars"][0]) * bs
    beat_phase = (t / (bs / 4)) % 1.0
    W, H = G["W"] * SS, G["H"] * SS
    img = background(scene["bg"]).copy()
    d = ImageDraw.Draw(img)
    if scene["bg"] == "ocean":
        bubbles(d, W, H, t)
    for ch in scene.get("chars", []):
        draw_character(d, ch, scene, t, ts, beat_phase, bar)
    props = scene.get("props", [])
    if "table" in props:
        draw_table(d, W, H, ts, scene, props, bs)
    if "sink" in props:
        draw_sink(d, W, H, ts)
    # camera
    cam = scene.get("camera", "static")
    z = 1.0
    if cam == "slow_push_in":
        z = 1.0 + 0.07 * (ts / sd)
    elif cam == "beat_bounce":
        z = 1.0 + 0.025 * max(0.0, 1 - beat_phase * 3)
    cw, chh = W / z, H / z
    x0, y0 = (W - cw) / 2, (H - chh) * 0.4
    frame = img.resize((G["W"], G["H"]), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + chh), reducing_gap=2.0)
    fd = ImageDraw.Draw(frame)
    draw_words(fd, scene, ts, beat_phase, bar, frame)
    draw_subtitle(fd, t, bar)
    if G["vertical"] and G.get("short_title") and t - G["t0"] < 3.0:
        size = G["H"] * 0.04
        while fd.textlength(G["short_title"], font=font(size)) > G["W"] * 0.9:
            size *= 0.92
        text(fd, (G["W"] / 2, G["H"] * 0.07), G["short_title"], size, (255, 255, 255), (30, 42, 74))
    if not G["vertical"]:
        text(fd, (G["W"] * 0.08, G["H"] * 0.05), G["settings"]["brand"], G["H"] * 0.03, (255, 214, 80), (30, 42, 74))
    # soft white flash at each scene change (not on the first frame of the video)
    if ts < 0.17 and scene["bars"][0] * bs > G["t0"] + 0.01:
        frame = Image.blend(frame, Image.new("RGB", frame.size, (255, 255, 255)), 0.6 * (1 - ts / 0.17))
    return frame.tobytes()


def init_worker(ctx):
    G.update(ctx)


# ----------------------------------------------------------------------------- main
def write_srt(p, song, lang, t0, t1):
    bs = bar_seconds(song)

    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"

    n = 0
    with open(p, "w", encoding="utf-8") as f:
        for i, bar in enumerate(song["bars"]):
            s, e = i * bs, (i + 1) * bs
            if not bar.get(lang) or e <= t0 or s >= t1:
                continue
            n += 1
            f.write(f"{n}\n{ts(max(s, t0) - t0)} --> {ts(min(e, t1) - t0)}\n{bar[lang]}\n\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("song_id")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--short", default=None, help="id of a short from storyboard.json")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 2)
    ap.add_argument("--seconds", type=float, default=None, help="render only the first N seconds (for quick tests)")
    a = ap.parse_args()

    song = load_song(a.song_id)
    sb = load_storyboard(a.song_id)
    settings = load_settings()
    bs = bar_seconds(song)
    vertical = a.short is not None
    W, H = settings["video"]["short"] if vertical else settings["video"]["long"]
    fps = sb.get("fps", settings["video"]["fps"])
    t0, t1, short_title = 0.0, song_length_sec(song), None
    if vertical:
        sh = next(s for s in sb["shorts"] if s["id"] == a.short)
        t0, t1 = sh["bars"][0] * bs, min(sh["bars"][1] * bs + 0.6, song_length_sec(song))
        short_title = sh["title_" + a.lang].replace("#shorts", "").strip(" |")
    if a.seconds:
        t1 = min(t1, t0 + a.seconds)
    dur = t1 - t0
    n_frames = int(dur * fps)

    events = note_events(song)
    ctx = {"song": song, "storyboard": sb, "settings": settings, "lang": a.lang, "W": W, "H": H, "fps": fps,
           "bs": bs, "bps": song["tempo_bpm"] / 60, "vertical": vertical, "t0": t0, "notes": events,
           "note_starts": [e[0] for e in events], "short_title": short_title}

    kind = "shorts" if vertical else "episodes"
    d = out_dir(a.song_id, kind)
    name = f"{a.song_id}_{a.lang}" + (f"_short-{a.short}" if vertical else "")
    mp4 = os.path.join(d, name + ".mp4")
    audio = os.path.join(out_dir(a.song_id, "audio"), f"final_{a.lang}.wav")
    write_srt(os.path.join(d, name + ".srt"), song, a.lang, t0, t1)

    vcfg = settings["video"]
    afilter = f"afade=t=in:d=0.25,afade=t=out:st={max(0, dur - 0.8):.2f}:d=0.8" if vertical else "anull"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
           "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", audio,
           "-map", "0:v", "-map", "1:a", "-af", afilter,
           "-c:v", "libx264", "-preset", vcfg["preset"], "-crf", str(vcfg["crf"]), "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", mp4]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(a.workers, initializer=init_worker, initargs=(ctx,)) as pool:
        for k, frame in enumerate(pool.imap(render_frame, range(n_frames), chunksize=6)):
            proc.stdin.write(frame)
            if k % (fps * 10) == 0:
                print(f"  {name}: {k}/{n_frames} frames", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit(f"ffmpeg failed for {mp4}")
    print(f"Rendered {mp4} ({dur:.1f} s)")


if __name__ == "__main__":
    main()
