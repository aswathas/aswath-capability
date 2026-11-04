# Published LinkedIn post

Published 2026-11-04 as `urn:li:share:7523859182161276928`.

<https://www.linkedin.com/feed/update/urn:li:share:7523859182161276928/>

## The post

```
3,114 agent skills. I needed a way to pick the right one for a request, so I built the thing that picks it.

Then I gave it a harder job. When nothing covers what you need, it writes the missing skill, uses it, and asks before making it permanent.

That turned out to be the easy part.

The routing is where I got it wrong twice.

First version tagged a landing page design skill as "ecommerce" because its description mentioned "product page". It designs pages. It does not build a cart. So tagging reads the files a skill ships now: if it ships reference/critique.md, it critiques.

Second, I asked the reviewer "does this page look right?" and it said yes. The page still had body text at 2.8:1 contrast against a 4.5:1 minimum. It answered about the page instead of about the defect I handed it. Now every confirmed finding gets its own verdict, with the source line that proves it.

9 bugs in the build. 3 of them were tools failing silently, in a way that looked exactly like success.

Full write-up and the code are in the comments.

What are you shipping this week?

#buildinpublic
```

## First comment

The body carries no outbound link. The repo link goes in the first comment,
which LinkedIn treats as a separate content surface and which does not cost
the post its reach.

```
Full write-up and the code: https://github.com/aswathas/aswath-capability

3,114 agent skills indexed, 52 capabilities, 111 duplicate entries suppressed, 9 bugs found by testing it. docs/bugs-found.md has each one with symptom, cause and how it was caught.
```

## Notes on the shape

| Choice | Why |
|---|---|
| F7, odd-precision ledger | Strongest 2026 opener. An odd number in line 1 is the single largest positive first-line signal, +34% median likes. |
| Number-first, not a question | A question as line 1 is -34% median likes. The question moves to the close, where it is +3%. |
| No link in the body | Outbound links in the body cost reach. The link belongs in the first comment. |
| 1,089 chars, 23 sentences | 1,000+ characters is 1.18x and 20+ sentences is 1.14x on reach. |
| Two failures, both concrete | The stake has to be real. A contrast ratio and a mis-tagged skill beat any claim about capability. |
| "3 of them were tools failing silently" | Precise, and it is the part a working engineer will recognise. |
