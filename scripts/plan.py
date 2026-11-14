"""Deeni & Friends 1,000-day plan: every day 2 NEW long videos + 3 NEW Shorts, each in English and Hinglish.

The same code builds the planning spreadsheet AND tells the daily GitHub workflow what to make:
    from plan import get_day ; get_day(1) -> 5 slot dicts for Day 1
"""
import datetime as dt

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from plan_data import *  # noqa

START = dt.date(2027, 1, 4)
DAYS = 1000
BRAND = "Deeni & Friends"
VERIFY = " [VERIFY]"

EVENTS = {
    2027: dict(ramadan=dt.date(2027, 2, 8), eid_fitr=dt.date(2027, 3, 9), dhul_hijjah=dt.date(2027, 5, 7), eid_adha=dt.date(2027, 5, 16), new_year=dt.date(2027, 6, 6)),
    2028: dict(ramadan=dt.date(2028, 1, 28), eid_fitr=dt.date(2028, 2, 26), dhul_hijjah=dt.date(2028, 4, 26), eid_adha=dt.date(2028, 5, 5), new_year=dt.date(2028, 5, 25)),
    2029: dict(ramadan=dt.date(2029, 1, 16), eid_fitr=dt.date(2029, 2, 14), dhul_hijjah=dt.date(2029, 4, 15), eid_adha=dt.date(2029, 4, 24), new_year=dt.date(2029, 5, 14)),
}

# weekday -> (series of Long-A, series of Long-B)
WHEEL = {0: ("Dua & Routine Songs", "Allah Made It! (Preschool)"), 1: ("Arabic for Little Ones", "Values & Big Feelings"),
         2: ("Islamic Basics & Surahs", "Deeni & Bubbly Adventures"), 3: ("Dua & Routine Songs", "Allah Made It! (Preschool)"),
         4: ("Islamic Basics & Surahs", "Values & Big Feelings"), 5: ("Arabic for Little Ones", "Deeni & Bubbly Adventures"),
         6: ("Under the Sea with Deeni", "Bedtime Lullabies")}
SERIES_HI = {"Dua & Routine Songs": "Duaon Ke Gaane", "Allah Made It! (Preschool)": "Allah Ne Banaya", "Arabic for Little Ones": "Chhoton Ki Arabic",
             "Values & Big Feelings": "Achhi Aadatein", "Islamic Basics & Surahs": "Islam Ki Buniyaad", "Deeni & Bubbly Adventures": "Deeni Aur Bubbly Ki Sair",
             "Under the Sea with Deeni": "Samundar Ke Dost", "Bedtime Lullabies": "Loriyan", "Ramadan with Deeni": "Deeni Ka Ramzan",
             "Hajj & Eid al-Adha": "Hajj Aur Bakra Eid", "Eid Specials": "Eid Special", "Shorts Originals": "Shorts"}
THUMB_BRIEF = {
    "Dua & Routine Songs": "Ayaan or Amira close-up, big happy smile, doing the action; bright yellow background; text top-left",
    "Allah Made It! (Preschool)": "The object/animal BIG and clear, Bubbly pointing at it; background in that colour; text in the same colour, navy outline",
    "Arabic for Little Ones": "Giant 3D Arabic letter/number centre, Deeni pointing; single bright colour background",
    "Values & Big Feelings": "One clear feeling on one face (never distorted), one prop that tells the story; soft warm background",
    "Islamic Basics & Surahs": "Amira with masjid/Quran/Kaaba icon (exterior only); calm green & gold palette",
    "Deeni & Bubbly Adventures": "Deeni & Bubbly mid-action in the new place, wide shot, sunny colours",
    "Under the Sea with Deeni": "Deeni next to the sea creature, both big; turquoise water, bubbles",
    "Bedtime Lullabies": "Sleepy character under stars/moon, dark blue & soft gold, calm (no bright text)",
    "Ramadan with Deeni": "Crescent moon + lanterns, purple-night palette, 'Day N' badge",
    "Hajj & Eid al-Adha": "Kaaba exterior silhouette, white & gold, sunny desert colours",
    "Eid Specials": "All 4 characters in Eid clothes, confetti, big 'Eid Mubarak!'",
}
HOOK = {
    "Dua & Routine Songs": "Ayaan stops: \"Wait! What do we say before {x}?\" — chorus starts in 2 s",
    "Allah Made It! (Preschool)": "Bubbly gasps: \"Look what Allah made!\" — {x} pops onto the screen",
    "Arabic for Little Ones": "Deeni bursts out of a giant {x}: \"Say it with me!\"",
    "Values & Big Feelings": "Amira's face changes: \"Uh-oh…\" — a tiny problem kids recognise ({x})",
    "Islamic Basics & Surahs": "Amira waves: \"Do you know {x}? Let's learn together!\"",
    "Deeni & Bubbly Adventures": "Splash! Deeni's bubble lands at the {x} — \"Adventure time!\"",
    "Under the Sea with Deeni": "Deeni swims up: \"Guess who lives under the sea… the {x}!\"",
    "Bedtime Lullabies": "Soft music, slow fade into a starry night: \"Shhh… time to sleep\"",
    "Ramadan with Deeni": "The crescent moon twinkles: \"Ramadan is here!\"",
    "Hajj & Eid al-Adha": "Takbeer bells ring: \"Let's go to Makkah!\"",
    "Eid Specials": "Confetti pop! \"EID MUBARAK!\" in the first second",
}
POST = {"Long-A": ("18:30", "17:30"), "Long-B": ("12:30", "11:30"), "Short-1": ("08:00", "09:00"), "Short-2": ("13:30", "14:30"),
        "Short-3": ("20:30", "21:30")}
BASE_TAGS_EN = ["islamic songs for kids", "muslim kids", "nursery rhymes", "kids songs", "islamic cartoon", "deeni and friends"]
BASE_TAGS_HI = ["bachon ki nazam", "islamic nazam for kids", "urdu islamic songs", "hindi islamic songs for kids", "bachon ke gaane", "deeni and friends"]


def season(d):
    for y in (d.year, d.year + 1):
        e = EVENTS.get(y)
        if e and e["ramadan"] - dt.timedelta(days=14) <= d < e["ramadan"]:
            return "pre_ramadan", (d - (e["ramadan"] - dt.timedelta(days=14))).days, y
    e = EVENTS.get(d.year)
    if e:
        if e["ramadan"] <= d < e["eid_fitr"]:
            return "ramadan", (d - e["ramadan"]).days, d.year
        if e["eid_fitr"] <= d < e["eid_fitr"] + dt.timedelta(days=3):
            return "eid_fitr", (d - e["eid_fitr"]).days, d.year
        if e["dhul_hijjah"] <= d < e["eid_adha"]:
            return "hajj", (d - e["dhul_hijjah"]).days, d.year
        if e["eid_adha"] <= d < e["eid_adha"] + dt.timedelta(days=3):
            return "eid_adha", (d - e["eid_adha"]).days, d.year
        if d == e["new_year"]:
            return "new_year", 0, d.year
    return None, None, None


class Counter:
    def __init__(self):
        self.n = {}

    def next(self, key):
        v = self.n.get(key, 0)
        self.n[key] = v + 1
        return v


def pick(series, c):
    """Return dict(en, hi, thumb_en, thumb_hi, lesson, source, fmt_en, fmt_hi, needs, key) for the next episode of a series."""
    n = c.next(series)
    if series == "Dua & Routine Songs":
        t = DUAS[n % len(DUAS)]
        f = DUA_FORMATS[(n // len(DUAS)) % len(DUA_FORMATS)]
        return dict(en=t[0], hi=t[1], te=t[2], th=t[3], lesson=t[4], src=t[5], fe=f[0], fh=f[1], needs="Auto; religious source must be in approved list", x=t[0].split(":")[0].lower())
    if series == "Arabic for Little Ones":
        t = ARABIC[n % len(ARABIC)]
        f = ARABIC_FORMATS[(n // len(ARABIC)) % len(ARABIC_FORMATS)]
        return dict(en=t[0], hi=t[1], te=t[2], th=t[3], lesson=t[4], src=t[5], fe=f[0], fh=f[1], needs="Auto; Arabic voice spot-check", x=t[2].rstrip("!"))
    if series == "Values & Big Feelings":
        t = VALUES[n % len(VALUES)]
        s = SETTINGS[(n // len(VALUES)) % len(SETTINGS)]
        f = VALUE_FORMATS[(n // (len(VALUES) * len(SETTINGS))) % len(VALUE_FORMATS)]
        return dict(en=f"{t[0]} {s[0]}", hi=f"{t[1]} {s[1]}", te=t[2], th=t[3], lesson=t[4], src=t[5], fe=f[0], fh=f[1], needs="Auto", x=t[0].lower())
    if series == "Allah Made It! (Preschool)":
        t = PRESCHOOL[n % len(PRESCHOOL)]
        f = PRESCHOOL_FORMATS[(n // len(PRESCHOOL)) % len(PRESCHOOL_FORMATS)]
        return dict(en=t[0], hi=t[1], te=t[2], th=t[3], lesson=t[4], src=t[5], fe=f[0], fh=f[1], needs="Auto", x=t[2].rstrip("!"))
    if series == "Islamic Basics & Surahs":
        t = BASICS[n % len(BASICS)]
        cyc = n // len(BASICS)
        if t[0].startswith("Learn Surah"):
            f = SURAH_FORMATS[cyc % len(SURAH_FORMATS)]
            needs = "Auto; religious source must be in approved list"
        else:
            f = BASICS_FORMATS[cyc % len(BASICS_FORMATS)]
            needs = "Auto; religious source must be in approved list"
        return dict(en=t[0], hi=t[1], te=t[2], th=t[3], lesson=t[4], src=t[5], fe=f[0], fh=f[1], needs=needs, x=t[0].split(":")[0])
    if series == "Deeni & Bubbly Adventures":
        p = PLACES[n % len(PLACES)]
        v = VALUES[(7 * (n % len(PLACES)) + n // len(PLACES)) % len(VALUES)]
        return dict(en=f"{p[0]} Adventure: {v[0]}", hi=f"{p[1]} Ki Sair: {v[1]}", te=f"{p[0]}!", th=f"{p[1]}!", lesson=v[4], src=v[5],
                    fe="Story + Song", fh="Kahani + Gaana", needs="Auto", x=p[0].lower())
    if series == "Under the Sea with Deeni":
        s = SEA[n % len(SEA)]
        f = SEA_FORMATS[(n // len(SEA)) % len(SEA_FORMATS)]
        return dict(en=f"Under the Sea: {s[0]}", hi=f"Samundar Ke Dost: {s[1]}", te=f"{s[0]}!", th=f"{s[1]}!", lesson=f"Learn about the {s[0].lower()}",
                    src=CREATOR, fe=f[0], fh=f[1], needs="Auto", x=s[0].lower())
    if series == "Bedtime Lullabies":
        lu = LULLABIES[n % len(LULLABIES)]
        sc = NIGHT_SCENES[(n // len(LULLABIES)) % len(NIGHT_SCENES)]
        return dict(en=f"{lu[0]} ({sc[0]})", hi=f"{lu[1]} ({sc[1]})", te="Sleepy Time", th="Neend Aayi", lesson="Calm down and get ready for sleep",
                    src=lu[2], fe="10-Min Calm Lullaby", fh="10 Minute Lori", needs="Auto", x="")
    raise ValueError(series)


def seasonal(kind, k, yr, slot):
    a = slot == "Long-A"
    if kind == "pre_ramadan":
        t = PRE_RAMADAN[k % len(PRE_RAMADAN)]
        fe, fh = ("Song", "Gaana") if a else ("Story", "Kahani")
        return "Ramadan with Deeni", dict(en=f"Ramadan {yr} Is Coming: {t[0]}", hi=f"Ramzan {yr} Aa Raha Hai: {t[1]}", te="Ramadan Soon!", th="Ramzan Aaya!",
                                          lesson="Get excited and ready for Ramadan", src="Quran 2:185", fe=fe, fh=fh, needs="Auto", x="")
    if kind == "ramadan":
        t = RAMADAN[(k * 2 + (0 if a else 1) + (yr - 2027) * 5) % len(RAMADAN)]
        fe, fh = ("Song", "Gaana") if a else (["Story", "Activity"][k % 2], ["Kahani", "Activity"][k % 2])
        return "Ramadan with Deeni", dict(en=f"Ramadan {yr} Day {k + 1}: {t[0]}", hi=f"Ramzan {yr} Din {k + 1}: {t[1]}", te=f"Day {k + 1}", th=f"Din {k + 1}",
                                          lesson=t[0], src=t[2], fe=fe, fh=fh, needs="Auto; religious source must be in approved list", x="")
    if kind in ("eid_fitr", "eid_adha"):
        bank = EID_FITR if kind == "eid_fitr" else EID_ADHA
        t = bank[k * 2 + (0 if a else 1)]
        name = "Eid al-Fitr" if kind == "eid_fitr" else "Eid al-Adha"
        name_hi = "Eid ul-Fitr" if kind == "eid_fitr" else "Bakra Eid"
        return "Eid Specials", dict(en=f"{name} {yr}: {t[0]}", hi=f"{name_hi} {yr}: {t[1]}", te="Eid Mubarak!", th="Eid Mubarak!",
                                    lesson="Celebrate Eid the Sunnah way", src=EID_SRC, fe="Song", fh="Gaana", needs="Auto", x="")
    if kind == "hajj":
        t = HAJJ[k % len(HAJJ)]
        fe, fh = ("Song", "Gaana") if a else ("Story", "Kahani")
        return "Hajj & Eid al-Adha", dict(en=f"Dhul Hijjah {yr}: {t[0]} ({fe})", hi=f"Zul Hijjah {yr}: {t[1]} ({fh})", te="Hajj!", th="Hajj!",
                                          lesson=t[0], src=t[2], fe=fe, fh=fh, needs="Auto; religious source must be in approved list", x="")
    if kind == "new_year":
        if a:
            return "Islamic Basics & Surahs", dict(en=f"Happy Hijri New Year {yr}", hi=f"Naya Islami Saal {yr} Mubarak", te="New Year!", th="Naya Saal!",
                                                   lesson="The Islamic year begins with Muharram", src="Quran 9:36", fe="Song", fh="Gaana", needs="Auto", x="")
        return None, None
    return None, None


def fit(options, limit=100):
    for o in options:
        if len(o) <= limit:
            return o
    return options[-1][:limit]


def long_meta(series, it, slot, day, ep):
    en_title = fit([f"{it['en']} | {it['fe']} | Islamic Songs for Kids | {BRAND}", f"{it['en']} | {it['fe']} | Kids Song | {BRAND}",
                    f"{it['en']} | {it['fe']} | {BRAND}"])
    hi_title = fit([f"{it['hi']} | {it['fh']} | Bachon Ki Islamic Nazam | {BRAND}", f"{it['hi']} | {it['fh']} | Bachon Ki Nazam | {BRAND}",
                    f"{it['hi']} | {it['fh']} | {BRAND}"])
    src = it["src"]
    src_line = src if src.startswith(("No religious", "Arabic")) else src + VERIFY
    hook = HOOK.get(series, "").format(x=it.get("x") or it["en"])
    en_desc = (f"{it['en']} 🎵 Sing along with Deeni, Ayaan, Amira and Bubbly!\n\n"
               f"Today's lesson: {it['lesson']}.\n"
               f"📖 Source: {src}\n\n"
               f"✨ Sing, dance and do the actions together.\n👶 Made for little Muslims aged 1–6.\n"
               f"▶️ More from the series '{series}' in our playlist.\n\n"
               f"{BRAND}: Little Hearts, Big Imaan.\n#IslamicSongsForKids #MuslimKids #NurseryRhymes")
    hi_desc = (f"{it['hi']} 🎵 Deeni, Ayaan, Amira aur Bubbly ke saath gaao!\n\n"
               f"Aaj ka sabaq: {it['hi']}.\n"
               f"📖 Source: {src}\n\n"
               f"✨ Saath mein gaao, naacho aur actions karo.\n👶 1–6 saal ke chhote Muslim bachon ke liye.\n"
               f"▶️ '{SERIES_HI.get(series, series)}' ki aur videos playlist mein.\n\n"
               f"{BRAND}: Little Hearts, Big Imaan.\n#BachonKiNazam #IslamicNazam #UrduNazam")
    topic_tag = it["en"].split(":")[-1].strip().lower()
    en_tags = ", ".join([topic_tag, series.lower().split(" (")[0], it["fe"].lower()] + BASE_TAGS_EN)
    hi_tags = ", ".join([it["hi"].split(":")[-1].strip().lower(), SERIES_HI.get(series, series).lower()] + BASE_TAGS_HI)
    return dict(en_title=en_title, hi_title=hi_title, en_desc=en_desc, hi_desc=hi_desc, en_tags=en_tags, hi_tags=hi_tags,
                hook=hook, src=src_line)


def short_original(i, c):
    """Short-3: an original mini, rotating 7 types by day. Returns (series_label, en, hi, te, th, lesson, src, hook)."""
    kind = i % 7
    n = c.next(f"s3-{kind}")
    if kind == 0:
        d = DUAS[n % len(DUAS)]
        s = SITUATIONS[(n // len(DUAS)) % len(SITUATIONS)]
        return ("Dua in 30 Seconds", f"Dua in 30 Seconds: {d[0]} {s[0]}", f"30 Second Dua: {d[1]} {s[1]}", d[2], d[3], d[4], d[5],
                "Timer appears: \"30 seconds to learn a dua — go!\"")
    if kind == 1:
        d = DUAS[n % len(DUAS)]
        s = SITUATIONS[(n // len(DUAS)) % len(SITUATIONS)]
        return ("What Do We Say? Quiz", f"What Do We Say? {d[0]} Quiz {s[0]}", f"Kya Bolte Hain? {d[1]} Quiz {s[1]}", "What do we say?", "Kya Bolein?",
                d[4], d[5], "Bubbly freezes: \"Quick! What do we say?\" — 3-2-1 countdown")
    if kind == 2:
        num = n % 10 + 1
        o = COUNT_OBJECTS[(n // 10) % len(COUNT_OBJECTS)]
        return ("Count with Deeni", f"Count {num} {o[0]} with Deeni", f"Deeni Ke Saath {num} {o[1]} Gino", f"{num} {o[0]}!", f"{num} {o[1]}!",
                f"Count to {num}", NO_SRC, f"{num} {o[0].lower()} pop up one by one — \"Count with me!\"")
    if kind == 3:
        col = COLOURS[n % len(COLOURS)]
        p = HUNT_PLACES[(n // len(COLOURS)) % len(HUNT_PLACES)]
        return ("Colour Hunt", f"Colour Hunt: Find {col[0]} {p[0]}", f"Rang Dhoondo: {col[1]} {p[1]}", f"Find {col[0]}!", f"{col[1]} Dhoondo!",
                f"Spot the colour {col[0].lower()}", CREATOR, f"Everything turns grey… except one {col[0].lower()} thing!")
    if kind == 4:
        v = VALUES[n % len(VALUES)]
        p = PLACES[(n // len(VALUES)) % len(PLACES)]
        return ("Bubbly's Funny Fail", f"Bubbly's Funny Fail: {v[0]} ({p[0]})", f"Bubbly Ki Galti: {v[1]} ({p[1]})", "Oops Bubbly!", "Oops Bubbly!",
                v[4], v[5], "Bubbly slips — \"Oops!\" — can you help him?")
    if kind == 5:
        l = LETTERS[n % len(LETTERS)]
        a = LETTER_ANGLES[(n // len(LETTERS)) % len(LETTER_ANGLES)]
        return ("Arabic Letter in 30 Seconds", f"Arabic Letter {l}: {a[0]}", f"Arabic Harf {l}: {a[1]}", f"{l}!", f"{l}!", f"Learn the letter {l}",
                "Arabic pronunciation check by teacher", f"A giant {l} drops in with a boing!")
    sn = SUNNAHS[n % len(SUNNAHS)]
    p = PLACES[(n // len(SUNNAHS)) % len(PLACES)]
    return ("Sunnah Minute", f"Sunnah Minute: {sn[0]} ({p[0]})", f"Sunnat Ka Minute: {sn[1]} ({p[1]})", sn[0] + "!", sn[1] + "!", sn[0],
            sn[2], "\"Did you know the Prophet ﷺ did this?\" — shown with objects only")


HEAD = ["Day", "Date", "Slot", "Series", "Topic (EN)", "Status", "Hook (first 3 s)", "Lesson", "Source (verify before use)",
        "EN Title", "HI Title (Hinglish)", "EN Thumbnail Text", "HI Thumbnail Text", "Thumbnail Design Brief", "Format",
        "EN Description", "HI Description", "EN Tags", "HI Tags", "Needs", "EN Post (IST)", "HI Post (IST)", "Weekday",
        "Season / Event", "Phase", "Episode ID", "EN YouTube Link", "HI YouTube Link"]


RAW = []


def build_rows():
    c = Counter()
    rows = []
    RAW.clear()
    ep = 0
    for i in range(DAYS):
        day = i + 1
        d = START + dt.timedelta(days=i)
        wd = d.weekday()
        phase = "Launch" if day <= 60 else ("Growth" if day <= 365 else "Scale")
        kind, k, yr = season(d)
        longs = []
        for slot, base_series in zip(("Long-A", "Long-B"), WHEEL[wd]):
            series, it = (None, None)
            if kind:
                series, it = seasonal(kind, k, yr, slot)
            if it is None:
                series = base_series
                it = pick(series, c)
            if day == 1 and slot == "Long-A":
                it.update(en="Bismillah Before We Begin", hi="Bismillah Se Shuru Karein", fe="Song", fh="Gaana",
                          needs="Auto; religious source must be in approved list")
            ep += 1
            longs.append((slot, series, it, f"E{ep:04d}"))
        event = {"pre_ramadan": "Pre-Ramadan (publish early for search)", "ramadan": "Ramadan (date ±1 day)", "eid_fitr": "Eid al-Fitr",
                 "hajj": "First 10 days of Dhul Hijjah", "eid_adha": "Eid al-Adha", "new_year": "Islamic New Year"}.get(kind, "")
        for slot, series, it, eid in longs:
            m = long_meta(series, it, slot, day, eid)
            RAW.append(dict(day=day, date=d, slot=slot, series=series, item=it, episode=eid, meta=m, post=POST[slot], event=event, kind=kind))
            rows.append([day, d, slot, series, it["en"], "Planned", m["hook"], it["lesson"], m["src"], m["en_title"], m["hi_title"],
                         it["te"], it["th"], THUMB_BRIEF.get(series, ""), it["fe"], m["en_desc"], m["hi_desc"], m["en_tags"], m["hi_tags"],
                         it["needs"], POST[slot][0], POST[slot][1], d.strftime("%a"), event, phase, eid, None, None])
        # Shorts 1 & 2: new vertical cuts built around each long episode's chorus
        for j, (slot, series, it, eid) in enumerate(longs):
            s_slot = f"Short-{j + 1}"
            en = f"{it['en']} ({it['fe']}) Sing-Along"
            hi = f"{it['hi']} ({it['fh']}) Saath Gaao"
            rows.append([day, d, s_slot, series, en, "Planned", "Chorus in the first second, big face, loop-friendly ending", it["lesson"],
                         it["src"] + ("" if it["src"].startswith(("No religious", "Arabic")) else VERIFY),
                         fit([f"{it['te']} {en} 🎵 #shorts", f"{en} 🎵 #shorts"]), fit([f"{it['th']} {hi} 🎵 #shorts", f"{hi} 🎵 #shorts"]), it["te"], it["th"],
                         "Vertical 1080x1920; first frame = character mid-chorus; no text over the face",
                         "Vertical Short 20–45 s (new vertical edit)",
                         f"{it['en']}: sing the chorus with {BRAND}! Full song on our channel. #shorts #IslamicSongsForKids",
                         f"{it['hi']}: chorus saath gaao! Poora gaana channel par. #shorts #BachonKiNazam",
                         ", ".join(["shorts", it["en"].split(':')[-1].strip().lower()] + BASE_TAGS_EN[:3]),
                         ", ".join(["shorts", it["hi"].split(':')[-1].strip().lower()] + BASE_TAGS_HI[:3]),
                         "Auto (vertical cut of today's episode)", POST[s_slot][0], POST[s_slot][1], d.strftime("%a"), event, phase, eid + "-S", None, None])
        for j, (slot, series, it, eid) in enumerate(longs):
            RAW.append(dict(day=day, date=d, slot=f"Short-{j + 1}", series=series, item=it, episode=eid + "-S", source_episode=eid,
                            post=POST[f"Short-{j + 1}"], event=event, kind=kind))
        lbl, en, hi, te, th, lesson, src, hook = short_original(i, c)
        RAW.append(dict(day=day, date=d, slot="Short-3", series="Shorts Originals: " + lbl, episode=f"S3-{day:04d}", post=POST["Short-3"],
                        event=event, kind=kind, item=dict(en=en, hi=hi, te=te, th=th, lesson=lesson, src=src, fe="Short", fh="Short", x="", hook=hook)))
        rows.append([day, d, "Short-3", "Shorts Originals: " + lbl, en, "Planned", hook, lesson,
                     src + ("" if src.startswith(("No religious", "Arabic")) else VERIFY), fit([f"{en} 🤩 #shorts"]), fit([f"{hi} 🤩 #shorts"]), te, th,
                     "Vertical; one character + one big object/word; bright single-colour background",
                     "Original vertical Short 15–40 s",
                     f"{en}. Learn with {BRAND}! #shorts #MuslimKids", f"{hi}. {BRAND} ke saath seekho! #shorts #BachonKiNazam",
                     ", ".join(["shorts", lbl.lower()] + BASE_TAGS_EN[:3]), ", ".join(["shorts"] + BASE_TAGS_HI[:3]),
                     "Auto (original mini)", POST["Short-3"][0], POST["Short-3"][1], d.strftime("%a"), event, phase, f"S3-{day:04d}", None, None])
    return rows


def main(path):
    rows = build_rows()
    wb = Workbook()
    fill = PatternFill("solid", fgColor="DDEFE4")
    bold = Font(bold=True)

    fmt = wb.active
    fmt.title = "Format"
    lines = [
        ["Deeni & Friends: 1,000-Day Format v2"],
        ["Every day: 2 NEW long videos + 3 NEW Shorts, each published in English and Hinglish = 10 uploads a day"],
        ["Day 1 = Mon 4 Jan 2027 · Day 1,000 = Sat 29 Sep 2029 · No compilations, no repeats: every topic is new"],
        ["100% free and automatic: GitHub Actions makes, checks and uploads every day at 00:05 IST (public repo = free minutes)"],
        [],
        ["DAILY SLOTS", "What it is", "EN time / HI time (IST)"],
        ["Long-A", "New song episode (~1.5–2 min), made automatically", "18:30 / 17:30"],
        ["Long-B", "Second new song episode (~1.5–2 min), made automatically", "12:30 / 11:30"],
        ["Short-1", "New vertical sing-along built on Long-A's chorus", "08:00 / 09:00"],
        ["Short-2", "New vertical sing-along built on Long-B's chorus", "13:30 / 14:30"],
        ["Short-3", "Original mini: Dua in 30 s · Quiz · Count · Colour Hunt · Bubbly's Funny Fail · Arabic Letter · Sunnah Minute", "20:30 / 21:30"],
        [],
        ["WEEKLY WHEEL", "Long-A series", "Long-B series"],
    ] + [[["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][k], WHEEL[k][0], WHEEL[k][1]] for k in range(7)] + [
        [],
        ["SEASONAL TAKEOVERS", "When", "Note"],
        ["Ramadan with Deeni", "14 days before Ramadan to the last day", "Parents search early. Dates are estimates: confirm by moon sighting"],
        ["Eid Specials", "Eid al-Fitr and Eid al-Adha + 2 days", "Big yearly search spikes"],
        ["Hajj & Eid al-Adha", "1–9 Dhul Hijjah", "Kaaba exterior only, gentle Qurbani"],
        ["Islamic New Year", "1 Muharram", "Long-A only"],
        [],
        ["THUMBNAIL RULES"],
        ["1. One big, happy, clear face. Never distorted faces, screaming mouths or fake shock"],
        ["2. Max 3 words (the 'Thumbnail Text' columns), huge and readable on a phone"],
        ["3. Bright single-colour background, navy outline around characters"],
        ["4. Same layout per series so parents recognise it instantly"],
        ["5. Small Deeni logo bottom-left on every thumbnail"],
        ["6. Shrink to 10%: if you can't tell what it is, redo it"],
        [],
        ["WATCH-TIME RULES"],
        ["1. Hook in the first 3 seconds (see 'Hook' column), no long intros"],
        ["2. Chorus at least 3 times; toddlers love repetition"],
        ["3. Every video goes into its series playlist (separate EN and HI playlists)"],
        ["4. Made for Kids = ON. Honest titles and thumbnails"],
        ["5. Never publish a weak video to keep the streak: mark it 'Skipped' and catch up later"],
        [],
        ["RELIGIOUS SAFETY"],
        ["Every source marked [VERIFY] must be in config/approved_sources.json before that video can upload (one-time check of ~95 sources)."],
        ["Surah recitation is NOT in the automatic plan: AI must never recite the Quran."],
        ["Prophets are never shown. 'Sunnah Minute' shows objects and characters only."],
        [],
        ["TOTALS (live)", "Count"],
        ["Long videos (topics)", "=COUNTIF('1000-Day Plan'!C:C,\"Long*\")"],
        ["Shorts (topics)", "=COUNTIF('1000-Day Plan'!C:C,\"Short*\")"],
        ["Total uploads (EN + HI)", "=2*(B49+B50)"],
        ["Published (topics)", "=COUNTIF('1000-Day Plan'!F:F,\"Published\")"],
        [],
        ["Views can't be guaranteed: check YouTube Analytics monthly and do more of what works."],
    ]
    for r in lines:
        fmt.append(r)
    fmt["A1"].font = Font(bold=True, size=16)
    for row in fmt.iter_rows():
        v = row[0].value
        if isinstance(v, str) and v.isupper():
            for cc in row[:3]:
                cc.font = bold
                cc.fill = fill
    for col, w in zip("ABC", [36, 70, 60]):
        fmt.column_dimensions[col].width = w
    for row in fmt.iter_rows(min_row=4):
        for cc in row:
            cc.alignment = Alignment(wrap_text=True, vertical="top")

    ws = wb.create_sheet("1000-Day Plan")
    ws.append(HEAD)
    for r in rows:
        ws.append(r)
    for cc in ws[1]:
        cc.font = bold
        cc.fill = fill
    widths = [6, 13, 8, 26, 40, 11, 40, 32, 34, 50, 50, 16, 16, 40, 22, 50, 50, 40, 40, 30, 9, 9, 7, 24, 9, 10, 24, 24]
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = w
    for cc in ws["B"][1:]:
        cc.number_format = "ddd d mmm yyyy"
    ws.freeze_panes = "C2"

    kd = wb.create_sheet("Key Islamic Dates")
    kd.append(["Event", "Estimated date", "Plan day", "Note"])
    for y, e in EVENTS.items():
        for name, key in [("1st Ramadan", "ramadan"), ("Eid al-Fitr", "eid_fitr"), ("1st Dhul Hijjah", "dhul_hijjah"),
                          ("Eid al-Adha", "eid_adha"), ("Islamic New Year", "new_year")]:
            dd = e[key]
            pd_ = (dd - START).days + 1
            kd.append([f"{name} {y}", dd, pd_ if 1 <= pd_ <= DAYS else "outside plan", "Astronomical estimate; confirm by moon sighting"])
    for cc in kd[1]:
        cc.font = bold
        cc.fill = fill
    for cc in kd["B"][1:]:
        cc.number_format = "ddd d mmm yyyy"
    for col, w in zip("ABCD", [26, 18, 12, 46]):
        kd.column_dimensions[col].width = w
    wb.save(path)
    return rows


_CACHE = {}


def get_day(day):
    """All 5 slots (Long-A, Long-B, Short-1, Short-2, Short-3) for a plan day (1..1000)."""
    if not _CACHE:
        build_rows()
        for r in RAW:
            _CACHE.setdefault(r["day"], []).append(r)
    return _CACHE[day]


def day_for(date):
    return (date - START).days + 1


if __name__ == "__main__":
    import collections
    import sys
    rows = main(sys.argv[1] if len(sys.argv) > 1 else "deeni-1000-day-plan.xlsx")
    print("rows", len(rows), "cells", len(rows) * len(HEAD))
    longs = [r for r in rows if r[2].startswith("Long")]
    shorts = [r for r in rows if r[2].startswith("Short")]
    print("long", len(longs), "shorts", len(shorts))
    for label, rs in (("long EN titles", longs), ("short EN titles", shorts)):
        t = [r[9] for r in rs]
        dups = [x for x, n in collections.Counter(t).items() if n > 1]
        print(label, "unique", len(set(t)), "of", len(t), "dups", dups[:4])
    t = [r[10] for r in rows]
    print("HI titles unique", len(set(t)), "of", len(t), [x for x, n in collections.Counter(t).items() if n > 1][:4])
    print(collections.Counter(r[3] for r in longs))
    print("max EN len", max(len(r[9]) for r in rows), "max HI len", max(len(r[10]) for r in rows))
    for r in rows[:5] + rows[5 * 300:5 * 300 + 5]:
        print(r[2], "|", r[9], "||", r[10])
