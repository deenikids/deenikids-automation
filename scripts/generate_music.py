"""Generate the ORIGINAL instrumental for a song from its song.json, using pure synthesis.

No samples, soundfonts or paid tools: every sound (marimba, ukulele, bass, drums,
bubbles) is generated with maths, so DEENIKIDS owns 100% of the result.

Outputs (in output/<song_id>/audio/):
  backing.wav       - drums + bass + ukulele chords (put vocals on top of this)
  lead.wav          - the melody line played on marimba
  instrumental.wav  - backing + lead (use when there are no vocals yet)
  singer_guide.wav  - lead + click track, for a human singer to record along to

Usage: python scripts/generate_music.py bismillah-before-we-begin
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter

from common import (CHORDS, NOTE_INDEX, SR, bar_seconds, hz, load_song, note_events,
                    out_dir, song_length_sec, validate_song)

RNG = np.random.default_rng(786)  # fixed seed -> identical output every run


def env_adsr(n, a=0.005, d=0.1, s=0.6, r=0.05):
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    e = np.full(n, s, dtype=np.float32)
    a_n = min(a_n, n)
    e[:a_n] = np.linspace(0, 1, a_n, endpoint=False)
    d_end = min(n, a_n + d_n)
    e[a_n:d_end] = np.linspace(1, s, d_end - a_n, endpoint=False)
    if r_n and n > r_n:
        e[-r_n:] *= np.linspace(1, 0, r_n)
    return e


def marimba(freq, dur):
    n = int((dur + 0.35) * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * freq * t) * np.exp(-t * 7)
    overtone = 0.35 * np.sin(2 * np.pi * freq * 3.98 * t) * np.exp(-t * 22)
    click = 0.15 * np.sin(2 * np.pi * freq * 9.2 * t) * np.exp(-t * 80)
    return (body + overtone + click).astype(np.float32)


def pluck(freq, dur, brightness=0.5):
    """Karplus-Strong plucked string (ukulele-like)."""
    n = int((dur + 0.6) * SR)
    period = max(2, int(round(SR / freq)))
    burst = np.zeros(n, dtype=np.float32)
    burst[:period] = RNG.uniform(-1, 1, period).astype(np.float32)
    burst[:period] = lfilter([brightness], [1, -(1 - brightness)], burst[:period])
    a = np.zeros(period + 2)
    a[0] = 1.0
    a[period] = -0.496
    a[period + 1] = -0.496
    return lfilter([1.0], a, burst).astype(np.float32)


def bass_note(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    w = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * 2 * freq * t)
    return (w * env_adsr(n, 0.01, 0.15, 0.7, 0.06)).astype(np.float32)


def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 110 * np.exp(-t * 18) + 45
    phase = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(phase) * np.exp(-t * 9)).astype(np.float32)


def clap():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    noise = RNG.uniform(-1, 1, n)
    noise = lfilter([1, -1], [1, -0.6], noise)  # crude high-pass
    e = np.exp(-t * 28)
    for k in (0.0, 0.012, 0.024):  # three quick hits = handclap
        e[int(k * SR):] += 0.5 * np.exp(-(t[int(k * SR):] - k) * 60)
    return (0.5 * noise * e).astype(np.float32)


def shaker():
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    noise = lfilter([1, -1], [1, -0.3], RNG.uniform(-1, 1, n))
    return (0.25 * noise * np.exp(-t * 60)).astype(np.float32)


def bubble():
    n = int(0.18 * SR)
    t = np.arange(n) / SR
    f = 500 + 2200 * t / t[-1]
    return (0.25 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)).astype(np.float32)


def add(buf, sig, start_sec, gain=1.0):
    i = int(start_sec * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += gain * sig[: j - i]


def to_stereo(mono, pan=0.0):
    left = mono * np.sqrt(0.5 * (1 - pan))
    right = mono * np.sqrt(0.5 * (1 + pan))
    return np.stack([left, right], axis=1)


def chord_midis(name, octave):
    root, offsets = CHORDS[name]
    base = 12 * (octave + 1) + NOTE_INDEX[root]
    return [base + o for o in offsets]


def write_wav(p, stereo, peak_db=-1.0):
    peak = np.max(np.abs(stereo)) or 1.0
    target = 10 ** (peak_db / 20)
    data = np.clip(stereo / peak * target, -1, 1)
    wavfile.write(p, SR, (data * 32767).astype(np.int16))


def build(song):
    validate_song(song)
    total = int(song_length_sec(song) * SR)
    bs = bar_seconds(song)
    beat = bs / 4
    drums = np.zeros(total, np.float32)
    bass = np.zeros(total, np.float32)
    uke = np.zeros(total, np.float32)
    lead = np.zeros(total, np.float32)
    click = np.zeros(total, np.float32)
    fx = np.zeros(total, np.float32)

    T = int(song.get("transpose", 0))  # key change for auto songs (semitones)
    n_bars = len(song["bars"])
    for i, bar in enumerate(song["bars"]):
        t0 = i * bs
        section = bar["section"]
        last = i == n_bars - 1
        # Drums: build-up in the first two bars, full groove after, single hit on the last bar
        calm = song.get("tempo_bpm", 108) <= 90
        if calm:
            pass  # lullabies: no drums
        elif last:
            add(drums, kick(), t0, 0.9)
        else:
            for b in range(4):
                if i >= 2 or b in (0, 2):
                    add(drums, kick(), t0 + b * beat, 0.9 if b in (0, 2) else 0.0)
                if i >= 2 and b in (1, 3):
                    add(drums, clap(), t0 + b * beat, 0.42)
            if i >= 2:
                for e in range(8):
                    add(drums, shaker(), t0 + e * beat / 2, 0.28 if e % 2 else 0.16)
        # Bass: root on beats 1 and 3 (just one long note on the last bar)
        root = chord_midis(bar["chord"], 2)[0] + T
        if last:
            add(bass, bass_note(hz(root), bs), t0, 0.8)
        else:
            add(bass, bass_note(hz(root), beat * 1.8), t0, 0.8)
            add(bass, bass_note(hz(root + 7 if section != "ending" else root), beat * 1.8), t0 + 2 * beat, 0.6)
        # Ukulele: strum pattern down / down-up / up-down-up (classic, not tied to any song)
        notes = [m + T for m in chord_midis(bar["chord"], 4)]
        pattern = [0, 1, 1.5, 2.5, 3, 3.5] if not last else [0]
        for k, p in enumerate(pattern):
            for s, m in enumerate(notes):
                add(uke, pluck(hz(m), beat), t0 + p * beat + s * 0.012, 0.32 if k == 0 else 0.22)
        # Click for the singer guide
        for b in range(4):
            add(click, marimba(2000 if b == 0 else 1500, 0.02)[: int(0.03 * SR)], t0 + b * beat, 0.3)
        # Bubble sound effects in ocean / interlude sections
        if section in ("intro_instrumental", "interlude") and song.get("tempo_bpm", 108) > 90:
            for b in (0.5, 1.75, 2.25, 3.5):
                add(fx, bubble(), t0 + b * beat, 0.6)

    for start, dur, m, _bar in note_events(song):
        add(lead, marimba(hz(m + T), dur), start, 0.9)

    backing = (to_stereo(drums, 0.0) * 0.75 + to_stereo(bass, 0.0) * 0.65 +
               to_stereo(uke, -0.3) * 0.7 + to_stereo(fx, 0.4) * 0.6)
    lead_st = to_stereo(lead, 0.15)
    # Gentle fade-out over the tail
    fade = int(1.2 * SR)
    for arr in (backing, lead_st):
        arr[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return backing, lead_st, to_stereo(click, 0.0)


def main(song_id):
    song = load_song(song_id)
    backing, lead, click = build(song)
    d = out_dir(song_id, "audio")
    # Normalise all stems with the same factor so they stay balanced when mixed later
    full = backing + lead
    scale = (10 ** (-1 / 20)) / (np.max(np.abs(full)) or 1)
    write_wav(f"{d}/instrumental.wav", full * scale, peak_db=-1.0)
    wavfile.write(f"{d}/backing.wav", SR, (np.clip(backing * scale, -1, 1) * 32767).astype(np.int16))
    wavfile.write(f"{d}/lead.wav", SR, (np.clip(lead * scale, -1, 1) * 32767).astype(np.int16))
    write_wav(f"{d}/singer_guide.wav", lead + click * 0.6, peak_db=-3.0)
    print(f"Music written to {d} ({full.shape[0] / SR:.1f} s)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bismillah-before-we-begin")
