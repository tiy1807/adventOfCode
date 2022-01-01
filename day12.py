from utils import read_file

lines = read_file("day12input")

class Connection:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Cave:
    def __init__(self, name):
        self.name = name
        self.big_cave = (self.name == self.name.upper())
        self.connections = []

    def add_connection(self, second_cave):
        connection = Connection(self, second_cave)
        self.connections.append(connection)
        second_cave.connections.append(connection)

    def get_connected_caves(self):
        connected_caves = []
        for connection in self.connections:
            if self == connection.start:
                connected_caves.append(connection.end)
            else:
                connected_caves.append(connection.start)
        return connected_caves

    def __eq__(self, other):
        if type(other) == str:
            return self.name == other
        else:
            return self.name == other.name

    def __repr__(self):
        return self.name


class Caves:
    def __init__(self):
        self.caves = []

    def add_cave(self, name):
        if name not in self.caves:
            self.caves.append(Cave(name))

    def get_cave(self, name):
        return [cave for cave in self.caves if cave.name == name][0]


class Path:
    def __init__(self, initial_path=[]):
        self.path = initial_path
        self.revisited = False
        for cave in self.path:
            if self.count_visits(cave) > 1 and not cave.big_cave:
                self.revisited = True

    def last_position(self):
        return self.path[-1]

    def add_cave(self, cave):
        if self.last_position() != "end" and cave != "start":
            if not cave.big_cave:
                if self.revisited:
                    if not cave in self.path:
                        self.path.append(cave)
                else:
                    if cave in self.path:
                        self.revisited = True
                    self.path.append(cave)
            elif cave.big_cave:
                self.path.append(cave)

    def count_visits(self, cave_to_count):
        counter = 0
        for cave in self.path:
            if cave == cave_to_count:
                counter += 1
        return counter

    def __repr__(self):
        return str(self.path)

    def __eq__(self, other):
        if type(other) == list:
            return self.path == other
        else:
            return self.path == other.path

caves = Caves()
for line in lines:
    start, end = [t.strip() for t in line.split("-")]
    caves.add_cave(start)
    caves.add_cave(end)

    start_cave = caves.get_cave(start)
    end_cave = caves.get_cave(end)
    start_cave.add_connection(second_cave=end_cave)

START = caves.get_cave("start")
initial_path = Path([START])
paths = [initial_path]

new_number_of_paths = 1
number_of_paths = 0
while new_number_of_paths > number_of_paths:
    new_paths = [path for path in paths if path.last_position() == "end"]
    number_of_paths = len(new_paths)
    for path in paths:
        if path.last_position() != "end":
            print(f"Starting path {path} with connections {path.last_position().get_connected_caves()}")
            for connection in path.last_position().get_connected_caves():
                new_path = Path(path.path.copy())
                new_path.add_cave(connection)
                if new_path != path:
                    print(f"New path: {new_path}")
                    new_paths.append(new_path)
    paths = new_paths
    new_number_of_paths = len(paths)

print(len(paths))
print(paths)
