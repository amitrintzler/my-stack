---
name: handoff
description: Write a decision trail so another engineer, another runtime, or a future session can pick the work up. Use for handoff, pause safely, going to bed, take this over, resume this later.
---

# Handoff

You work across Claude Code, Codex, Gemini, Cowork, and local models. Work started in one runtime is routinely finished in another. The handoff file is the only thing that survives the switch.

## When

Any task spanning more than one session, any task the owner steps away from, any context that is about to compact, and any work another engineer will take over.

## Steps

1. Write `HANDOFF-YYYY-MM-DD-HHmm.md` in the working tree, next to the work.
2. Contents, in this order. The goal in one sentence. What is done, with file paths. What is in flight and the exact next command. Every decision made and why, because the reasoning is the part that does not survive. Everything deliberately not done. The verification that has and has not been run.
3. Name the runtime and model roles used, so the next session can match or deliberately differ.
4. Commit it on the working branch. It is part of the work, not a note about the work.
5. Never leave the tree in a state that only makes sense with the session transcript.

## Reply

Path to the handoff file, the single next command, and the one open question if there is one.
