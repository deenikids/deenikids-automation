"""Runs ON KAGGLE (free T4/P100 GPU). Started automatically by scripts/sing_kaggle.py.

Reads the day's jobs from the attached dataset (our original instrumentals + lyrics) and uses
ACE-Step 1.5 (MIT licence) in COVER mode: it keeps our melody, tempo and song structure and adds
a real sung vocal with the lyrics. Output files go to /kaggle/working/out/<song_id>_<lang>.<ext>.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import traceback

_jobs = sorted(glob.glob("/kaggle/input/**/jobs.json", recursive=True))  # Kaggle nests datasets (e.g. /kaggle/input/datasets/<user>/<slug>/)
IN = os.path.dirname(_jobs[0]) if _jobs else sorted(glob.glob("/kaggle/input/*"))[0]
print("Input folder:", IN, flush=True)
OUT = "/kaggle/working/out"
ACE = "/tmp/ace"  # not in /kaggle/working: everything there is downloaded back as output
os.makedirs(OUT, exist_ok=True)

if os.environ.get("DEENI_INNER") != "1":
    # Kaggle runs Python 3.13; ACE-Step needs 3.11-3.12 and installs with uv (its README: `uv sync`).
    # So: clone, `uv sync` (uv fetches Python 3.12 itself), then re-run this same file inside that environment.
    def run(cmd):
        print("+", cmd, flush=True)
        subprocess.run(cmd, shell=True, check=True)
    if not os.path.isdir(ACE):
        run(f"git clone --depth 1 https://github.com/ACE-Step/ACE-Step-1.5.git {ACE}")
    run("pip install -q uv")
    run(f"cd {ACE} && uv sync")
    me = "/tmp/sing_inner.py"
    shutil.copy(os.path.abspath(__file__), me)
    env = dict(os.environ, DEENI_INNER="1", ACESTEP_DTYPE="float32")  # T4 is pre-Ampere: float16 overflows to NaN
    sys.exit(subprocess.run(f"cd {ACE} && uv run python {me}", shell=True, env=env).returncode)

sys.path.insert(0, ACE)

from acestep.handler import AceStepHandler  # noqa: E402
from acestep.inference import GenerationConfig, GenerationParams, generate_music  # noqa: E402

dit = AceStepHandler()
dit.initialize_service(project_root=ACE, config_path="acestep-v15-turbo", device="cuda")
try:
    from acestep.llm_inference import LLMHandler  # the LM is skipped for cover tasks, but some versions want an object
    llm = LLMHandler()
except Exception:
    llm = None

CAPTION = ("cheerful children's nursery rhyme, preschool kids song, bright warm female vocal, clear simple pronunciation, "
           "ukulele, xylophone, soft hand claps, happy, major key, family friendly")
CAPTION_LULLABY = "gentle children's lullaby, soft warm female vocal, calm, slow, music box, soft pads, sleepy, major key"

jobs = json.load(open(os.path.join(IN, "jobs.json"), encoding="utf-8"))
log = []
for j in jobs:
    for lang, lyrics in j["lyrics"].items():
        dest_stub = os.path.join(OUT, f"{j['id']}_{lang}")
        ok = False
        for vocal_lang in ([lang, "unknown"] if lang != "en" else ["en"]):
            try:
                params = GenerationParams(
                    task_type="cover", src_audio=os.path.join(IN, f"{j['id']}.wav"),
                    caption=CAPTION_LULLABY if j.get("calm") else CAPTION, lyrics=lyrics, vocal_language=vocal_lang,
                    bpm=j["bpm"], keyscale=j.get("keyscale", "C Major"), duration=j["duration"], seed=j["seed"],
                    inference_steps=8, audio_cover_strength=0.85)
                cfg = GenerationConfig(batch_size=1, use_random_seed=False)
                tmp = f"/tmp/gen/{j['id']}_{lang}"
                res = generate_music(dit, llm, params, cfg, save_dir=tmp)
                if res.success and res.audios:
                    src = res.audios[0]["path"]
                    shutil.copy(src, dest_stub + os.path.splitext(src)[1])
                    ok = True
                    break
                log.append(f"{j['id']} {lang} ({vocal_lang}): {getattr(res, 'error', 'no audio')}")
            except Exception:
                log.append(f"{j['id']} {lang} ({vocal_lang}): {traceback.format_exc()[-800:]}")
        log.append(f"{j['id']} {lang}: {'OK' if ok else 'FAILED'}")
with open(os.path.join(OUT, "log.txt"), "w") as f:
    f.write("\n".join(log))
print("\n".join(log))
