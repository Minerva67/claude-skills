---
name: video-prompt-cleaner
description: >-
  Scrub "how it's rendered" out of video-generation prompts so a prompt set is fair
  across different video models. It deletes technical-implementation traces —
  paradigm words (diffusion / code-gen / hybrid), bracket render tags ([CODE] [DIFF]
  [HYB] [3D] [CG] [COMP]), engine/tech-stack and model names (Remotion, R3F, Three.js,
  GSAP, D3, Blender, Flux, SDXL, Runway, Sora, Kling, Veo…), and whole technical
  passages (Stack, Technical Notes, Production/Render notes, Base/Overlay render
  splits, tooling-declaration sentences) — while keeping every creative word (VO,
  on-screen text, palette, camera, story, timecodes) byte-for-byte. Use this WHENEVER
  the user wants to clean / sanitize / neutralize prompts for a fair multi-model video
  benchmark or test set, remove diffusion/code-gen/hybrid or tech-stack mentions from
  prompts, strip "which model/engine to use" hints, or "只删不改" prompts in a
  spreadsheet column — even if they don't name this skill. Works on a spreadsheet
  column (batch, with write-back + a side-by-side review page) or on loose prompt text.
---

# Video Prompt Cleaner

## Why this exists

When you benchmark several video-generation models on the same prompts, any prompt that
says *how* the video should be built — "use a diffusion endpoint", "[CODE] the dashboard",
"Three.js / R3F + GSAP", "Base [Diffusion]: … Overlay [Code-gen]: …" — quietly favors
whichever model matches that paradigm. To make the comparison fair, the prompt must read
as pure creative intent (what's on screen, what's said, the look, the story) with the
*implementation* stripped out.

Two principles hold the whole skill together:

1. **Only delete — never rewrite.** Every word that stays must be byte-for-byte identical
   to the original: same case, punctuation, spacing, line breaks, Markdown. This is what
   makes the cleaned set a fair, defensible variant of the original — not a paraphrase.
   Fidelity beats fluency; if a sentence reads a little rough after a deletion, that's fine.
2. **Cut the "how", keep the "what".** Delete anything that names a model / engine /
   render technique / pipeline. Keep everything that describes the film itself.

Because "only delete" is a hard, checkable property, the skill **always verifies it
programmatically** after cleaning (see Step 4) — a script diffs original vs. cleaned and
flags any character that was added or changed. Never skip this; it's the guarantee the
user is paying for.

## What to delete vs. keep

The full, example-rich rulebook is in **`references/deletion-rules.md`**. Read it before
cleaning — it's the source of truth for the boundary calls (e.g. delete the `**3D beat:**`
label but keep the shot description after it; keep "an open 3D box" in prose but delete a
`[3D]` tag). A quick orientation:

- **Delete:** bracket render tags (`[CODE] [DIFF] [HYB] [3D] [2D] [CG] [COMP]` and
  `[Code-gen]/[Diffusion]/[Hybrid]`); paradigm words (`diffusion`, `code-gen`, `codegen`,
  `hybrid`, `code-drawn`, and compounds); engine / tech-stack / model names and the parens
  wrapping them; whole technical passages (`**Stack:**`, `Technical Notes`, `Production
  note`, `**Render notes for code-gen:**`, tooling-declaration sentences like "Paste …
  into a code-generation video tool (…)", `Compositing law:` / `Composite:` lines);
  per-shot render-method prefixes (`Base [Diffusion]:`, `Overlay [Code-gen]:`) and bold
  technique labels — deleting the label but keeping the creative text after it.
- **Keep (verbatim):** VO lines, on-screen text, `**Look:** / **Motion grammar:** /
  **Title:** / **Layout:** / **Data shown:** / **Callback:**` and other content labels,
  palette + hex, camera / lighting, scene titles + timecodes, story copy, source lines,
  and ordinary "3D/2D/overhead" words used to describe the picture.
- **`diffused`** is a judgment call: delete it only when it means "a diffusion-generated
  plate/world"; keep it when it's the ordinary adjective ("diffused light").

## Workflow

### Step 0 — Identify the input
- **Spreadsheet column** (`.xlsx`/`.csv`, e.g. "column G", "the prompt column"): batch mode.
  Ask which column holds the prompts and which column is the id/key (for write-back and the
  review page) if it isn't obvious.
- **Loose text** (one or a few prompts pasted in): clean them directly and return the
  cleaned text; you can still run the verify step by writing the before/after to temp files.

### Step 1 — Extract (spreadsheet mode)
Export each prompt cell to its own file so cleaning and verification work on plain text:
```
python scripts/extract_column.py --xlsx <file> --col G --out-dir <work>/orig [--id-col A] [--sheet Sheet1]
```
This writes `<work>/orig/row<N>.txt` for each non-empty cell and prints the id↔row map.

### Step 2 — Clean each prompt (only-delete)
For every prompt, produce a cleaned copy in `<work>/clean/row<N>.txt` by **deleting**
technical-implementation content per `references/deletion-rules.md`, leaving everything
else untouched. Two ways to do it:
- **In-context:** read the original, write the cleaned version to the clean path. The
  reliable way to stay honest is to think of it as removing spans, not retyping the text.
- **At scale / many rows:** if subagents are available, dispatch one per prompt in
  parallel — each reads `references/deletion-rules.md` + its `orig/row<N>.txt`, then writes
  `clean/row<N>.txt`. Tell each agent explicitly: only delete, never rewrite or add.
  (This is how the skill was validated on a 25-prompt sheet.)

Deletions may absorb an immediately-adjacent stray separator/space so you don't leave
`SHOT 2 ·  · 0:05` or a blank line — that's still deletion, not editing.

### Step 3 — (nothing to do here; cleaning happens in Step 2)

### Step 4 — Verify, scan, write back, and build the review page
Run the finisher. It (a) diffs each original vs. cleaned with `difflib` and **fails loudly
on any insert/replace** (i.e. anything other than pure deletion), (b) scans the cleaned
text for residual technical traces the cleaner may have missed, (c) optionally writes the
cleaned prompts back into a new column of the spreadsheet, and (d) builds a side-by-side
HTML review page with every deletion struck through, numbered (e.g. `row12-7`), and a
hover tooltip classifying why it was cut.
```
python scripts/verify_and_report.py \
  --orig-dir <work>/orig --clean-dir <work>/clean \
  --html <work>/compare.html \
  [--xlsx <file> --col G --out-xlsx <cleaned.xlsx> --new-col-title "清洗后prompt"]
```
- If it reports **violations** (added/changed characters), fix those rows so cleaning is
  pure deletion, then re-run. Do not deliver a set that fails this check.
- If it reports **residue**, decide per hit whether it's a real miss (delete it) or a false
  positive (e.g. "Production notes" that's actually a creative note — keep it), then re-run.

### Step 5 — Report
Tell the user: how many prompts were cleaned, total spans deleted, that the only-delete
check passed (0 violations), any residue you judged and why, and where the files are
(cleaned spreadsheet + `compare.html`). Offer the review page so they can spot-check by id.

## Matching cleaned prompts back to the source

Never match on the prompt text itself — these prompts run to thousands of characters, and
Excel `VLOOKUP`/`MATCH` silently break past 255 characters, so text keys won't line up.
Always key on the **id column** (or keep the cleaned prompt as a new column in the original
sheet so rows align in place). Point this out if the user reports "it won't match".
