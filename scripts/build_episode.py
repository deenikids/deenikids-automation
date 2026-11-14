"""Build one complete episode: music -> vocals -> long videos -> Shorts -> thumbnails -> QC.

Usage:
  python scripts/build_episode.py bismillah-before-we-begin
  python scripts/build_episode.py bismillah-before-we-begin --test   (first 12 s only, fast)
"""
import argparse
import subprocess
import sys
import time

from common import load_settings, load_song, load_storyboard, validate_song


def step(title, cmd):
    print(f"\n=== {title} ===", flush=True)
    t = time.time()
    r = subprocess.run([sys.executable] + cmd)
    if r.returncode != 0:
        sys.exit(f"FAILED at step: {title}")
    print(f"--- {title}: {time.time() - t:.0f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("song_id")
    ap.add_argument("--test", action="store_true", help="render only 12 seconds of each video")
    ap.add_argument("--no-shorts", action="store_true")
    a = ap.parse_args()

    song = load_song(a.song_id)
    validate_song(song)
    sb = load_storyboard(a.song_id)
    langs = load_settings()["languages"]
    extra = ["--seconds", "12"] if a.test else []

    step("Music", ["scripts/generate_music.py", a.song_id])
    step("Vocals + mix", ["scripts/generate_voice.py", a.song_id])
    for lang in langs:
        step(f"Episode ({lang})", ["scripts/render_animatic.py", a.song_id, "--lang", lang] + extra)
        if not a.no_shorts:
            for sh in sb.get("shorts", []):
                step(f"Short {sh['id']} ({lang})", ["scripts/render_animatic.py", a.song_id, "--lang", lang, "--short", sh["id"]] + extra)
    step("Thumbnails", ["scripts/generate_thumbnail.py", a.song_id])
    if a.test:
        print("\nTest mode: skipping QC duration checks. Build finished.")
        return
    step("Quality check", ["scripts/quality_check.py", a.song_id])
    print("\nBuild finished and passed QC.")


if __name__ == "__main__":
    main()
