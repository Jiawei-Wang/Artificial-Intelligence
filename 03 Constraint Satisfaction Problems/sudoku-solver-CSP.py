"""
# Sudoku solver
# Author: Jiawei Wang
# 3/7/2020

# About this version:
# 1. Allows user to choose between an easy puzzle and a hard Puzzle
# 2. Solves the puzzle using CSP (Constraint satisfaction problem) Method
# 3. Prints out the answer with beautiful format
"""

# Initialize the board
easy_puzzle = [
    [6, 0, 8, 7, 0, 2, 1, 0, 0],
    [4, 0, 0, 0, 1, 0, 0, 0, 2],
    [0, 2, 5, 4, 0, 0, 0, 0, 0],
    [7, 0, 1, 0, 8, 0, 4, 0, 5],
    [0, 8, 0, 0, 0, 0, 0, 7, 0],
    [5, 0, 9, 0, 6, 0, 3, 0, 1],
    [0, 0, 0, 0, 0, 6, 7, 5, 0],
    [2, 0, 0, 0, 9, 0, 0, 0, 8],
    [0, 0, 6, 8, 0, 5, 2, 0, 3]
]

hard_puzzle = [
    [0, 7, 0, 0, 4, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 6, 1, 0],
    [3, 9, 0, 0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 4, 0, 0, 9],
    [0, 0, 3, 0, 0, 0, 7, 0, 0],
    [5, 0, 0, 1, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 7, 6],
    [0, 5, 4, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 1, 0, 0, 5, 0]
]


# Print the initial board
def print_board(Board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(Board[i][j])
            else:
                print(str(Board[i][j]) + " ", end="")


# Find cells without value
def find_empty_cell(Board):
    for row in range(9):
        for col in range(9):
            if Board[row][col] == 0:
                return row, col
    return None, None


# Find possible options for cells
def get_valid_options(Board, row, col):
    invalid = set([])

    for i in range(9):
        if Board[row][i] != 0:
            invalid.update([Board[row][i]])
        if Board[i][col] != 0:
            invalid.update([Board[i][col]])

    box_row = row - (row % 3)
    box_col = col - (col % 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if Board[i][j] != 0:
                invalid.update([Board[i][j]])

    return set(range(1, 10)) - invalid


# Solve the board
def solve_sudoku(Board):
    row, col = find_empty_cell(Board)

    if row is None and col is None:
        return True

    valid_options = get_valid_options(Board, row, col)
    for i in valid_options:
        Board[row][col] = i
        if solve_sudoku(Board):
            return True
        Board[row][col] = 0

    return False


# Let's solve it
print("Please choose the puzzle you want to solve.")
print("Press 1 for easy and 2 for hard:")
ans = input()
if ans == "1":
    Board = easy_puzzle
else:
    Board = hard_puzzle
print("The initial board is:")
print_board(Board)
print("---------------------------------------")
if solve_sudoku(Board):
    print("Puzzle has been solved:")
    print_board(Board)
else:
    print("No Solution found")
