# Sudoku solution finder using backtracking algorithm

table = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def backtrack_solve(tb):
    find = find_empty(tb)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if check(tb, i, (row, col)):
            tb[row][col] = i

            if backtrack_solve(tb):
                return True

            tb[row][col] = 0

    return False


def check(tb, num, pos):
    # Check row
    for i in range(len(tb[0])):
        if tb[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(tb)):
        if tb[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if tb[i][j] == num and (i, j) != pos:
                return False

    return True


def print_table(tb):
    for i in range(len(tb)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(tb[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(tb[i][j])
            else:
                print(str(tb[i][j]) + " ", end="")


def find_empty(tb):
    for i in range(len(tb)):
        for j in range(len(tb[0])):
            if tb[i][j] == 0:
                return (i, j)

    return None


print_table(table)
backtrack_solve(table)
print("\n= = = = = = = = = = = = \n")
print_table(table)
