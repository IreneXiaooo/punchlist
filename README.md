# punchlist

**Budget-aware collaboration between large and small coding models.**

[中文说明](README.zh-CN.md) · [Roadmap](docs/roadmap.md) · [Budget design](docs/budget-model.md) · [Contributing](CONTRIBUTING.md)

> **Status: project bootstrap, protocol draft 0.2.** This repository contains schemas, a design configuration, an example plan, and a protocol validator. There is no task runner, provider adapter, subscription integration, or published package yet. Savings and task-quality improvements have not been demonstrated.

## The goal

Let a user set a task budget—for example, five percentage points of a subscription usage window—and decide when a small model should execute, when an instruction should be rewritten, and when a stronger model is worth its cost.

The research objective is to improve task completion under a measured budget. A quota target is not a hard cap unless the provider exposes sufficiently reliable accounting and enforceable per-call bounds. When the budget is insufficient, the system should stop with useful partial work and a clear receipt.

## What is here today

| Component | Status |
| --- | --- |
| Plan, state, and worker report schemas | Draft 0.2; runtime-accounting gaps documented |
| Example task and configuration | Design examples; commands are not executed by validation |
| Protocol validation and CI configuration | Available in this repository |
| Runner, model adapters, quota observation, recovery | Planned for the first runnable milestone |
| Benchmark results | None; experiment protocol is specified |

## Validate the design

Requires Python 3.11 or newer. From a checkout:

```bash
python -m venv .venv
# Activate .venv using your shell's activation command.
python -m pip install -r requirements-dev.txt
python scripts/check_protocol.py
```

Validation checks schema validity, local references, the example plan, dependency cycles, budget consistency, and review-lane semantics. It does not run an agent or execute commands embedded in a plan.

Do not install a similarly named package expecting this project: no package has been released.

## Planned execution model

1. Observe the relevant account quota pools and load the user's constraints.
2. Reserve budget before every model call, including planning, rewriting, and review.
3. Run a bounded attempt using the configured model tier.
4. Inspect changes against recorded Git baselines and run task-specific checks.
5. Settle known costs; retain unresolved spending as unknown after interruptions.
6. Retry, rewrite, upgrade, or stop according to the selected policy and remaining budget.

Passing checks produces `verified`. A separate human or configured review decision produces `accepted`; neither is a proof of universal correctness. Generic tests and lint alone cannot establish that a new request was fulfilled.

The initial integration target is one supported subscription-backed coding tool plus one cheaper API or local worker, with serial execution. Reusing both ChatGPT/Codex and Claude subscriptions is a later adapter goal, not an existing capability. Authentication and integration support must be verified against each tool before implementation; credentials must not be copied between harnesses.

## First milestone

Build the budget loop before parallel execution or learned routing:

- account/pool/window quota identities and fresh observations;
- reservation, settlement, and conservative crash recovery;
- serial runner with explicit Git baselines and goal-specific checks;
- one subscription adapter and one cheaper worker;
- receipts and a small baseline experiment that include all model calls.

The [backlog](docs/backlog.md) contains ready-to-use issue drafts and acceptance criteria. The [benchmark protocol](benchmark/README.md) defines the comparisons; a small pilot is for debugging the experiment, not establishing general superiority.

## Repository map

| Path | Purpose |
| --- | --- |
| `schema/` | Draft plan, state, and report contracts |
| `examples/` | Example coding task |
| `config.example.yaml` | Proposed runtime settings, not executable today |
| `scripts/check_protocol.py` | Design validation |
| `docs/` | Budget model, protocol decisions, roadmap, backlog |
| `benchmark/` | Evaluation protocol; no fabricated results |
| `templates/` | Task handoff template |

## License

[MIT](LICENSE). Project name is provisional; no package-name or trademark availability is claimed.
