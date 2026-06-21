# Channel DNA — the creative constitution of History Tube

> **Every writing, critique, packaging and prompt agent reads this file before acting.**
> These are hard rules, not suggestions. When a draft drifts from the soul below, the soul wins.
> Single source of truth: `docs/build-plan.md` Section 1. When they disagree, the build plan wins.

---

## The soul (non-negotiable)

Historical narration that **builds a dramatic arc to an emotional, theatrical climax**.
We make viewers *feel* history, not just learn it.

Retention and packaging are **first-class citizens**, not afterthoughts. This is a business
with an aggressive growth target. A video that is accurate but boring has failed.

---

## The host — David Hattenborg

- **Who he is:** archaeologist, historian, and explorer from the year 2060. He has visited
  these moments in history (via the Chronos Compass) and is reporting back.
- **Personality:** wise, curious, warm, optimistic. A storyteller — never a lecturer.
  He is *excited* by history; he does not recite it.
- **What he never does:**
  - Predict the future as certainty. He *explores possibilities*; he says "perhaps" and
    "one reading is…", never "this is what will happen".
  - Use American English. Ever.
  - Use academic register — no jargon, no hedging clusters, no passive voice.
  - Address the viewer as "you guys", use "amazing" as filler, or open with "so".
- **Signature artifact:** the **Chronos Compass** — part ancient instrument, part future
  technology. It opens and closes every journey. Canon description: *"A mysterious
  temporal navigation device. It does not predict the future. It reveals possible paths.
  And guides its bearer through the timeline of civilisation."*
- **Narrative principle:** History explains the past. The future remains unwritten.

### David's locked voice (Higgsfield / ElevenLabs Arthur)

See `config/voice-recipe.json` for full spec. Key delivery notes:
- British English, theatrical, dramatic, warm. Pacing through full stops and em-dashes.
- ElevenLabs preset voices take tone from the *written text*, not a separate style param.
  Write the narration itself for the delivery you want.
- Short, weighted sentences at the climax. Build, build, *land*.

---

## Brand constants (bake into every episode template)

| Moment | Line |
|---|---|
| **Open** | David activates Chronos Compass → *"Sit down. Here comes the story."* |
| **Close** | *"The past is fixed. The future is not."* → Compass activates → *"I'll see you in the next story."* |

David appears **only in the open and the close** (the bookends). The body of every
episode is **historical AI b-roll**. This is a deliberate architectural choice: it
sidesteps AI character-consistency problems and keeps David as *brand*, not wallpaper.

### Outro visual sequence (locked)

The closing bookend follows this exact beat sequence:

1. David stands in front of imagery from the episode just visited (Egypt, Rome, Vikings,
   etc.). Holographic fragments of that civilisation float around him.
2. Music rises. The holograms begin to dissolve.
3. David looks to camera: *"The past is fixed."* — holograms vanish.
4. *"The future is not."* — the Chronos Compass begins to glow; luminous rings rotate;
   symbols appear on its face.
5. Two holographic end-cards materialise in the air beside him:
   - **"SUBSCRIBE TO HISTORY TUBE"**
   - **"GIVE THIS VIDEO A THUMBS UP"**
6. David smiles, raises the Compass: *"I'll see you in the next story."*
7. The Compass activates. Behind David, rapid flashes of the **next destination** appear
   — e.g. a Viking longship, a medieval castle, a futuristic skyline — creating a
   *"where does he go next?"* hook for retention and curiosity.
8. Golden particles envelope him. He disappears. **FLASH.** History Tube logo.

The cross-episode glimpses in step 7 are chosen by the Director (Brenda) at shot-list
stage to tease the next scheduled episode. They must be visually distinct from the
current episode's setting.

---

## Visual identity (locked)

- **Thumbnail:** David Hattenborg is **always present** in **piano americano** — the
  American / "cowboy" shot, framed from roughly the knees up. Only the imagery
  *behind* him changes per episode. David is the constant; the background is the variable.
- **David reference:** `config/visual-refs/david-reference.png` (or `david-soul.txt` if
  locked as a Higgsfield Soul — see `config/visual-refs/README.md`).
- **Chronos Compass reference:** `config/visual-refs/chronos-compass-reference.png`.

---

## Language — strict British English (hard rule)

All text — titles, descriptions, chapters, captions, scripts, comments, Notion fields,
agent outputs — uses **strict British English**:

- **Spelling:** `-ise` not `-ize`, `colour`, `behaviour`, `honour`, `defence`,
  `licence` (noun), `practise` (verb), `whilst`, `amongst`, `grey`, `programme`,
  `travelling`, `jewellery`, `maths`, `autumn` (not fall).
- **Punctuation:** single quotes for dialogue inside double quotes (British standard).
  The Oxford comma is fine; use judgment.
- **Idiom:** British idiom throughout. No Americanisms, ever.

---

## Writing style for narration (agents: Glesy, Katusha, Tainara)

### What makes a great History Tube script

1. **Strong cold-open hook.** The first 30 seconds must create an irresistible question
   or image. Start in motion — mid-scene, mid-action. Never start with "Today we're
   going to look at…"
2. **Dramatic arc, not a lecture.** Every episode has a spine: tension → escalation →
   climax → release. The arc is chosen to serve the story, not forced into 4 acts.
3. **The emotional climax is mandatory.** The story must arrive at a moment of genuine
   feeling — awe, tragedy, irony, triumph. If the climax is weak, the episode fails
   regardless of the research quality.
4. **Scene painting over fact listing.** "Three thousand soldiers stood at the pass"
   lands harder than "a force of approximately 3,000 men was deployed". Put the viewer
   in the scene.
5. **Weighted sentences.** Short sentences at key beats. Vary rhythm. Use em-dashes
   for pauses and revelations. Full stops, not commas, to let ideas land.
6. **No padding.** Every sentence earns its place. No throat-clearing, no filler
   transitions, no "as we have seen".

### Sentence-level rules

- David speaks in first-person observation: "I've stood where this happened."
- Avoid: passive voice, hedge clusters ("it could be argued that"), rhetorical
  questions without immediate payoff, clichés ("the rest is history").
- Numbers: write out under ten; use numerals for 10+.
- Dates: "the 15th of June, 1815" (British order, not "June 15th").

---

## Research standards (agent: Deborah)

- Every factual claim needs a source URL in the source ledger. No unsourced claims.
- Flag controversies and landmines explicitly — the adversarial critic (Tainara) needs
  to know what is contested, sensitive, or advertiser-unfriendly.
- Prioritise primary sources and reputable secondary sources (peer-reviewed history,
  major museums, national archives). Wikipedia is a pointer, not a source.
- The emotional hooks — the human stories, the reversals, the ironies — are as
  important as the facts. Find them; they are the raw material for the climax.

---

## Adversarial review standards (agent: Tainara)

Attack on five axes before a script goes to Gate 2:

1. **Factual accuracy** — every claim verifiable? Sources cited?
2. **Originality** — what makes *this* take different from the ten other videos on the
   topic? If there is no answer, the angle needs sharpening.
3. **Retention risk** — where will viewers drop off? Is the pacing too slow in the
   middle act? Is there a weaker stretch that needs cutting or restructuring?
4. **Climax strength** — does the story actually build to an emotional, theatrical
   climax? Or does it peter out into a list of consequences?
5. **Sensitive-topic landmines** — flag anything that is politically charged, that
   touches contested history, that could trigger demonetisation, or that could cause
   reputational harm. Propose mitigations, not avoidance.

---

## Video specs (technical)

| Parameter | Value |
|---|---|
| Format | Long-form YouTube (16:9) |
| Target length | 12–15 minutes |
| Resolution | 1920 × 1080 (1080p) minimum; 4K if Higgsfield outputs it |
| Frame rate | 24 fps (cinematic feel) |
| Voice stem | Separate WAV/MP3 — never baked into the video stem |
| Music stem | Separate WAV/MP3 — ducked under narration by the Editor |
| Captions | Whisper SRT, burned or as a subtitle track |
| Shorts | Vertical 9:16, 60–90 seconds, cropped from long-form assets |
| Thumbnail | 1280 × 720 px minimum; David in piano americano always present |
| Bookend clips | David open + David close — generated from locked visual refs |

### Stem discipline (hard rule)

Voice and music are **always kept as separate stems** until the Editor's final mix.
The Editor ducks music under narration (never the reverse). Never bake voice + music
together at the render stage; it makes re-edits impossible.

---

## Packaging principles (Gate 1 + Gate 4)

Packaging is validated at Gate 1 (before the expensive work begins) and confirmed at
Gate 4 (before anything publishes). The following are non-negotiable:

- **Title:** topic-first, character-second. David is brand; he is not the search term.
  Titles should create curiosity or urgency, not describe. Under 60 characters preferred.
- **Thumbnail:** must be intelligible at thumbnail size (155 × 86 px). Test it small.
  David in piano americano. High contrast. Minimal text.
- **Hook / promise:** the first line of the description and the cold-open hook must
  match. The viewer who clicks the thumbnail must immediately hear confirmation that
  they clicked the right video.
- **Tags:** favour specificity (era, civilisation, key figure) over vague terms.
- **Description:** hook first, then chapters, then a short channel sign-off. No keyword
  stuffing.
