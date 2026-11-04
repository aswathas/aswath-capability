3,114 agent skills. 111 of them were the same skill, listed three times.

Nobody can hold that list in their head, so I built an index of it. Here is every number, nothing rounded:

- local skills indexed: 253
- plugin skills: 30
- marketplace skills: 2,831
- installable plugins catalogued: 3,605
- capabilities in the taxonomy: 52
- duplicate entries suppressed: 111
- lines of Python: 2,182
- defects found by testing during the build: 9

What it replaces: reading every SKILL.md to work out which one to call.

Routing was the part that surprised me. A skill that mentions a capability is not a provider of it, so tagging reads the reference files a skill ships: if it ships reference/critique.md, it critiques. The cheapest skill that fully covers the need wins.

Then it needed to do more than route. When nothing covers what a task needs, it writes the missing skill, uses it, and asks before making it permanent.

The surprise was not the missing skills. It was a bug where the system reported "clean" on a page whose body text still sat at 2.8:1 contrast, against a 4.5:1 minimum. The reviewer had been asked whether the page looked right, so it answered about the page rather than about the defect it was told to fix.

Verification now returns one verdict per confirmed finding, with the line of source that proves it. The diff, not the agent's own report, is the ground truth for whether a fix landed.

I put it together as aswath-capability, an orchestrator skill for Claude Code that runs the whole thing: brief, feasibility, plan, build, roast, verify.

Engineers used to be the people who knew their tools. Now the list grows every week. The useful skill is the one that knows the list.

What are you shipping this week?

P.S. Full design, the registry spec, and all nine bugs with symptom and cause: https://github.com/aswathas/aswath-capability

#buildinpublic