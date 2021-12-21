with open("day4input") as f:
    values = [value.strip() for value in f.readlines()]

drawn_numbers = [int(value) for value in values[0].split(",")]

boards = []
board = []
for value in values[2:]:
    if value == "":
        cols = []
        for col in range(len(row)):
            cols.append([row[col] for row in board])
        boards.append(board + cols)
        board = []
    else:
        row = [int(value) for value in value.split(' ') if len(value) > 0]
        board.append(row)


def is_board_finished(board):
    for line in board:
        if len(line) == 0:
            return True
    return False

board_set = [False for board in boards]
last_winner = -1
for number in drawn_numbers:
    for bid, board in enumerate(boards):
        for line in board:
            for nu in line:
                if number == nu:
                    line.remove(number)
        if is_board_finished(board):
            board_set[bid] = True
    print(sum(board_set))
    if last_winner >= 0:
        score = sum([sum(line) for line in boards[last_winner][:5]]) * number
        print(boards[last_winner])
        print(score)
    if sum(board_set) == len(board_set) - 1:
        last_winner = [board_id for board_id, board_won in enumerate(board_set) if not board_won][0]
        score = sum([sum(line) for line in boards[last_winner]])*number
        print(boards[last_winner])
        print(board_set)
        print(score)
