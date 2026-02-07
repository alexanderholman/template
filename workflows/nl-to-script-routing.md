# Workflow: NL to Script Routing

## Workflow ID
workflow-nl-to-script-routing-001

## Purpose
Translate natural language requests into deterministic script execution by resolving existing automations first, then creating reusable scripts only when missing.

## Sequence
1. Intake (ProjectSpec/Manager): classify intent, constraints, and definition of done.
2. Registry lookup (Builder): resolve against `scripts/registry.yaml` by task intent and capabilities.
3. Parameter binding (Builder): map user request to script arguments with defaults and explicit assumptions.
4. Execution path decision (Builder):
   - If script exists: run selected script with bound parameters using `[SCRIPT:resolve-script]` and `scripts/registry.yaml`.
   - If no script and task is repeatable: author reusable script, register it in `scripts/registry.yaml`, then run it.
5. Model gate (Builder/Specialist): if model-required, evaluate local training feasibility; choose local pipeline when feasible, otherwise scripted deterministic fallback.
6. Validation (Tester/Skeptic): run script-level checks and output quality gates.
7. Logging (ProjectManager): record script ID, parameters, validation command, and outcomes in append-only run logs.

## Inputs/Outputs
- Inputs:
  - User natural language request
  - `scripts/registry.yaml`
  - Relevant specs and task context
  - Data/hardware/runtime constraints (for model-required tasks)
- Outputs:
  - Selected script + parameters
  - New script and registry entry when needed
  - Validation evidence
  - Run log entry with reproducible command

## Validation
- A script lookup is documented for each repeatable task via `[SCRIPT:resolve-script]` or a `scripts/...` reference.
- Repeatable tasks do not execute ad-hoc when no script exists; a reusable script is created first and registered in `scripts/registry.yaml`.
- Commands are parameterized and replayable.
- For model-required tasks, feasibility gate and chosen path are documented.
- `./validate_agents.sh` passes after workflow-affecting changes.
