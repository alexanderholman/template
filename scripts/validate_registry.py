#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

import yaml


REQUIRED_FIELDS = ("id", "intent", "capabilities", "description", "command", "status")
ALLOWED_STATUS = {"active", "inactive"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate scripts/registry.yaml schema")
    parser.add_argument("--registry", default="scripts/registry.yaml", help="Path to script registry")
    args = parser.parse_args()

    try:
        data = yaml.safe_load(Path(args.registry).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"registry-schema-check: failed to load yaml: {exc}")
        return 1

    errors = []
    if not isinstance(data, dict):
        errors.append("root must be a mapping")
    scripts = data.get("scripts") if isinstance(data, dict) else None
    if not isinstance(scripts, list):
        errors.append("scripts must be a list")
        scripts = []

    seen_ids = set()
    for idx, script in enumerate(scripts, start=1):
        prefix = f"scripts[{idx}]"
        if not isinstance(script, dict):
            errors.append(f"{prefix} must be a mapping")
            continue
        for field in REQUIRED_FIELDS:
            if field not in script:
                errors.append(f"{prefix} missing required field: {field}")

        script_id = script.get("id")
        if not isinstance(script_id, str) or not script_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
        elif script_id in seen_ids:
            errors.append(f"duplicate script id: {script_id}")
        else:
            seen_ids.add(script_id)

        if not isinstance(script.get("intent"), list) or not script.get("intent"):
            errors.append(f"{prefix}.intent must be a non-empty list")

        if not isinstance(script.get("capabilities"), list) or not script.get("capabilities"):
            errors.append(f"{prefix}.capabilities must be a non-empty list")

        status = script.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{prefix}.status must be one of {sorted(ALLOWED_STATUS)}")

        command = script.get("command", "")
        if not isinstance(command, str) or not command.strip():
            errors.append(f"{prefix}.command must be a non-empty string")

    policy = data.get("policy") if isinstance(data, dict) else None
    if not isinstance(policy, dict):
        errors.append("policy must be a mapping")

    if errors:
        print("registry-schema-check: failed")
        for item in errors:
            print(f"- {item}")
        return 1

    print("registry-schema-check: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
