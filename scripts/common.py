"""Shared helpers for the DEENIKIDS pipeline: paths, song loading, timing."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100  # audio sample rate
TAIL_SEC = 1.8  # ring-out after the last bar

NOTE_INDEX = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3, "E": 4, "F": 5,
              "F#": 6, "GB": 6, "G": 7, "G#": 8, "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}

CHORDS = {  # chord name -> semitone offsets from root, root note name
    "C": ("C", [0, 4, 7]), "Dm": ("D", [0, 3, 7]), "Em": ("E", [0, 3, 7]), "F": ("F", [0, 4, 7]),
    "G": ("G", [0, 4, 7]), "G7": ("G", [0, 4, 7, 10]), "Am": ("A", [0, 3, 7]),
}


def path(*parts):
    return os.path.join(ROOT, *parts)


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_json(p, data):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_settings():
    return load_json(path("config", "settings.json"))


def song_dir(song_id):
    return path("content", "songs", song_id)


def load_song(song_id):
    return load_json(os.path.join(song_dir(song_id), "song.json"))


def load_storyboard(song_id):
    return load_json(os.path.join(song_dir(song_id), "storyboard.json"))


def out_dir(song_id, *parts):
    d = path("output", song_id, *parts)
    os.makedirs(d, exist_ok=True)
    return d


def midi(note):
    """'C5' -> 72, 'F#4' -> 66."""
    m = re.fullmatch(r"([A-Ga-g][#bB]?)(-?\d)", note)
    if not m:
        raise ValueError(f"Bad note name: {note}")
    name = m.group(1).upper()
    return 12 * (int(m.group(2)) + 1) + NOTE_INDEX[name]


def hz(midi_num):
    return 440.0 * 2 ** ((midi_num - 69) / 12.0)


def parse_lead(text):
    """'E5:0.5 R:1 G5:2' -> [(midi or None, beats), ...]"""
    out = []
    for tok in text.split():
        name, beats = tok.split(":")
        out.append((None if name.upper() == "R" else midi(name), float(beats)))
    return out


def bar_seconds(song):
    return 4 * 60.0 / song["tempo_bpm"]


def song_length_sec(song):
    return len(song["bars"]) * bar_seconds(song) + TAIL_SEC


def validate_song(song):
    """Raise if any bar's notes don't add up to 4 beats or chords are unknown."""
    errors = []
    for i, bar in enumerate(song["bars"]):
        total = sum(b for _, b in parse_lead(bar["lead"]))
        if abs(total - 4.0) > 1e-6:
            errors.append(f"bar {i}: lead adds up to {total} beats, expected 4")
        if bar["chord"] not in CHORDS:
            errors.append(f"bar {i}: unknown chord {bar['chord']}")
    if errors:
        raise ValueError("Song data problems:\n  " + "\n  ".join(errors))


def lyric_cues(song, lang):
    """List of (start_sec, end_sec, text) for every bar that has a lyric in `lang` ('en' or 'hi')."""
    bs = bar_seconds(song)
    cues = []
    for i, bar in enumerate(song["bars"]):
        text = bar.get(lang)
        if text:
            cues.append((i * bs, (i + 1) * bs, text))
    return cues


def note_events(song):
    """Absolute (start_sec, dur_sec, midi, bar_index) for every lead note."""
    bs = bar_seconds(song)
    beat = bs / 4
    events = []
    for i, bar in enumerate(song["bars"]):
        t = i * bs
        for m, beats in parse_lead(bar["lead"]):
            if m is not None:
                events.append((t, beats * beat, m, i))
            t += beats * beat
    return events
