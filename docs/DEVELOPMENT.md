# Development

How to work on this, upgrade it, and let it improve itself.

## Where things live

| | Path | What it is |
|---|---|---|
| **Source of truth** | `C:\Users\ADMIN\aswath-repo` | The git checkout. Edit here. |
| **Installed copy** | `~/.agents/skills/aswath-capability` | What Claude Code loads. A copy of `skill/aswath-capability`. |
| **Personal state** | `~/.agents/skills/aswath-capability/registry/ledger.json` | Your accept/reject scores. Never overwritten by an install. |
| **Staged** | `~/.agents/skills/aswath-capability/registry/staged.json` | Marketplace plugins waiting for your approval. |
| **Generated** | `~/.agents/skills/aswath-capability/registry/skills.json` | The index. Rebuilt on every install. |

The checkout is a normal git repository with `origin` set to
`github.com/aswathas/aswath-capability`. The installed copy is a **copy, not a
symlink**, because Windows holds a lock on the skill directory while any agent
process has it open. `install.py` reconciles the two, so drift is visible
rather than silent.

## The edit loop

```bash
cd C:\Users\ADMIN\aswath-repo

# 1. edit skill/aswath-capability/...
# 2. see what would change
python install.py --check

# 3. install it live
python install.py

# 4. commit
git add -A
git commit -m "..."
git push
```

`install.py` copies the source skill into `~/.agents/skills/`, **preserves your
ledger and staged files**, rebuilds the registry, and prints the result.

The registry is rebuilt automatically because it is derived state. If you change
`registry/capabilities.json`, the tags change on the next install.

## The upgrade loop

```bash
cd C:\Users\ADMIN\aswath-repo
git pull
python install.py
```

Tags are released as `vX.Y.Z` with a GitHub release. `git pull` gets the new
version; `install.py` puts it live and rebuilds the index.

If a new version changes the registry format, `install.py` rebuilds it from
scratch, so the index is never stale.

## The self-evolution loop

This is the part that answers "does it improve itself?" honestly. Three of the
four mechanisms are automatic; the fourth needed building, and is now in the
repo.

### Automatic

1. **Discovery.** `build-registry.py` finds every skill on disk and in the
   marketplace catalogs. Nine UI skills appeared on the machine mid-build and
   were indexed and tagged on the next rebuild without anyone wiring them up.

2. **Scoring.** `record-outcome.py` writes your accept/reject to the ledger.
   The score feeds ranking directly, so a skill you reject stops being
   selected however well its description matches.

3. **Gap detection.** A capability nothing covers is reported rather than
   answered with the nearest available skill, and the orchestrator writes a
   skill for it mid-build and proposes it for permanent life.

### Proposed, then approved

4. **The taxonomy.** Until now, `registry/capabilities.json` was only ever
   improved by hand, which meant routing could quietly rot. `taxonomy-audit.py`
   closes that loop:

   ```bash
   cd ~/.agents/skills/aswath-capability
   python scripts/taxonomy-audit.py
   ```

   It reports, with concrete suggestions:

   | Section | What it finds | What to do |
   |---|---|---|
   | `UNROUTABLE` | Skills nothing can reach, with the capability their own reference files point at | Add the capability, or add a `strong` keyword |
   | `STALE TAGS` | A tag the evidence does not support | Confirm, then drop it |
   | `REJECTED BUT ROUTED` | Skills you keep rejecting that routing keeps selecting | Narrow the capability or rewrite the description |
   | `STARVED CAPABILITIES` | Capabilities with no local provider | Author a skill, or stage an install |
   | `OVER-BROAD` | A capability held by many skills on a weak signal alone | Tighten the keyword rule |

   It is read-only. It proposes; it never edits the taxonomy. You apply the
   edits, then `python scripts/build-registry.py`.

The first run of this audit found 79 unroutable skills, 18 stale tags, and 4
starved capabilities. It also found a capability named `design-direction-types`
that I had created by accident and never used.

## Running the tests

There is no test suite yet. The roast loop is the test:

```bash
cd C:\Users\ADMIN\aswath-test
# bad-page/index.html is a deliberately broken landing page
python ~/.agents/skills/aswath-capability/workflows/roast-and-fix.py \
    --target ./bad-page/index.html --max-rounds 1 --max-findings 3 \
    --verify-lenses 2 --workers 6 --timeout 300 --report ./roast-report.json
```

A run should report findings, kill some of them in verification, apply the
survivors, and then re-verify each one individually. If it says "clean" while
a confirmed finding is unfixed, something has regressed.

## Conventions

- **Never edit an atomic skill in place.** The orchestrator composes them; it
  does not rewrite them. If you want to improve one, that is a fork and a
  proposal.
- **The registry is generated.** Edit `capabilities.json`, never `skills.json`.
- **Every fix needs a test.** A defect found by reading the code is a
  hypothesis. The nine defects in `docs/bugs-found.md` were all found by
  running the thing.
- **Failure modes that look like success are the ones that matter.** An empty
  response, a zero exit code, or a "clean" verdict are all worth distrusting
  until proven against the source.
