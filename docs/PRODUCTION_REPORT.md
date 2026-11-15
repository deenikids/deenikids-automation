# Production report (15 Nov 2026)

**Honest status:** the pipeline, visuals, names and thumbnails are upgraded. Only 4 episodes exist as videos so far; the other planned episodes are made one day at a time by the daily schedule, not all in advance.

| Item | Status |
|---|---|
| Character names (Deeni, Ali, Mina, Bubbles) | Updated in songs, planner, storyboards, docs, README |
| Language | English only (Hindi/Hinglish switched off in settings and uploads) |
| Animation | Lyric-driven poses, chorus bounce and sway, spotlight hop, stars, notes, confetti, karaoke subtitles |
| Thumbnails | New style (big sticker-outlined faces); one example checked by eye |
| Singing | Works on some short songs at strength 0.25 (42% words recognised on one test); otherwise falls back to the spoken voice |
| Publishing | Blocked to Private until the YouTube API audit is approved |
| Religious sources | 95 sources checked by AI; a qualified person should spot-check docs/SOURCES_TO_REVIEW.md |

Episodes rendered earlier (before the name change and new look) must be re-rendered: e0003, e0004, s3-0002 and the Bismillah song. Each daily run checks every video and thumbnail and writes `reports/day-NNNN.json`.
