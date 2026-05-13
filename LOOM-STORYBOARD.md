# Loom storyboard — prospect-pulse demo for a Cursor GTM engineer

**Format:** screen share + face-cam bubble (bottom-right by default)
**Target length:** 3:45–4:30
**Goal:** peer-to-peer feedback ask, not a job inquiry. The thesis carries the credibility — you're handing them something concrete to react to.
**Demo arc:** thesis → corroboration design → headline evidence (Modal vs Replicate) → operational layer (routing pass + JVM split-pitch) → honest limit → repo + ask.

> **Open dependency:** the 0:00–0:25 hook reference and the 3:45–4:15 ask framing both depend on who the Cursor GTM engineer is and what they showed at the webinar. Those two spots are marked `[CUSTOMIZE]` below. Everything else is locked.

---

## Pre-flight checklist — do these before you hit record

### Repo state fix (required — the demo currently has a hole here)

`prospects/2026-05-13.md` is the **6-company JVM contrast set**, not the 20-company AI-tech scan. The Modal (Tier 2, 84) and Replicate (Tier 1, 94) rows the POV.md narrates as the headline finding are **only in git history** (commit `fb7fe9a`). If you flip to the prospects file on camera right now to "show the digest output," the rows aren't there.

Restore both digests as separate files before recording:

```bash
cd "/Users/ryan/Documents/Claude/Projects/Operation get a new job/prospect-pulse"

# Save the 20-company AI-tech scan from git history
git show fb7fe9a:prospects/2026-05-13.md > prospects/2026-05-13-aitech.md

# Rename current file to make its contents obvious
git mv prospects/2026-05-13.md prospects/2026-05-13-contrast.md

# Verify both exist and contain what you expect
head -5 prospects/2026-05-13-aitech.md     # should say "Scanned 20 accounts"
head -5 prospects/2026-05-13-contrast.md   # should say "Scanned 6 accounts"
```

You don't have to commit before recording — the files just need to exist on disk so they open in your editor. POV.md already links to `prospects/2026-05-13.md` in its inline references; if you commit the rename you'll want to fix that link too, but for the demo it's a non-issue.

### Tabs / windows to pre-open (left to right in your editor or browser)

1. **POV.md** — rendered preview (VS Code preview pane works; GitHub render works; whichever reads cleaner at 125% zoom). Scroll to top.
2. **prospects/2026-05-13-aitech.md** — scrolled so rows 4 (Replicate) and 5 (Modal Labs) are mid-screen.
3. **routing.py** — open to line 56 so `SPLIT_PITCH_JVM` is the first thing visible.
4. **prospects/2026-05-13-contrast.md** — scrolled to row 3 (Databricks) mid-screen.
5. **GitHub repo landing page** — https://github.com/ryanmichaels-jpg/prospect-pulse — open in a fresh tab, in incognito to confirm the public view (`main` already has the v2 README, verified today).

### Recording environment

- **Zoom**: 125–150% in editor and browser. Test on POV.md section headers — they should read at-a-glance, not squint-mode.
- **Face-cam bubble**: bottom-right. Confirm it doesn't cover the top of code/markdown files when you're scrolling.
- **Quit** Slack, mail, calendar reminders. Disable notifications.
- **Dock**: hide it (`Cmd-Option-D` on Mac) if you're worried about clutter showing in screen share.
- **Mic check**: do a 10-second test recording first. Loom's auto-volume sometimes clips on the first 2 seconds.

---

## The beats

### Beat 1 — Hook (0:00 → 0:25) · ~25 sec · face-cam centered, no screen

**What's visible:** just you. Either full-screen face-cam or screen-share inactive so the camera tile is large.

**What you're communicating:** the thesis in one sentence, plus the structural reason it matters. Don't open with "hey I'm Ryan, I'm an SDR at Pave" — open with the bet.

**Beats to hit (your words, your delivery):**
- The hypothesis: "AI-native" stops being a useful ICP signal by Q3 2026 because every B2B SaaS company scores yes on it.
- The structural alternative: stack-shape — specifically, is this a company Cursor's Composer and Tab disproportionately win on.
- `[CUSTOMIZE]` one-beat reference to the webinar / the engineer's talk to anchor why you're sending this to *them* specifically. Held for the GTM-engineer info to land.

**Pacing:** brisk. Don't oversell. The work is going to speak — the hook is just orientation.

---

### Beat 2 — POV.md thesis on screen (0:25 → 0:55) · ~30 sec · screen + camera bubble

**Switch to screen share.** POV.md open, scrolled to the top, rendered preview.

**What to point at (literally — move your cursor):**
- The H1: *"Stack-Shape, Not AI-Native — A POV on Cursor's Outbound ICP"*
- The thesis paragraph (line 5). Specifically the clause: *"is this company's engineering stack the shape that Cursor's Composer and Tab disproportionately win on?"*
- The four structural reasons (same paragraph): TS/React training-data density, multi-file edit compounding inside monorepos, boilerplate-heavy UI as Tab's sweet spot, frontend-bound IDE culture vs. terminal-bound infra culture.

**Talking-over-the-screen note:** don't read the paragraph verbatim. Paraphrase the four structural reasons in your own words while the cursor moves down them. The reader can do the reading; you're translating.

**Hold time:** ~5 seconds on the thesis line before you start moving. Let them read it.

---

### Beat 3 — How I tested it (0:55 → 1:25) · ~30 sec · screen + camera bubble

**Still in POV.md.** Scroll down to the *"How I tested it"* section (line 9 onward).

**What to point at:**
- The phrase "public-signal ICP scorer" — establishes that everything is verifiable from artifacts an SDR can check.
- The list of signals: GitHub language stats by repo count, `package.json` framework markers, NPM org cross-referentiality, careers-page keywords, hire velocity.
- The v1→v2 swap callout: `ai_native` reweighted 15→5, two stack-shape signals added, JVM disqualifier shipped.
- The validation gate line (line 11): *"no published Cursor customer drops below Tier 2 under v2. … v2 also passes 8/11."*

**The point of this beat:** establish that the rubric is testable and you tested it before shipping the new weights. The validation gate is the credibility move — a v2 that loses customers would be a v2 that's wrong.

**Pacing:** don't linger. This is the bridge to the headline evidence.

---

### Beat 4 — Modal vs Replicate, the headline (1:25 → 2:30) · ~65 sec · screen + camera bubble

This is the beat that earns the rest of the runtime. Two screens.

**Screen A — POV.md comparison table (1:25 → 2:00):**

Scroll to the *"The case the rubric was designed to find"* heading (line 13).

What to point at:
- The framing line above the table (line 15): *"Same starting cohort. Both AI-infra. Both Series B. Both ~80 employees. Both flagged ai_native: true. Both Tier 1 in v1, within 5 points of each other."*
- The table itself (lines 19–22). Specifically: Modal −20 vs Replicate −5.
- The mechanical explainer below the table (line 24): *"Both lost 20 points mechanically. … Replicate recovered 15 of them on the new stack-shape signals. Modal recovered zero."*
- The concrete evidence (line 26): point at the `@replicate/types-rest-api → @replicate/types-openapi` cross-reference and the `scribble-diffusion` / `llama-chat` Next.js demos. This is the SDR-verifiable artifact.

**Hold time on the table:** ~10 seconds. The −20 vs −5 delta is the visual punch.

**Screen B — prospects/2026-05-13-aitech.md (2:00 → 2:30):**

Switch tabs to the 20-company digest. Pre-scrolled so rows 4–5 are mid-screen.

What to point at:
- Row 4 — **Replicate · Tier 1 · 94**.
- Row 5 — **Modal Labs · Tier 2 · 84**.
- The `Why` cell for Replicate: the `v2 signals — strong ts_js_dominance` and `strong npm_org` strings. This is the rubric output narrating its own reasoning.
- The `Why` cell for Modal Labs: absence of those signals. Same vertical, same stage, opposite read.

**The narrative beat:** "Same evidence on a Monday-morning digest, opposite prioritization. The v1 rubric structurally couldn't see this — every weight that fired on Modal also fired on Replicate. v2 sees it because the corroboration is built in."

---

### Beat 5 — The routing pass (2:30 → 3:30) · ~60 sec · screen + camera bubble

The operational payoff. Two screens again.

**Screen A — routing.py, lines 56–74 (2:30 → 3:00):**

Switch to the `SPLIT_PITCH_JVM` constant.

What to point at:
- The `Route` dataclass name on line 22 (one-second nod — show that this is a typed object, not a string).
- The `pitch` string on lines 60–63: *"Public footprint shows JVM backend dominance AND substantial frontend / design-system investment. Lead with the frontend platform team, not the JVM service-ownership team. Cite the NPM org evidence in the opener."*
- The `target_seats` list (lines 64–68): frontend platform / design system / web platform.
- The `avoid_seats` list (lines 69–73): service ownership / backend service / JVM platform.

**Frame:** "The disqualifier subtracts points and stops. The routing pass converts the disqualifier outcome into a named outbound motion. Each route carries seats to target and seats to avoid — so the digest doesn't stop at 'Databricks lost 6 points,' it adds 'lead with the frontend platform team, cite @databricks/design-system.'"

**Screen B — prospects/2026-05-13-contrast.md, row 3 (3:00 → 3:30):**

Switch tabs to the contrast set digest.

What to point at:
- Row 3 — **Databricks · Tier 1 · 93**.
- The `Why` cell. Specifically these three strings, in order:
  - `strong jvm_disqualifier [JVM in top 3 active langs: Scala · JD refs: consul, envoy]`
  - `strong npm_org [@databricks: 13 packages · cross-ref: @databricks/lakebase depends on @databricks/sdk-experimental · DS primitives: @databricks/design-system]`
  - `route: split_pitch_jvm — Public footprint shows JVM backend dominance AND substantial frontend / design-system investment. Lead with the frontend platform team…`

**Frame:** "Disqualifier and positive signal co-firing on the same account. A v1-style rubric reads Databricks as a no. v2 reads it as a Tier 1 with a specific carve-out — the frontend team where `@databricks/design-system` lives, not the JVM service-ownership team."

**Hold time on the `route:` string:** ~3 seconds. That's the operational artifact — proof the rubric doesn't just score, it tells the rep what to do next.

---

### Beat 6 — The honest limit (3:30 → 3:50) · ~20 sec · screen + camera bubble

Stay in POV.md. Scroll to *"What v2 still can't see"* (line 50).

What to point at:
- The Brex demotion (line 52): *"score 77, public footprint is grpc-java-heavy, even though James Reggio's quoted statement implies heavy internal TS/React frontend adoption."*
- The framing line (line 54): *"the rubric scores what it can see; it tells you when public signal is going to misrepresent."*

**Frame:** "The rubric flags its own blind spot. There's a route in routing.py — `PUBLIC_UNDERESTIMATES_INTERNAL` — built for this case. Manual flag in seeds.yml, lead with the customer quote, pursue the frontend platform team."

**Why this beat matters:** showing you know where the work is wrong is the credibility move. A pitch that claims full coverage gets discounted; one that says "here's what I can't see and how I route around it" gets believed.

---

### Beat 7 — Repo + ask (3:50 → 4:20) · ~30 sec · screen + camera bubble, then camera-only

**Switch to the GitHub landing page tab.** README visible. Camera bubble bottom-right.

What's visible: the v2 README. The pipeline diagram. The routing pass section.

What to point at:
- The repo URL in the address bar.
- One brief glance at the README pipeline diagram so they see the architecture lives there.

**The ask `[CUSTOMIZE]`:** held for the GTM-engineer info to land. The framing is feedback, not job. Specific question is better than open ("does the thesis hold up under stack-shape over time?" or "where does this break for the segment you're focused on?" or whatever fits what they showed at the webinar).

**Last 5 seconds (4:15 → 4:20):** consider cutting to camera-only for the sign-off. Loom recordings that end on a human face land better than ones that end on a static screenshot.

---

## Pacing summary

| Beat | Time | Duration | Screen |
|---|---|---|---|
| 1 — Hook | 0:00–0:25 | 25s | Camera only |
| 2 — POV.md thesis | 0:25–0:55 | 30s | POV.md top |
| 3 — How I tested it | 0:55–1:25 | 30s | POV.md mid |
| 4a — Comparison table | 1:25–2:00 | 35s | POV.md table |
| 4b — Digest output | 2:00–2:30 | 30s | aitech digest rows 4–5 |
| 5a — Route definition | 2:30–3:00 | 30s | routing.py L56–74 |
| 5b — Route firing | 3:00–3:30 | 30s | contrast digest row 3 |
| 6 — Honest limit | 3:30–3:50 | 20s | POV.md "What v2 still can't see" |
| 7 — Repo + ask | 3:50–4:20 | 30s | GitHub + camera |
| **Total** | | **4:20** | |

Buffer for transitions, hesitation, re-takes of single beats: realistically lands 4:00–4:45.

## General pacing notes

- **Scroll slowly when you're talking; pause scrolling when you want a beat read.** Common mistake: scrolling while delivering the punchline, so the viewer's eye is moving while the words are landing.
- **Use the cursor as a pointer.** Don't drag-select text unless you want to highlight it. The mouse moving toward a phrase is enough to direct attention.
- **Don't read the screen.** Translate it. If the markdown says "strong ts_js_dominance [top 3 active langs: TypeScript (24), Go (8), Python (6)]," you say "TypeScript dominates their public repos, with corroboration from a package.json." The viewer reads the precise version, you carry the meaning.
- **Aim for one breath per beat.** If you find yourself running out of breath mid-beat, the beat is too long — cut something.

## What to do if you flub something at minute 3

Don't re-record from the top. Pause, take a breath, redeliver the beat, and edit the cut in post if Loom's trim isn't enough. Re-recording five times to get one perfect take usually makes the take stiffer than the first attempt. The peer-feedback frame tolerates a small stumble — perfection signals "this is a pitch" and breaks the frame.

---

## What to send me next

To close Beat 1 and Beat 7:

- The Cursor GTM engineer's name + what they showed at the webinar + their angle on GTM-engineering-as-a-discipline. One paragraph is enough.

Once that lands I'll backfill the two `[CUSTOMIZE]` spots and the storyboard is ready to record from end-to-end.
