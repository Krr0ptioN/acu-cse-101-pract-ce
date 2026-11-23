"""Automated unit tests for Week 09 Graded Challenges."""

import pytest

from .challenge import (
    count_lines,
    find_matching_lines,
    safe_read_int,
    write_numbered_lines,
)


@pytest.mark.parametrize(
    "content, expected",
    [
        ("", 0),
        ("single line", 1),
        ("one\ntwo\nthree\n", 3),
        ("a\n\nb\n", 3),
        ("line 1\nline 2", 2),
    ],
)
def test_count_lines(tmp_path, content, expected):
    file_path = tmp_path / "sample.txt"
    file_path.write_text(content, encoding="utf-8")
    assert count_lines(file_path) == expected, "Return the total number of lines in the file."


@pytest.mark.parametrize(
    "lines, expected",
    [
        (["apple", "banana"], "1. apple\n2. banana\n"),
        (["only one"], "1. only one\n"),
        ([], ""),
        (["first", "second", "third"], "1. first\n2. second\n3. third\n"),
    ],
)
def test_write_numbered_lines(tmp_path, lines, expected):
    file_path = tmp_path / "numbered.txt"
    write_numbered_lines(file_path, lines)
    assert file_path.read_text(encoding="utf-8") == expected, (
        "Write each line prefixed with its 1-based index, e.g. '1. apple\\n'."
    )


@pytest.mark.parametrize(
    "content, keyword, expected",
    [
        ("Hello\nPython 3\nlearn python\nJava\n", "python", ["Python 3", "learn python"]),
        ("INFO: start\nERROR: disk full\nerror: retry\n", "ERROR", ["ERROR: disk full", "error: retry"]),
        ("alpha\nbeta\ngamma\n", "delta", []),
        ("", "anything", []),
    ],
)
def test_find_matching_lines(tmp_path, content, keyword, expected):
    file_path = tmp_path / "search.txt"
    file_path.write_text(content, encoding="utf-8")
    assert find_matching_lines(file_path, keyword) == expected, (
        "Return matching lines (case-insensitive) stripped of trailing newlines."
    )


def test_safe_read_int_valid(tmp_path):
    file_path = tmp_path / "num.txt"
    file_path.write_text("  42 \n", encoding="utf-8")
    assert safe_read_int(file_path) == 42, "Parse a valid integer from the file."

    neg_path = tmp_path / "neg.txt"
    neg_path.write_text("-17", encoding="utf-8")
    assert safe_read_int(neg_path, default=99) == -17, "Parse negative integers correctly."


def test_safe_read_int_missing_file(tmp_path):
    missing = tmp_path / "does_not_exist.txt"
    assert safe_read_int(missing) == 0, "Return default (0) when the file does not exist."
    assert safe_read_int(missing, default=-1) == -1, "Return the provided default when the file is missing."


@pytest.mark.parametrize("bad_content", ["hello", "", "3.14", "12 abc"])
def test_safe_read_int_invalid_content(tmp_path, bad_content):
    file_path = tmp_path / "bad.txt"
    file_path.write_text(bad_content, encoding="utf-8")
    assert safe_read_int(file_path, default=-99) == -99, (
        "Return default when the file content cannot be converted to an int."
    )
