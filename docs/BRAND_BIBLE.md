# DEENIKIDS Brand Bible (v1.0)

**Name:** DEENIKIDS
**Tagline:** Little Hearts, Big Imaan.
**Mission:** Make Islamic learning fun, memorable and trustworthy for children aged 1–6 around the world.
**Promise to parents:** Every religious line is checked against a named, reliable source and approved by a qualified person before it goes public.

## 1. Audience
| Who | What they need |
|---|---|
| Children 1–3 | Repetition, simple words, bright colours, slow scene changes, singalong choruses |
| Children 4–6 | Short stories, simple Arabic words, characters they recognise, "what do we say?" questions |
| Parents | Authentic content, no music they object to (see §6), no ads aimed at kids inside the video, no scary or rude moments |

## 2. Brand voice
- Warm, cheerful, gentle. Never preachy, never scary (no "you will be punished" messages for toddlers).
- Short sentences. One lesson per episode.
- Positive framing: "We say Bismillah!" rather than "Don't forget or else…"
- Islamic terms always said correctly and shown in Arabic script plus a simple meaning.

## 3. Colour palette
| Role | Name | Hex |
|---|---|---|
| Primary | Deeni Blue | `#269AD6` |
| Primary | Imaan Green | `#2E9E5B` |
| Accent | Sunshine Yellow | `#FFD63F` / `#FFD650` |
| Accent | Mina Pink | `#F27BA8` |
| Neutral | Cream | `#FFF1D0` |
| Outline / text panels | Night Navy | `#1E2A4A` |

Rules: navy outlines on all characters; white text with navy outline for on-screen words; yellow for the logo.

## 4. Typography (all free, SIL Open Font License, files in `assets/fonts/`)
- **Baloo 2 ExtraBold**: titles, subtitles, logo.
- **Noto Naskh Arabic Bold**: all Arabic (Bismillah, duas). Arabic is always shown with full harakat (vowel marks).

## 5. Logo (until a designed logo exists)
Word-mark "DEENIKIDS" in Baloo 2 ExtraBold, Sunshine Yellow, navy outline. The final logo should be designed once and saved in `assets/brand/`.

## 6. Content rules (non-negotiable)
1. **No invented religion.** No Hadith, dua, Arabic text, translation or religious claim unless it is in `religious_sources` of the song file with a reference (e.g. Sahih al-Bukhari 5376) and a link.
2. **Human approval** of every religious script before upload (`review_gate.py` enforces this).
3. **Never depict Prophets** or the Companions. Stories about them are told by narration, with scenery and objects only.
4. **No depictions of Allah**, angels, or the Ka'bah interior. The Ka'bah exterior may be shown respectfully in Hajj episodes.
5. **Modesty:** Mina always wears her hijab (hair, ears and neck covered), long sleeves, long dress. No romance, no mocking anyone.
6. **Music:** current decision is songs with instruments. If the channel later offers a "vocals and percussion only" version for families who avoid instruments, keep it as a separate playlist.
7. **Kids' safety:** no dangerous stunts children could copy, no scary monsters, no loud jump-scares, no requests for personal information.
8. **Originality:** all melodies, lyrics, characters and artwork are made for DEENIKIDS. See §7.

## 7. Staying clear of Baby Shark, CoComelon and others
- Never use the words "Baby Shark", "Shark family", "Mommy/Daddy/Grandma Shark", "doo doo doo" or "CoComelon" in titles, tags, descriptions or lyrics.
- Never reuse or imitate their melodies, dances, logos, fonts or character designs.
- **Deeni must stay visually distinct from Pinkfong's sharks.** His signature features: the clear travelling bubble, the white crescent mark on his dorsal fin, his turquoise-blue (`#269AD6`) colour and his rounder body. Do not change these.
- Keep the master character sheets dated in this repo as a record that the designs are ours.

## 8. Titles and descriptions
- Format: `<Song or lesson name> | <What it is> | DEENIKIDS`
- First description line says what the child learns. Second line lists the source (e.g. "Lesson source: Sahih al-Bukhari 5376").
- Every video is set **Made for Kids**.
