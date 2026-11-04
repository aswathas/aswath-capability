# aswath-capability

An orchestrator skill that takes a one-line brief to shipped work.

Say *"build me an ecommerce site"*. It brainstorms the brief with you, researches
whether the idea will actually work, plans the UI and the architecture, then
resolves and invokes the right skills, subagents, hooks, MCP servers and plugins
for each step. When it hits a capability nothing covers, it writes the missing
skill, uses it immediately, and asks before making it permanent.

It is not a god-skill that does everything. It is the thing that works out what
everything should be, then assembles it.

## The problem

Every few weeks the agent-skill market gets bigger. The point of a skill system
is to route a request to the right capability, but once you have hundreds of
local skills plus thousands in the marketplace, nobody can hold that map in
their head. And a name-based router fails in a specific, annoying way: it
cannot tell the difference between a skill that **mentions** a capability and
one that **provides** it.

Both problems have the same shape, and the same answer: a registry.

## Numbers

| | |
|---|---|
| Skills indexed | 3,114 unique (253 local, 30 plugin, 2,831 marketplace) |
| Installable plugins catalogued | 3,605 |
| Duplicate entries suppressed | 111 |
| Capabilities in the taxonomy | 52 |
| Phases in a build | 8, with 3 approval gates |
| Lines of Python | 2,182 |
| Defects found by testing during the build | 9 |

## Three layers

| Layer | What it is | Who owns it |
|---|---|---|
| **Atomic skills** | Single-purpose markdown units. `hallmark` does one job. `impeccable` does one job. | Humans and marketplaces. Never edited in place. |
| **Skillsets** | Curated pipelines for a use case: which atomic skills fire in what order, with gates between them. | This project. A skillset is a plan with checks, not a doc. |
| **aswath-capability** | The composer. Resolves a goal into skillsets, finds gaps, authors what is missing, orchestrates the build. | Continuously. |

## How routing works

A skill is tagged with the capabilities it actually **provides**, using three
evidence channels, strongest first:

1. **`files`** — the reference files a skill ships. A skill shipping
   `reference/critique.md` critiques. This is proof, not a claim.
2. **`strong`** — a keyword anywhere in the description.
3. **`weak`** — a keyword in the skill's **name** only.

The three-channel rule exists because of a specific failure. `design-taste-frontend`
was tagged "ecommerce" because its description mentioned "product page" — but it
is a landing-page design skill, not a cart implementation. Under `weak`,
`shopify-cart` is a provider of ecommerce and a design skill that mentions a
product page is not.

The same logic applies to the orchestrator itself. Its description contains the
trigger phrase *"build me an ecommerce site"*, so without an explicit exclusion
it competed with the very skills it dispatches.

Cost is a ranking signal, not an afterthought. The registry carries each skill's
token cost on invoke, and the cheapest skill that fully covers the need wins.
Loading a 9,884-token skill to do a 190-token job is a routing failure.

## Gap detection

When the registry cannot cover a capability the work depends on, that is
reported as a gap rather than papered over:

```
== gap analysis: build an ecommerce site with cart, checkout and payments ==
   inferred capabilities: ecommerce, payments

  [GAP]  ecommerce              no local skill covers this
  [GAP]  payments               no local skill covers this

   -> author a skill, or stage a marketplace install:
      Paymob Integration  v3.4.0  [e-commerce,payment gateway,shopify]
      wake-storefront      v1.0.0  [checkout flow,storefront]
```

A gap is resolved in this order: a local skill covers it under another name
(search harder first), the marketplace has it (stage it, and wait for your
approval), or nothing does (author it in-session, use it, then propose it).

## The eight phases

```
Intake → Brainstorm (gate 1) → Feasibility → Resolve → Plan (gate 2)
       → Build → Roast & Fix → Verify & Report → Promote (gate 3)
```

Three gates, no more: after the brainstorm, after the plan, and before anything
is written permanently.

**Roast & Fix** is the phase that decides whether the build is actually done.
Three critics run in parallel with different lenses (visual taste, correctness
and accessibility, would-a-user-want-this), every finding is judged by
independent lenses that try to **refute** it, the survivors are applied, and
then each confirmed finding is re-verified individually against the source.

That last step is the one that matters. An earlier version asked a reviewer
"is this clean?" and it answered yes while a confirmed critical finding was
still unfixed. Now a finding that was not addressed is reported as not fixed,
with the line of source that proves it.

## Delegation

Loops are handed to external agent CLIs, not orchestrated in-process. The seam
is one script and the backends are configurable.

| Backend | Role | Why |
|---|---|---|
| `agy` | structured output, constrained edits | `--json-schema` is enforced at the tool layer, so the shape is guaranteed rather than requested. It also applies a constrained fix brief exactly. |
| `cmdc` | exploratory work | Strong editing skills and a taste memory. But it does not reliably follow a constrained brief: measured, it ran its own audit and applied different fixes than the ones it was given. |

Both backends refuse to act in headless mode without an explicit permission
bypass, and both fail in ways that look like success. `agy` returns an empty
response when its tools are denied. `cmdc` refuses file writes in prose while
reporting success. The delegate treats an empty-plus-denied result as a
failure, and treats the **diff** as the ground truth for whether a fix landed,
not the agent's own report.

## Install

```bash
git clone https://github.com/aswathas/aswath-capability.git
cp -r aswath-capability/skill/aswath-capability ~/.agents/skills/

cd ~/.agents/skills/aswath-capability
python scripts/build-registry.py        # index local + marketplace skills
python scripts/install-agents.py        # register the researcher/planner/critic briefs
```

Requires Python 3.11+. `agy` and `cmdc` are optional: without them, everything
except the delegated roast loop still works.

## Documentation

| Document | What it answers |
|---|---|
| [docs/architecture.md](docs/architecture.md) | The three layers, the resolution model, the promotion contract. |
| [docs/registry.md](docs/registry.md) | How the index is built, how capability tagging works, how to sharpen it. |
| [docs/delegation.md](docs/delegation.md) | The backends, their contracts, and the failure modes they have. |
| [docs/bugs-found.md](docs/bugs-found.md) | The nine defects testing found, with symptom, cause and how each was caught. |
| [docs/build-log.md](docs/build-log.md) | The build in order: what was decided, what broke, what changed. |
| [skill/aswath-capability/docs/QUICKSTART.md](skill/aswath-capability/docs/QUICKSTART.md) | Commands you will actually type. |

## Related

`[capability-router](https://github.com/aswathas/capability-router)` is the
sibling project: it routes a single prompt to the right capability as a hook,
at zero permanent context cost. This project sits one level up, orchestrating
a whole build and filling gaps in the map.

## License

Apache 2.0. See [LICENSE](LICENSE).
