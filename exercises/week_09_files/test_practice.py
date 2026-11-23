"""ACU CSE 101 - Automated Unit Tests for Week 09 Practice."""

from .practice import (
    append_line,
    copy_non_empty_lines,
    parse_int_file,
    read_lines,
    safe_read_file,
    write_lines,
)


def test_write_and_read_lines(tmp_path):
    file_path = tmp_path / "notes.txt"
    write_lines(file_path, ["alpha", "beta", "gamma"])
    assert file_path.read_text(encoding="utf-8") == "alpha\nbeta\ngamma\n"
    assert read_lines(file_path) == ["alpha", "beta", "gamma"]


def test_read_lines_empty_file(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")
    assert read_lines(file_path) == []


def test_append_line(tmp_path):
    file_path = tmp_path / "log.txt"
    append_line(file_path, "first")
    append_line(file_path, "second")
    assert file_path.read_text(encoding="utf-8") == "first\nsecond\n"


def test_safe_read_file(tmp_path):
    existing = tmp_path / "hello.txt"
    existing.write_text("Hello, CSE 101!", encoding="utf-8")
    missing = tmp_path / "missing.txt"

    assert safe_read_file(existing) == "Hello, CSE 101!"
    assert safe_read_file(missing) == ""
    assert safe_read_file(missing, default="N/A") == "N/A"


def test_copy_non_empty_lines(tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("line 1\n\n   \nline 2\n\t\nline 3\n", encoding="utf-8")

    count = copy_non_empty_lines(src, dst)
    assert count == 3
    assert dst.read_text(encoding="utf-8").splitlines() == ["line 1", "line 2", "line 3"]


def test_parse_int_file(tmp_path):
    file_path = tmp_path / "numbers.txt"
    file_path.write_text("10\nnot a number\n  -5 \n\n42\n3.14\n", encoding="utf-8")
    assert parse_int_file(file_path) == [10, -5, 42]
