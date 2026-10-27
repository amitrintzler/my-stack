# LinkedIn package

Article URL: https://claude.ai/code/artifact/51a300ca-5124-4ea3-a223-6da324c81648

Before posting, open the artifact and use its share menu. It is private until you do,
and an unshared link shows visitors nothing.

---

## Option A: the main post (2,766 characters, inside the 3,000 limit)

I built a watchdog for my own engineering work. Then I audited it and found it had been telling me to merge a build that was failing.

Here is how that happened.

GitHub returns two different node types in the same array when you ask for a pull request's checks. A modern CheckRun carries a "conclusion" field. A legacy StatusContext, which is what you get when Jenkins or an older CI posts commit statuses, carries "state" and no conclusion at all.

My filter read only "conclusion".

So in any repository whose CI posts statuses rather than checks, every failing run was invisible. Then it got worse. With zero failures seen and an approving review, that same pull request matched the next rule down and came back as "approved and green, waiting only on your merge".

Not a missed alert. A confident wrong recommendation on a red build.

Two more defects came out of the same review. A ledger date written as a timestamp instead of a bare date reported a permanent stall of 9999 days. A hash function that does not exist on macOS returned an empty string rather than an error, which silently suppressed an entire category of findings after their first report.

All three failed the same way. They produced plausible output instead of an error. A missing field became zero failures. An unparseable date became a very old date. A missing binary became an empty hash.

The rule I am taking forward: absence of data must never be representable as a value. If a probe cannot answer, it has to say so, and the report has to distinguish "nothing is wrong" from "I could not look".

The rest of what came out of building this is mostly not about the tool.

1. Separate gathering from judgment. Most of what we ask agents to do daily is not judgment, it is querying. Put that in shell scripts that emit JSON and let the model read the output. Costs nothing, reproducible, and structurally unable to write back.

2. Name roles, not vendors. No instruction file should contain a model name. One indirection file, and your work survives every deprecation and every runtime switch.

3. Write your stop list in terms of effects, not commands. I wrote mine as "no git push", then realised a connected MCP server opens a pull request without ever touching a shell. Scope the token instead of trusting the prose.

4. Give knowledge exactly one home. Once an agent writes things down and reads them back, a constraint from one project turns up as an assumption on the next, phrased as knowledge so nobody questions it.

5. Measure what you ignore. Not whether people find the reports useful, which produces polite answers. How many days each finding sat there unactioned.

Full write-up with the diagrams, link in the first comment.

#DevOps #PlatformEngineering #AIEngineering #SRE

---

## First comment (post this immediately after)

Full article, including the three defects in detail and the design decisions behind the tool:
https://claude.ai/code/artifact/51a300ca-5124-4ea3-a223-6da324c81648

Built as an overlay on pstack (poteto mode) by Lauren Tan, MIT. Nothing copied from it, referenced by name only.

---

## Option B: the short post (676 characters)

I built a watchdog for my own engineering work, then audited it and found it had been telling me to merge a failing build.

GitHub returns two node types in one array. CheckRun has a "conclusion" field. Legacy StatusContext has "state" and no conclusion. My filter read only "conclusion", so every failing legacy status was invisible, and the pull request then matched the "approved and green" rule.

Not a missed alert. A confident wrong recommendation on a red build.

Two more defects, same shape: all three produced plausible output instead of an error.

Absence of data must never be representable as a value.

Full write-up in the comments.

#DevOps #PlatformEngineering

---

## Images

Attach in this order. LinkedIn shows the first as the preview, so lead with the defect.

| Order | File | Why this one |
| --- | --- | --- |
| 1 | 04-what-broke.png | The hook. Anyone who has run Jenkins will recognise it immediately. |
| 2 | 03-deterministic-half.png | The most reusable idea in the piece. |
| 3 | 01-four-layers.png | The mental model, for people who want the framing. |
| 4 | 05-knowledge-scope.png | The contamination problem, which surprises people. |
| 5 | 02-overlay-not-fork.png | The narrowest, so last. |

All are 1200x1200 at 2x, which is LinkedIn's square format.

Uploading two to five images makes LinkedIn render a carousel-style grid.
If you would rather have a single strong image, post only 04-what-broke.png.

## Posting notes

Put the link in the first comment rather than the post body. LinkedIn suppresses
reach on posts with outbound links, and a first comment does not carry that penalty.

The first two lines are all that shows before "see more", so they carry the whole
decision to expand. Both options above are built around that.

Best days for this audience are Tuesday to Thursday, roughly 08:00 to 10:00 in the
timezone where most of your network works. For a team split across Israel, India and
the USA, 09:00 Jerusalem catches India's afternoon and Europe's morning, and misses
the US entirely, so consider whether the US half matters more than the volume.

Expect the reply guy who says the API is documented. He is right. That is the point:
it was documented, I read it, and I still handled one of the two shapes. Say that
rather than defending the bug.
