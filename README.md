# Deeni & Friends: Fully Automatic, 100% Free

**Every day GitHub Actions makes, checks and uploads 2 new episodes + 3 new Shorts, in English and Hinglish (10 uploads), with nobody touching anything.**
Workflow: `.github/workflows/daily.yml` runs at 00:05 IST. Plan: `scripts/plan.py` (1,000 days, 5,000 unique topics).

```
plan.py (today's 5 topics) -> auto_song.py (original lyrics EN+Hinglish, new melody, storyboard)
 -> generate_music.py -> generate_voice.py (free Kokoro AI voice) -> render_animatic.py (2D video + Shorts)
 -> generate_thumbnail.py -> quality_check.py -> source check -> upload_youtube.py (Made for Kids) -> ledger
```

### Real singing like Baby Shark / CoComelon (free)
Songs are sung by **ACE-Step 1.5** (open-source, MIT licence) running on **Kaggle's free GPU** (about 30 hours a week).
GitHub sends Kaggle each day's original instrumentals + lyrics; ACE-Step keeps our melody and structure and adds a sung vocal.
Every sung song is checked automatically: same length as our song, and free Whisper speech recognition must recognise
at least 35% of the lyric words. If a song fails, or Kaggle is unavailable, the normal AI voice is used, so the day never breaks.
**Setup (once):** free account at kaggle.com, verify your phone (needed for GPU), Settings > API > Create New Token,
then add GitHub Secrets `KAGGLE_USERNAME` and `KAGGLE_KEY` (values from the downloaded kaggle.json).

### The only one-time jobs (then it runs by itself)
1. **Accounts + secrets**: Steps 1, 2 and 5 below (Gmail, YouTube channel, GitHub org + public repo, 3 YouTube secrets).
2. **Approve religious sources once**: a qualified person checks the ~95 references in `docs/SOURCES_TO_REVIEW.md` and copies each correct one into `config/approved_sources.json`. Videos whose source isn't approved are built but never uploaded, so nothing unchecked reaches children.
3. **YouTube API audit (free)**: until Google audits your API project, every API upload is forced to Private. Apply with the "YouTube API Services - Audit and Quota Extension" form, then set `"api_project_audited": true` in `config/settings.json` and videos get scheduled to go public at the planned times automatically.

### What "free and automatic" means for quality
- Singing is AI (ACE-Step). Without Kaggle secrets, or when a song fails the checks, the voice is AI speech in rhythm instead.
- Animation is 2D (Blender 3D on free runners is far too slow for 10 videos a day).
- Lyrics come from fixed, safe templates + the topic, so songs feel similar. YouTube may decline to monetise channels it sees as mass-produced; to stay safe, keep improving templates and visuals over time.
- No Quran recitation (AI must never recite Quran), so Surah episodes were replaced.

---

# DEENIKIDS Automation
**Little Hearts, Big Imaan.** An automated, free, open-source production pipeline for an Islamic preschool YouTube channel.
Separate from DEENIFY: its own GitHub repo, its own Google account, its own YouTube channel.

```
song.json + storyboard.json
      │
      ├─ generate_music.py     original instrumental (pure synthesis, 100% ours)
      ├─ generate_voice.py     human vocals  ▸ else free AI voice (Kokoro) ▸ else instrumental
      ├─ render_animatic.py    1920x1080 episode + 1080x1920 Shorts, burned-in subtitles, .srt files
      ├─ generate_thumbnail.py 1280x720 thumbnails
      ├─ quality_check.py      resolution, duration, audio, clipping, silence, black frames, frames, subtitles, duplicates
      ├─ review_gate.py        a human must approve religious + language content
      └─ upload_youtube.py     Made for Kids, private by default, never uploads twice
```

## What works today (tested)
| Part | Status |
|---|---|
| Original music for "Bismillah Before We Begin" (77 s, 108 BPM) | ✅ tested |
| English + Hindi/Urdu episode videos (1920x1080, 24 fps) | ✅ tested |
| 3 Shorts per language (chorus, "What do we say?", meet Deeni) | ✅ tested |
| Thumbnails (EN + HI) | ✅ tested |
| Automatic QC (and it correctly fails broken files) | ✅ tested |
| Review gate blocks upload until approved | ✅ tested |
| Upload plan (dry run) | ✅ tested |
| Real YouTube upload | ⏳ needs your Google secrets |
| Free AI voice (Kokoro) | ⏳ runs on GitHub; not heard yet |
| 3D characters in Blender | ⏳ Phase 3 |

The videos are a **2D animatic**: real timing, scenes, subtitles and music, with simple placeholder drawings of the characters. The 3D Blender versions replace the drawings in Phase 3 using the same storyboard.

---

## Setup, step by step (no coding needed)

### Step 1: Accounts (one time)
1. Create a new Gmail for DEENIKIDS. Use it to create the **DEENIKIDS** YouTube channel and **verify it by phone** (studio.youtube.com > Settings > Channel > Feature eligibility). Phone verification is needed for custom thumbnails.
2. In YouTube Studio > Settings > Channel > Advanced settings, set **Audience: "Yes, set this channel as made for kids"**.
3. GitHub: logged in to your existing GitHub, click **+ (top right) > New organization > Free**, and name it (e.g. `deenikids`). GitHub allows one free personal account per person; an organization is the free, allowed way to get a separate name.

### Step 2: Create the repository
1. In the new organization: **Repositories > New** > name `deenikids-automation` > **Public** (public = unlimited free Actions minutes; private = 2,000 minutes a month) > Create.
2. On the empty repo page, click **uploading an existing file**. Unzip `deenikids-automation.zip` on your computer and drag **everything inside the folder** (including the `.github` folder) into the page > **Commit changes**.
   - On a Mac the `.github` folder is hidden: press `Cmd + Shift + .` in Finder to show it.
3. Open the **Actions** tab. If asked, click **"I understand my workflows, go ahead and enable them"**.

### Step 3: First test build (about 5 minutes)
1. **Actions > Build episode > Run workflow**, tick **Quick test**, then **Run workflow**.
2. When it shows a green tick, open the run and scroll to **Artifacts**. Download `bismillah-before-we-begin-videos` and watch the clips.
3. Run it again **without** Quick test for the full episode and Shorts (about 15–25 minutes the first time, while it downloads the free voice model).

### Step 4: Human review (required before any upload)
1. Ask an alim or qualified teacher to check the lyrics and sources in `content/songs/bismillah-before-we-begin/song.json` (open it on GitHub to read).
2. Ask a native Hindi/Urdu speaker to check the `hi` lines.
3. Decide on the proposed outro lyric change (listed under `lyric_changes`).
4. Edit `song.json` on GitHub (pencil icon) and set each review item to `"status": "approved"`, with `"reviewer"` and `"date"` filled in > Commit.

### Step 5: Connect YouTube (one time, about 20 minutes)
Do all of this signed in with the **DEENIKIDS Gmail**.
1. Go to https://console.cloud.google.com, then **Select project > New project** > name `deenikids-uploader` > Create.
2. **APIs & Services > Library**, search **YouTube Data API v3** > **Enable**.
3. **APIs & Services > OAuth consent screen** (Google Auth Platform): app name `DEENIKIDS Uploader`, user type **External**, your email as support and developer contact. Under **Audience**, click **Publish app** so it is **In production**. (In "Testing" mode the login expires after 7 days and uploads stop. An "unverified app" warning during sign-in is expected because it's your own app.)
4. **Clients > Create client > Web application**. Under **Authorised redirect URIs** add `https://developers.google.com/oauthplayground` > Create. Copy the **Client ID** and **Client secret**.
5. Open https://developers.google.com/oauthplayground and click the **gear icon** (top right). Tick **Use your own OAuth credentials** and paste the Client ID and secret.
6. In the left box, type `https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube` > **Authorize APIs**. Sign in with the DEENIKIDS Gmail, choose the DEENIKIDS channel and allow access.
7. Click **Exchange authorization code for tokens** and copy the **Refresh token**.
8. On GitHub: **repo > Settings > Secrets and variables > Actions > New repository secret**. Add three secrets:
   - `YT_CLIENT_ID`: the Client ID
   - `YT_CLIENT_SECRET`: the Client secret
   - `YT_REFRESH_TOKEN`: the refresh token

Never paste these into a file, a chat or a commit.

### Step 6: Upload
**Actions > Build episode > Run workflow**, untick Quick test, tick **Upload**. Videos arrive in YouTube Studio as **Private** and marked Made for Kids. Watch each one once in Studio, then click **Publish**.

Videos uploaded through a new Google Cloud project are forced to Private until the project passes YouTube's free API audit. Publishing by hand in Studio is fine. Apply for the audit (YouTube API Services, Audit and Quota Extension form) once you are happy with the pipeline.

### Step 7: Add real singing (recommended)
1. From the build's artifacts, download `audio/singer_guide.wav` (the melody plus a click track).
2. A singer listens on headphones and records the song **from 0:00**, in a quiet room, on a phone or USB mic. Clean it up in Audacity (free) and export as WAV.
3. Upload it to GitHub as `audio/vocals/bismillah-before-we-begin/en.wav`, and the Hindi/Urdu version as `hi.wav`.
4. Run **Build episode** again. The pipeline uses the human vocals automatically.

---

## Adding the next song
1. Copy `content/songs/bismillah-before-we-begin/` to a new folder, e.g. `alhamdulillah-song/`.
2. Edit `song.json` (lyrics per bar, melody notes, chords, sources, review set to `pending`) and `storyboard.json` (scenes).
3. Push. The **Checks** workflow validates the files automatically (every bar must add up to 4 beats).
4. Run **Build episode** with the new folder name.

## Folder map
```
.github/workflows/  episode.yml (build, QC, upload), checks.yml (auto-tests on every push)
assets/fonts/       Baloo 2 + Noto Naskh Arabic (SIL Open Font License)
audio/vocals/       human vocal recordings: <song_id>/<lang>.wav
characters/         locked character sheets and Blender models (Phase 3)
config/             settings.json (languages, voices, YouTube, QC limits), content_queue.json
content/songs/      one folder per song: song.json + storyboard.json
database/           uploads.json: ledger of everything uploaded (prevents duplicates)
docs/               brand bible, character bible, free-stack limits, storyboard, progress
scripts/            the pipeline (see diagram above)
output/             generated files (not committed to git)
```

## Run locally (optional)
```
pip install numpy scipy pillow
python scripts/build_episode.py bismillah-before-we-begin --test
```
Needs FFmpeg on your PATH.
