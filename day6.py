class Fish:
    def __init__(self, initial_count=False):
        self.count = initial_count

    def increment(self):
        if self.count > 0:
            self.count -= 1
            fish = [self]
        else:
            self.count = 6
            fish = [self, Fish(initial_count=8)]
        return fish

    def __repr__(self):
        return str(self.count)

from utils import read_file

lines = read_file("day6input")

for line in lines:
    fishes = [int(count) for count in line.split(",")]

grouped = {key: 0 for key in range(9)}
for fish in fishes:
    grouped[fish] += 1

print(grouped)
for day in range(256):
    new_grouped = {key: grouped[key+1] for key in grouped.keys() if key < 8}
    new_grouped[6] += grouped[0]
    new_grouped[8] = grouped[0]
    grouped = new_grouped
    print(grouped)

print(sum(grouped.values()))