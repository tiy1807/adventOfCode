from utils import read_file
from utils import Grid

lines = read_file("day15input")

class ChitonGrid(Grid):
    def path_cost(self, path):
        position = (0, 0)
        cost = 0
        for xstep, ystep in path:
            position = (position[0] + xstep, position[1] + ystep)
            cost += self.get_item(position[1], position[0])
        return cost

    def expand(self):
        initial_columns = self.size()[1]
        for row_id, line in enumerate(self.grid):
            print(row_id)
            new_line = line[:initial_columns]
            for increment in range(1, 5):
                new_line += [score + increment if score + increment <= 9 else score + increment - 9 for score in line]
            self.grid[row_id] = new_line
            print(self)

        increment = 1
        initial_rows = self.size()[0]
        while increment <= 4:
            print(increment)
            row_id = 0
            new_grid = []
            print(f"initial_rows: {initial_rows}")
            while row_id < initial_rows:
                new_grid.append([score + increment if score + increment <= 9 else score + increment - 9 for score in self.grid[row_id]])
                row_id += 1
            self.grid += new_grid
            print(self)
            increment += 1


grid = ChitonGrid(int)
grid.add_values(lines)

W = (-1, 0)
N = (0, -1)
E = (1, 0)
S = (0, 1)

grid.expand()
print(grid.size())

def add_tuples(*args):
    x = 0
    y = 0
    for arg in args:
        x += arg[0]
        y += arg[1]
    return (x, y)


minimum_score = {}
minimum_score[(0, 0)] = 0
minimum_score[(0, 1)] = grid.get_item(0, 1)
minimum_score[(1, 0)] = grid.get_item(1, 0)

minimum_score[(1, 1)] = min(minimum_score[(0, 1)], minimum_score[(1, 0)]) + grid.get_item(1, 1)

points = []
for i in range(2, grid.size()[0]):
    for j in range(i + 1):
        points += [(i, j), (j, i)]

updated = True
first_time = True
while updated:
    print("Next iteration")
    updated = False
    for next_point in points:

        options = []
        north = add_tuples(next_point, N)
        west = add_tuples(next_point, W)
        east = add_tuples(next_point, E)
        south = add_tuples(next_point, S)

        if minimum_score.get(east):
            options.append(minimum_score[east])
        if minimum_score.get(south):
            options.append(minimum_score[south])

        if minimum_score.get(north):
            if grid.is_valid_xy(north):
                options.append(minimum_score[north])
            if grid.is_valid_xy(west) and minimum_score.get(add_tuples(west, N)):
                options.append(grid.get_xy(west) + minimum_score[add_tuples(west, N)])
            if grid.is_valid_xy(east) and minimum_score.get(add_tuples(east, N)):
                options.append(grid.get_xy(east) + minimum_score[add_tuples(east, N)])

        if minimum_score.get(west):
            if grid.is_valid_xy(west):
                options.append(minimum_score[west])
            if grid.is_valid_xy(south) and minimum_score.get(add_tuples(south, W)):
                options.append(grid.get_xy(south) + minimum_score[add_tuples(south, W)])
            if grid.is_valid_xy(north) and minimum_score.get(add_tuples(north, W)):
                options.append(grid.get_xy(north) + minimum_score[add_tuples(north, W)])

        new_score = min(options) + grid.get_xy(next_point)
        if minimum_score.get(next_point) and new_score < minimum_score[next_point]:
            updated = True

        minimum_score[next_point] = min(options) + grid.get_xy(next_point)
        if first_time:
            updated = True
        first_time = False
        #print(minimum_score)

print(minimum_score)
print(minimum_score[(2,2)])
print(minimum_score[add_tuples(grid.size(), (-1, -1))])


grid.export_to_text(filename="day15expanded")
