#!/usr/bin/env python3
"""A small command-line todo list backed by a JSON file."""
import argparse
import json
import os
from datetime import datetime

DEFAULT_PATH = os.path.expanduser("~/.todo-cli.json")


def load(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save(path, todos):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(todos, handle, indent=2)


def parse_due(due):
    """Validate an optional YYYY-MM-DD due date and return it normalised."""
    if due is None or due == "":
        return None
    try:
        return datetime.strptime(due, "%Y-%m-%d").date().isoformat()
    except ValueError as error:
        raise ValueError("due date must be formatted as YYYY-MM-DD") from error


def add(todos, text, due=None):
    text = text.strip()
    if not text:
        raise ValueError("todo text must not be empty")
    todos.append(
        {
            "text": text,
            "done": False,
            "created": datetime.now().isoformat(timespec="seconds"),
            "due": parse_due(due),
        }
    )
    return todos


def complete(todos, index):
    todos[index]["done"] = True
    return todos


def remove(todos, index):
    return todos[:index] + todos[index + 1:]


def pending(todos):
    return [todo for todo in todos if not todo["done"]]


def overdue(todos, today=None):
    """Return unfinished todos whose due date is before today."""
    if today is None:
        today = datetime.now().date().isoformat()
    today = parse_due(today)
    return [
        todo
        for todo in todos
        if not todo["done"]
        and todo.get("due")
        and todo["due"] < today
    ]


def format_todos(todos):
    if not todos:
        return "No todos yet."
    lines = []
    for number, todo in enumerate(todos, start=1):
        mark = "x" if todo["done"] else " "
        line = f"{number}. [{mark}] {todo['text']}"
        if todo.get("due"):
            line += f" (due {todo['due']})"
        lines.append(line)
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(prog="todo", description=__doc__)
    parser.add_argument("--file", default=DEFAULT_PATH)
    commands = parser.add_subparsers(dest="command", required=True)
    add_cmd = commands.add_parser("add")
    add_cmd.add_argument("text")
    add_cmd.add_argument("--due", help="due date in YYYY-MM-DD form")
    done_cmd = commands.add_parser("done")
    done_cmd.add_argument("index", type=int)
    remove_cmd = commands.add_parser("rm")
    remove_cmd.add_argument("index", type=int)
    commands.add_parser("list")
    commands.add_parser("overdue")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    todos = load(args.file)
    if args.command == "add":
        add(todos, args.text, args.due)
    elif args.command == "done":
        complete(todos, args.index - 1)
    elif args.command == "rm":
        todos = remove(todos, args.index - 1)
    if args.command == "overdue":
        print(format_todos(overdue(todos)) or "No overdue todos.")
        return
    save(args.file, todos)
    print(format_todos(todos))


if __name__ == "__main__":
    main()


def export_csv(todos, path):
    """Write todos to path as CSV with done, text, and created columns."""
    import csv

    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["done", "text", "created"])
        for todo in todos:
            writer.writerow([todo["done"], todo["text"], todo.get("created", "")])
    return path
