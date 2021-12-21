with open("day3input") as f:
    values = [value.strip() for value in f.readlines()]

bits = [[int(value[position]) for value in values] for position in range(len(values[0]))]

## Part 1

bit = [1 if sum(bit) > len(bit)/2 else 0 for bit in bits]
inverse = [1 if digit == 0 else 0 for digit in bit]

print(bit)
print(inverse)

decimal_bit = sum([2**position if digit == 1 else 0 for position, digit in enumerate(bit[::-1])])
decimal_inverse = sum([2**position if digit == 1 else 0 for position, digit in enumerate(inverse[::-1])])

print(decimal_bit*decimal_inverse)

## Part 2

# Oxygen

oxygen = [[int(value[position]) for position in range(len(values[0]))] for value in values]
CO2 = [[int(value[position]) for position in range(len(values[0]))] for value in values]

def list_filter(numbers, value):
    return [number[1:] for number in numbers if number[0] == value]

answer_ox = []
answer_co2 = []
for position in range(len(values[0])):
    initial_bits_ox = [value[0] for value in oxygen]
    if sum(initial_bits_ox) >= len(initial_bits_ox)/2:
        most_common = 1
    else:
        most_common = 0
    oxygen = list_filter(oxygen, most_common)
    answer_ox.append(most_common)
decimal_ox = sum([2**position if digit == 1 else 0 for position, digit in enumerate(answer_ox[::-1])])
print(decimal_ox)

for position in range(len(values[0])):
    initial_bits_C02 = [value[0] for value in CO2]
    if sum(initial_bits_C02) == len(initial_bits_C02):
        most_common = 0
    elif sum(initial_bits_C02) >= len(initial_bits_C02)/2:
        most_common = 1
    else:
        most_common = 0
    CO2 = list_filter(CO2, 1 - most_common)
    answer_co2.append(1 - most_common)


decimal_co2 = sum([2**position if digit == 1 else 0 for position, digit in enumerate(answer_co2[::-1])])

print(decimal_ox*decimal_co2)
