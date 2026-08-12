"""Storage and archive lookup helpers for training.py."""

from __future__ import annotations

import json
import re
from pathlib import Path

CODE_NAMES = ("Main.java", "solution.py", "solution.c", "solution.cpp", "solution.ts")
CODE_LANGUAGES = {"Main.java": "java", "solution.py": "python", "solution.c": "c",
                  "solution.cpp": "cpp", "solution.ts": "typescript"}


def clean(value: str) -> str:
    value = re.sub(r'[^0-9A-Za-z\u4e00-\u9fff._-]+', "-", value.strip())
    return value.strip(".-")[:60] or "plan"


def roots(project_root: str) -> tuple[Path, Path]:
    workspace = Path(project_root).resolve() / "code-solver-workspace"
    return workspace, workspace / "training"


def read_json(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def active_dir(project_root: str, kind: str | None) -> Path:
    _, training = roots(project_root)
    active = read_json(training / "active.json", {})
    kind = kind or active.get("lastKind")
    value = active.get(kind) if kind else None
    if not value:
        raise SystemExit(f"No active {kind} plan")
    return training / value


def load_state(plan_dir: Path) -> dict:
    state = read_json(plan_dir / "state.json", {})
    if not state.get("items"):
        raise SystemExit("Training state has no items")
    return state


def save_state(plan_dir: Path, state: dict) -> None:
    write_json(plan_dir / "state.json", state)


def resolve_paths(project_root: str, kind: str, name: str) -> dict:
    _, training = roots(project_root)
    plan_dir = training / kind / clean(name)
    (plan_dir / "submissions").mkdir(parents=True, exist_ok=True)
    active_path = training / "active.json"
    active = read_json(active_path, {})
    active[kind] = str(plan_dir.relative_to(training))
    active["lastKind"] = kind
    write_json(active_path, active)
    return {"planDir": str(plan_dir), "plan": str(plan_dir / "计划.md"),
            "state": str(plan_dir / "state.json"),
            "progress": str(plan_dir / "进度.md"),
            "summary": str(plan_dir / "总结.md"),
            "submissions": str(plan_dir / "submissions")}


def note_index(workspace: Path) -> list[dict]:
    result = []
    notes = workspace.rglob("题解.md") if workspace.exists() else []
    for note in notes:
        if "training" in note.parts:
            continue
        folder = note.parent
        code = next((path for base in (folder, folder / "src")
                     for name in CODE_NAMES if (path := base / name).exists()), None)
        parts = folder.relative_to(workspace).parts
        match = re.match(r"([^-]+)-(.+?)-(java|python|c|cpp|typescript)$", folder.name)
        problem_id, title, language = (
            match.groups() if match else (folder.name.split("-", 1)[0], folder.name, "")
        )
        language = language or (CODE_LANGUAGES.get(code.name, "") if code else "")
        result.append({"platform": parts[0] if parts else "local",
                       "category": parts[1] if len(parts) > 1 else "其他",
                       "problemId": problem_id, "title": title,
                       "language": language, "note": str(note),
                       "code": str(code) if code else None})
    return result


def find_existing(workspace: Path, item: dict) -> dict | None:
    problem_id = str(item.get("problemId", ""))
    platform = str(item.get("platform", "local")).lower()
    language = str(item.get("language", "")).lower()
    record = next((record for record in note_index(workspace)
                   if record["problemId"] == problem_id
                   and record["platform"].lower() == platform), None)
    if record and language and record.get("language") != language:
        record = {**record, "code": None}
    return record


def safe_cell(value) -> str:
    return str(value or "-").replace("|", "／").replace("\n", " ")


def render_progress(plan_dir: Path, state: dict) -> None:
    rows = ["# 训练进度", "",
            "| # | 题目 | 状态 | 用时 | 方法 | 主要问题 | 提交 | 题解 |",
            "|---:|---|---|---:|---|---|---|---|"]
    for item in state.get("items", []):
        values = (item.get("seq"), item.get("title"), item.get("status", "pending"),
                  item.get("minutes"), item.get("method"), item.get("issue"),
                  item.get("submission"), item.get("note"))
        rows.append("| " + " | ".join(safe_cell(value) for value in values) + " |")
    (plan_dir / "进度.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
