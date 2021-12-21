from utils import read_file

lines = read_file("day5input")
part2 = True

coords = []
for line in lines:
    start_coord = line.split(" ")[0].split(",")
    end_coord = line.split(" ")[2].split(",")
    coords.append({"x1": int(start_coord[0]), "y1": int(start_coord[1]), "x2": int(end_coord[0]), "y2": int(end_coord[1])})

if not part2:
    orth_lines = [coord for coord in coords if (coord["x1"] == coord["x2"] or coord["y1"] == coord["y2"])]
else:
    orth_lines = coords

all_coords = []
for coord in orth_lines:
    if coord["x1"] == coord["x2"]:
        for y in range(min(coord["y1"],coord["y2"]), max(coord["y1"],coord["y2"]) + 1):
            all_coords.append({"x": coord["x1"], "y": y})
    elif coord["y1"] == coord["y2"]:
        for x in range(min(coord["x1"],coord["x2"]), max(coord["x1"],coord["x2"]) + 1):
            all_coords.append({"x": x, "y": coord["y1"]})
    elif part2:
        print(coord)
        if coord["x1"] > coord["x2"]:
            x_range = range(coord["x1"], coord["x2"] - 1, -1)
        else:
            x_range = range(coord["x1"], coord["x2"] + 1, 1)
        if coord["y1"] > coord["y2"]:
            y_range = range(coord["y1"], coord["y2"] - 1, -1)
        else:
            y_range = range(coord["y1"], coord["y2"] + 1, 1)
        for x, y in zip(x_range, y_range):
            all_coords.append({"x": x, "y": y})

print("Calculated coords")
#duplicates = set()
#total_number_of_coords = len(all_coords)
#for id, coord in enumerate(all_coords):
#    if coord in all_coords[:id] + all_coords[id+1:]:
#        print(f'{id} out of {total_number_of_coords}')
#        duplicates.add((coord["x"], coord["y"]))

board = {}
for coord in all_coords:
    board[f'{coord["x"]},{coord["y"]}'] = board.get(f'{coord["x"]},{coord["y"]}', 0) + 1

print(board)
duplicates = sum([1 for value in board.values() if value > 1])
print(duplicates)