"""Make a contact sheet of still frames (one per scene) to check an episode without rendering video.

Usage: python scripts/preview_frames.py bismillah-before-we-begin --lang en [--short chorus]
Writes output/<song_id>/preview_<lang>[_short].png
"""
import argparse

from PIL import Image

import render_animatic as R
from common import bar_seconds, load_settings, load_song, load_storyboard, note_events, out_dir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("song_id")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--short", default=None)
    a = ap.parse_args()
    song, sb, settings = load_song(a.song_id), load_storyboard(a.song_id), load_settings()
    bs = bar_seconds(song)
    vertical = a.short is not None
    W, H = settings["video"]["short"] if vertical else settings["video"]["long"]
    events = note_events(song)
    R.G.update({"song": song, "storyboard": sb, "settings": settings, "lang": a.lang, "W": W, "H": H, "fps": 24,
                "bs": bs, "bps": song["tempo_bpm"] / 60, "vertical": vertical, "t0": 0.0, "notes": events,
                "note_starts": [e[0] for e in events], "short_title": None})
    times = [(sc["bars"][0] + min(1.4, (sc["bars"][1] - sc["bars"][0]) * 0.6)) * bs for sc in sb["scenes"]]
    thumbs = []
    for t in times:
        R.G["t0"] = t - 0.5  # so the scene-change flash doesn't show
        img = Image.frombytes("RGB", (W, H), R.render_frame(int(0.5 * 24)))
        thumbs.append(img.resize((W // 4, H // 4)))
    cols = 4 if not vertical else 6
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W // 4, rows * H // 4), (255, 255, 255))
    for k, im in enumerate(thumbs):
        sheet.paste(im, ((k % cols) * W // 4, (k // cols) * H // 4))
    p = f"{out_dir(a.song_id)}/preview_{a.lang}{'_short' if vertical else ''}.png"
    sheet.save(p)
    print(p)


if __name__ == "__main__":
    main()
