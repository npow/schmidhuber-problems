# Pivot moments — verbatim Yad prompts

*By Yad Konrad — [@0bserver07](https://github.com/0bserver07)*

Every user prompt during the build that was longer than a status check, with the timestamp it landed and (where applicable) what changed afterwards. Pulled directly from `analysis/data/sessions.jsonl`, orchestrator session `63285119-154e-42ab-9555-7a42471b0309`.

Twelve of these are quotable. Six reshaped the build.

## During the build (2026-05-06 → 2026-05-08)

### Initial direction (~16 minutes before wave 0)

**2026-05-06T23:08**

> /Users/yadkonrad/dev_dev/year26/may26/schmidhuber-problems  
> https://github.com/cybertronai/schmidhuber-problems/tree/main  
> https://github.com/cybertronai/hinton-problems  
> hinton session reference: d8af4bb0-1435-4528-a5da-ac91c30b7bcb  
> Okay, so I'm specifically interested in Yaroslav pointing out that we potentially should try implementing Schmidt-Uber et al.'s problems and the repository I have cl...

**What changed:** Orchestrator opened SPEC issue #1 at 23:20, did TeamCreate at 23:23, dispatched the first teammate (`nbb-xor-builder`) at 23:24. The hinton-problems precedent was lifted directly as the template.

### Wave-1 trigger

**2026-05-07T00:11**

> alright shall we do clean up and dispathc multiple agents to finish the rest of the waves?

**What changed:** First parallel-dispatch wave. Six wave-1 builders launched 9 minutes later.

### Audit-then-dispatch protocol

**2026-05-07T00:15**

> review it/audit and post the comment, then dispatch after please

**What changed:** Locked in the per-wave protocol that held for the next 11 waves: audit subagent runs before the next wave dispatches.

### ⭐ Branch-spam pushback (Type A pivot #1)

**2026-05-07T01:31**

> why are u doing a branch per impl, should it be per waves?? why the branch spam. THIS IS WRONG PRACTICE COURSE CORRECT!

**What changed:** PR #2 closed at 01:38; reissued as PR #5 on `wave/0-sanity` branch. All `impl/<slug>` remote branches deleted. From wave 2+, per-stub branches stay LOCAL ONLY (`wave-N-local/<slug>`). This is the single highest-leverage hop of the build.

### Status pressure

**2026-05-07T01:54**

> there is 1 comment and 1 pr, whats up man. where hte progress why stop?

**What changed:** Orchestrator picked up the wave-2 dispatch. Wave 2 PR #6 landed 39 minutes later.

### ⭐ Autonomous-mode trigger (Type A pivot #2)

**2026-05-07T02:11**

> I need you to not rely on me anymore until you finish it all, basically, do wave into 1 per, audit, post to pr then trigger next wave

**What changed:** Eight subsequent waves (3 through 10) ran without further direction. The orchestrator handled the audit→PR→shutdown→next-wave loop end-to-end. Verified by the 8-hour gap between wave 3 launch and the next user prompt.

### Overnight gap surfaced

**2026-05-07T12:11**

> what do u mean wait, its been 12 hours and you stopped i asked you to not stop and continue, this terrible you have slowed me down

**What changed:** Lead resumed dispatching. Wave 3 audit at 12:12, then waves 4/5/6/7/8/9/10 cascaded over the next 6 hours. (The "stopped" was real — overnight idle gap between 2026-05-07T03:35 and 12:11.)

### v1.5 trigger

**2026-05-08T13:55**

> lets please finish everything and deal with the full impelmentations  
> remember what Yaroslav asked for? when we finish we need to draw the full pictres as well  
> stats, site, build notes and all the other stuff  
> **BUT FIRST FIRST FINISH THESE THINGS REMAINING**

**What changed:** Wave 11 (v1.5, 8 heavyweight-env stubs) dispatch. The "stats, site, build notes" became the meta PR #16.

### Site-formatting nudge

**2026-05-08T14:44**

> its mdBook, make sure its similar to Hinton's one and dont make things up buba

**What changed:** Lead built the schmidhuber-problems site to mirror the hinton-problems mdBook structure exactly — same SUMMARY.md hierarchy, same RESULTS.md table format, same BUILD_NOTES.md template.

### ⭐ Verify-before-claiming-done (Type A pivot #3)

**2026-05-08T15:42**

> i still see the agents man  
> where and why the site link is not in the gihub repo, why and where is the merge branch by branch, and have we verified thse things to be truely done or left over? same as hinton's work or not?

**What changed:** Surfaced the unmerged-PRs gap. Explicit merge instruction followed. The batch-merge of all 13 PRs (PR #5, #4, #6, #7, #8, #9, #10, #11, #12, #13, #14, #15, #16) happened minutes later in a 90-second burst at 15:49–15:50 UTC.

### Site 404 reported

**2026-05-08T16:31**

> on the site docs  
> Document not found (404)  
> This URL is invalid, sorry. Please use the navigation bar or search to continue.  
> https://cybertronai.github.io/schmidhuber-problems/BUILD_NOTES.html

**What changed:** mdBook generates lowercase-hyphenated HTML filenames; the original prose referenced `BUILD_NOTES.md`. PR `fix(build-book): rewrite uppercase meta-doc links to lowercase HTML targets` fixed the link rewrites in `bin/build_book.py`.

### Tg post for finished build

**2026-05-08T16:44**

> ok what a brief message for the Tg since its done  
> we did it again, 780k token, took a little longer, since only paid attention every 18 hour window while i have other things going on/  
> we have the things Yaroslav asked:  
> https://cybertronai.github.io/schmidhuber-problems/  
> Site: https://cybertronai.github.io/schmidhuber-problems/  
> Catalog: RESULTS.md  
> Visual tour: VISUAL_TOUR.md  
> Build notes: BUILD_NOTES.md

**Note:** The "780k token" referred to the harness's context-window meter — was misread as total tokens. Correction posted in issue #19 + PR #20 (token-math-correction). Lesson: the harness number is context utilization, not total token spend; **the actual was ~661M tokens across 63 sessions (lead + 62 dispatches), 93.5% cache_read.**

### Token math correction

**2026-05-08T16:57**

> ok, quesiton on token consumtion.  
> do we have a good answer for Yaro how we are so token efficient? is it coutable or we are wrong for the sessions?parallel agents not counted?  
> > I'm surprised it's so token efficient, 780k is less than $30 if you paid full API costs

**What changed:** Triggered the deeper audit. Lead pulled actual numbers from the JSONL session logs, posted issue #19 with the analysis at 2026-05-08T17:09, then PR #20 to correct BUILD_NOTES.

**2026-05-08T17:08**

> make a github issue explaining the math aof the toens, sessions, and not the dollar, but the cache and such

**What changed:** Issue #19 *"Note: how to read the token / session / cache numbers for this build"* opened with the corrected math. PR #20 closed it.

### Hinton-parity follow-up

**2026-05-08T19:22**

> shall we now look at the session doing this for the Hinton session and id?  
> https://github.com/cybertronai/hinton-problems  
> Session ID: d8af4bb0-1435-4528-a5da-ac91c30b7bcb Project: SutroYaro (the lead session was checked out there) Output: cybertronai/hinton-problems — 53 stubs, all merged Span: 2026-05-01 21:52 → 2026-05-04 03:35 (~30 wall hours, with overnight idle gaps)

**What changed:** Triggered the same BUILD_NOTES-from-JSONL extraction on the hinton-problems repo. The hinton-problems repo got an analogous BUILD_NOTES update mirroring the schmidhuber format.

### Final merge approval

**2026-05-08T19:37**

> fix merge both PRs?

**What changed:** Schmidhuber PR #20 (token math) and the hinton-problems counterpart PR both merged.

## After the build (2026-05-09)

### SutroYaro role question

**2026-05-09T18:07**

> so what is SutroYaro useful for?

**What changed:** Triggered the "Scoped role of this repo" section in `CLAUDE.md` and the SutroYaro reshuffle issue #96. Made explicit that SutroYaro is the dispatcher + lab memory, not a benchmark repo.

## Patterns in these prompts

- **No prepared briefs.** Every Type-A prompt is one paragraph max, ungroomed for grammar.
- **Direct frustration is high-leverage.** "THIS IS WRONG PRACTICE" was the catalyst for the wave-1 → wave-2 fix.
- **"Verify, don't claim"** — "have we verified thse things to be truely done" surfaced the unmerged PRs that the autonomous loop had left untouched.
- **The 18-hour gap** between Yad's attention windows is real and visible in the JSONL timestamps. The autonomous loop has to survive these gaps without drift.

## Quotes worth reusing in the writeup

The five highest-impact, in order of leverage:

1. *"why are u doing a branch per impl, should it be per waves?? why the branch spam. THIS IS WRONG PRACTICE COURSE CORRECT!"* — 2026-05-07T01:31 UTC
2. *"I need you to not rely on me anymore until you finish it all"* — 2026-05-07T02:11 UTC
3. *"have we verified thse things to be truely done or left over?"* — 2026-05-08T15:42 UTC
4. *"alright shall we do clean up and dispathc multiple agents to finish the rest of the waves?"* — 2026-05-07T00:11 UTC
5. *"only paid attention every 18 hour window while i have other things going on"* — 2026-05-08T16:44 UTC, self-summarizing the rhythm

Each is a sentence that reshaped or characterized the build. Verbatim including typos.
