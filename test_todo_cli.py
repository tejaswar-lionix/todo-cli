import os
import tempfile
import unittest

from todo import (
    add,
    by_priority,
    complete,
    format_todos,
    load,
    overdue,
    pending,
    remove,
    save,
)


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


class DueDateTests(unittest.TestCase):
    def test_add_stores_due_date(self):
        todos = add([], "pay rent", due="2026-11-15")
        self.assertEqual(todos[0]["due"], "2026-11-15")

    def test_add_without_due_date_stores_none(self):
        todos = add([], "someday")
        self.assertIsNone(todos[0]["due"])

    def test_add_rejects_bad_due_date(self):
        with self.assertRaises(ValueError):
            add([], "pay rent", due="15/11/2026")

    def test_overdue_lists_only_unfinished_past_items(self):
        todos = add([], "past", due="2026-11-10")
        add(todos, "future", due="2026-11-20")
        add(todos, "undated")
        add(todos, "done", due="2026-11-01")
        complete(todos, 3)
        self.assertEqual(
            [todo["text"] for todo in overdue(todos, today="2026-11-16")],
            ["past"],
        )

    def test_overdue_excludes_due_today(self):
        todos = add([], "today", due="2026-11-16")
        self.assertEqual(overdue(todos, today="2026-11-16"), [])


class PriorityTests(unittest.TestCase):
    def test_add_defaults_to_medium(self):
        todos = add([], "write tests")
        self.assertEqual(todos[0]["priority"], "medium")

    def test_add_stores_priority(self):
        todos = add([], "pay rent", priority="high")
        self.assertEqual(todos[0]["priority"], "high")

    def test_add_rejects_unknown_priority(self):
        with self.assertRaises(ValueError):
            add([], "pay rent", priority="urgent")

    def test_by_priority_returns_only_matching_in_order(self):
        todos = add([], "low one", priority="low")
        add(todos, "high one", priority="high")
        add(todos, "low two", priority="low")
        self.assertEqual(
            [todo["text"] for todo in by_priority(todos, "low")],
            ["low one", "low two"],
        )

    def test_by_priority_rejects_unknown_priority(self):
        with self.assertRaises(ValueError):
            by_priority([], "urgent")

    def test_format_includes_priority(self):
        todos = add([], "pay rent", due="2026-11-15", priority="high")
        self.assertEqual(
            format_todos(todos),
            "1. [ ] pay rent [high] (due 2026-11-15)",
        )


class ExportTests(unittest.TestCase):
    def test_export_csv_writes_header_and_rows(self):
        import csv

        from todo import export_csv

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "todos.csv")
            export_csv(
                [{"done": False, "text": "a,b", "created": "2026-01-01"}],
                path,
            )
            with open(path, encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
        self.assertEqual(rows[0], ["done", "text", "created"])
        self.assertEqual(rows[1][1], "a,b")


if __name__ == "__main__":
    unittest.main()
