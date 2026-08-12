#!/usr/bin/env python3
"""CLI for lightweight daily and drill training state."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime

from training_store import (
    active_dir, find_existing, load_state, note_index, render_progress,
    resolve_paths, roots, save_state,
)


def emit(value) -> None:
    print(json.dumps(value, ensure_ascii=False))


def cmd_notes(args: argparse.Namespace) -> None:
    workspace, _ = roots(args.project_root)
    emit(note_index(workspace))


def cmd_resolve(args: argparse.Namespace) -> None:
    if not args.kind:
        raise SystemExit("resolve requires --kind daily or drill")
    emit(resolve_paths(args.project_root, args.kind, args.name))


def cmd_current(args: argparse.Namespace) -> None:
    workspace, _ = roots(args.project_root)
    plan_dir = active_dir(args.project_root, args.kind)
    state = load_state(plan_dir)
    kind = args.kind or state.get("kind", "daily")
    items, index = state.get("items", []), int(state.get("current", 0))
    if index >= len(items):
        emit({"finished": True, "summary": str(plan_dir / "总结.md")})
        return
    if kind == "daily" and state.get("lastCompletedDate") == date.today().isoformat():
        emit({"doneToday": True, "current": index,
              "progress": str(plan_dir / "进度.md")})
        return
    item = items[index]
    note, code = item.get("note"), item.get("code")
    existing = None if note and code else find_existing(workspace, item)
    note = note or (existing or {}).get("note")
    code = code or (existing or {}).get("code")
    emit({"finished": False, "planDir": str(plan_dir), "index": index,
          "item": item, "note": note, "code": code,
          "reuse": bool(note and code)})


def cmd_link(args: argparse.Namespace) -> None:
    plan_dir = active_dir(args.project_root, args.kind)
    state = load_state(plan_dir)
    item = state["items"][int(state.get("current", 0))]
    item["note"], item["code"] = args.note, args.code
    save_state(plan_dir, state)
    emit({"linked": True})


def cmd_status(args: argparse.Namespace) -> None:
    plan_dir = active_dir(args.project_root, args.kind)
    state = load_state(plan_dir)
    emit({"planDir": str(plan_dir), "kind": state.get("kind"),
          "status": state.get("status"), "current": state.get("current", 0),
          "progress": str(plan_dir / "进度.md"),
          "summary": str(plan_dir / "总结.md")})


def cmd_record(args: argparse.Namespace) -> None:
    plan_dir = active_dir(args.project_root, args.kind)
    state = load_state(plan_dir)
    kind = args.kind or state.get("kind", "daily")
    index = int(state.get("current", 0))
    item = state["items"][index]
    item.update({"status": args.status, "minutes": args.minutes,
                 "method": args.method, "issue": args.issue,
                 "submission": args.submission,
                 "completedAt": datetime.now().isoformat(timespec="seconds")})
    fields = ("status", "minutes", "method", "issue", "submission", "completedAt")
    entry = {"seq": item.get("seq"), "problemId": item.get("problemId"),
             **{key: item.get(key) for key in fields}}
    with (plan_dir / "history.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")
    state["current"] = index + 1
    if kind == "daily":
        state["lastCompletedDate"] = date.today().isoformat()
    if state["current"] >= len(state["items"]):
        state["status"] = "completed"
    save_state(plan_dir, state)
    render_progress(plan_dir, state)
    emit({"recorded": True, "finished": state.get("status") == "completed",
          "summary": str(plan_dir / "总结.md")})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("notes", "resolve", "current", "link", "record", "status"))
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--kind", choices=("daily", "drill"))
    parser.add_argument("--name", default="plan")
    parser.add_argument("--note")
    parser.add_argument("--code")
    parser.add_argument("--status", choices=("completed", "partial", "blocked", "skipped"), default="completed")
    parser.add_argument("--minutes", type=int)
    parser.add_argument("--method")
    parser.add_argument("--issue")
    parser.add_argument("--submission")
    args = parser.parse_args()
    globals()[f"cmd_{args.action}"](args)


if __name__ == "__main__":
    main()
