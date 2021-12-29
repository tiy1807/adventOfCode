from utils import read_file
from utils import Grid

class Octopus:
    def __init__(self, character):
        self.count = int(character)

    def step(self):
        if self.count == 9:
            self.count = 0
        else:
            self.count += 1

    def get_value(self):
        return self.count

    def __repr__(self):
        return str(self.get_value())


class OctoGrid(Grid):
    def __init__(self, text):
        super().__init__(Octopus)
        self.add_values(text)

    def step(self):
        flashes = []
        for rowid, row in enumerate(self.grid):
            for colid, item in enumerate(row):
                item.step()
                if item.count == 0:
                    flashes.append([rowid, colid])

        already_flashed = []
        while flashes:
            rowid, colid = flashes[0]
            print(self)
            print(f'{rowid},{colid} flashing')
            # Flashing explosion
            for row_offset in [-1, 0, 1]:
                for col_offset in [-1, 0, 1]:
                    if row_offset != 0 or col_offset != 0:
                        near_coords = [rowid + row_offset, colid + col_offset]
                        near_item = self.get_item(*near_coords)
                        if near_item and near_item.count > 0 and near_coords not in already_flashed:
                            near_item.step()
                            if near_item.count == 0:
                                print(f'{near_coords} added to flashing')
                                flashes.append(near_coords)
            already_flashed.append(flashes.pop(0))
        return len(already_flashed)

lines = read_file("day11input")

Octogrid = OctoGrid(lines)
flash_number = 0
#for step_number in range(100):
#    print("step")
#    flash_number += Octogrid.step()
#print(Octogrid)
#print(flash_number)

number_of_steps = 0
while flash_number < Octogrid.number_of_values():
    number_of_steps += 1
    flash_number = Octogrid.step()
print(number_of_steps)