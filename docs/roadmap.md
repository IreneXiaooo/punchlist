# Roadmap

Protocol draft numbers and implementation releases are separate. Protocol 0.2 does not mean a 0.2 runner exists.

## Bootstrap — available

- Organized draft schemas and example plan.
- English and Chinese project introductions, MIT license, contribution guide.
- Local protocol validator and GitHub Actions workflow configuration.
- Budget requirements, experiment protocol, and implementation backlog.

## M1 — first runnable budget loop

Serial execution only. Establish quota-pool identity, observation freshness, budget reservations, reconciliation, and an append-only event journal. Implement interrupted-call handling before real spending. Add explicit attempt and accepted-code baselines, task-specific acceptance, and a useful halt receipt.

Then connect one supported subscription coding tool and one cheaper API/local worker. Provider support and authentication must be checked at implementation time. Unknown spend stops execution by default. Every planner, rewrite, execution, continuation, and review call is budgeted.

Exit criteria: a real task either completes with auditable accounting or stops with preserved work; fault injection does not silently permit duplicate spending; staged edits, deletions, and new files are detected; unsupported quota sources are refused.

## M2 — pilot evidence

Run 10–20 development tasks to debug the evaluation pipeline. Compare large-only, small-only, upgrade-first, rewrite-first, and failure-aware policies with all overhead counted. Keep held-out tasks separate. Publish failures, uncertainty, and budget overshoots alongside successes.

## M3 — expansion justified by evidence

Additional subscription adapters, a middle tier, and stronger review. Parallel execution requires shared-pool atomic reservations and isolated worktrees. Learned routing requires sufficient training data and a separate held-out evaluation.

## Research release

Freeze task selection and policies before held-out experiments. Release reproducible configurations, redacted receipts, analysis code, and limitations. An arXiv submission is a goal, not evidence of novelty or peer review.
