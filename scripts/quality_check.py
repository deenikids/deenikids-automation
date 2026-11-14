"""Automatic quality control. Nothing is uploaded unless this passes.

Checks every video in output/<song_id>/episodes and /shorts:
  resolution, duration, audio present, audio not clipping, audio not silent,
  black screens, missing frames, subtitle file + timing, file naming,
  already-uploaded duplicates, and thumbnails (size + 1280x720).

Usage: python scripts/quality_check.py bismillah-before-we-begin
Writes output/<song_id>/qc_report.json and exits with code 1 if anything fails.
"""
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

from PIL import Image

from common import load_json, load_settings, out_dir, path, save_json

NAME_RE = re.compile(r"^[a-z0-9-]+_(en|hi)(_short-[a-z0-9-]+)?\.mp4$")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(f):
    r = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", f])
    return json.loads(r.stdout or "{}")


def audio_levels(f):
    r = run(["ffmpeg", "-hide_banner", "-i", f, "-af", "volumedetect", "-vn", "-f", "null", "-"])
    mx = re.search(r"max_volume: (-?[\d.]+) dB", r.stderr)
    mean = re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr)
    return (float(mx.group(1)) if mx else None, float(mean.group(1)) if mean else None)


def black_seconds(f):
    r = run(["ffmpeg", "-hide_banner", "-i", f, "-vf", "blackdetect=d=0.3:pic_th=0.95", "-an", "-f", "null", "-"])
    return sum(float(x) for x in re.findall(r"black_duration:([\d.]+)", r.stderr))


def srt_ok(srt, duration):
    if not os.path.exists(srt):
        return False, "subtitle file missing"
    text = open(srt, encoding="utf-8").read()
    times = re.findall(r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)", text)
    if not times:
        return False, "subtitle file has no cues"
    for t in times:
        s = int(t[0]) * 3600 + int(t[1]) * 60 + int(t[2]) + int(t[3]) / 1000
        e = int(t[4]) * 3600 + int(t[5]) * 60 + int(t[6]) + int(t[7]) / 1000
        if e <= s or e > duration + 0.5:
            return False, f"bad cue timing {s:.2f}-{e:.2f}"
    return True, f"{len(times)} cues"


def sha256(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_video(f, kind, cfg, uploaded_hashes):
    res = {"file": os.path.basename(f), "kind": kind, "checks": {}}
    c = res["checks"]

    def ok(name, passed, detail=""):
        c[name] = {"pass": bool(passed), "detail": detail}

    ok("filename", NAME_RE.match(os.path.basename(f)), os.path.basename(f))
    info = probe(f)
    v = next((s for s in info.get("streams", []) if s["codec_type"] == "video"), None)
    a = next((s for s in info.get("streams", []) if s["codec_type"] == "audio"), None)
    dur = float(info.get("format", {}).get("duration", 0))
    want = cfg["video"]["long"] if kind == "episode" else cfg["video"]["short"]
    ok("resolution", v and [v["width"], v["height"]] == want, f"{v and v['width']}x{v and v['height']} (want {want[0]}x{want[1]})")
    lo, hi = cfg["qc"]["long_duration_sec"] if kind == "episode" else cfg["qc"]["short_duration_sec"]
    ok("duration", lo <= dur <= hi, f"{dur:.1f}s (allowed {lo}-{hi})")
    ok("audio_present", a is not None, a["codec_name"] if a else "no audio stream")
    if v:
        frames = int(v.get("nb_frames") or 0)
        num, den = v.get("r_frame_rate", "24/1").split("/")
        fps = float(num) / float(den or 1)
        expected = dur * fps
        ok("frames", frames and abs(frames - expected) <= fps, f"{frames} frames, expected ~{expected:.0f}")
    mx, mean = audio_levels(f)
    ok("no_clipping", mx is not None and mx <= cfg["qc"]["max_peak_db"], f"peak {mx} dB")
    ok("not_silent", mean is not None and mean >= cfg["qc"]["min_mean_db"], f"mean {mean} dB")
    blk = black_seconds(f)
    ok("no_black_screen", blk <= cfg["qc"]["max_black_sec"], f"{blk:.2f}s black")
    passed, detail = srt_ok(f[:-4] + ".srt", dur)
    ok("subtitles", passed, detail)
    digest = sha256(f)
    res["sha256"] = digest
    ok("not_duplicate", digest not in uploaded_hashes, "already uploaded" if digest in uploaded_hashes else "new")
    res["pass"] = all(x["pass"] for x in c.values())
    return res


def check_thumbs(song_id, langs):
    out = []
    for lang in langs:
        p = os.path.join(out_dir(song_id, "thumbnails"), f"{song_id}_{lang}.jpg")
        if not os.path.exists(p):
            out.append({"file": os.path.basename(p), "pass": False, "detail": "missing"})
            continue
        size = os.path.getsize(p)
        dims = Image.open(p).size
        good = size < 2_000_000 and dims == (1280, 720)
        out.append({"file": os.path.basename(p), "pass": good, "detail": f"{dims[0]}x{dims[1]}, {size // 1024} KB"})
    return out


def main(song_id):
    cfg = load_settings()
    ledger_p = path("database", "uploads.json")
    ledger = load_json(ledger_p) if os.path.exists(ledger_p) else {"uploads": []}
    uploaded = {u["sha256"] for u in ledger["uploads"]}
    results = []
    for kind, folder in (("episode", "episodes"), ("short", "shorts")):
        for f in sorted(glob.glob(os.path.join(out_dir(song_id, folder), "*.mp4"))):
            r = check_video(f, kind, cfg, uploaded)
            results.append(r)
            print(("PASS " if r["pass"] else "FAIL ") + r["file"])
            for name, x in r["checks"].items():
                if not x["pass"]:
                    print(f"     - {name}: {x['detail']}")
    has_episode = any(r["kind"] == "episode" for r in results)
    thumbs = check_thumbs(song_id, cfg["languages"]) if has_episode else []
    for t in thumbs:
        print(("PASS " if t["pass"] else "FAIL ") + t["file"] + f" ({t['detail']})")
    report = {"song_id": song_id, "videos": results, "thumbnails": thumbs,
              "pass": bool(results) and all(r["pass"] for r in results) and all(t["pass"] for t in thumbs)}
    save_json(os.path.join(out_dir(song_id), "qc_report.json"), report)
    print("QC RESULT:", "PASS" if report["pass"] else "FAIL")
    return report["pass"]


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else "bismillah-before-we-begin") else 1)
