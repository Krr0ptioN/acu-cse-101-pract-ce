"""Week 09 Guided Workshop: File Reading, Writing and Exceptions.

Think Python: Chapter 14.
Build each example together in class with your instructor / TA.
Replace pass as you go.
"""


# 1. Writing Files: Write Lines
# Write each string in lines to filepath (UTF-8), one per line ending with "\n".
# Example: write_lines("notes.txt", ["hello", "world"]) writes:
#   hello
#   world
def write_lines(filepath, lines):
    pass


# 2. Reading Files: Read Lines
# Read all lines from filepath (UTF-8) and return them as a list of strings
# with trailing newline characters removed.
# Example: read_lines("notes.txt") returns ["hello", "world"]
def read_lines(filepath):
    pass


# 3. Appending to Files: Append Line
# Append a single line (followed by "\n") to the end of filepath (UTF-8).
# Creates the file if it does not exist.
def append_line(filepath, line):
    pass


# 4. Exceptions: Safe File Read
# Open filepath (UTF-8) and return its full text content.
# If the file does not exist (FileNotFoundError), return default instead.
# Example: safe_read_file("missing.txt", default="N/A") returns "N/A"
def safe_read_file(filepath, default=""):
    pass


# 5. Processing Files: Copy Non-Empty Lines
# Read lines from src_path and write only non-blank lines (lines with non-whitespace
# characters) to dst_path. Return the number of lines written.
def copy_non_empty_lines(src_path, dst_path):
    pass


# 6. Exceptions & Parsing: Parse Integers from File
# Read lines from filepath and convert each valid integer line to int.
# Ignore blank lines or lines that cannot be converted (ValueError).
# Return the list of parsed integers in order.
# Example: file with "10\nabc\n25\n" returns [10, 25]
def parse_int_file(filepath):
    pass


if __name__ == "__main__":
    print("Safe read missing file:", safe_read_file("does_not_exist.txt", default="(missing)"))
