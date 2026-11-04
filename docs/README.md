# Documentation

| Document | What it answers |
|---|---|
| [architecture.md](architecture.md) | The three layers, the eight phases, the three gates, the promotion contract, and why there is no model training. |
| [registry.md](registry.md) | How the index is built, how capability tagging works, how to sharpen it, how deduplication works. |
| [delegation.md](delegation.md) | The external agent backends, their contracts, model tiers, and the three failure modes that look like success. |
| [bugs-found.md](bugs-found.md) | The nine defects testing found, each with symptom, cause and how it was caught. |
| [build-log.md](build-log.md) | The build in order: what was decided, what broke, what changed, what was dropped. |
| [../skill/aswath-capability/docs/QUICKSTART.md](../skill/aswath-capability/docs/QUICKSTART.md) | The commands you will actually type. |
| [../skill/aswath-capability/docs/DESIGN.md](../skill/aswath-capability/docs/DESIGN.md) | The design doc the build followed, including the parts that were rejected. |

## Where things live

```
aswath-capability/
├── SKILL.md                  the orchestrator: 8 phases, 3 gates, the rules
├── registry/
│   ├── capabilities.json     the taxonomy (files / strong / weak evidence)
│   ├── backends.json         external agent runtimes and role assignment
│   ├── skills.json           generated index - git-ignored
│   ├── ledger.json           quality scores - git-ignored
│   └── staged.json           marketplace candidates awaiting approval - git-ignored
├── scripts/
│   ├── build-registry.py     rebuild the index
│   ├── query-registry.py     the resolution engine
│   ├── record-outcome.py     ledger writes and promotion proposals
│   ├── stage-install.py      stage a marketplace plugin for approval
│   ├── delegate.py           the delegation seam to external runtimes
│   └── install-agents.py     register the subagent briefs as agent types
├── skillsets/
│   └── ui-design.json        the flagship: 8 phases, gates, quality bar
├── agents/                   researcher, planner, critic briefs
├── workflows/
│   └── roast-and-fix.py      the delegated roast loop
└── reference/                authoring, promotion, quality bar
```
