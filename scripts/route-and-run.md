# Route And Run Guide

Use `scripts/route_and_run.py` to resolve natural language requests to registered automations and execute them safely.

## Safety Model
- Default mode is dry-run and does not execute commands.
- Execution requires explicit `--execute`.
- Placeholder values like `<request>` must be provided via `--query` or `--arg key=value`.

## Common Usage
```bash
# Dry-run route selection
python3 scripts/route_and_run.py --query "validate agent definitions"

# Pin to a specific script id (dry-run)
python3 scripts/route_and_run.py --script-id resolve-script --arg request="validate agent definitions"

# Execute selected command
python3 scripts/route_and_run.py --query "validate agent definitions" --execute
```

## Forge Shortcut
```bash
scripts/forge-route "validate agent definitions"
scripts/forge-route --execute "validate agent definitions"
```

## Troubleshooting
- `error: no matching script found`: add/register the script in `scripts/registry.yaml`.
- `missing required placeholder values`: provide `--arg key=value` for all placeholders.
- command failed with non-zero exit: run the rendered command directly to inspect details.
