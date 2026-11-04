# Delegation

Work that needs a loop is handed to an external agent runtime. The seam is one
script, `scripts/delegate.py`, and the backends are declared in
`registry/backends.json`.

```bash
python scripts/delegate.py --backends                       # what is configured
python scripts/delegate.py --backend agy --prompt "..."     # one call
python scripts/delegate.py --backend agy --model fast --prompt "..."
```

## The envelope

Every call returns the same shape, whatever the backend:

```json
{
  "ok": true,
  "text": "the agent's final message",
  "parsed": { "...": "schema-enforced object when the backend supports it" },
  "usage": { "input": 0, "output": 0, "cache_read": 0 },
  "duration_s": 42.1,
  "session_id": "...",
  "error": null
}
```

`usage` is where delegated cost comes from, and it is what the efficiency
report is built on.

## Backends

### `agy` — structured roles and constrained edits

`--json-schema` is enforced at the tool layer, so the output shape is
*guaranteed* rather than requested. That matters more than it sounds: the
alternative is asking an agent in prose to return JSON and hoping, and agents
with their own skills routinely ignore that request in favour of their own
output format.

It also applies a constrained fix brief exactly. Measured: briefed with one
finding naming four selectors, it changed those four and nothing else.

### `cmdc` — exploratory work

Ships a strong editing skill set, and `cmd taste learn` gives it a taste
memory, which is a second learning substrate next to the ledger.

But it does **not** reliably follow a constrained brief. Measured: briefed with
two confirmed findings, it ran its own audit and applied different fixes
(button styling, a responsive grid) than the two it was given.

That is why the editing role defaults to `agy`. cmdc stays available as an
explicit override for exploration.

## Roles

| Role | Backend | Model |
|---|---|---|
| Critic | `agy` | strong |
| Verifier | `agy` | fast |
| Fixer | `agy` | strong |
| Re-verifier | `agy` | fast |

Assigned by `role_backends` in `backends.json`. Override per run with
`--backend`, `--structured-backend`, `--editing-backend`.

## Model tiers

Criticism and fixing need taste and depth. Verification is a narrow text
judgement and does not.

| Tier | Model | Cost of one call |
|---|---|---|
| `strong` | gemini-4-argon-high | ~36s |
| `fast` | gemini-3.8-flash-low | ~12s |

Splitting them is what makes a 20-call loop affordable. Note the caveat:
delegated calls carry their own agent's system prompt (~24k tokens), which is
paid *per call* and does not benefit from your session's prompt cache.

## Three failure modes that look like success

This is the part worth reading.

### 1. Headless permission denial

`agy` auto-denies tool calls in headless mode unless
`--dangerously-skip-permissions` is passed. A critic that cannot read the
file returns an **empty response**, not an error. Read-only roles use
`--mode plan`, which keeps the agent from editing despite the bypass.

The delegate treats an empty-plus-denied result as a **failure**, not a result.

`cmdc` has the same class of problem: it refuses file writes in print mode
unless `--yolo` is passed, and `--permission-mode accept-edits` alone is **not**
enough. It reports the refusal in prose while exiting 0, so it looks like a
successful run that did nothing.

### 2. Competing output formats

`cmdc` ships its own skills and will follow *their* output format instead of
the JSON instruction. This is why schema-enforced output is preferred over
parsed prose everywhere it is available.

### 3. The prompt flag that swallows the next argument

`agy --print` must have its prompt **attached**:

```
agy --print="do the thing" --output-format json
```

A detached `--print` makes agy treat `--output-format` as the prompt. Every
structured call then silently produces nothing. `cmdc -p` takes the prompt as
the following argument. Each backend declares its own `prompt_style`.

## The diff is the ground truth

An agent that applied fixes will say it applied fixes. Sometimes it did not.
Sometimes it applied *different* ones.

So after a fix, the loop computes the actual diff and uses that, not the
agent's self-report. And after that, each confirmed finding is re-verified
individually against the source, with the reviewer required to quote the line
that proves its verdict.

That last step replaced a weaker question. An earlier version asked a reviewer
"is this clean?" and it answered yes while a confirmed critical finding was
still unfixed.

## Scope guard

A fixer that rewrites the page instead of fixing it is detected:

- a changed-line budget scaled to the number of findings
- newly invented proper nouns in the **visible text** (markup and class names
  are ignored, because renaming a class is not inventing a brand)
- terms the findings themselves asked for are not counted as invented

The guard also reports deviation: changes the fixer made that no finding
requested.

## Cost

Delegated work is not free and it is not as cheap as in-process subagents.
Each `agy` call carries its own ~24k-token system prompt. A 20-call loop is
roughly 700k input tokens.

This is why `--max-findings` caps **before** verification rather than after.
Capping afterwards means verifying 21 findings and then discarding 18.
