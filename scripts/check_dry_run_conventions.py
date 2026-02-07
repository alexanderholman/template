#!/usr/bin/env python3

import argparse
from pathlib import Path

import yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Check dry-run convention for executable scripts")
    parser.add_argument("--registry", default="scripts/registry.yaml", help="Path to script registry")
    args = parser.parse_args()

    data = yaml.safe_load(Path(args.registry).read_text(encoding="utf-8"))
    scripts = data.get("scripts", []) if isinstance(data, dict) else []

    failures = []
    for script in scripts:
        if not isinstance(script, dict):
            continue
        if script.get("status") != "active":
            continue
        intent = script.get("intent", [])
        script_id = script.get("id", "<unknown>")
        if "execute" not in intent:
            continue

        command = script.get("command", "")
        params = script.get("parameters", [])
        desc = script.get("description", "").lower()
        has_execute_gate = "execute" in params or "--execute" in command or "dry-run" in desc
        if not has_execute_gate:
            failures.append(script_id)

    if failures:
        print("dry-run-convention-check: failed")
        for script_id in failures:
            print(f"- {script_id} missing execute/dry-run gating")
        return 1

    print("dry-run-convention-check: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
