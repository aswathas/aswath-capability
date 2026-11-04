# The registry

The registry is what makes routing possible. It is generated, never hand-edited.

## What is in it

| Source | Count | Notes |
|---|---|---|
| `~/.agents/skills/*/SKILL.md` | 253 | Local skills |
| `~/.claude/plugins/**/skills/*/SKILL.md` | 30 | Installed plugin skills, minus local duplicates |
| `~/.claude/plugins/plugin-catalog-cache.json` | 2,831 | Marketplace skills, with token cost and install counts |
| `~/.claude/plugins/plugin-directory-cache-v2.json` | 3,605 | Installable plugins, with repo and review state |

3,114 unique skills. 111 duplicate entries suppressed.

```bash
python scripts/build-registry.py
```

## Deduplication

The same skill shows up in more than one place. `frontend-design` was listed
three times: as a local skill, as an installed plugin skill, and in the
marketplace catalog. Left alone, "cheapest wins" ranking would have had three
entries for one skill and might have picked the marketplace copy.

Precedence is **local > plugin > marketplace**. A marketplace copy of a skill
you already have is not a second option, it is the same skill.

## Capability tagging

Three evidence channels, strongest first.

### 1. `files` — the reference files a skill ships

The strongest signal, because it is proof rather than a claim. A skill shipping
`reference/critique.md` critiques; one shipping `reference/cart.md` handles
carts. Matching is on **exact filename stems**, never substrings.

Substring matching was tried first and was a disaster: `type` matched every
TypeScript file, `SKILL.md` matched every skill, and `review` put 82 skills
into `design-critique`. Only 1 of 244 local skills was left untagged. With
exact stems and a generic-stem blacklist (`skill`, `readme`, `license`,
`index`, `package`, `changelog`) the same taxonomy produces the right answer.

### 2. `strong` — a keyword anywhere in the description

### 3. `weak` — a keyword in the skill's **name** only

`weak` exists because of one specific failure. `design-taste-frontend` was
tagged "ecommerce" because its description mentions "product page" — but it
designs landing pages, it does not implement a cart. Under `weak`, a skill
named `shopify-cart` provides ecommerce and a design skill that mentions a
product page does not.

## Exclusions

Some skills describe **trigger phrases** rather than capabilities. The
orchestrator's own description contains *"build me an ecommerce site"*, so
without an explicit exclusion it competed with the skills it dispatches.

`_exclude` in `registry/capabilities.json` handles this.

## Cost as a ranking signal

Every skill carries `tokens_est`, and marketplace skills carry the real
`on_invoke` cost from the catalog. The cheapest skill that **fully** covers the
need wins.

This is not a micro-optimisation. Loading `design-taste-frontend` (9,884
tokens) to do a job `principle-redesign-from-first-principles` (190 tokens)
does perfectly is a routing failure, because the context is gone for the rest
of the session.

Marketplace skills also carry `installs`, which is a popularity signal for
*"what is the current best at this"*.

## Using it

```bash
# what covers this need?
python scripts/query-registry.py need "roast my landing page and fix it"

# what covers this capability?
python scripts/query-registry.py cap design-critique --limit 8

# what does NOTHING cover? This is the important one.
python scripts/query-registry.py gap "build an ecommerce site with cart and checkout"

# what could I install for a gap?
python scripts/query-registry.py install "stripe checkout"

# one skill, full detail
python scripts/query-registry.py show impeccable

# coverage stats
python scripts/query-registry.py stats
```

Ranking order is: quality score from the ledger, then local-over-marketplace,
then popularity, then cost.

## Keeping it sharp

When routing sends you to the wrong skill, fix the **taxonomy**, not the query.

```bash
$EDITOR registry/capabilities.json
python scripts/build-registry.py
```

`registry/skills.json` is generated and machine-specific, so it is
git-ignored. `registry/ledger.json` and `registry/staged.json` are personal
state and are git-ignored too. `capabilities.json` and `backends.json` are
config and are committed.

## Names and slugs

Plugin skills declare `name: Agent Cost Report` but are referenced everywhere as
`agent-cost-report`. Every entry carries a `slug`, and lookups resolve by
either form. Without that, a skillset referencing a plugin skill resolves to
nothing.
