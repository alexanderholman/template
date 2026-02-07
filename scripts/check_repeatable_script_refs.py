#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path


REPEATABLE_RE = re.compile(r"\brepeatable\b|\[REPEATABLE\]", re.IGNORECASE)
SCRIPT_REF_RE = re.compile(r"scripts/[\w./-]+|\[SCRIPT:[^\]]+\]|scripts/registry\.yaml")


def gather_markdown_files(root):
    files = []
    for rel in ("workflows", "tasks"):
        base = root / rel
        if not base.exists():
            continue
        files.extend(sorted(base.rglob("*.md")))
    specs = root / "specs.md"
    if specs.exists():
        files.append(specs)
    return files


def has_script_ref(lines, idx):
    start = max(0, idx - 2)
    end = min(len(lines), idx + 5)
    window = "\n".join(lines[start:end])
    return bool(SCRIPT_REF_RE.search(window))


def check_file(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    failures = []
    for idx, line in enumerate(lines):
        if REPEATABLE_RE.search(line) and not has_script_ref(lines, idx):
            failures.append((idx + 1, line.strip()))
    return failures


def main():
    parser = argparse.ArgumentParser(description="Fail if repeatable tasks lack script references")
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = gather_markdown_files(root)

    failures = []
    for file_path in files:
        for line_no, line_text in check_file(file_path):
            failures.append((file_path.relative_to(root), line_no, line_text))

    if failures:
        print("Found repeatable task documentation without script references:")
        for rel, line_no, line_text in failures:
            print(f"- {rel}:{line_no} -> {line_text}")
        print("Add a script reference like `scripts/...` or `[SCRIPT:<id>]` nearby.")
        return 1

    print("repeatable-script-ref-check: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
