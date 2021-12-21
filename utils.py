def read_file(filename):
    with open(filename) as f:
        lines = [value.strip() for value in f.readlines()]
    return lines
