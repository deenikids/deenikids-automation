"""Give today's songs a real SUNG vocal, for free, using Kaggle's free GPU + ACE-Step 1.5 (MIT licence).

Flow (all automatic):
  1. upload today's instrumentals + lyrics to a private Kaggle dataset (deeni-sing-inputs)
  2. start the Kaggle notebook kaggle/sing_kernel.py on a free GPU
  3. wait for it, download the sung songs
  4. CHECK each one: same length as our song (so subtitles and scenes still line up) and the words are
     understandable (free Whisper speech recognition compares what it hears with our lyrics)
  5. passed -> output/<id>/audio/sung_<lang>.wav, which generate_voice.py then uses.
     failed or Kaggle unavailable -> nothing is written and the normal AI voice is used instead.

Needs GitHub Secrets KAGGLE_USERNAME and KAGGLE_KEY (free Kaggle account -> Settings -> API -> Create New Token).
Usage: python scripts/sing_kaggle.py <song_id> [<song_id> ...]
"""
import difflib
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

import hashlib

from common import ROOT, load_settings, load_song, out_dir, song_length_sec

MIN_WORD_MATCH = 0.35     # share of lyric words Whisper must recognise
MAX_LENGTH_DIFF = 2.0     # seconds


def sh(cmd, check=True):
    print("+", cmd, flush=True)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(r.stdout[-2000:], r.stderr[-2000:], flush=True)
    if check and r.returncode != 0:
        raise RuntimeError(cmd)
    return r


def lyrics_for(song, lang):
    """ACE-Step lyric format: [Verse]/[Chorus] blocks, one line per bar. Hindi uses Devanagari."""
    key = "hi_tts" if lang == "hi" else "en"
    blocks, cur, cur_sec = [], [], None
    names = {"verse1": "[Verse 1]", "verse2": "[Verse 2]", "verse3": "[Verse 3]", "chorus": "[Chorus]", "bridge": "[Bridge]",
             "intro": "[Intro]", "outro": "[Outro]"}
    for b in song["bars"]:
        sec = b["section"]
        if sec != cur_sec and cur:
            blocks.append(cur)
            cur = []
        if sec != cur_sec and b.get(key):
            cur.append(names.get(sec, "[Verse]"))
        cur_sec = sec
        if b.get(key):
            cur.append(b[key])
    if cur:
        blocks.append(cur)
    return "\n\n".join("\n".join(x) for x in blocks if len(x) > 1)


def words(text):
    return [w for w in re.findall(r"[\w']+", text.lower()) if len(w) > 1]


def understandable(path, song, lang):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("  faster-whisper not installed; cannot check words, rejecting to be safe")
        return False, 0.0
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(path, language="hi" if lang == "hi" else "en", vad_filter=True)
    heard = words(" ".join(s.text for s in segs))
    expected = set(words(" ".join(b.get("hi_tts" if lang == "hi" else "en", "") for b in song["bars"])))
    if not expected:
        return True, 1.0
    hit = sum(1 for w in expected if difflib.get_close_matches(w, heard, n=1, cutoff=0.75))
    score = hit / len(expected)
    return score >= MIN_WORD_MATCH, score


def main(song_ids):
    if not (os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY")):
        print("No Kaggle secrets: skipping real singing (the normal AI voice will be used).")
        return 0
    user = os.environ["KAGGLE_USERNAME"]
    settings = load_settings()
    work = tempfile.mkdtemp()
    data = os.path.join(work, "data")
    os.makedirs(data)
    jobs = []
    for sid in song_ids:
        song = load_song(sid)
        wav = os.path.join(out_dir(sid, "audio"), "instrumental.wav")
        shutil.copy(wav, os.path.join(data, f"{sid}.wav"))
        jobs.append({"id": sid, "bpm": song["tempo_bpm"], "duration": round(song_length_sec(song), 2),
                     "seed": int(hashlib.sha1(sid.encode()).hexdigest()[:6], 16), "calm": song["tempo_bpm"] <= 90,
                     "lyrics": {lang: lyrics_for(song, lang) for lang in settings["languages"]}})
    with open(os.path.join(data, "jobs.json"), "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=1)
    ds = f"{user}/deeni-sing-inputs"
    with open(os.path.join(data, "dataset-metadata.json"), "w") as f:
        json.dump({"title": "deeni-sing-inputs", "id": ds, "licenses": [{"name": "other"}]}, f)
    exists = sh(f"kaggle datasets status {ds}", check=False).returncode == 0
    if exists:
        sh(f'kaggle datasets version -p "{data}" -m "daily run" --dir-mode zip')
    else:
        sh(f'kaggle datasets create -p "{data}" --dir-mode zip')
    time.sleep(60)  # let Kaggle finish processing the new dataset version

    kern = os.path.join(work, "kernel")
    os.makedirs(kern)
    shutil.copy(os.path.join(ROOT, "kaggle", "sing_kernel.py"), os.path.join(kern, "sing_kernel.py"))
    with open(os.path.join(kern, "kernel-metadata.json"), "w") as f:
        json.dump({"id": f"{user}/deeni-sing", "title": "deeni-sing", "code_file": "sing_kernel.py", "language": "python",
                   "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
                   "dataset_sources": [ds], "competition_sources": [], "kernel_sources": []}, f)
    sh(f'kaggle kernels push -p "{kern}"')
    deadline = time.time() + 75 * 60
    status = ""
    while time.time() < deadline:
        time.sleep(60)
        status = sh(f"kaggle kernels status {user}/deeni-sing", check=False).stdout.lower()
        if "complete" in status or "error" in status or "cancel" in status:
            break
    if "complete" not in status:
        print(f"Kaggle run did not complete ({status.strip()}): using the normal AI voice.")
        return 0
    got = os.path.join(work, "got")
    os.makedirs(got)
    sh(f'kaggle kernels output {user}/deeni-sing -p "{got}"', check=False)
    for sid in song_ids:
        song = load_song(sid)
        target = song_length_sec(song)
        for lang in settings["languages"]:
            found = glob.glob(os.path.join(got, "**", f"{sid}_{lang}.*"), recursive=True)
            if not found:
                print(f"  {sid} {lang}: no sung file")
                continue
            dest = os.path.join(out_dir(sid, "audio"), f"sung_{lang}.wav")
            sh(f'ffmpeg -hide_banner -loglevel error -y -i "{found[0]}" -ar 44100 -ac 2 "{dest}"')
            dur = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{dest}"').stdout.strip() or 0)
            ok_len = abs(dur - target) <= MAX_LENGTH_DIFF
            ok_words, score = understandable(dest, song, lang) if ok_len else (False, 0.0)
            print(f"  {sid} {lang}: length {dur:.1f}s vs {target:.1f}s, words recognised {score:.0%}")
            if not (ok_len and ok_words):
                os.remove(dest)
                print("    -> rejected, normal AI voice will be used")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
