from utils import read_file

lines = read_file("day8input")

output_values = []
numbers = {}
for line in lines:
    output_values += line.split("|")[1].strip().split(" ")
    length_outputs = [len(output_value) for output_value in output_values]

numbers[1] = sum([1 for length in length_outputs if length == 2])
numbers[4] = sum([1 for length in length_outputs if length == 4])
numbers[7] = sum([1 for length in length_outputs if length == 3])
numbers[8] = sum([1 for length in length_outputs if length == 7])

print(output_values)
print(sum(numbers.values()))

def convert(digit_string):
    return {letter: 1 if letter in digit_string else 0 for letter in ["a","b","c","d","e","f","g"]}

def stringify(digit_dict):
    return "".join([key for key in digit_dict.keys() if digit_dict[key] == 1])

output_values = []
all_values = []
for line in lines:
    output_values.append(line.split("|")[1].strip().split(" "))
    all_values.append([convert(digit) for digit in line.split(" ") if digit != "|"])

decoded_number = 0
for id, line in enumerate(all_values):
    numbers = {}
    numbers[1] = [value for value in line if sum(value.values()) == 2][0]
    numbers[4] = [value for value in line if sum(value.values()) == 4][0]
    numbers[7] = [value for value in line if sum(value.values()) == 3][0]
    numbers[8] = [value for value in line if sum(value.values()) == 7][0]

    top = [letter for letter in ["a","b","c","d","e","f","g"] if letter in stringify(numbers[7]) and letter not in stringify(numbers[1])][0]
    six_segments = [value for value in line if sum(value.values()) == 6]
    for digit in six_segments:
        if stringify(numbers[1])[0] not in stringify(digit) or stringify(numbers[1])[1] not in stringify(digit):
            numbers[6] = digit
            top_right = [letter for letter in ["a","b","c","d","e","f","g"] if letter not in stringify(digit)][0]
            if top_right == stringify(numbers[1])[0]:
                bottom_right = stringify(numbers[1])[1]
            else:
                bottom_right = stringify(numbers[1])[0]

    five_segments = [value for value in line if sum(value.values()) == 5]
    for digit in five_segments:
        if top_right not in stringify(digit):
            numbers[5] = digit

    anti_5 = {letter: 1-numbers[5][letter] for letter in ["a","b","c","d","e","f","g"]}
    bottom_left = [letter for letter in anti_5.keys() if anti_5[letter] == 1 and letter != top_right][0]

    for digit in six_segments:
        if bottom_left not in stringify(digit):
            numbers[9] = digit

    for digit in six_segments:
        if digit != numbers[6] and digit != numbers[9]:
            numbers[0] = digit

    for digit in five_segments:
        if bottom_left in stringify(digit):
            numbers[2] = digit

    for digit in five_segments:
        if digit != numbers[2] and digit != numbers[5]:
            numbers[3] = digit

    decoded_output = []
    for output in output_values[id]:
        output_dict = convert(output)
        for number, encoded in numbers.items():
            if encoded == output_dict:
                decoded_output.append(number)

    decoded_number += sum([number*10**(3-place_value) for place_value, number in enumerate(decoded_output)])
    print(decoded_number)