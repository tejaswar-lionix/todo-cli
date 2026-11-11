# todo-cli

A small command-line todo list backed by a JSON file.

## Usage

```bash
python3 todo.py add "write the weekly plan"
python3 todo.py list
python3 todo.py done 1
python3 todo.py rm 1
```

## Features

- Add, list, complete, and remove todos
- JSON persistence in ~/.todo-cli.json
- CSV export with export_csv(todos, path)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
