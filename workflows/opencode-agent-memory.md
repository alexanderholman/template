# Workflow: OpenCode Agent Memory

## Workflow ID
opencode-agent-memory-001

## Purpose
Ensure OpenCode agents consistently initialize, log, and validate continuity memory across sessions.

## Sequence
1. Install AgentMemory and confirm `memlog` is available.
2. Run `memlog doctor --root ~/opencode --strict` before action work.
3. Log action-phase events with `memlog log`.
4. Run `memlog validate --root ~/opencode --strict` before handoff.
5. Use `memlog load` to retrieve context for the next agent or session.

## Inputs/Outputs
- Inputs: `agent_id`, `session_id`, workspace root, event details
- Outputs: linked markdown continuity artifacts and validation status

## Validation
- `memlog doctor` succeeds
- `memlog validate` succeeds
- Event records include wiki links to action artifacts
