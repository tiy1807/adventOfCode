from utils import read_file

lines = read_file("day10input")

CORRECT = 0
CORRUPT = 1
INCOMPLETE = 2

score = {")": 3, "]": 57, "}": 1197, ">": 25137}
auto_score = {")": 1, "]": 2, "}": 3, ">": 4}
auto_scores = []

corrupted = 0
line_status = CORRECT
for line_num, line in enumerate(lines):
    line_status = CORRECT
    expected = []
    autocomplete_score = 0
    for character in line:
        if character in ["[", "{", "<", "("]:
            if character == "(":
                expected.append(chr(ord(character) + 1))
            else:
                expected.append(chr(ord(character)+2))
        elif character in ["]", "}", ">", ")"]:
            if character == expected[-1]:
                expected.pop()
            else:
                if line_status == CORRECT:
                    corrupted += score[character]
                    line_status = CORRUPT
                    print(f"Corrupted {line_num} - expected {expected[-1]} got {character}")
    if line_status == CORRECT and len(expected) > 0:
        print(f"Incomplete {line_num}")
        print(expected[::-1])
        line_status = INCOMPLETE
        for character in expected[::-1]:
            autocomplete_score = autocomplete_score * 5 + auto_score[character]
        auto_scores.append(autocomplete_score)

auto_scores.sort()
print(auto_scores[(len(auto_scores)-1)//2])