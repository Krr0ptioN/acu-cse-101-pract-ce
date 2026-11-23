"""ACU CSE 101 - Automated Unit Tests for Week 09 Practice."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from practice import (
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

def write_lines(file_path, lines):
    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")


def test_read_lines_empty_file(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")
    assert read_lines(file_path) == []

def read_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def test_append_line(tmp_path):
    file_path = tmp_path / "log.txt"
    append_line(file_path, "first")
    append_line(file_path, "second")
    assert file_path.read_text(encoding="utf-8") == "first\nsecond\n"

def append_line(file_path, line):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(line + "\n")

def test_safe_read_file(tmp_path):
    existing = tmp_path / "hello.txt"
    existing.write_text("Hello, CSE 101!", encoding="utf-8")
    missing = tmp_path / "missing.txt"

    assert safe_read_file(existing) == "Hello, CSE 101!"
    assert safe_read_file(missing) == ""
    assert safe_read_file(missing, default="N/A") == "N/A"

def safe_read_file(file_path, default=""):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return default


def test_copy_non_empty_lines(tmp_path):
    src = tmp_path / "src.txt"
    dst = tmp_path / "dst.txt"
    src.write_text("line 1\n\n   \nline 2\n\t\nline 3\n", encoding="utf-8")

    count = copy_non_empty_lines(src, dst)
    assert count == 3
    assert dst.read_text(encoding="utf-8").splitlines() == ["line 1", "line 2", "line 3"]

def copy_non_empty_lines(src, dst):
    count = 0
    with open(src, "r", encoding="utf-8") as source:
        with open(dst, "w", encoding="utf-8") as destination:
            for line in source:
                if line.strip():
                    destination.write(line.strip() + "\n")
                    count += 1
    return count


def test_parse_int_file(tmp_path):
    file_path = tmp_path / "numbers.txt"
    file_path.write_text("10\nnot a number\n  -5 \n\n42\n3.14\n", encoding="utf-8")
    assert parse_int_file(file_path) == [10, -5, 42]
def parse_int_file(file_path):
    numbers = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                numbers.append(int(line.strip()))
            except ValueError:
                continue
    return numbers