# Trait: Script First Automation

## Trait ID
trait-script-first-automation-001

## Purpose
Enforce the "Only Write Once" policy so agents prefer deterministic, reusable scripts over repeated ad-hoc manual execution.

## Applies To
- agent
- specialism
- task

## Behavior
- MUST classify task intent and check for an existing script/workflow before execution.
- MUST use `scripts/registry.yaml` (or documented workflow references) to resolve runnable automation.
- MUST parameterize script inputs; avoid hardcoded one-off values.
- MUST create a reusable script first when the action is repeatable and no script exists.
- MUST log script selection, parameters, and outcome in run artifacts.
- SHOULD include a dry-run mode when feasible.
- SHOULD include idempotency and validation checks for scripts that mutate state.
- MUST apply feasibility gates before model training: data availability, hardware budget, runtime budget, acceptance metric.
- SHOULD prefer local model pipelines when feasible; otherwise use deterministic scripted fallback.
- MUST NOT repeat the same multi-step manual action across runs when it can be scripted.

## Checks
- Registry check: output references a script ID/path or explicitly records "script missing -> created".
- Parameterization check: run record includes input parameters and validation command.
- Repeatability check: script includes usage/help and can be rerun with different parameters.
- Model feasibility check: run record states feasibility gate result and selected path.

## Overrides
- Allowed only for truly one-off, non-repeatable work where scripting overhead is unjustified.
- Override MUST include `[ASSUMPTION] one-off` with rationale and expected non-reuse scope.
- Override MUST be recorded in `decisions.md` when used in production workflows.
