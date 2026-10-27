# Generic playbook

Fallback when pstack is not installed and no specific playbook matches.

1. State the goal in one sentence and the observable that proves it is done.
2. Read before writing. Map the files that own the behavior and name them.
3. Name the data shape and the boundary the change crosses.
4. Write the smallest change. Delete first where deletion is available.
5. Verify against the real artifact. Capture the actual output.
6. Preserve recoverability. Use existing version control and preserve unrelated work; commit only within the task's requested delivery scope.
7. Reply per `references/house-style.md`, ending with the three closing items.
