# Script Template

Use `scripts/templates/new_script.py` when adding reusable automations.

Required conventions:
- Include `--execute`; default behavior MUST be dry-run.
- Print a clear dry-run message with the rendered action.
- Exit non-zero on validation or runtime failures.
- Add the new script to `scripts/registry.yaml` with `intent` and `capabilities`.
