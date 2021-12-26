from utils import read_file

lines = read_file("day9input")

low_points = []
for row, heights in enumerate(lines):
    for column, height in enumerate(heights):
        neighbouring_heights = []
        if column > 0:
            neighbouring_heights.append(heights[column-1])
        if column < len(heights) - 1:
            neighbouring_heights.append(heights[column + 1])
        if row > 0:
            neighbouring_heights.append(lines[row-1][column])
        if row < len(lines) - 1:
            neighbouring_heights.append(lines[row+1][column])
        if int(height) < min([int(n_height) for n_height in neighbouring_heights]):
            low_points.append((row, column))

basins = []
for low_point in low_points:
    print(low_point)
    basin = [low_point]
    changed = True
    while changed:
        changed = False
        for point in basin:
            for proposed_new_point in [(point[0], point[1] - 1), (point[0], point[1] + 1), (point[0] - 1, point[1]), (point[0] + 1, point[1])]:
                print("proposed: " + str(proposed_new_point))
                if proposed_new_point[0] >= 0 and proposed_new_point[1] >= 0 and proposed_new_point[0] < len(lines) and proposed_new_point[1] < len(lines[0]):
                    if int(lines[proposed_new_point[0]][proposed_new_point[1]]) >= int(lines[point[0]][point[1]]) and int(lines[proposed_new_point[0]][proposed_new_point[1]]) != 9:
                        if proposed_new_point not in basin:
                            basin.append((proposed_new_point[0], proposed_new_point[1]))
                            changed = True
                            print("Added to basin")
                        else:
                            print("Already in basin")
                    else:
                        print("Lower than point")
                else:
                    print("Not in range")

    print(basin)
    basins.append(basin)
size = [len(basin) for basin in basins]
size.sort(reverse=True)
print(size)
print(size[0]*size[1]*size[2])
