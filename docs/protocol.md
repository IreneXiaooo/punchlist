# Protocol 0.2 and migration requirements

The three schemas and example plan are retained from the reviewed design. They are drafts, not a complete runtime accounting contract. The validator checks structural consistency; it does not certify that a task is correct, safe to execute, or affordable.

## Contracts

- [Plan](../schema/plan.schema.json): goal, dependencies, scope, checks, lanes, escalation, budget requests.
- [State](../schema/state.schema.json): proposed runtime summary and attempt history.
- [Report](../schema/report.schema.json): a worker's output and usage evidence.
- [Example](../examples/plan.example.json): illustrative task; the target application is not included.

## Required changes before runtime use

1. Introduce account/pool/window/epoch identities and per-constraint costs instead of treating lane totals as sufficient quota accounting.
2. Define and version an event-journal schema with unique IDs, call roles, reservations, starts, completion/interruption, and reconciliation.
3. Record immutable attempt-start and accepted-code baselines separately. Link journal events, reports, and commits explicitly.
4. Require acceptance provenance for accepted results and retain uncertainty for independent model reviews.
5. Provide per-lane estimates for escalations, rather than assuming the first lane's estimate applies to every model.

These changes require a new draft version and updated examples. Existing per-lane 0.2 fields are insufficient for claiming that a quota cap was enforced.

## Git change inspection

Plain `git diff` compares the worktree with the index and can miss staged modifications or deletions. In an isolated task worktree, include eligible untracked paths and compare against an explicit immutable attempt-start commit, not whichever HEAD is current after an attempt was committed. A candidate command sequence to implement and test is:

```bash
git add -A -N
git diff "$attempt_base" --numstat -M -z --
git diff "$attempt_base" --raw --no-abbrev -M -z --
```

This sequence is not a sandbox or a complete filesystem inventory: ignored files, binary changes, submodules, modes, symlinks, and rename endpoints need explicit policies. Reject writes outside mounted paths at the sandbox boundary. A second comparison against the accepted-code baseline evaluates the accumulated result. Worker changes and runner-owned acceptance files need separate ownership and accounting.

## Recovery

Journal the reservation and start before dispatch; append completion and usage afterward. State is a derived view only to the extent the journal contains the necessary events. A crash after remote execution but before local recording leaves an unresolved call, not a free retry. A crash between Git and journal writes requires reconciliation, not a claim of an atomic cross-system commit.

## Acceptance

Task-specific checks are required for goal-related evidence. Generic tests and lint may establish regression checks but cannot establish that a new request is fulfilled. Fast path is disabled in the example configuration until that distinction is implemented. Human acceptance or configured independent review is recorded separately from check success.
