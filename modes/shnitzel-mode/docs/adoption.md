# Using this over months, not days

Most of this kit does nothing on day one that you could not do by hand. The value is in the parts that compound, and the parts that compound only compound if three specific habits stick. This document is about which parts those are and in what order to adopt them.

## What compounds and what does not

Be clear-eyed about this, because it decides where to spend attention.

**Compounds.** The repo profiles, because every session that reads one skips a rediscovery. The lessons files, because a constraint written down once stops being relearned. The open-age metrics, because four weeks of them turn a guess about noise into a measurement. The feature ledgers, because the retro that compares the shipped metric to the PRD's claim is the only thing that improves an estimate.

**Does not compound.** The playbooks and the domain cards. They are as useful in month twelve as in week one and no more so. They are worth having, they simply do not get better.

**Actively decays if neglected.** The feature ledgers again, in the other direction. A ledger nobody updates makes `feature-track` report fiction, which is worse than reporting nothing, because a wrong status is acted on and a missing status is investigated.

## Adoption order

Do not turn everything on. The failure mode here is thirty skills and no habits.

**Day one.** Install, run `/setup-shnitzel-mode`, list your repos in `watch.conf`, and run `bin/digest.sh --pretty --all` once. Read the output against what you already know is true. If the severity ranking disagrees with your instincts, fix the config before anything else runs on a schedule. A harness whose priorities you disagree with is one you will learn to ignore in a fortnight.

**Week one, nothing scheduled.** Use `/watch` by hand each morning. This is deliberate. You are calibrating, and you cannot calibrate something that arrives while you are asleep. At the end of the week you will know which finding kinds you acted on and which you skimmed, and that is the input to the first tuning pass.

**Week two.** Turn on the interrupt watch and the morning brief. Leave the weekly hygiene pass off for now. Start using `learn` in the moment, not in retrospect: the correction you make on Tuesday is worth writing on Tuesday, because by Thursday you will remember the correction and not the reason, and the reason is the useful half.

**Weeks three and four.** Run `profile-repo` against the two or three repositories you touch most. Twenty minutes each, and every later session in them starts informed. Put one real feature through `feature-flow`, ideally one already in flight, backfilling the PRD and HLD from what is in your head. That tells you whether the gates match how your team actually decides, before four more features are committed to the format.

**Month two.** First `tune` pass, once there are four weeks of metrics. Before that the numbers are noise and tuning on noise is worse than not tuning. Turn on the weekly hygiene pass.

**Quarter one.** First real retro on a shipped feature. Compare what happened to what the PRD claimed. This is the single highest-value hour in the whole system and it is the one everybody skips.

## The three habits

Everything else is optional. These three are what turn the kit from a pile of markdown into something that pays.

**Write the gate.** One line in `04-progress.md` when a stage advances: the date, the decision, who made it. Ten seconds. Without it the ledger is a folder of documents and `feature-track` has nothing to report.

**Run `learn` in the moment.** When you correct the agent, or discover a constraint the hard way, write it before the context is gone. Pick the narrowest scope that fits. A wrong global rule is expensive and invisible.

**Let `tune` cut.** When it proposes dropping a finding kind you have ignored for a month, accept it. The instinct is to keep the check "just in case", and that instinct is exactly how the harness becomes noise. A check you ignore is not a safety net, it is a habit of ignoring.

## Absorbing new pstack releases

Use the explicit check/build/apply process in [upstream-sync.md](upstream-sync.md). Never update an unrelated marketplace behind the active pinned distribution. The lock records both source revisions, and failed compatibility checks leave the working engine unchanged. Live acceptance is separate from building the engine.

## What to stop doing

Asking the agent to check CI. That is what the watch harness is for, and asking by hand means the dedupe state never learns.

For substantial features, preserve accepted plans in their feature directory. Simple changes need no feature ledger.

Keeping a finding kind you never act on because it feels responsible. It is not responsible, it is noise with good intentions.

Letting a feature sit green because nobody updated it. Silence is amber.

Adding a skill because a task felt awkward once. Add it when it has been awkward three times, and then delete something.
