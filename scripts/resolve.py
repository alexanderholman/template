#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


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
    for i in script.get("intent", []):
        intent_tokens |= tokenize(i)
    capability_tokens = set()
    for c in script.get("capabilities", []):
        capability_tokens |= tokenize(c)
    id_tokens = tokenize(script.get("id", ""))
    desc_tokens = tokenize(script.get("description", ""))

    score = 0
    score += 5 * len(query_tokens & intent_tokens)
    score += 3 * len(query_tokens & capability_tokens)
    score += 2 * len(query_tokens & id_tokens)
    score += 1 * len(query_tokens & desc_tokens)
    return score


def format_result(script, score):
    return {
        "id": script.get("id"),
        "description": script.get("description", ""),
        "command": script.get("command", ""),
        "intent": script.get("intent", []),
        "capabilities": script.get("capabilities", []),
        "parameters": script.get("parameters", []),
        "score": score,
    }


def main():
    parser = argparse.ArgumentParser(description="Resolve NL intent to registered script")
    parser.add_argument("--registry", default="scripts/registry.yaml", help="Path to script registry")
    parser.add_argument("--query", default="", help="Natural language request")
    parser.add_argument("--intent", action="append", default=[], help="Intent token(s)")
    parser.add_argument("--top-k", type=int, default=3, help="Max matches to return")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--list", action="store_true", help="List active script IDs")
    args = parser.parse_args()

    try:
        scripts = load_registry(args.registry)
    except Exception as exc:
        print(f"error: failed loading registry: {exc}", file=sys.stderr)
        return 2

    if args.list:
        for script in sorted(scripts, key=lambda s: s.get("id", "")):
            print(script.get("id", ""))
        return 0

    raw_query = " ".join([args.query] + args.intent).strip()
    if not raw_query:
        print("error: provide --query and/or --intent", file=sys.stderr)
        return 2

    query_tokens = tokenize(raw_query)
    ranked = []
    for script in scripts:
        score = score_script(script, query_tokens)
        if score > 0:
            ranked.append((score, script))
    ranked.sort(key=lambda t: (-t[0], t[1].get("id", "")))

    results = [format_result(script, score) for score, script in ranked[: max(1, args.top_k)]]
    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    if not results:
        print("No matching script found. Create a reusable script and register it in scripts/registry.yaml.")
        return 1

    for idx, result in enumerate(results, start=1):
        print(f"{idx}. {result['id']} (score={result['score']})")
        print(f"   description: {result['description']}")
        print(f"   command: {result['command']}")
        if result.get("capabilities"):
            print(f"   capabilities: {result['capabilities']}")
        if result.get("parameters"):
            print(f"   parameters: {result['parameters']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
