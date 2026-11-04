# Published LinkedIn post

Published 2026-11-04 as `urn:li:share:7523859182161276928`.

<https://www.linkedin.com/feed/update/urn:li:share:7523859182161276928/>

## The post

```
3,114 agent skills. I built the thing that picks the right one for a request.

It runs on Claude Code, and when nothing covers the job, it writes the missing skill itself. Then it asks before making it permanent.

3 of the 9 bugs I hit were tools failing silently, in a way that looked exactly like success.

P.S. https://github.com/aswathas/aswath-capability

What are you shipping this week?

#buildinpublic
```

## Earlier drafts

This post went live three times. The same URN was edited in place each time,
so the live post is the final version and the earlier ones are history.

| Version | Chars | Change |
|---|---|---|
| 1 | 1,898 | Numbers-led ledger with an 8-item bullet list, GitHub link in the P.S. |
| 2 | 1,089 | Simplified: one number, two concrete failures, link moved out of the body. |
| 3 | 409 | Short form. One number, one stake, the link back in the P.S. per the brand voice profile's link_rule. |

## Notes on the shape

| Choice | Why |
|---|---|
| F7, odd-precision opener | Strongest 2026 opener. An odd number in line 1 is the single largest positive first-line signal, +34% median likes. |
| Number-first, not a question | A question as line 1 is -34% median likes. The question moves to the close, where it is +3%. |
| Short band (300-500 chars) | The brand voice profile asks for a link on every post, and the skill bundle's short band keeps the body to one idea. The reach data favours 1,000+ chars (1.18x), so this is a deliberate trade against that. |
| Link in the P.S. | The voice profile's `link_rule` requires it. A P.S. sign-off is also +7.5% on its own. |
| One concrete stake | "3 of the 9 bugs were tools failing silently" is the kind of detail a working engineer recognises, and it is true. |
| No product name in the body | One mention maximum, and only where it is the natural conclusion. The link carries the name. |

## Notes on the platform

- The post was created with `cli-anything-linkedin post create`, then edited in
  place with `post edit`. LinkedIn keeps the same URN across edits, so the
  permalink is stable.
- Reading a post back is not possible. `r_member_social` does not grant it, so
  `post show` returns 403. The create/edit response and the CLI's local
  journal are the only record that will ever exist.
- The comments API is not enabled for the LinkedIn app behind that token. Every
  path under `/rest/comments` returns 404 `No virtual resource found`, so a
  first comment has to be added by hand.
