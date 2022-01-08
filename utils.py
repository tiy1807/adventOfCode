def read_file(filename):
    with open(filename) as f:
        lines = [value.strip() for value in f.readlines()]
    return lines


class Grid:
    def __init__(self, constructor):
        self.grid = []
        self.constructor = constructor

    def add_values(self, text):
        for line_num, line in enumerate(text):
            self.grid.append([])
            for character in line:
                self.grid[line_num].append(self.constructor(character))

    def get_item(self, row, column):
        item = None
        if self.is_valid_point(row, column):
            item = self.grid[row][column]
        return item

    def is_valid_point(self, row, column):
        return (len(self.grid) > row >= 0) and (len(self.grid[0]) > column >= 0)

    def get_xy(self, coords):
        return self.get_item(coords[1], coords[0])

    def is_valid_xy(self, coords):
        return self.is_valid_point(coords[1], coords[0])

    def size(self):
        return len(self.grid), len(self.grid[0])

    def number_of_values(self):
        row_size, column_size = self.size()
        return row_size * column_size

    def apply(self, function):
        for row in self.grid:
            for item in row:
                function(item)

    def export_to_text(self, filename="output.csv"):
        with open(filename, 'w') as f:
            f.write(self.__repr__())

    def __repr__(self):
        return "\n".join(["".join([str(item) for item in row]) for row in self.grid])