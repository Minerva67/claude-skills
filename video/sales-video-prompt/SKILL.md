---
name: sales-video-prompt
description: Turn a dense, abstract, hard-to-sell product or analysis (trusts, insurance, tax structures, funds, compliance software — anything where the PDF/PPT goes unread) into ONE complete, personalized sales-enablement video prompt for a hybrid generation engine (precision motion graphics + spatial 3D + atmospheric footage). Use whenever the user wants to pitch or explain a complex offering to a SPECIFIC client or prospect as a video — "make a video prompt", "转成视频提示词", "帮客户做个视频", "sales video", "advisor marketing video", "把这个分析/报告/PPT做成视频", personalized pitch film, sales enablement video. Trigger even if they never say "sales" — any request to script a client-facing video about a complex/boring product qualifies.
---

# Sales-Video-Prompt: The Mirror Method

Produce ONE complete, self-contained video-generation prompt that sells an abstract,
high-ticket product to one specific person. The output is a master prompt a hybrid
video engine can execute — never a script, never per-scene fragments, never a deck.

## Why this method exists

An AirPods ad is one-to-many because the product is identical for everyone. Here the
product is boring and identical (a trust is a trust, a fund is a fund) — but **the
client isn't**. The video's job is not to teach the product; it is to make one specific
person feel *seen* — their numbers, their family, their built thing — and then present
the product as the obvious way to protect what they already care about. Personalization
IS the product. That is what a PPT physically cannot do and what justifies the spend.

The proven visual grammar is Ray Dalio's "How the Economic Machine Works" (motion
designer Jonathan Jarvis): *distilled visuals serve as anchors that take the heavy
descriptive lifting off the narration — visuals keep the details clear, narration keeps
the big picture clear.* Sophisticated audiences watch 30 minutes of that. They will not
watch 30 seconds of stock-footage sentimentality.

Read `references/worked-example.md` before writing your first prompt — it is the
gold-standard output (a $16M estate-tax film) with annotations on why each choice won.

## The pipeline

Work through these steps IN ORDER. Each step's output feeds the next.

### Step 0 — Explore the client (the personalization layer)

Extract from the user's brief (ask only if truly missing; otherwise infer and flag):

- **Who**: name, age, family, what they built / their identity anchor
- **The event**: liquidity event, deal lost, deadline — the reason NOW
- **The hero number**: ONE figure that quantifies the pain (tax owed, deal size lost,
  months burned). Real, verified from the brief, used sparingly.
- **The dominant motivation**: FAMILY / CONTROL / GROWTH / GIVING / FEAR-OF-WASTE —
  this re-weights the promise and CTA beats
- **The recommended move**: the one product/structure being sold, named plainly once
- **Buyer sophistication**: consumer vs. sophisticated (see Register Calibration below)

Put these in a `PERSONALIZATION LAYER` / `FIXED FACTS` block with `{SLOTS}` so the
same skeleton can be re-skinned for the next client. Never invent numbers; compute
derived figures (gaps, projections) explicitly and state assumptions (e.g. "6%/yr").

### Step 1 — Knowledge backbone: compress to ~6 beats on the sales arc

Compress everything the source material says into the beats that survive. Kill jokes,
repetition, and anything the buyer already knows. The arc (rename beats per topic):

1. **WHY YOU MUST CARE** — insight-based anxiety. Never one scary number they already
   know; instead a *reframe* — several forces compounding against them that their
   current plan didn't price in ("your shield is frozen, your money isn't, and the
   rules change in 2026"). Smart people are hooked by "I hadn't thought of it that
   way", insulted by "boo, taxes."
2. **THE REVERSAL** — the outcome they want, asserted as real. Short. Emotional turn.
3. **THE MACHINE** — how it actually works. The densest beat. Full mechanism, real
   thresholds, real rates. This is where trust is earned; do not dumb it down.
4. **RISK ANSWERED** — the floor ("worst case you get your money back"), then the
   multiplier (roll it, stack it, repeat it). Objections die here, before the pitch.
5. **THE LEDGER** — the payoff. Two futures side by side on the same timeline:
   do-nothing vs. the move, numbers rolling, one final difference-figure that HOLDS.
   This beat gets the most seconds. It is the moment only video can deliver.
6. **LEGACY + CTA** — one earned, dignified image; then a quiet door: "we've already
   modeled this on your actual numbers — ready when you are." Never urgency.

### Step 2 — Time budget

Divide total runtime across beats by narrative weight, not evenly. Defaults for 5
minutes: 50 / 35 / 60 / 55 / 60 / 40 = 300s. The ledger (payoff) and the machine
(trust) get the most; the reversal and CTA the least. State the arithmetic in the
prompt's footer so the engine and the user can check it sums to target.

### Step 3 — Engine assignment (per beat, stated in the prompt)

- **PRECISION layer** (~70% of screen time, the protagonist): everything exact —
  charts, flows, formulas, timelines, counters, ledgers, on-screen text. Crisp flat
  vector motion graphics; monospaced digits so numbers roll and align. Anything a
  diffusion model would misspell or misplace belongs here.
- **SPATIAL layer** (only where a physical object argues faster than words): minimal
  dimensional objects — a rising water level, a lever on a fulcrum, a stack of vaults,
  two doors. Each object IS an argument; never decoration.
- **ATMOSPHERE layer** (rare, expensive-feeling): soft filmic desaturated footage for
  mood and era — the thing that is costly to hand-build and easy to get wrong by
  geometry (a 2015 office, erosion tides, one legacy image). Always UNDER the
  graphics; never touching a number; typically only in beats 1, 2, and 6.

Never name models, engines, or tech stacks in the output prompt (no "Manim", "Sora",
"Three.js", "diffusion model X"). Describe layers by role and look only.

### Step 4 — Art system (one look, end to end)

- One base palette (e.g. ink-navy base, bone-white type, one metallic accent) held
  across ALL beats — six scenes must read as one film.
- **Semantic colors**: assign LOSS and GAIN (or product-A/product-B) each a color in
  beat 1 and reuse them everywhere — the viewer learns the code once and then reads
  every later chart instantly.
- **Recurring motifs**: introduce devices once (the frozen line, the red gap, the
  vault, the shear-off stream) and reuse them, so the film teaches its own visual
  language and each beat reads faster than the last.
- Serif headlines + monospaced numerals; unhurried, premium pacing. Atmosphere footage
  low-saturation with subtle grain.

### Step 5 — VO: every line carries a fact, every fact gets an anchor

**THE ANCHOR RULE (prime directive — put it verbatim at the top of the prompt):**
Every fact the narrator speaks must trigger a synchronized on-screen event in the same
second — a line freezing, a curve climbing, a gap filling, a number rolling. Visuals
carry the details; narration carries the big picture. During data beats no frame sits
still longer than ~4 seconds. Mood footage may breathe; data may not.

VO rules: dense and concrete (real figures, real rates, real dates); the hero number
spoken once at full weight; second person throughout ("your sixteen million"); no
filler, no flattery, no repeated points. Write VO in the language of the deal (default
English for US financial products; localize on request).

### Step 6 — Assemble the master prompt, then run the director gate

Assemble into the Output Skeleton below. Then self-check — if any answer is no,
rewrite before delivering:

1. **Would the client buy?** Watch it as the buyer. Does anything smell like being
   sold to (stock sentimentality, flattery, fear-mongering, urgent CTA)?
2. **Does every VO sentence have a same-second visual event?** Scan beat by beat.
3. **Does the payoff beat exist** — a side-by-side moment only video can do?
4. **Is every number real** (from the brief or explicitly assumed) and personalized?
5. **Is it ONE self-contained prompt** with zero engine/stack names?

## Register calibration

Choose by buyer, it changes everything:

| Lever | Consumer buyer | Sophisticated buyer (HNW, exec, CTO) |
|---|---|---|
| Anxiety | fear, loss, urgency | insight-reframe; compounding forces they hadn't priced |
| Emotion | warm montage | ONE restrained, dignified image, earned late |
| Numbers | big scary figure | the figure they DIDN'T know; "recoverable, not lost" |
| Posture | persuade | respect — assume they have advisors and a plan already |
| Social proof | testimonials | peer-norm framing ("families holding this kind of liquidity") |
| CTA | act now | quiet door: analysis already run on their numbers, no urgency |

## Output skeleton

Deliver exactly one fenced block in this shape (rename labels per topic):

```
MASTER PROMPT — "<Title>" | Personalized <audience> Film, ~<N>s
Structure: <arc summary>.

═══ PRIME DIRECTIVE: THE ANCHOR RULE ═══  <verbatim rule>
═══ ENGINE ASSIGNMENT ═══                 <three layers, roles, % of screen time>
═══ ART SYSTEM ═══                        <base palette, semantic colors, motifs, type>
═══ FIXED FACTS ═══                       <real numbers; {SLOTS} for personalization>

BEAT 1 — <NAME> (<sec>s) | <purpose> 
<layered visual: what appears, in what order, synced to which VO line>
VO: "<dense, factual, second-person>"
... (all beats) ...

BUDGET: <a+b+c... = total>s. <which layers lead which beats; which motifs recur>
```

## Hard rules

- ONE complete prompt, never fragments. No model/engine/stack names inside it.
- Real numbers only; state growth/rate assumptions.
- Atmosphere never touches a number. Precision layer is the protagonist.
- The film must feel made for this one person — because the numbers are theirs.
