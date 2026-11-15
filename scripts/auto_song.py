"""Turn one plan slot into a complete song folder (song.json + storyboard.json), automatically and for free.

- Lyrics: from tested templates per series (English + Roman Hinglish), filled with the topic's
  word and its curated lesson line. Templates make NO religious claims of their own: the only
  religious content is the lesson line + source that sit in plan_data.py (reviewed once).
- Melody: a new ORIGINAL melody per episode, generated from a seed (the episode id), in a
  major key, with a repeating chorus hook. Same seed = same song, so reruns are identical.
- Hindi/Urdu voice text: Roman Hinglish converted to Devanagari for the free Kokoro Hindi voice.

Usage: python scripts/auto_song.py <day> <slot>    e.g. 12 Long-A
"""
import hashlib
import json
import os
import random
import re
import sys

from common import CHORDS, path
from plan_data import AR_DIGITS, AR_LETTERS, AR_NAMES, BASICS_EMOJI, EMOJI, LETTERS, SERIES_EMOJI

PROGRESSIONS = [["C", "G", "Am", "F"], ["C", "F", "G", "C"], ["Am", "F", "C", "G"], ["C", "Am", "F", "G"], ["F", "G", "C", "Am"],
                ["C", "F", "Am", "G"], ["C", "Em", "F", "G"]]
RHYTHMS = [[1, 1, 1, 1], [0.5, 0.5, 1, 1, 1], [1, 0.5, 0.5, 1, 1], [0.5, 0.5, 0.5, 0.5, 1, 1], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1],
           [1, 1, 2], [0.5, 0.5, 1, 2], [0.5, 0.5, 0.5, 0.5, 2]]
SCALE = [67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]  # G4..C6 in C major
NAMES = {0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B"}


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def note_name(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


# ------------------------------------------------------------------ melody
def chord_tones(ch):
    root, offs = CHORDS[ch]
    pcs = {( {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[root] + o) % 12 for o in offs}
    return [m for m in SCALE if m % 12 in pcs]


def bar_melody(rng, chord, prev, long_end=False):
    rhythm = [0.5, 0.5, 1, 2] if long_end else rng.choice(RHYTHMS)
    notes, t = [], 0.0
    tones = chord_tones(chord)
    for k, b in enumerate(rhythm):
        strong = t in (0.0, 2.0) or k == len(rhythm) - 1
        if strong:
            m = min(tones, key=lambda x: abs(x - prev) + rng.random() * 3)
        else:
            i = SCALE.index(min(SCALE, key=lambda x: abs(x - prev)))
            i = max(0, min(len(SCALE) - 1, i + rng.choice([-2, -1, 1, 1, 2])))
            m = SCALE[i]
        notes.append(f"{note_name(m)}:{b:g}")
        prev, t = m, t + b
    return " ".join(notes), prev


def make_melodies(seed):
    rng = random.Random(seed)
    prog_v, prog_c = rng.choice(PROGRESSIONS), rng.choice(PROGRESSIONS)
    prev = 76
    verse, chorus = [], []
    for k in range(4):
        mel, prev = bar_melody(rng, prog_v[k], prev, long_end=(k == 3))
        verse.append((prog_v[k], mel))
    prev = 79
    hook, prev = bar_melody(rng, prog_c[0], prev)
    for k in range(4):
        if k == 2:
            mel = hook  # the hook comes back on line 3: catchy repetition
        else:
            mel, prev = bar_melody(rng, prog_c[k], prev, long_end=(k == 3))
        chorus.append((prog_c[k], hook if k == 0 else mel))
    tempo = rng.choice([100, 104, 108, 112, 116])
    transpose = rng.choice([0, 2, -3, 5, -1])
    return verse, chorus, tempo, transpose, rng


# ------------------------------------------------------------------ lyrics
V1_EN = [["Hello friends, come sing with me,", "Today we learn about {S}!", "Ali and Mina, one, two, three,", "Deeni and Bubbles, happy as can be!"],
         ["Clap your hands and tap your feet,", "Let's learn {S}, it's so sweet!", "Deeni swims and Bubbles spins,", "Here we go, the song begins!"],
         ["Are you ready? Here we go!", "{S}, we want to know!", "Sing it loud and sing it slow,", "Deeni and friends, on with the show!"]]
V1_HI = [["Aao dosto, gaao saath,", "Aaj seekhenge {S} ki baat!", "Ali, Mina, ek do teen,", "Deeni Bubbles khush aur haseen!"],
         ["Taali bajao, pair hilao,", "{S} seekho, saath mein gaao!", "Deeni tairey, Bubbles ghoome,", "Gaana shuru, sab mil ke jhoome!"],
         ["Taiyaar ho? Chalo chalein!", "{S} ko hum seekh lein!", "Zor se gaao, dheere gaao,", "Deeni ke saath mauj manao!"]]
V2 = {
    "dua": (["{L}!", "We say it softly every day,", "{W}, {W},", "That's a lovely Muslim way!"],
            ["{Lh}!", "Roz isey pyaar se bolein,", "{W}, {W},", "Achhi aadat apna lein!"]),
    "arabic": (["Say it slowly, say it clear,", "{W}, {W}, now you hear!", "{L}!", "Arabic is fun, my dear!"],
               ["Dheere bolo, saaf bolo,", "{W}, {W}, munh kholo!", "{Lh}!", "Arabic seekhna mazedaar, bolo!"]),
    "values": (["When we're kind and when we're true,", "Our hearts feel happy, yours will too!", "{L}!", "That's what little Muslims do!"],
               ["Sach bolein aur pyaar karein,", "Sab ke dil khush rakhein,", "{Lh}!", "Achhe bachche yehi karein!"]),
    "preschool": (["Look around, what can you see?", "{W}! Allah made it for you and me!", "{L}!", "Learning is as fun as can be!"],
                  ["Dekho dekho, kya hai yahaan?", "{W}! Allah ne banaya jahaan!", "{Lh}!", "Seekhna hai kitna aasaan!"]),
    "basics": (["Little Muslims, come and see,", "Learning Islam happily!", "{L}!", "Say it with your family!"],
               ["Chhote Muslim, aao dekho,", "Islam ki baatein seekho,", "{Lh}!", "Ghar walon ke saath bolo!"]),
    "adventure": (["Off we go, a brand new place,", "With a smile on every face!", "{L}!", "Deeni and Bubbles, what a race!"],
                  ["Chalo chalein nayi jagah,", "Muskurahat har taraf yahaan!", "{Lh}!", "Deeni Bubbles ki mauj wahaan!"]),
    "sea": (["Splish and splash, down in the sea,", "The {W} swims with Deeni!", "{L}!", "Bubbles float up, one, two, three!"],
            ["Chhap chhap, samundar mein,", "{W} tairey Deeni ke saath mein!", "{Lh}!", "Bulbule upar, ek do teen!"]),
    "lullaby": (["Sleepy eyes and stars so bright,", "The moon is shining soft and white,", "{L}.", "Goodnight, goodnight, sleep tight tonight."],
                ["Neend bhari aankhein, taare chamkein,", "Chanda mama dheere damkein,", "{Lh}.", "Shab bakhair, ab so jao tum."]),
    "ramadan": (["The crescent moon is shining bright,", "Ramadan is here tonight!", "{L}!", "Little Muslims, what a sight!"],
                ["Chaand chamakta aasmaan mein,", "Ramzan aaya hamare ghar mein!", "{Lh}!", "Khushiyan hain sab ke dil mein!"]),
    "hajj": (["Labbaik, the pilgrims say,", "To the Kaaba, far away,", "{L}!", "Allahu Akbar, we all say!"],
             ["Labbaik bolein haaji saare,", "Kaaba ki taraf chalein pyaare,", "{Lh}!", "Allahu Akbar, mil ke pukaarein!"]),
    "eid": (["Eid Mubarak, here we are!", "Hugs and smiles from near and far!", "{L}!", "Every friend is a shining star!"],
            ["Eid Mubarak, aayi Eid,", "Gale milo sab, khushi ki Eid!", "{Lh}!", "Mithai baanto, meethi Eid!"]),
}
CH_EN = [("Sing it with me, one, two, three!", "Deeni and friends sing happily!"), ("Clap your hands and sing along!", "This is our happy song!"),
         ("Jump up high and touch the sky!", "Wave your hands and say hi!")]
CH_HI = [("Mere saath gaao, ek do teen!", "Deeni aur dost gaayein haseen!"), ("Taali bajao, saath mein gaao!", "Khushi ka gaana, sab dohraao!"),
         ("Upar uchhlo, aasmaan chhoo lo!", "Haath hilaao, salaam bolo!")]
LULL_CH = (["{W}, {W},", "Close your eyes and rest,", "{W}, {W},", "Sleep is the very best."],
           ["{W}, {W},", "Aankhein band karo,", "{W}, {W},", "Aaram se so jao."])
BRIDGE = {
    "quiz": (["Quiz time! Are you ready?", "What did we learn today?", "Yes! {W}!", "Great job, little star!"],
             ["Quiz ka waqt! Taiyaar ho?", "Aaj kya seekha, batao?", "Haan! {W}!", "Shabaash, chhote sitaare!"]),
    "story": (["Once upon a time, Ali forgot,", "Then Mina helped a lot:", "\"Remember: {L}!\"", "Ali smiled: \"Thank you a lot!\""],
              ["Ek din Ali bhool gaya,", "Mina ne pyaar se kaha:", "\"Yaad rakho: {Lh}!\"", "Ali bola: \"Shukriya!\""]),
    "plain": (["Now let's say it all together,", "{W}! {W}!", "{L}!", "Hooray, we did it together!"],
              ["Ab mil kar sab bolo,", "{W}! {W}!", "{Lh}!", "Hooray, humne kar dikhaaya!"]),
}
V3 = (["Now let's sing it one more time,", "Faster, faster, keep the rhyme!", "{W}, {W},", "Everybody, feeling fine!"],
      ["Ek baar phir se gaao,", "Tez tez, sur milao!", "{W}, {W},", "Sab mil kar khushi manao!"])

DEVA_FIX = {"allah": "अल्लाह", "bismillah": "बिस्मिल्लाह", "alhamdulillah": "अल्हम्दुलिल्लाह", "inshaallah": "इंशाअल्लाह",
            "mashaallah": "माशाअल्लाह", "subhanallah": "सुब्हानअल्लाह", "astaghfirullah": "अस्तग़फ़िरुल्लाह", "deeni": "दीनी",
            "bubbly": "बबली", "ayaan": "अयान", "amira": "अमीरा", "ammi": "अम्मी", "abbu": "अब्बू", "ramzan": "रमज़ान", "eid": "ईद",
            "mubarak": "मुबारक", "quran": "क़ुरआन", "masjid": "मस्जिद", "salaam": "सलाम", "dua": "दुआ", "sabr": "सब्र",
            "shabaash": "शाबाश", "quiz": "क्विज़", "hooray": "हुर्रे", "labbaik": "लब्बैक", "kaaba": "काबा", "akbar": "अकबर",
            "allahu": "अल्लाहु", "hai": "है", "hain": "हैं", "mein": "में", "nahi": "नहीं", "haan": "हाँ", "ek": "एक", "do": "दो",
            "teen": "तीन", "ki": "की", "ka": "का", "ke": "के", "se": "से", "ko": "को", "aur": "और", "sab": "सब"}


def to_devanagari(text):
    """Roman Hinglish -> Devanagari for the Hindi voice. Good enough for TTS; not for display."""
    try:
        from indic_transliteration import sanscript
        from indic_transliteration.sanscript import transliterate
    except ImportError:
        return text
    out = []
    for tok in re.findall(r"[A-Za-z']+|[^A-Za-z']+", text):
        if not re.match(r"[A-Za-z]", tok):
            out.append(tok)
            continue
        low = tok.lower().replace("'", "")
        if low in DEVA_FIX:
            out.append(DEVA_FIX[low])
            continue
        w = re.sub(r"ein$", "eM", low)
        w = re.sub(r"ain$", "aiM", w)
        w = re.sub(r"([^aeiou])i$", r"\1ii", w)
        w = re.sub(r"([^aeiou])a$", r"\1aa", w) if len(w) > 2 else w
        d = transliterate(w, sanscript.ITRANS, sanscript.DEVANAGARI)
        out.append(d.rstrip("्"))
    return "".join(out)


# ------------------------------------------------------------------ visuals
def visual(series, it):
    en = it["en"]
    v = {"emoji": None, "arabic": None}
    m = re.match(r"Arabic Letter (\w+)", en)
    if m and m.group(1) in LETTERS:
        v["arabic"] = AR_LETTERS[LETTERS.index(m.group(1))]
        return v
    m = re.match(r"Arabic Number (\d+)", en)
    if m:
        v["arabic"] = AR_DIGITS[int(m.group(1)) - 1]
        return v
    for name, ar in AR_NAMES.items():
        if name in en:
            v["arabic"] = ar
            return v
    if en in EMOJI:
        v["emoji"] = EMOJI[en]
        return v
    for key in sorted(EMOJI, key=len, reverse=True):
        if re.search(r"\b" + re.escape(key) + r"\b", en):
            v["emoji"] = EMOJI[key]
            return v
    for key, e in BASICS_EMOJI.items():
        if key.lower() in en.lower():
            v["emoji"] = e
            return v
    v["emoji"] = SERIES_EMOJI.get(series.split(": ")[0])
    return v


def kind_of(series, event_kind):
    if event_kind in ("ramadan", "pre_ramadan"):
        return "ramadan"
    if event_kind == "hajj":
        return "hajj"
    if event_kind in ("eid_fitr", "eid_adha"):
        return "eid"
    return {"Dua & Routine Songs": "dua", "Arabic for Little Ones": "arabic", "Values & Big Feelings": "values",
            "Allah Made It! (Preschool)": "preschool", "Islamic Basics & Surahs": "basics", "Deeni & Bubbles Adventures": "adventure",
            "Under the Sea with Deeni": "sea", "Bedtime Lullabies": "lullaby"}.get(series, "dua" if "Dua" in series or "Quiz" in series else "basics")


def fill(lines, W, L, Lh, S):
    return [ln.format(W=W, L=L, Lh=Lh, S=S) for ln in lines]


# ------------------------------------------------------------------ build
def build(row, short_original=False):
    it = row["item"]
    seed = int(hashlib.sha1(row["episode"].encode()).hexdigest()[:8], 16)
    verse, chorus, tempo, transpose, rng = make_melodies(seed)
    kind = kind_of(row["series"], row.get("kind"))
    W = it["te"].rstrip("!").strip()
    Wh = it["th"].rstrip("!").strip()
    L, Lh = it["lesson"], it["hi"]
    S, Sh = W, Wh
    if kind == "values":
        S = re.sub(r" (at|in) .*$", "", it["en"]).replace("Big Feelings: ", "feeling ")
        Sh = re.sub(r" (Ghar Par|Park Mein|Masjid Mein|School Mein|Bazaar Mein)$", "", it["hi"])
    elif kind in ("basics", "ramadan", "hajj", "eid"):
        S = it["en"].split(": ")[-1] if kind != "basics" else it["en"].split(":")[0]
        Sh = it["hi"].split(": ")[-1] if kind != "basics" else it["hi"].split(":")[0]
    var = seed % 3
    fmt = (it.get("fe") or "").lower()
    bridge_key = "quiz" if "quiz" in fmt else ("story" if "story" in fmt or "forgets" in fmt or "role" in fmt else "plain")
    if kind == "lullaby":
        tempo, ch_en, ch_hi = 76, fill(LULL_CH[0], W, L, Lh, S), fill(LULL_CH[1], Wh, L, Lh, Sh)
    else:
        a, b = CH_EN[var]
        ah, bh = CH_HI[var]
        ch_en, ch_hi = [f"{W}, {W}!", a, f"{W}, {W}!", b], [f"{Wh}, {Wh}!", ah, f"{Wh}, {Wh}!", bh]
    v1_en, v1_hi = fill(V1_EN[var], W, L, Lh, S), fill(V1_HI[var], Wh, L, Lh, Sh)
    v2_en, v2_hi = fill(V2[kind][0], W, L, Lh, S), fill(V2[kind][1], Wh, L, Lh, Sh)
    br_en, br_hi = fill(BRIDGE[bridge_key][0], W, L, Lh, S), fill(BRIDGE[bridge_key][1], Wh, L, Lh, Sh)
    v3_en, v3_hi = fill(V3[0], W, L, Lh, S), fill(V3[1], Wh, L, Lh, Sh)

    bars = []

    def add(section, mel, en=None, hi=None):
        for k, (ch, lead) in enumerate(mel):
            b = {"section": section, "chord": ch, "lead": lead}
            if en:
                b.update(en=en[k], hi=hi[k], hi_tts=to_devanagari(hi[k]))
            bars.append(b)

    if short_original:
        add("intro_instrumental", chorus[:1])
        add("chorus", chorus, ch_en, ch_hi)
        add("verse1", verse, v2_en, v2_hi)
        add("chorus", chorus, ch_en, ch_hi)
        add("ending", [(chorus[0][0], "C6:4")])
    else:
        add("intro_instrumental", chorus[:2])
        add("verse1", verse, v1_en, v1_hi)
        add("chorus", chorus, ch_en, ch_hi)
        add("verse2", verse, v2_en, v2_hi)
        add("chorus", chorus, ch_en, ch_hi)
        add("bridge", verse, br_en, br_hi)
        add("chorus", chorus, ch_en, ch_hi)
        add("interlude", chorus[2:])
        add("verse3", verse, v3_en, v3_hi)
        add("chorus", chorus, ch_en, ch_hi)
        add("chorus", chorus, ch_en, ch_hi)
        add("ending", [(chorus[0][0], chorus[0][1]), (chorus[3][0], "C6:4")])
    # last bar must hold a long note on the tonic of its chord
    bars[-1]["lead"] = "C6:4" if bars[-1]["chord"] in ("C", "Am", "F") else "B5:4"

    sid = f"{row['episode'].lower()}-{slugify(it['en'])}"
    meta = row.get("meta", {})
    song = {
        "id": sid, "auto": True, "plan_day": row["day"], "slot": row["slot"], "series": row["series"],
        "title_en": it["en"], "title_hi": it["hi"], "lesson": L, "tempo_bpm": tempo, "transpose": transpose,
        "key": "C major (transposed)", "time_signature": "4/4",
        "religious_sources": [] if it["src"].startswith(("No religious", "Arabic")) else [{"reference": it["src"]}],
        "source_text": it["src"],
        "review": {"mode": "auto", "note": "Religious sources are checked against config/approved_sources.json before upload"},
        "visual": visual(row["series"], it), "word_en": W + "!", "word_hi": Wh + "!",
        "bars": bars,
        "youtube": {
            "en": {"title": meta.get("en_title", it["en"]), "description": meta.get("en_desc", it["en"]), "tags": meta.get("en_tags", "").split(", "), "language": "en"},
            "hi": {"title": meta.get("hi_title", it["hi"]), "description": meta.get("hi_desc", it["hi"]), "tags": meta.get("hi_tags", "").split(", "), "language": "hi"},
        },
    }
    return song, storyboard(song, kind, rng, short_original)


BG_BY_KIND = {"dua": ["kitchen", "home"], "arabic": ["home", "stage_green"], "values": ["home", "kitchen"], "preschool": ["home", "ocean"],
              "basics": ["masjid", "home"], "adventure": ["ocean", "home"], "sea": ["ocean", "ocean"], "lullaby": ["night", "night"],
              "ramadan": ["night", "masjid"], "hajj": ["masjid", "stage_green"], "eid": ["stage_pink", "home"]}
CAST = [("ayaan", 0.2, 0.74), ("amira", 0.4, 0.74), ("deeni", 0.62, 0.62), ("bubbly", 0.82, 0.76)]


def storyboard(song, kind, rng, short_original):
    bars = song["bars"]
    bg_a, bg_b = BG_BY_KIND.get(kind, ["home", "stage_green"])
    stages = ["stage_green", "stage_pink"] if kind != "lullaby" else ["night", "night"]
    scenes, start = [], 0
    word = {"text": song["word_en"], "text_hi": song["word_hi"], "arabic": song["visual"].get("arabic"), "emoji": song["visual"].get("emoji")}
    sections = []
    for i, b in enumerate(bars):
        if not sections or sections[-1][0] != b["section"] or b["section"] == "chorus" and i - sections[-1][1] >= 4:
            sections.append([b["section"], i])
    sections = [(s, a, (sections[k + 1][1] if k + 1 < len(sections) else len(bars) + 1)) for k, (s, a) in enumerate(sections)]
    chorus_n = 0
    calm = kind == "lullaby"
    for k, (sec, a, b) in enumerate(sections):
        sc = {"id": f"S{k + 1:02d}", "bars": [a, b], "camera": "slow_push_in" if calm else "static", "chars": [], "props": []}
        if sec == "intro_instrumental":
            sc.update(bg=bg_a, title_card=True)
            sc["chars"] = [{"name": "deeni", "x": 0.5, "y": 0.62, "action": "swim_in"}, {"name": "bubbly", "x": 0.82, "y": 0.75, "action": "bob" if calm else "wave"}]
        elif sec == "chorus":
            sc.update(bg=stages[chorus_n % 2] if not calm else "night", camera="slow_push_in" if calm else "beat_bounce", word=word)
            order = CAST if chorus_n % 2 == 0 else list(reversed(CAST))
            xs = [0.16, 0.38, 0.62, 0.84]
            sc["chars"] = [{"name": n, "x": xs[j], "y": y, "action": "bob" if calm else "dance"} for j, (n, _, y) in enumerate(order)]
            chorus_n += 1
        elif sec in ("verse1", "verse3"):
            sc.update(bg=bg_b if sec == "verse3" else bg_a)
            sc["chars"] = [{"name": "ayaan", "x": 0.26, "y": 0.7, "action": "sing" if not calm else "bob"},
                           {"name": "amira", "x": 0.5, "y": 0.7, "action": "sing" if not calm else "bob"},
                           {"name": "deeni", "x": 0.76, "y": 0.52, "action": "bob"}]
        elif sec == "verse2":
            sc.update(bg=bg_b, subject=word)
            sc["chars"] = [{"name": "bubbly", "x": 0.18, "y": 0.74, "action": "wave" if not calm else "bob"},
                           {"name": "amira", "x": 0.84, "y": 0.72, "action": "sing" if not calm else "bob"}]
        elif sec == "bridge":
            sc.update(bg=bg_a, subject=word, props=["question_mark"] if "Quiz" in bars[a].get("en", "") else [])
            sc["chars"] = [{"name": "bubbly", "x": 0.5, "y": 0.68, "action": "bob"},
                           {"name": "ayaan", "x": 0.2, "y": 0.74, "action": "happy" if not calm else "bob"},
                           {"name": "amira", "x": 0.8, "y": 0.74, "action": "happy" if not calm else "bob"}]
        elif sec == "interlude":
            sc.update(bg="ocean" if not calm else "night")
            sc["chars"] = [{"name": "bubbly", "x": 0.5, "y": 0.62, "action": "juggle" if not calm else "bob"}]
        else:  # ending
            sc.update(bg=stages[0], end_card=True)
            sc["chars"] = [{"name": n, "x": x, "y": y, "action": "wave" if not calm else "bob"} for n, x, y in CAST]
        scenes.append(sc)
    n = len(bars)
    ch_idx = [i for i, b in enumerate(bars) if b["section"] == "chorus"]
    shorts = []
    if short_original:
        shorts.append({"id": "original", "bars": [0, n], "title_en": f"{song['title_en']} 🤩 #shorts"[:100],
                       "title_hi": f"{song['title_hi']} 🤩 #shorts"[:100]})
    else:
        first = ch_idx[0]
        ten = f"{song['word_en']} {song['title_en']} Sing-Along 🎵 #shorts"
        thi = f"{song['word_hi']} {song['title_hi']} Saath Gaao 🎵 #shorts"
        shorts.append({"id": "singalong", "bars": [max(0, first - 4), min(n, first + 8)],
                       "title_en": ten if len(ten) <= 100 else f"{song['title_en']} Sing-Along 🎵 #shorts"[:100],
                       "title_hi": thi if len(thi) <= 100 else f"{song['title_hi']} Saath Gaao 🎵 #shorts"[:100]})
    return {"episode": song["id"], "fps": 24, "auto": True, "scenes": scenes, "shorts": shorts}


def write(song, sb):
    d = path("content", "songs", song["id"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "song.json"), "w", encoding="utf-8") as f:
        json.dump(song, f, ensure_ascii=False, indent=1)
    with open(os.path.join(d, "storyboard.json"), "w", encoding="utf-8") as f:
        json.dump(sb, f, ensure_ascii=False, indent=1)
    return song["id"]


if __name__ == "__main__":
    import plan
    day, slot = int(sys.argv[1]), sys.argv[2]
    row = next(r for r in plan.get_day(day) if r["slot"] == slot)
    song, sb = build(row, short_original=(slot == "Short-3"))
    print(write(song, sb))
