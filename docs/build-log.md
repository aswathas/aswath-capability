# Build log

The build in order. What was decided, what broke, what changed.

## The brief

> "I want a master intelligence skillset for specific use cases. aswath-capability
> can invoke anything from this world of skills and also build itself like a
> complete agent."

And the original framing: a UI skillset that composes `impeccable`,
`frontend-design`, `design-taste-frontend` and `hallmark`, takes references from
the user or offers template choices, tests for efficiency, and roasts the page
and improves it. Plus a system that keeps up with a market producing new skills
every week.

## Decisions made up front

**Three layers, not one.** Atomic skills are a commodity. Skillsets are curated
pipelines with gates. The orchestrator composes them. A single universal skill
was explicitly rejected: it loads its full weight on every use and cannot be
improved in one place without breaking the others.

**The autonomy boundary.** Three options were on the table: session-only
authoring, full autonomy, or session-first with promotion on approval. The
middle one won. It keeps a bad learn, or a hostile upstream skill, out of the
directory that every future session loads, while still letting the orchestrator
heal itself mid-build.

**No model training.** The obvious reading of "self-improving" is to accumulate
trajectories and fine-tune a model. That needs a data pipeline and training
infrastructure, against a session running 253 local skills in a 524k window.
The compounding lever is a score ledger and a promotion rule instead. An
embedding index over skill docs is the agreed bolt-on later.

## What the machine already had

A recon pass changed the shape of the build more than expected.

- `ask-matt` was already a router over skills, so the resolution layer was
  half-built.
- `design-taste-frontend` already shipped a 247-site reference library, a
  browser inspector and a linter. The "templates to choose from" and "actually
  look at it" requirements were largely done.
- `impeccable` already shipped a `finish_reviewer` and a `hooks.md`, so the
  "roast and improve" loop was half-designed.
- `plugin-catalog-cache.json` turned out to carry per-skill token cost **and**
  install counts, which is a real "what is the current best" signal.
- The claude-mem MCP server gave the learning loop its persistence substrate.

The point of the recon was to avoid rebuilding what existed and to find the
parts that were genuinely missing. The parts that were missing were the
registry, the gap detector, the delegation seam and the promotion contract.

## The build, in order

1. **Registry builder.** Scanned the filesystem and the marketplace catalogs.
   First version tagged skills by substring matching on descriptions, which
   produced `design-taste-frontend` as an ecommerce provider.

2. **Capability taxonomy.** Rewritten twice. The final version has three
   evidence channels, and the `files` channel came out of a specific
   observation: the reference files a skill ships are proof of what it does.

3. **Resolution engine.** `need`, `cap`, `gap`, `install`, `list`, `stats`.
   Ranking by quality, then installed-over-marketplace, then popularity, then
   cost.

4. **Gap detector.** The piece that makes the system honest. When nothing
   covers a capability, it says so instead of answering with the nearest
   available skill.

5. **Ledger and promotion.** Accept/reject writes a score. `--propose` batches
   everything worth keeping into one approval request.

6. **Staging.** Marketplace candidates are found and staged. Nothing installs
   without a yes.

7. **Subagent briefs.** Researcher (feasibility verdict with evidence),
   planner (executable plan with costs and named gaps), critic (one lens).

8. **The UI skillset.** Eight phases, each with a checkable gate and a quality
   bar that names what fails the work.

9. **Delegation.** Replaced an in-process orchestrator with the external agent
   CLIs, on instruction. Both backends turned out to fail in ways that look
   like success.

10. **Testing.** Every phase above was exercised against a deliberately bad
    landing page. Nine defects, all in [bugs-found.md](bugs-found.md).

## The part that mattered most

The first delegated roast run reported `fixer applied 0 fixes; 0 file(s)
changed` and then `reverify clean`.

Both halves of that sentence were wrong in different ways. The fixer had
reported no structured result because it does not produce one, and the
re-verifier had been asked a general question about a page, so it answered
about the page rather than about the specific defect it had been given.

The fix was not a better prompt. It was changing what counts as evidence:
the **diff** is the ground truth for whether a fix landed, and each confirmed
finding gets its own verdict with the source line that proves it.

After that change the same run reported, correctly:

```
NOT CLEAN: 2/2 confirmed findings still unfixed
  evidence: index.html:37 still defines ".stat .label { font-size: 13px; color: #999; }"
```

A loop that says "clean" when it is not clean is worse than no loop, because it
hides the problem it exists to find.

## Things that were tried and dropped

- **Substring filename matching** for capability tagging. Too loose; see bug 3.
- **A unified mega-skill.** Rejected for cost and coupling.
- **cmdc as the editing backend.** It runs its own audit instead of the brief.
- **The findings cap applied after verification.** Verifies 21, uses 3.

## Where it stands

Verified end to end for the registry, resolution, gap detection, delegation and
the roast loop. The eight-phase pipeline has not been driven through a complete
real build; that is the next thing to exercise.
