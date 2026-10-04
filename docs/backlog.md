# Initial issue drafts

These are local drafts, not issues already created on GitHub. Implement in the order below.

## 1. Version quota and event contracts

Priority: P0. Deliver a new protocol draft for provider/account/pool/window/epoch identity, call roles, observations, and event IDs. Update examples and migration notes.

Acceptance: one lane can affect two windows; two lanes can share a pool; reset-straddling unknown usage remains unknown; every model role can be recorded before a step exists.

## 2. Implement reservation and recovery core

Priority: P0. Build a provider-independent serial controller using persisted reserve/start/settle/reconcile events. Use a fake provider first.

Acceptance: duplicate settlement is idempotent; outstanding reservations consume available budget; interrupted calls do not receive a free retry; fault injection at each event boundary preserves conservative accounting; reserves remain within the total cap.

## 3. Implement change inspection and acceptance

Priority: P0. Use isolated worktrees and separate attempt/accepted baselines. Distinguish worker edits from verifier-owned files.

Acceptance: detect new files, staged edits, deletions, renames and mode changes; define binary and ignored-file policy; a no-op worker cannot satisfy an unmet goal solely through pre-existing passing tests; failed attempts do not become accepted baselines.

## 4. Deliver the first serial end-to-end task

Priority: P0. Connect one supported subscription coding tool and one cheaper API/local worker after verifying supported invocation and accounting interfaces. Integrate all call roles with the controller.

Acceptance: no credentials copied between harnesses; unknown or stale quota blocks spending by default; all attempts produce receipts; insufficient budget stops with preserved progress; no claim of an enforced hard cap without a reliable per-call upper bound.

## 5. Run the baseline pilot

Priority: P1. Follow the [benchmark protocol](../benchmark/README.md). Start with large-only, small-only, upgrade-first, and rewrite-first; add failure-aware routing after the accounting and classifier are stable.

Acceptance: identical tasks and independent checks, all overhead included, pinned model/configuration identifiers, randomized run order where practical, raw redacted receipts, success/cost/time/overshoot metrics, and a documented held-out split.
