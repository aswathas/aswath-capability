# Architecture

## The shape

Three layers. You only write the top one.

```
Atomic skills          one job each, markdown, ~2,000 of them exist
      │
      ▼
Skillsets              curated pipelines for a use case, with gates
      │
      ▼
aswath-capability     resolves, detects gaps, authors what's missing, orchestrates
```

**Atomic skills are a commodity.** They come from humans and marketplaces. The
orchestrator never edits one in place, because a skill you have silently
rewritten is a skill whose behaviour you can no longer reason about.

**A skillset is a plan with checks**, not a document. It says which atomic
skills fire in what order and what has to be true before the next one starts.
`skillsets/ui-design.json` has eight phases and each one carries a `gate` that
is checkable: a command that passes, a screenshot that exists.

**The orchestrator** is the only thing that reasons about which of the three to
use.

## The eight phases

| Phase | Job | Gate |
|---|---|---|
| 0. Intake | Parse goal, surface, constraints, unknowns | none |
| 1. Brainstorm | Ground the brief with the user | **gate 1** — design doc approved |
| 2. Feasibility | GO / GO-WITH-CHANGES / NO-GO, with evidence | none |
| 3. Resolve | Query the registry, detect gaps, author what's missing | none |
| 4. Plan | Phases, skills, agents, gates, cost | **gate 2** — plan approved |
| 5. Build | Execute; delegate loops to external runtimes | none |
| 6. Roast & Fix | Criticise, refute, fix, re-verify | none |
| 7. Verify & Report | What was verified, what was not, what it cost | none |
| 8. Promote | Record outcomes, propose what becomes permanent | **gate 3** — user approves |

Three gates. There is no fourth, and adding one is a design change.

### Why the brainstorm gate exists

Even when the brief looks complete. The most expensive failure in this system is
building the wrong thing confidently, and a gate costs one exchange.

### Why feasibility is its own phase

Because "will this actually work" and "how should we build it" are different
questions with different failure modes. A verdict with `CONFIDENCE: low` and
named gaps is more useful than a confident verdict built on thin research. The
build phase trusts the confidence rating, so it has to be explicit.

## The promotion contract

```
GAP FOUND
   ↓
author into session scratch        ← always allowed
   ↓
use it for the current task         ← always allowed
   ↓
did it work?                       ← evidence, not vibes
   ↓
propose at the end of the build     ← one proposal, batched
   ↓
USER APPROVES → write to ~/.agents/skills/<name>/   ← requires a yes
   ↓
rebuild the registry                ← so the next session routes to it
```

Three rules hold this together:

1. **Nothing is written permanently without approval.** That includes skills,
   settings hooks, and installed plugins.
2. **Third-party installs are a supply-chain decision, not a technical one.**
   An installed plugin can run code and inject instructions into every future
   session. Searching and staging is free; installing needs a yes. Plugins that
   also register hooks or MCP servers are never auto-installed, because those
   run outside the skill system and cannot be audited at call time.
3. **A local skill beats a marketplace install.** A skill you can read is worth
   more than an install you trust.

Your accept/reject is the highest-weight signal in the system. A skill you
rejected stops being selected, even if its description matches perfectly.

## Why the orchestrator does not train anything

The obvious way to make a skill system "self-improving" is to accumulate
trajectories and fine-tune a model on them. That needs a data pipeline, training
infrastructure and a serving path, against a session that runs 253 local skills
in a 524k window.

The compounding lever is not weights. It is a **measured score ledger and a
promotion rule**: every skill version gets scored on the same evals, new
market skills must beat the incumbent to be promoted, and your accept/reject
outranks both.

A semantic-embedding index over skill documentation is the agreed bolt-on later.
It would make *"find the skill that does exactly this"* work across 3,605
installable plugins, including ones whose names you would never guess. It
cannot rank quality, only relevance, so it belongs beside the ledger, not
instead of it.

## What "self-improving" actually means here

It is three concrete mechanisms, not one:

1. **The registry notices new skills.** Nine UI skills appeared on the machine
   mid-build. The registry picked them up on the next rebuild, the taxonomy
   tagged them, and the `ui-design` skillset absorbed them. Nobody wired that
   up by hand.
2. **The ledger remembers what worked.** Accept/reject writes a score that
   feeds ranking directly.
3. **A skill that was written for a real gap gets proposed for permanent
   life** once it has been used and has evidence behind it.
