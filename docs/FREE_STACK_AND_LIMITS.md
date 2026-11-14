# Free software stack and its real limits (checked November 2026)

## The stack
| Job | Tool | Cost / licence | Status |
|---|---|---|---|
| Code + automation | GitHub + GitHub Actions | Free (see limits) | Built |
| Music | `scripts/generate_music.py`: pure maths synthesis (marimba, ukulele, bass, drums, bubbles) | Free, 100% DEENIKIDS-owned | Built and tested |
| Video assembly | FFmpeg | Free (LGPL/GPL) | Built and tested |
| 2D animatic | Python + Pillow | Free | Built and tested |
| Fonts | Baloo 2, Noto Naskh Arabic | Free (SIL OFL) | Included |
| AI voice (speech) | Kokoro-82M: English + Hindi voices, runs on CPU | Free (Apache-2.0) | Code written; runs on GitHub (model host is blocked in my workspace, so not yet heard) |
| Song vocals | Human recording (phone + Audacity) over `singer_guide.wav` | Free | Supported |
| 3D animation | Blender + Rigify | Free (GPL) | Phase 3 |
| Lip-sync | Rhubarb Lip Sync | Free (MIT) | Phase 3 |
| Upload | YouTube Data API v3 + OAuth | Free | Built; needs your secrets to test |

## Limits you must plan around

**GitHub Actions**
- Standard runners are free and unlimited **only for public repositories**. A private repo gets 2,000 free minutes a month on the Free plan.
- One job can run at most 6 hours. The Free plan allows 20 jobs at once. There are **no GPUs** on free runners.
- Artifacts (the downloadable videos) are deleted after the retention period (set to 14 days). Never commit videos into git: files over 100 MB are rejected and the repo becomes slow.
- A **public** repo means anyone can see the scripts and the character files. The brand name and characters are still yours, but think about registering the DEENIKIDS trademark once the channel grows.
- GitHub's Actions terms expect hosted runners to be used for the software project itself. Heavy daily video rendering is a grey area, so keep a backup: any old PC can be connected as a free **self-hosted runner** with unlimited minutes.

**YouTube Data API**
- Since 1 June 2026, uploads have their own quota: about 100 `videos.insert` calls per day per Google Cloud project, plus 10,000 units a day for everything else. Setting a thumbnail or adding to a playlist costs 50 units each. **5 uploads a day fits easily.**
- **Videos uploaded from an unverified API project are forced to PRIVATE.** You can still publish them by hand in YouTube Studio. To publish automatically you must pass YouTube's free API compliance audit. Apply once the channel and pipeline are stable. Until then, `upload_youtube.py` uploads as private on purpose.
- Custom thumbnails need a phone-verified channel.

**Made for Kids**
- Required for this channel. It switches off comments, the notification bell, end screens, cards and personalised ads, so earnings per view are lower than on DEENIFY. Contextual ads can still run.

**AI voice**
- Kokoro speaks well but **does not sing**. Use it for spoken parts (stories, "What do we say?") and as a test voice. For songs, one human recording per language is far better and is reused for every Short cut from that song.
- Kokoro has no Urdu voice. Roman Hinglish/Urdu lines are voiced with the Hindi voice from a Devanagari copy (`hi_tts` in song.json). **Arabic words must be checked by ear.** The English pronunciation overrides in `config/settings.json` are untested.

**3D rendering (Phase 3): the real bottleneck**
- Two 4-minute episodes a day is about 11,500 frames a day at 24 fps, before Shorts.
- Free runners are CPU-only. If one simple stylised frame takes about 20 seconds (to be measured in Phase 3), that is about 64 runner-hours a day: just possible with 20 parallel jobs on a public repo, but it uses the grey area above heavily.
- Plan: measure real seconds-per-frame in Phase 3, then choose between (a) lower-cost toon rendering (Blender Workbench/EEVEE at 12–15 fps with held frames), (b) your own PC as a self-hosted runner, (c) fewer, better long videos.

**Hidden costs: none required.** Optional one-time costs: a freelance 3D model/rig commission, a decent USB microphone, a logo designer.

## The 1,000-day target, honestly
- **Technically,** uploading 2 long videos + 3 Shorts a day is within API quota.
- **Production** is the limit: 2 new, reviewed, original songs or stories a day means writing, checking and animating about 730 episodes a year.
- **Policy:** YouTube does not monetise "mass-produced or repetitive" content, judged across the whole channel. Many near-identical template videos is exactly the pattern that loses monetisation.
- **Recommended ramp:** Phase 7 makes 10 test videos. Phase 8 starts at 3–4 long videos a week + 1 Short a day. Scale up only while every video still passes review and quality control, and keep each one clearly different (new song, new scene, new lesson). The streak counter in `database/` should never push out a weak video.

## Sources
- GitHub-hosted runners: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- GitHub Actions limits: https://docs.github.com/en/actions/reference/limits
- YouTube `videos.insert` (private restriction): https://developers.google.com/youtube/v3/docs/videos/insert
- YouTube quota (granular buckets, 2026): https://www.upload-post.com/youtube-api/
- Made for Kids features: https://support.google.com/youtube/answer/9632097
- Kokoro-82M: https://huggingface.co/hexgrad/Kokoro-82M
