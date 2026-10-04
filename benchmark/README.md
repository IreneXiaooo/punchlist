# Evaluation protocol

No experiments have been run by this repository. No savings numbers are available.

Research question: under a shared task-budget policy, does choosing retry, instruction rewrite, or model upgrade from failure evidence improve successful completion compared with fixed policies?

## Comparisons

| Policy | Purpose |
| --- | --- |
| Large-only | Strong-model reference, including its actual overhead |
| Small-only | Lower-cost reference |
| Upgrade-first | Simple collaboration baseline |
| Rewrite-first | Test whether rewriting pays for its own cost |
| Failure-aware | Test whether failure classification improves decisions |

Use the same task starts, independent acceptance checks, resource ceilings, and accounting definitions across policies. Also report any unconstrained large-only reference separately; do not hide its different budget. A failure to finish within budget is an outcome, not a discarded sample.

## Pilot and held-out evaluation

Use 10–20 development tasks to debug instrumentation and policies. Keep evaluation tasks separate before tuning. Prefer verifiable bug fixes, bounded changes, and tasks with both easy and difficult cases. Human review should be blinded to policy where practical. Model-written tests alone are insufficient ground truth.

Record model identifiers, runtime versions, configuration, task commit, timestamps, prompt/protocol revisions, quota-pool observations and raw redacted receipts. Repeat runs where practical and randomize policy order to reduce quota-window and service-load confounding. Account-level usage affected by outside activity must be labelled; do not report it as exact task spend.

## Metrics

- Independently accepted completion rate and check-pass rate, separately.
- Subscription consumption per pool/window with attribution confidence.
- Total API USD and tokens, including planner, rewrite, retry, and review overhead.
- Wall-clock time, budget overshoot rate and magnitude, and useful partial outcomes.
- Missing/unknown cost frequency and recovery failures.

Publish per-task outcomes and uncertainty, not only averages over successes. Compare quality–resource tradeoffs; a cheaper unsuccessful policy does not establish efficient completion. Freeze routing policies before held-out evaluation. A pilot alone does not establish broad superiority.
