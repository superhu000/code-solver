#!/usr/bin/env python3
"""Validate documentation contracts that must not drift."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
required = {
    "README.md": ["当前正式版本：**" + version + "**", "spec/CURRENT.md"],
    "command/code-solver.md": ["skill/code-solver/SKILL.md", "/code-solver train daily"],
    "skill/code-solver/SKILL.md": ["当前发布契约：" + version, "## Train 入口", "references/training.md"],
    "spec/CURRENT.md": ["# Code Solver " + version + " 当前 Spec", "solve fast", "train daily"],
    "spec/CHANGELOG.md": ["## " + version],
}
errors = []
for relative, tokens in required.items():
    body = (ROOT / relative).read_text(encoding="utf-8")
    for token in tokens:
        if token not in body:
            errors.append(f"{relative}: missing {token!r}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"documentation contracts are synchronized for {version}")
