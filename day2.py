with open("day2input") as f:
    values = [value.split(" ") for value in f.readlines()]

# Part 1
operations = ["forward", "up", "down"]
total = {}

for operation in operations:
    total[operation] = sum([int(value[1]) for value in values if value[0] == operation])

print(total["forward"] * (total["down"] - total["up"]))

# Part 2

aim = 0
depth = 0
position = 0

for command, magnitude in values:
    magnitude = int(magnitude)
    if command == "forward":
        position += magnitude
        depth += aim * magnitude
    elif command == "up":
        aim -= magnitude
    elif command == "down":
        aim += magnitude

print(position * depth)

