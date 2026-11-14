"""Make the vocal track for each language and mix it with the music.

Priority for each language:
  1. HUMAN RECORDING  audio/vocals/<song_id>/<lang>.wav  (recommended for songs)
     Record it while listening to output/<song_id>/audio/singer_guide.wav on headphones,
     starting at 0:00, so it lines up automatically.
  1b. REAL AI SINGING  output/<song_id>/audio/sung_<lang>.wav made by sing_kaggle.py (ACE-Step on Kaggle's
     free GPU), only if it passed the length + word checks.
  2. AI CHANT (free, Kokoro-82M, Apache-2.0) - each lyric line is spoken rhythmically at
     the start of its bar. Good for testing and for spoken parts; it does NOT sing.
  3. INSTRUMENTAL ONLY - if neither is available.

Outputs: output/<song_id>/audio/final_<lang>.wav and voice_manifest.json

Usage: python scripts/generate_voice.py bismillah-before-we-begin
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly

from common import SR, bar_seconds, load_settings, load_song, out_dir, path, save_json

KOKORO_SR = 24000


def read_wav(p):
    sr, raw = wavfile.read(p)
    data = raw.astype(np.float32)
    if raw.dtype.kind in "iu":  # 16-bit / 32-bit integer WAV
        data /= float(np.iinfo(raw.dtype).max)
    if data.ndim == 1:
        data = np.stack([data, data], axis=1)
    if sr != SR:
        g = np.gcd(SR, sr)
        data = resample_poly(data, SR // g, sr // g, axis=0)
    return data[:, :2]


def write_wav(p, stereo, peak_db=-1.0):
    peak = np.max(np.abs(stereo)) or 1.0
    stereo = stereo / peak * (10 ** (peak_db / 20))
    wavfile.write(p, SR, (np.clip(stereo, -1, 1) * 32767).astype(np.int16))


def apply_pronunciations(text, lang, settings):
    """Kokoro/misaki accepts [word](/IPA/) to force a pronunciation of Islamic terms."""
    for word, ipa in settings["tts"]["pronunciations"].get(lang, {}).items():
        text = text.replace(word, f"[{word}](/{ipa}/)")
    return text


def kokoro_chant(song, lang, settings, length):
    """Return a stereo vocal track made with Kokoro, or None if Kokoro isn't installed."""
    try:
        from kokoro import KPipeline
    except ImportError:
        print("  Kokoro not installed - skipping AI voice")
        return None
    cfg = settings["tts"][lang]
    pipe = KPipeline(lang_code=cfg["lang_code"])
    bs = bar_seconds(song)
    track = np.zeros(int(length * SR), np.float32)
    text_key = "hi_tts" if lang == "hi" else "en"
    for i, bar in enumerate(song["bars"]):
        text = bar.get(text_key)
        if not text:
            continue
        text = apply_pronunciations(text, lang, settings)
        speed = cfg["speed"]
        for _attempt in range(3):  # speed up if the line doesn't fit in its bar
            chunks = [np.asarray(audio, dtype=np.float32) for _, _, audio in pipe(text, voice=cfg["voice"], speed=speed)]
            if not chunks:
                break
            clip = resample_poly(np.concatenate(chunks), 147, 80)  # 24 kHz -> 44.1 kHz
            if len(clip) / SR <= bs * 0.95:
                break
            speed *= (len(clip) / SR) / (bs * 0.92)
        else:
            clip = clip[: int(bs * 0.95 * SR)]
        start = int((i * bs + 0.04) * SR)
        end = min(len(track), start + len(clip))
        track[start:end] += clip[: end - start]
    return np.stack([track, track], axis=1)


def main(song_id):
    song = load_song(song_id)
    settings = load_settings()
    d = out_dir(song_id, "audio")
    backing = read_wav(f"{d}/backing.wav")
    lead = read_wav(f"{d}/lead.wav")
    manifest = {}
    for lang in settings["languages"]:
        human = path("audio", "vocals", song_id, f"{lang}.wav")
        sung = os.path.join(d, f"sung_{lang}.wav")
        vocals, mode = None, "instrumental"
        if not os.path.exists(human) and os.path.exists(sung):
            # Real singing from ACE-Step (already mixed with music and checked by sing_kaggle.py)
            mix = read_wav(sung)
            n = len(backing)
            full = np.zeros_like(backing)
            full[: min(n, len(mix))] = mix[:n]
            write_wav(f"{d}/final_{lang}.wav", full)
            manifest[lang] = "sung_ai"
            print(f"  {lang}: sung_ai")
            continue
        if os.path.exists(human):
            vocals, mode = read_wav(human), "human"
        elif settings["tts"]["enabled"]:
            vocals = kokoro_chant(song, lang, settings, len(backing) / SR)
            mode = "ai_chant" if vocals is not None else "instrumental"
        if vocals is not None:
            n = len(backing)
            v = np.zeros_like(backing)
            v[: min(n, len(vocals))] = vocals[:n]
            v = v / (np.max(np.abs(v)) or 1) * 0.9
            mix = backing + lead * 0.45 + v
        else:
            mix = backing + lead
        write_wav(f"{d}/final_{lang}.wav", mix)
        manifest[lang] = mode
        print(f"  {lang}: {mode}")
    save_json(f"{d}/voice_manifest.json", manifest)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bismillah-before-we-begin")
