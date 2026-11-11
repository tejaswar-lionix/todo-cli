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


def add(todos, text):
    text = text.strip()
    if not text:
        raise ValueError("todo text must not be empty")
    todos.append(
        {
            "text": text,
            "done": False,
            "created": datetime.now().isoformat(timespec="seconds"),
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


def format_todos(todos):
    if not todos:
        return "No todos yet."
    lines = []
    for number, todo in enumerate(todos, start=1):
        mark = "x" if todo["done"] else " "
        lines.append(f"{number}. [{mark}] {todo['text']}")
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(prog="todo", description=__doc__)
    parser.add_argument("--file", default=DEFAULT_PATH)
    commands = parser.add_subparsers(dest="command", required=True)
    add_cmd = commands.add_parser("add")
    add_cmd.add_argument("text")
    done_cmd = commands.add_parser("done")
    done_cmd.add_argument("index", type=int)
    remove_cmd = commands.add_parser("rm")
    remove_cmd.add_argument("index", type=int)
    commands.add_parser("list")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    todos = load(args.file)
    if args.command == "add":
        add(todos, args.text)
    elif args.command == "done":
        complete(todos, args.index - 1)
    elif args.command == "rm":
        todos = remove(todos, args.index - 1)
    save(args.file, todos)
    print(format_todos(todos))


if __name__ == "__main__":
    main()
