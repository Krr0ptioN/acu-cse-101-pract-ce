"""Week 09 Graded Challenges: File Reading, Writing and Exceptions.

Complete the four functions below. Replace pass with your code.
Return results; do not use input().
Keep names and parameters unchanged so the automated tests can call them.
"""


# Challenge 1 (File Reading): Count Lines
def count_lines(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)


# Challenge 2 (File Writing): Write Numbered Lines
def write_numbered_lines(filepath, lines):
    with open(filepath, "w", encoding="utf-8") as file:
        for index, text in enumerate(lines, start=1):
            file.write(f"{index}. {text}\n")


# Challenge 3 (Searching Files): Find Matching Lines
def find_matching_lines(filepath, keyword):
    matches = []
    target = keyword.lower()
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.rstrip("\r\n")
            if target in clean_line.lower():
                matches.append(clean_line)
    return matches


# Challenge 4 (Exception Handling): Safe Read Integer
def safe_read_int(filepath, default=0):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read().strip()
            return int(content)
    except (FileNotFoundError, ValueError):
        return default
