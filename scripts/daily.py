"""The fully automatic daily run. GitHub Actions calls this once a day; nobody needs to touch anything.

For today's plan day it makes, checks and uploads:
  Long-A + Long-B   new episodes, English and Hinglish      (4 long videos)
  Short-1 + Short-2 vertical sing-alongs of those episodes  (4 Shorts)
  Short-3           an original mini song                   (2 Shorts)
= 10 uploads, all Made for Kids.

Safety (never skipped):
  * quality_check.py must pass for a video to be uploaded
  * a video whose Quran/hadith source is not in config/approved_sources.json is NOT uploaded;
    it waits in reports/waiting_for_approval.md until the reviewer adds that source (one-time list)
  * the uploads ledger stops duplicates, so re-running a day is always safe

Usage:
  python scripts/daily.py                 (today's day, from the plan start date, in IST)
  python scripts/daily.py --day 12        (a specific day)
  python scripts/daily.py --day 12 --no-upload --test
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys

import auto_song
import plan
from common import load_json, load_settings, path, save_json

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))


def run(args):
    print("+", " ".join(args), flush=True)
    return subprocess.run([sys.executable] + args).returncode == 0


def approved_sources():
    p = path("config", "approved_sources.json")
    return set(load_json(p)["approved"]) if os.path.exists(p) else set()


def needs_approval(src):
    return not src.startswith(("No religious", "Arabic"))


def song_for(row, short_original=False):
    """Use a hand-made song folder if one exists for this topic, otherwise generate one."""
    manual = path("content", "songs", auto_song.slugify(row["item"]["en"]))
    if not short_original and os.path.exists(os.path.join(manual, "song.json")):
        return os.path.basename(manual)
    song, sb = auto_song.build(row, short_original=short_original)
    return auto_song.write(song, sb)


def publish_time(date, hhmm):
    h, m = map(int, hhmm.split(":"))
    local = dt.datetime(date.year, date.month, date.day, h, m, tzinfo=IST)
    return local.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", type=int)
    ap.add_argument("--no-upload", action="store_true")
    ap.add_argument("--test", action="store_true", help="12-second renders (fast check)")
    a = ap.parse_args()

    settings = load_settings()
    day = a.day or plan.day_for(dt.datetime.now(IST).date())
    if not 1 <= day <= plan.DAYS:
        print(f"Day {day} is outside the 1,000-day plan (starts {plan.START}). Nothing to do.")
        return 0
    rows = {r["slot"]: r for r in plan.get_day(day)}
    approved = approved_sources()
    extra = ["--seconds", "12"] if a.test else []
    report = {"day": day, "date": str(rows["Long-A"]["date"].date() if hasattr(rows["Long-A"]["date"], "date") else rows["Long-A"]["date"]),
              "items": []}
    ok_all = True

    jobs = [("Long-A", "Short-1", False), ("Long-B", "Short-2", False), ("Short-3", None, True)]
    # 1) write the songs and their original music
    sids, music_ok = {}, {}
    for slot, _short, original in jobs:
        sids[slot] = song_for(rows[slot], short_original=original)
        music_ok[slot] = run(["scripts/generate_music.py", sids[slot]])
    # 2) real singing for all of today's songs in ONE free Kaggle GPU run (skipped if no Kaggle secrets)
    if not a.test:
        run(["scripts/sing_kaggle.py"] + [sids[s] for s, ok in music_ok.items() if ok])
    # 3) voice, video, checks and upload, song by song
    for slot, short_slot, original in jobs:
        row = rows[slot]
        sid = sids[slot]
        print(f"\n===== Day {day} {slot}: {sid} =====", flush=True)
        good = music_ok[slot] and run(["scripts/generate_voice.py", sid])
        for lang in settings["languages"]:
            if not original:
                good = good and run(["scripts/render_animatic.py", sid, "--lang", lang] + extra)
                good = good and run(["scripts/render_animatic.py", sid, "--lang", lang, "--short", "singalong"] + extra)
            else:
                good = good and run(["scripts/render_animatic.py", sid, "--lang", lang, "--short", "original"] + extra)
        if not original:
            good = good and run(["scripts/generate_thumbnail.py", sid])
        qc = (not a.test) and run(["scripts/quality_check.py", sid])
        src = row["item"]["src"]
        religious_ok = (not needs_approval(src)) or src in approved
        entry = {"slot": slot, "song_id": sid, "built": good, "qc": qc, "source": src, "source_approved": religious_ok, "uploaded": False}
        if good and qc and religious_ok and not a.no_upload:
            post = row["post"]
            for lang, when in zip(("en", "hi"), post):
                if lang not in settings["languages"]:
                    continue  # English-only channel: skip languages that are switched off
                args = ["scripts/upload_youtube.py", sid, "--lang", lang, "--what", "all" if not original else "original"]
                if settings["youtube"]["api_project_audited"]:
                    args += ["--publish-at", publish_time(rows[slot]["date"], when)]
                entry["uploaded"] = run(args) or entry["uploaded"]
            if short_slot:
                pass  # the sing-along Short was uploaded together with its episode ("--what all")
        ok_all = ok_all and good
        report["items"].append(entry)

    os.makedirs(path("reports"), exist_ok=True)
    save_json(path("reports", f"day-{day:04d}.json"), report)
    waiting = [i for i in report["items"] if not i["source_approved"]]
    if waiting:
        with open(path("reports", "waiting_for_approval.md"), "a", encoding="utf-8") as f:
            for i in waiting:
                f.write(f"- Day {day} {i['slot']} `{i['song_id']}`: add \"{i['source']}\" to config/approved_sources.json after checking it\n")
    print(json.dumps(report, indent=1, default=str))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
