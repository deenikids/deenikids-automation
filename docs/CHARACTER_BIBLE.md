# DEENIKIDS Character Bible (v1.0)

The **master character sheets are the source of truth**. Once a sheet is approved it is "locked" (v1). Episodes only ever *reuse* the locked model; they never generate a new-looking character. The 2D drawings in `scripts/characters2d.py` are placeholders that follow these specs until the Blender models exist.

Proportions use **head units (H)**: the height of the character's head.

---

## DEENI: the main mascot
- **What:** a friendly baby shark who travels everywhere inside his own clear water bubble, so he can visit the kitchen, the park or the masjid garden.
- **Personality:** curious, funny, a little clumsy, always first to say "Bismillah!" Loves learning new words.
- **Catchphrase:** "Splish-splash, let's learn!"
- **Design specs:**
  - Body: turquoise-blue `#269AD6`, rounded "bean" shape, about 1.7 × as long as tall. No sharp teeth, ever.
  - Belly: cream `#FFF1D0`, from the chin to the tail base.
  - Eyes: very large, about 1/3 of head height, black pupils with one white shine.
  - Fins: darker blue `#1C80BE`, soft rounded tips.
  - **Signature 1:** white crescent-moon mark on the dorsal fin.
  - **Signature 2:** clear travelling bubble with a white shine arc (top-left).
  - Pink blush on the cheek, small smiling mouth.
- **Never:** yellow body, teeth, a "shark family", the colours or face of Pinkfong's characters.

## AYAAN
- **What:** a Muslim preschool boy, about 4.
- **Personality:** curious, eager, sometimes forgets and then remembers ("Oh! Bismillah!"). Loves helping Abbu.
- **Catchphrase:** "I can do it, InshaAllah!"
- **Design specs:** 3 H tall. Warm medium-brown skin `#E2B082`. Dark brown hair `#3C281E`, short.
  - White prayer cap (taqiyah) with a small dotted band.
  - Green kurta `#2E9E5B`, knee length, three white buttons.
  - Cream trousers `#F5E9CD`, brown shoes.

## AMIRA
- **What:** a Muslim preschool girl, about 5.
- **Personality:** kind, confident, helpful, loves Arabic letters and telling stories.
- **Catchphrase:** "Let's help together!"
- **Design specs:** 3 H tall. Warm light-brown skin `#E8BA8E`.
  - Pink hijab `#F27BA8` covering hair, ears and neck, draping over the shoulders.
  - Long modest pink dress `#F9B0CE`, long sleeves, ankle length, with a white trim line.
  - Plum shoes.
- **Always:** hijab on, nothing tight-fitting.

## BUBBLY
- **What:** a cute yellow octopus, Deeni's best friend.
- **Personality:** silly, giggly, makes mistakes so kids can correct him; asks the "What do we say?" questions.
- **Catchphrase:** "Bubble-tastic!"
- **Design specs:** sunshine yellow `#FFD23F` with orange spots `#FFA828`. Round head, 8 short wavy tentacles (6 visible from the front). Big eyes like Deeni's, pink blush.

---

## Reference prompts (for concept art and turnaround sheets)

Use these with any image tool for **concept art only**. Free image tools cannot keep a character identical from picture to picture, so the approved turnaround sheet plus the 3D model are the reference, never a fresh AI image.

**Shared style line (paste at the end of every prompt):**
`original character design, high-quality 3D preschool animation style, soft rounded shapes, soft studio lighting, bright friendly colours, clean navy outline feel, plain white background, full body, character turnaround sheet, consistent proportions, no text, no logo`

1. **Deeni, turnaround:** "A friendly baby shark mascot with a turquoise-blue (#269AD6) rounded bean-shaped body, cream belly, very large expressive eyes, soft rounded fins, a small white crescent-moon mark on the dorsal fin, no teeth, floating inside a clear transparent water bubble. Show FRONT view, SIDE view, BACK view and THREE-QUARTER view in one row, same size and pose."
2. **Ayaan, turnaround:** "A cheerful 4-year-old Muslim boy with warm medium-brown skin, short dark brown hair, a white taqiyah prayer cap, a knee-length green kurta with three white buttons, cream trousers and brown shoes, big friendly eyes, 3 heads tall. FRONT, SIDE, BACK and THREE-QUARTER views in one row."
3. **Amira, turnaround:** "A kind 5-year-old Muslim girl with warm light-brown skin, a pink hijab fully covering her hair, ears and neck, a long-sleeved ankle-length pink dress with a white trim, plum shoes, big friendly eyes, 3 heads tall. FRONT, SIDE, BACK and THREE-QUARTER views in one row."
4. **Bubbly, turnaround:** "A cute round yellow octopus with orange spots, big shiny eyes, pink cheeks, eight short wavy tentacles, very friendly and silly. FRONT, SIDE, BACK and THREE-QUARTER views in one row."
5. **Expression sheet (each character):** "<character description>, expression sheet, 8 head close-ups in a grid: happy, laughing, surprised, curious, thinking, sad, proud, sleepy."
6. **Mouth sheet (each character):** "<character description>, lip-sync mouth chart, 8 close-up mouth shapes in a grid: rest, A/I, E, O, U, M/B/P, F/V, L/TH."

## Mouth shapes (visemes) every rig must have
`rest`, `A_I`, `E`, `O`, `U`, `MBP`, `FV`, `L_TH`, plus `smile` and `wide_sing`. Lip-sync maps sounds to these 8 shapes (open-source Rhubarb Lip Sync can do this automatically from audio).

## Consistency workflow
1. **Concept** (prompts above) → pick one image per character → fix colours to the hex codes above.
2. **Turnaround sheet** (front, side, back, three-quarter) drawn or cleaned up to match → approve → save in `characters/<name>/sheet_v1.png` with the date. **Locked.**
3. **3D model in Blender** built from the locked sheet → `characters/<name>/<name>_v1.blend`.
4. **Rig** with Blender's free Rigify add-on, plus shape keys for the 10 mouth shapes and 8 expressions.
5. **Action library:** idle, wave, dance-1, dance-2, clap, sing, eat, wash-hands, swim (Deeni), juggle (Bubbly), walk, sit → `animation/actions/`.
6. **Episodes reference assets by name only** (e.g. `deeni_v1` + `dance-1`). Any design change = new version (`v2`), reviewed, and never mixed with v1 in the same episode.

### Honest note on Phase 3 cost
Building four good, rigged 3D characters is the largest single job in the project. The free route is learning Blender modelling and rigging (several weeks for a beginner). The faster route is a one-time freelance commission for the four models and rigs; that would be a one-time cost, not a subscription. Everything after that (animation, rendering, upload) can stay free.
