# Budgets

Adaptive effort is the default, with no invented fixed token cap. An explicit user limit is strict. Count all participating calls, including planner, delegates, repeated input and verification. Cached tokens are part of input, not another total to add. Reasoning tokens are included in output where the provider reports them that way. Missing accounting is unknown.

`bin/budget.py preflight --runtime <name> --mode <mode> --max-tokens N` (or `--max-cost-usd N`) checks the versioned capability registry. Native flags and Goal continuation budgets are candidates, not verified exact enforcement. The shipped registry deliberately denies unverified hard caps. The user can choose uncapped adaptive execution or a separately verified request-controlled runner; never silently switch.

For a host that can intercept every request, `BudgetLedger` in `lib/budget.py` provides atomic shared reservations. Count complete input and reserve maximum output before dispatch; settle against measured usage afterward. Unknown pricing, incomplete responses, interruptions, retries without a reservation, or uncertain charges block further requests. Retain the reservation until the charge is known. Dollar limits cover the declared cost scope only; model-token costs must not be advertised as a full bill cap including tools.

Run ledgers live outside the repo under the Shnitzel state directory. `bin/budget.py record` accepts normalized runtime usage with its provenance; `summary` keeps measured and estimated records separate. No telemetry means no numeric saving claim. Local inference may consume tokens and time even when there is no API bill. Do not write prompts, code, credentials or model reasoning into usage ledgers.
