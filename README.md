# todo-cli

A small command-line todo list backed by a JSON file.

## Usage

```bash
python3 todo.py add "write the weekly plan"
python3 todo.py add "pay rent" --due 2026-11-15 --priority high
python3 todo.py list
python3 todo.py overdue
python3 todo.py priority high
python3 todo.py search plan
python3 todo.py done 1
python3 todo.py rm 1
python3 todo.py clear-done
```

## Features

- Add, list, complete, and remove todos
- Remove all completed todos without mutating the input with clear_done(todos) or `clear-done`
- Optional due dates and an overdue filter
- Low, medium, and high priorities with filtering via `priority`
- Case-insensitive text search with `search`
- JSON persistence in ~/.todo-cli.json
- CSV export with export_csv(todos, path)

## Tests

```bash
python3 -m unittest -q
```

## Additional API

- `stats(todos, today=None)` returns total, done, pending, and overdue counts.

## License

MIT
