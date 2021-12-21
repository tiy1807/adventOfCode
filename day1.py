with open("day1input") as f:
    values = [int(value) for value in f.readlines()]

diffs = [x - y for x, y in zip(values[3:], values[:-3])]
increased = sum([1 for diff in diffs if diff > 0])
print(increased)