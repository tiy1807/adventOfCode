from utils import read_file

lines = read_file("day13input")

coordinates = [line.strip() for line in lines if "," in line]
reflections = [line.strip() for line in lines if "=" in line]

xyCoords = []
for coord in coordinates:
    x, y = coord.split(",")
    xyCoords.append({"x": int(x), "y": int(y)})

for reflection in reflections:
    ref_direction = reflection.split("=")[0][-1]
    ref_location = int(reflection.split("=")[-1].strip())
    print(f"Reflecting in the line {ref_direction}={ref_location}")
    reflected_coords = []
    for coord in xyCoords:
        print(coord)
        ref_coord = {}
        if ref_direction == "x":
            ref_coord["y"] = coord["y"]
            distance_from_reflection = ref_location - coord["x"]
            if distance_from_reflection < 0:
                ref_coord["x"] = ref_location + distance_from_reflection
            else:
                ref_coord["x"] = coord["x"]
        elif ref_direction == "y":
            ref_coord["x"] = coord["x"]
            distance_from_reflection = ref_location - coord["y"]
            if distance_from_reflection < 0:
                ref_coord["y"] = ref_location + distance_from_reflection
            else:
                ref_coord["y"] = coord["y"]
        print(f"Reflected to: {ref_coord}")
        if ref_coord not in reflected_coords:
            reflected_coords.append(ref_coord)
    xyCoords = reflected_coords
    print(len(reflected_coords))

max_x = max([coord["x"] for coord in xyCoords])
max_y = max([coord["y"] for coord in xyCoords])

for y in range(max_y+1):
    for x in range(max_x + 1):
        if {"x": x, "y": y} in xyCoords:
            print("#", end='')
        else:
            print(".", end='')
    print('')