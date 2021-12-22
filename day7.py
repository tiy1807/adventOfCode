from utils import read_file

lines = read_file("day7input")

for line in lines:
    crabs = [int(count) for count in line.split(",")]

part1 = False

errors = []
for aligned_position in range(max(crabs)):
    error = 0
    for crab in crabs:
        if part1:
            error += abs(aligned_position - crab)
        else:
            diff = abs(aligned_position - crab)
            error += diff*(diff+1)//2
    errors.append(error)

len(errors)
print(errors)
print(min(errors))
