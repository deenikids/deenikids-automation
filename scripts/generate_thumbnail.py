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


def make(song, lang, settings):
    R.G.clear()
    R.G.update({"W": W, "H": H, "settings": settings})
    img = R.bg_stage(W * SS, H * SS, (60, 180, 110), (80, 196, 128))
    d = ImageDraw.Draw(img)
    u = 0.5 * H * SS
    poses = {"ayaan": "wave", "amira": "happy", "bubbly": "dance", "deeni": "idle"}
    spots = {"bubbly": (0.86, 0.72), "ayaan": (0.66, 0.74), "amira": (0.46, 0.76), "deeni": (0.62, 0.36)}
    for name in ("deeni", "bubbly", "ayaan", "amira"):
        x, y = spots[name]
        DRAW[name](d, x * W * SS, y * H * SS, u * (0.85 if name == "deeni" else 1), {"t": 0.3, "mouth": 0.8, "blink": False, "pose": poses[name], "bps": 1.8})
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
    while d.textlength(word, font=R.font(size)) > W * 0.46:
        size *= 0.92
    R.text(d, (W * 0.25, H * 0.43), word, size, (255, 255, 255), (30, 42, 74))
    sub = "Song for Kids" if lang == "en" else "Bachchon Ka Song"
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
