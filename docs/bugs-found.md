# Bugs found

Nine defects, all found by running the thing rather than reading it. Each entry
has the symptom, the cause, and how it was caught, because "the test passed"
is not a cause.

---

## 1. A design skill was tagged as a payment provider

**Symptom.** Querying `ecommerce` returned `design-taste-frontend`.

**Cause.** Capability tagging matched the keyword `product page` anywhere in
the description. `design-taste-frontend` designs landing pages; it does not
implement a cart. A skill that *mentions* a capability is not a provider of it.

**Fix.** Three evidence channels. `files` (the reference files a skill ships,
which is proof), `strong` (a keyword anywhere in the description), and `weak`
(a keyword in the skill's **name** only). Under `weak`, `shopify-cart` provides
ecommerce and a design skill that mentions a product page does not.

**Caught by.** Running `query-registry.py gap` on an ecommerce brief and
reading the output, which is where the wrong answer was obvious.

---

## 2. The orchestrator tagged itself as a capability provider

**Symptom.** `design-critique` resolved to `aswath-capability` alongside the
real design skills.

**Cause.** Its own description contains the trigger phrase *"build me an
ecommerce site"*. Routers describe triggers, not capabilities, and without an
exclusion the orchestrator competed with the skills it dispatches.

**Fix.** `_exclude` list in `registry/capabilities.json`.

---

## 3. Filename evidence matched 82 skills as design-critique

**Symptom.** 82 of 244 local skills tagged `design-critique`; only 1 untagged.

**Cause.** Filename matching used substrings. `type` matched every TypeScript
file, `SKILL.md` matched every skill's own file, and `review` matched every
code-review skill's directory.

**Fix.** Exact filename **stem** matching, plus a generic-stem blacklist
(`skill`, `readme`, `license`, `index`, `package`, `changelog`).

**Caught by.** The registry printed `local untagged: 72`, which is a different
number than it had been five minutes earlier and for no good reason.

---

## 4. `agy --print` swallowed the next argument

**Symptom.** Every structured delegated call returned nothing. No error, no
output, zero findings.

**Cause.** `agy --print` requires its prompt **attached**: `--print="text"`. A
detached `--print` makes agy treat the next argument as the prompt, so
`--output-format` became the prompt and `json` was nowhere to be seen.

**Fix.** A per-backend `prompt_style`: `attached` for `agy`, `next` for
`cmdc`.

**Caught by.** The delegate's `stderr_tail` carried agy's own explanation:
*"--print took --output-format as its prompt"*.

---

## 5. A denied tool looked like an empty result

**Symptom.** Critics returned zero findings with `ok: true`.

**Cause.** Two compounding bugs. `agy` auto-denies tool calls in headless mode
unless `--dangerously-skip-permissions` is passed, and a critic that cannot
read the file returns an **empty response**, not an error. Then the extractor
saw an empty `response` field and fell back to the raw CLI envelope, which
parsed cleanly into an object that looked like a result.

**Fix.** Pass the permission bypass (read-only roles use `--mode plan`, which
still prevents edits). Treat empty-plus-denied as a failure. Stop falling back
to the envelope.

**Caught by.** The failure looked exactly like "the page has no problems",
which is a dangerous kind of wrong.

---

## 6. The editing backend could not edit at all

**Symptom.** The fix phase reported success and changed nothing.

**Cause.** `cmdc` refuses file writes in print mode unless `--yolo` is passed.
`--permission-mode accept-edits` alone is not enough, and cmdc reports the
refusal **in prose** while exiting 0.

**Fix.** `--yolo` on the editing path. Verified with a probe that asked for one
property change and checked the file afterwards.

**Caught by.** A re-verifier that reported *"No fixes were applied; fix report
was empty and index.html remains unchanged with existing defects intact."*
The re-verifier was right and the fixer was lying by omission.

---

## 7. The fixer rewrote the page instead of fixing it

**Symptom.** Asked to fix a button's contrast, the fixer replaced the entire
page, inventing a product ("Shipwright, staged rollouts for platform teams"), a
nav, a skip link, and a new colour system.

**Cause.** The fix brief said "do not redesign" but did not forbid it, and
nothing measured the result.

**Fix.** Three things: hard anti-redesign constraints in the brief, an
automated scope guard (changed-line budget plus newly-invented-term detection
against the visible text), and a re-verifier that reports deviation explicitly
even when the result looks good.

---

## 8. The re-verifier said "clean" while a confirmed finding was unfixed

**Symptom.** A confirmed critical finding — body text at 2.8:1 against WCAG AA
— was reported as fixed. The `#999` was still `#999`.

**Cause.** The re-verifier was asked a general question: *"confirm the fixes
landed and look right."* It answered about the page as a whole. A page can look
right overall and still have the specific defect you were told to fix.

**Fix.** Per-finding verdicts. The reviewer receives the numbered confirmed
findings and must return a verdict for each, with evidence quoting the line
that proves it. "Clean" now means every confirmed finding was addressed.

**Caught by.** Reading the applied diff against the confirmed findings and
noticing the fixer had changed *different* things.

---

## 9. The same skill was listed three times

**Symptom.** `frontend-design` appeared as local, as plugin, and as
marketplace. "Cheapest wins" ranking had three entries for one skill and might
have picked the marketplace copy.

**Cause.** The registry indexed all three sources without reconciling them.

**Fix.** Deduplicate in precedence order: **local > plugin > marketplace**.
111 duplicates suppressed.

**Caught by.** Reading the output of a capability query and seeing the same
name twice.

---

## Also fixed along the way

- **Plugin skills were invisible.** The registry scanned only the local
  directory and the marketplace catalog, so a skillset referencing a
  claude-mem plugin skill resolved to nothing. Fixed by indexing
  `~/.claude/plugins/**/skills/*/SKILL.md` as a third source.
- **Names and slugs disagreed.** Plugin skills declare `name: Agent Cost
  Report` but are referenced as `agent-cost-report`. Every entry now carries a
  `slug` and lookups resolve by either form.
- **The findings cap was applied after verification.** It verified 21 findings
  and then discarded 18. Verification cost scales with finding count, so the
  cap now runs first.
- **Windows consoles are cp1252.** Agent output routinely contains arrows and
  em dashes that would crash a `print()`. Stdout is reconfigured to UTF-8.
