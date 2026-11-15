"""Make a 1280x720 YouTube thumbnail per language (original artwork, brand colours).

Usage: python scripts/generate_thumbnail.py bismillah-before-we-begin
Writes output/<song_id>/thumbnails/<song_id>_<lang>.jpg (under YouTube's 2 MB limit)
"""
import sys

from PIL import Image, ImageDraw

import render_animatic as R
from characters2d import DRAW
from common import load_settings, load_song, out_dir

W, H, SS = 1280, 720, 2


def sunburst(w, h, c1, c2):
    import math
    img = Image.new("RGB", (w, h), c1)
    d = ImageDraw.Draw(img)
    cx, cy, n = w * 0.62, h * 0.55, 18
    for i in range(0, n, 2):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        d.polygon([(cx, cy), (cx + math.cos(a0) * w * 2, cy + math.sin(a0) * w * 2), (cx + math.cos(a1) * w * 2, cy + math.sin(a1) * w * 2)], fill=c2)
    return img


def sticker(layer, w=14):
    """White cut-out outline around everything drawn on a transparent layer (pops on small screens)."""
    from PIL import ImageFilter
    a = layer.split()[3].filter(ImageFilter.MaxFilter(2 * w + 1))
    base = Image.new("RGBA", layer.size, (255, 255, 255, 0))
    base.paste((255, 255, 255, 255), mask=a)
    base.alpha_composite(layer)
    return base


def make(song, lang, settings):
    R.G.clear()
    R.G.update({"W": W, "H": H, "settings": settings})
    img = sunburst(W * SS, H * SS, (255, 196, 64), (255, 214, 102)).convert("RGBA")
    # big friendly faces: close, large, overlapping
    cast = [("deeni", 0.66, 0.38, 1.1, "idle"), ("amira", 0.50, 0.92, 1.45, "happy"),
            ("ayaan", 0.82, 1.0, 1.45, "wave"), ("bubbly", 0.93, 0.40, 0.8, "dance")]
    for name, x, y, k, pose in cast:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        DRAW[name](ld, x * W * SS, y * H * SS, 0.5 * H * SS * k, {"t": 0.3, "mouth": 0.9, "blink": False, "pose": pose, "bps": 1.8})
        img.alpha_composite(sticker(layer, 12 * SS))
    img = img.convert("RGB")
    img = img.resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    R.G["lang"] = lang
    if song.get("auto"):
        word = song["word_en"] if lang == "en" else song["word_hi"]
        vis = song.get("visual", {})
        if vis.get("arabic"):
            R.text(d, (W * 0.25, H * 0.2), vis["arabic"], H * 0.16, (255, 214, 80), (30, 42, 74), arabic=True)
        elif vis.get("emoji"):
            em = R.emoji_img(vis["emoji"], H * 0.24)
            if em:
                img.paste(em, (int(W * 0.25 - em.width / 2), int(H * 0.2 - em.height / 2)), em)
    else:
        word = "Bismillah!"
        R.text(d, (W * 0.25, H * 0.2), "بِسْمِ اللَّهِ", H * 0.13, (255, 214, 80), (30, 42, 74), arabic=True)
    size = H * 0.16
    while d.textlength(word, font=R.font(size)) > W * 0.44:
        size *= 0.92
    R.text(d, (W * 0.25, H * 0.43), word, size, (255, 255, 255), (30, 42, 74))
    sub = "Song for Kids"
    R.text(d, (W * 0.25, H * 0.61), sub, H * 0.08, (255, 214, 80), (30, 42, 74))
    d.rounded_rectangle([W * 0.04, H * 0.78, W * 0.4, H * 0.93], radius=H * 0.04, fill=(30, 42, 74))
    R.text(d, (W * 0.22, H * 0.855), settings["brand"], H * 0.07, (255, 214, 80))
    p = f"{out_dir(song['id'], 'thumbnails')}/{song['id']}_{lang}.jpg"
    img.save(p, quality=90)
    print(p)
    return p


def main(song_id):
    song, settings = load_song(song_id), load_settings()
    for lang in settings["languages"]:
        make(song, lang, settings)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bismillah-before-we-begin")
