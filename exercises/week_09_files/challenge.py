"""Week 09 Graded Challenges: File Reading, Writing and Exceptions.

Complete the four functions below. Replace pass with your code.
Return results; do not use input().
Keep names and parameters unchanged so the automated tests can call them.
"""


# Challenge 1 (File Reading): Count Lines
# Return the total number of lines in the text file at filepath (UTF-8).
# Return 0 for an empty file.
# Example: a file containing "a\nb\nc\n" returns 3
def count_lines(filepath):
    with open( filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return len(lines)


# Challenge 2 (File Writing): Write Numbered Lines
# Write each string in lines to filepath (UTF-8), numbered starting from 1
# in the format "{number}. {text}\n".
# Example: write_numbered_lines(path, ["apple", "banana"]) writes:
#   1. apple
#   2. banana
def write_numbered_lines(filepath, lines):
    with open(filepath, "w", encoding="utf-8") as file:
        number=1 
        for text in lines:
            file.write(f"{number}. {text}\n")
            number += 1 

   


# Challenge 3 (Searching Files): Find Matching Lines
# Read filepath (UTF-8) and return a list of lines (without trailing newlines)
# that contain keyword, matching case-insensitively.
# Preserve original order and original casing of each matching line.
# Example: searching "python" in ["Hello\n", "Python 3\n", "learn python\n"]
#          returns ["Python 3", "learn python"]
def find_matching_lines(filepath, keyword):
    result = []
    with open (filepath, "r", encoding="utf-8") as file:
        for line in file:
            if keyword.lower() in line.lower():
                result.append(line.rstrip("\n"))
    return result
               

# Challenge 4 (Exception Handling): Safe Read Integer
# Read the text from filepath (UTF-8), strip whitespace, and return it as an int.
# If the file does not exist (FileNotFoundError) or its content cannot be
# converted to an int (ValueError), return default.
# Examples: file containing " 42 \n" returns 42
#           missing file returns default
#           file containing "hello" returns default
def safe_read_int(filepath, default=0):
    try:
        with open (filepath, "r", encoding="utf-8") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return default

if __name__=="__main__": 
 with open("test.txt", "w", encoding="utf-8") as file:
    file.write("a\nb\nc\n")
 print(count_lines("test.txt"))

 write_numbered_lines("test.txt", ["apple", "banana"])
 print(open("test.txt", encoding="utf-8").read())

 with open("test.txt", "w", encoding="utf-8") as file:
    file.write("Hello\nPython 3\nlearn python\n")
 print(find_matching_lines("test.txt", "python"))

 with open("test.txt", "w", encoding="utf-8") as file:
     file.write(" 42 \n")
 print(safe_read_int("test.txt"))
 print(safe_read_int("yok.txt", 5))
     