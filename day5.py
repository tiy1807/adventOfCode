from utils import read_file

lines = read_file("day5input")

coords = []
for line in lines:
    start_coord = line.split(" ")[0].split(",")
    end_coord = line.split(" ")[2].split(",")
    coords.append({"x1": start_coord[0], "y1": start_coord[1], "x2": end_coord[0], "y2": end_coord[1]})

orth_lines = [coord for coord in coords if (coord["x1"] == coord["x2"] or coord["y1"] == coord["y2"])]
print(orth_lines)

all_coords = []
for coord in orth_lines:
    if coord["x1"] == coord["x2"]:
        for y in range(coord["y1"], coord["y2"]):
            all_coords.append({"x": coord["x1"], "y": y})