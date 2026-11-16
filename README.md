# todo-cli

A small command-line todo list backed by a JSON file.

## Usage

```bash
python3 todo.py add "write the weekly plan"
python3 todo.py add "pay rent" --due 2026-11-15 --priority high
python3 todo.py list
python3 todo.py overdue
python3 todo.py priority high
python3 todo.py done 1
python3 todo.py rm 1
```

## Features

- Add, list, complete, and remove todos
- Optional due dates and an overdue filter
- Low, medium, and high priorities with filtering via `priority`
- JSON persistence in ~/.todo-cli.json
- CSV export with export_csv(todos, path)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
