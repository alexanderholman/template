# Skill: AgentMemory

## Purpose
Define how agents use AgentMemory (`memlog`) for continuity across sessions and action runs.

## Inputs
- `agent_id`
- `session_id`
- Workspace root (default `~/opencode`)
- Event context and optional tool output summary

## Outputs
- Linked memory entries in:
  - `memory/master.md`
  - `memory/agents/{agent}.md`
  - `memory/sessions/{session}.md`
- Action records in `actions/{Y}/{m}/{His.millisecond}-{memory_uuid}.md`
- Raw artifacts in `actions/{Y}/{m}/raw/`

## Behavior
1. Install and verify:
   - `cd ~/AgentMemory && ./install.sh --force`
   - `memlog doctor --root ~/opencode --strict`
2. Before handoff/finalization:
   - `memlog validate --root ~/opencode --strict`
3. During action-phase events:
   - `memlog log --root ~/opencode --agent-id <agent> --session-id <session> --event-type <type> --message "..."`
4. For continuity retrieval:
   - `memlog load --root ~/opencode --source session --session-id <session> --reverse --limit 20`

## Constraints
- Treat memory index files as append-only.
- Avoid logging secrets/tokens in plaintext.
- Use summarized tool outputs with raw links for large artifacts.
