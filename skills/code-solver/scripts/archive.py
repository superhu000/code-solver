#!/usr/bin/env python3
"""Resolve one lightweight archive directory or list existing notes."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

CATEGORIES = {
    "array": "数组", "string": "字符串", "linked-list": "链表",
    "stack": "栈", "queue": "队列", "hash": "哈希表", "heap": "堆",
    "tree": "树", "graph": "图", "matrix": "矩阵",
    "two-pointers": "双指针", "sliding-window": "滑动窗口",
    "binary-search": "二分查找", "dfs": "深度优先搜索", "bfs": "广度优先搜索",
    "backtracking": "回溯", "sorting": "排序", "greedy": "贪心",
    "dynamic-programming": "动态规划", "divide-and-conquer": "分治",
    "prefix-sum": "前缀和", "difference-array": "差分",
    "monotonic-stack": "单调栈", "monotonic-queue": "单调队列",
    "union-find": "并查集", "trie": "字典树", "segment-tree": "线段树",
    "topological-sort": "拓扑排序", "shortest-path": "最短路径",
    "minimum-spanning-tree": "最小生成树", "bit-manipulation": "位运算",
    "math": "数学", "state-compression": "状态压缩",
    "string-matching": "字符串匹配", "simulation": "模拟",
    "design": "设计", "geometry": "几何", "other": "其他",
}

LANGUAGES = {
    "java": ("java", "Main.java", "Test.java"),
    "python": ("python", "solution.py", "test_solution.py"),
    "py": ("python", "solution.py", "test_solution.py"),
    "c": ("c", "solution.c", "test.c"),
    "cpp": ("cpp", "solution.cpp", "test.cpp"),
    "c++": ("cpp", "solution.cpp", "test.cpp"),
    "typescript": ("typescript", "solution.ts", "test.ts"),
    "ts": ("typescript", "solution.ts", "test.ts"),
}


def clean(value: str, fallback: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", value.strip())
    value = re.sub(r"\s+", "-", value).strip(" .-")
    return (value or fallback)[:60]


def resolve(args: argparse.Namespace) -> None:
    language, code_name, test_name = LANGUAGES.get(
        args.language.lower(), LANGUAGES["java"]
    )
    platform = clean(args.platform, "local")
    category = CATEGORIES.get(args.category, clean(args.category, "其他"))
    problem_id = clean(args.problem_id, "unknown")
    title = clean(args.title, "未命名题目")
    if args.mode == "review" and problem_id == "unknown":
        problem_id = datetime.now().strftime("%Y%m%d-%H%M")

    root = Path(args.project_root).resolve() / args.root
    archive_dir = root / platform / category / f"{problem_id}-{title}-{language}"
    archive_dir.mkdir(parents=True, exist_ok=True)
    note_name = "代码审查.md" if args.mode == "review" else "题解.md"
    result = {
        "archiveDir": str(archive_dir),
        "note": str(archive_dir / note_name),
        "code": str(archive_dir / code_name),
        "test": str(archive_dir / test_name) if args.mode == "detail" else None,
    }
    print(json.dumps(result, ensure_ascii=False))


def list_notes(args: argparse.Namespace) -> None:
    root = Path(args.project_root).resolve() / args.root
    notes = [] if not root.exists() else sorted(
        str(path.relative_to(root))
        for name in ("题解.md", "代码审查.md")
        for path in root.rglob(name)
    )
    print(json.dumps(notes, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("resolve", "list"))
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--root", default="code-solver-workspace")
    parser.add_argument("--platform", default="local")
    parser.add_argument("--category", default="other")
    parser.add_argument("--language", default="java")
    parser.add_argument("--problem-id", default="unknown")
    parser.add_argument("--title", default="未命名题目")
    parser.add_argument("--mode", choices=("fast", "detail", "review"), default="fast")
    args = parser.parse_args()
    resolve(args) if args.action == "resolve" else list_notes(args)


if __name__ == "__main__":
    main()

