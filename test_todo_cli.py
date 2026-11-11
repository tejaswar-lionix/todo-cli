import os
import tempfile
import unittest

from todo import add, complete, format_todos, load, pending, remove, save


class TodoTests(unittest.TestCase):
    def test_add_creates_open_todo(self):
        todos = add([], "write tests")
        self.assertEqual(todos[0]["text"], "write tests")
        self.assertFalse(todos[0]["done"])

    def test_add_rejects_blank_text(self):
        with self.assertRaises(ValueError):
            add([], "   ")

    def test_complete_marks_done(self):
        todos = add([], "ship it")
        complete(todos, 0)
        self.assertTrue(todos[0]["done"])

    def test_remove_drops_item(self):
        todos = add(add([], "one"), "two")
        self.assertEqual([todo["text"] for todo in remove(todos, 0)], ["two"])

    def test_pending_filters_done_items(self):
        todos = add(add([], "one"), "two")
        complete(todos, 0)
        self.assertEqual([todo["text"] for todo in pending(todos)], ["two"])

    def test_format_empty_list(self):
        self.assertEqual(format_todos([]), "No todos yet.")

    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "todos.json")
            save(path, add([], "persist"))
            self.assertEqual(load(path)[0]["text"], "persist")


if __name__ == "__main__":
    unittest.main()
