# Budget model — requirements for the first runner

This is a design, not an implemented quota controller. Draft 0.2 schemas do not yet encode every requirement below; see [protocol migration notes](protocol.md).

## Units and identity

API spend is recorded in USD and tokens. Subscription usage is recorded as a fraction of a provider-defined quota window; never convert tokens into a measured quota fraction using an assumed allowance.

An example task target of `0.05` means five percentage points of the window's total allowance, not five percent of its remaining allowance. A `0.01` verification reserve is part of that `0.05`, not additional budget.

Identify each constraint by provider, local account alias, quota pool, window, and reset timestamp. Different models may share a pool. A lane may consume several windows at once; each constraint must admit a call. API rate-limit windows and subscription allowances are distinct resource types.

## Observations

Record source, observation time, window identity, raw value, confidence, and attribution quality. An observed account delta is not automatically a task's exact spend. Concurrent user activity or other tasks can contaminate attribution. Stale, missing, rounded, delayed, or reset-straddling observations must retain their uncertainty.

On a reset, keep the earlier epoch's spend. If the final pre-reset usage is unavailable, mark that interval unresolved; resetting a baseline does not reconstruct missing consumption. Do not silently grant the task another full task budget after a reset. Cumulative usage across epochs may exceed one window, so a single scalar constrained to 0–1 is insufficient for long-lived totals.

The first provider adapter must establish which observation mechanisms are actually supported. CLI usage, local logs, manual observations, and API headers are candidate sources with different meanings, not interchangeable implemented integrations.

## Calls and reservations

Every paid or quota-consuming action has a unique call ID and a role: plan, replan, rewrite, execute, continue, or review. Planning cannot bypass the gate because no step exists yet.

Proposed controller operations:

```text
reserve(call_id, role, pool_estimates) -> reservation | defer | downgrade | halt
mark_started(reservation_id)
settle(reservation_id, actual_usage, evidence)
reconcile(reservation_id, observations)
cancel_before_start(reservation_id)
```

Persist a reservation atomically before dispatch. Include existing reservations in the budget check. Only a call known not to have started may have its reservation cancelled automatically. A timed-out or crashed call remains unresolved until reconciled; retries receive new IDs and require new reservations. Local IDs alone do not guarantee provider-side exactly-once execution.

Unknown cost defaults to halt. Reserve funds for designated final verification/replan roles. An opt-in estimate-based mode must expose its confidence and possible overshoot. Without enforceable per-call bounds and reliable accounting, quota limits are control targets rather than hard guarantees.

## Receipt

Report task outcome, spend per pool/window/epoch, observations and uncertainty, outstanding reservations, unknown costs, total API spend, wall time, and budget overshoot. Include all call roles and retries. Keep `verified` and `accepted` separate. Do not present an unobserved cost as zero.
