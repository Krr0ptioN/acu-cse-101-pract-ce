"""Week 09 Graded Challenges: File Reading, Writing and Exceptions.

Complete the four functions below. Replace pass with your code.
Return results; do not use input().
Keep names and parameters unchanged so the automated tests can call them.
"""


# Challenge 1 (File Reading): Count Lines
def count_lines(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        count = 0
        for _ in f:
            count += 1
    return count


# Challenge 2 (File Writing): Write Numbered Lines
def write_numbered_lines(filepath, lines):
    with open(filepath, "w", encoding="utf-8") as f:
        for number, text in enumerate(lines, start=1):
            f.write(f"{number}. {text}\n")


# Challenge 3 (Searching Files): Find Matching Lines
def find_matching_lines(filepath, keyword):
    matches = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            clean = line.rstrip("\n")
            if keyword.lower() in clean.lower():
                matches.append(clean)
    return matches


# Challenge 4 (Exception Handling): Safe Read Integer
def safe_read_int(filepath, default=0):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return default
