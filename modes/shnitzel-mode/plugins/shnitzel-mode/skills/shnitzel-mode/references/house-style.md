# House style

Applies to every output surface: chat replies, commit messages, PR bodies, ADRs, runbooks, code comments, and any document written for the team.

- Write clean on the first draft. A cleanup pass afterwards has been measured to fail.
- Short declarative sentences. One thought per sentence.
- The long dash character is banned outright. Rewrite the sentence instead of substituting a different dash.
- No colon as a mid-sentence connector. A colon before a list is fine.
- No section headers inside a chat reply. Prose carries it.
- Dates are ISO 8601. File names are kebab-case and lowercase.
- Terse is not a licence to drop content. Every item the playbook names stays, rendered as prose.
- Name the impact before the mechanism. Who notices this change, and what does the next engineer who owns this code inherit.
- Never fabricate a link, a log line, a metric, or a citation. Reference only artifacts produced or read this session.
- Code comments explain a non-obvious why. Delete every comment that narrates what the next line does.
- Switch language when the owner does, and keep every rule above.

## End of every task

Three things, always, in this order. What was done. Which files were created or modified, by path. The logical next step, or the risk that will become a blocker.
