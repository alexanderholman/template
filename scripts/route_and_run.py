#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml


PLACEHOLDER_RE = re.compile(r"<([a-zA-Z0-9_-]+)>")


def tokenize(text):
    if not text:
        return set()
    return set(re.findall(r"[a-z0-9][a-z0-9_-]*", text.lower()))


def load_registry(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    scripts = data.get("scripts", []) if isinstance(data, dict) else []
    return [s for s in scripts if isinstance(s, dict) and s.get("status") == "active"]


def score_script(script, query_tokens):
    intent_tokens = set()
    for item in script.get("intent", []):
        intent_tokens |= tokenize(item)
    id_tokens = tokenize(script.get("id", ""))
    desc_tokens = tokenize(script.get("description", ""))
    return 5 * len(query_tokens & intent_tokens) + 2 * len(query_tokens & id_tokens) + len(query_tokens & desc_tokens)


def select_script(scripts, script_id, query, intents):
    if script_id:
        for script in scripts:
            if script.get("id") == script_id:
                return script
        raise ValueError(f"script id not found or inactive: {script_id}")

    raw_query = " ".join([query] + intents).strip()
    if not raw_query:
        raise ValueError("provide --script-id or --query/--intent for routing")

    query_tokens = tokenize(raw_query)
    ranked = []
    for script in scripts:
        score = score_script(script, query_tokens)
        if score > 0:
            ranked.append((score, script))
    ranked.sort(key=lambda t: (-t[0], t[1].get("id", "")))

    if not ranked:
        raise ValueError("no matching script found; create and register one first")
    return ranked[0][1]


def parse_kv_args(items):
    values = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"invalid --arg value: {item}; expected key=value")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"invalid --arg key in: {item}")
        values[key] = value
    return values


def render_command(command, values):
    missing = set()

    def repl(match):
        key = match.group(1)
        if key in values:
            return values[key]
        missing.add(key)
        return match.group(0)

    rendered = PLACEHOLDER_RE.sub(repl, command)
    if missing:
        missing_keys = ", ".join(sorted(missing))
        raise ValueError(f"missing required placeholder values: {missing_keys}")
    return rendered


def main():
    parser = argparse.ArgumentParser(description="Resolve script from NL intent and execute with parameters")
    parser.add_argument("--registry", default="scripts/registry.yaml", help="Path to script registry")
    parser.add_argument("--query", default="", help="Natural language request")
    parser.add_argument("--intent", action="append", default=[], help="Additional intent tokens")
    parser.add_argument("--script-id", default="", help="Use explicit script id instead of resolver")
    parser.add_argument("--arg", action="append", default=[], help="Placeholder value key=value")
    parser.add_argument("--execute", action="store_true", help="Execute command (default is dry-run)")
    args = parser.parse_args()

    try:
        scripts = load_registry(args.registry)
        script = select_script(scripts, args.script_id.strip(), args.query.strip(), args.intent)
        values = parse_kv_args(args.arg)
        if args.query.strip() and "request" not in values:
            values["request"] = args.query.strip()
        command = script.get("command", "").strip()
        if not command:
            raise ValueError(f"selected script has empty command: {script.get('id', '<unknown>')}")
        rendered = render_command(command, values)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"Selected script: {script.get('id')}")
    print(f"Rendered command: {rendered}")
    if not args.execute:
        print("Dry run only. Re-run with --execute to run command.")
        return 0

    completed = subprocess.run(rendered, shell=True)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
