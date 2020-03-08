"""
# Sudoku solver
# Author: Jiawei Wang
# 3/7/2020

# About this version:
# 1. Allows user to choose between an easy puzzle and a hard Puzzle
# 2. Solves the puzzle using CSP + Backjumping
# 3. Prints out the answer with beautiful format
"""


from copy import deepcopy

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


# Validation check
def judge_unique(lis):
    n = []
    for i in lis:
        if i != 0:
            n.append(i)
    if len(n) != len(set(n)):
        return False
    return True


# Get the unit
def get_unit(x, y):
    return round((x - 1) / 3) + round((y - 1) / 3) * 3, x - round((x - 1) / 3) * 3 + 3 * y - 9 * round((y - 1) / 3)


class BackJumpingSudoku:
    column = []
    line = []
    unit = []
    all_conflict_set = []
    last_set = []

    def __init__(self):
        self.column = [[0 for i in range(9)] for j in range(9)]
        self.line = [[0 for i in range(9)] for j in range(9)]
        self.unit = [[0 for i in range(9)] for j in range(9)]
        self.all_conflict_set = [[[] for i in range(9)] for j in range(9)]

    def init_state(self, state):
        for i in range(9):
            for j in range(9):
                self.set_value(i, j, state[i][j])
        return True

    def set_value(self, x, y, value):
        self.column[x][y] = value
        self.line[y][x] = value
        unit_x, unit_y = get_unit(x, y)
        self.unit[unit_x][unit_y] = value

        for i in range(9):
            for j in range(9):
                unit_i, unit_j = get_unit(i, j)
                if (i == x) | (j == y) | (unit_i == unit_x):
                    self.all_conflict_set[i][j].append([value, [x, y]])
        return True

    def judge_constraint(self):
        for type in [self.column, self.line, self.unit]:
            for i in type:
                if not judge_unique(i):
                    return False
        return True

    def judge_one(self, x, y):
        unit_x, unit_y = get_unit(x, y)
        for i in [self.column[x], self.line[y], self.unit[unit_x]]:
            if not judge_unique(i):
                return False
        return True

    def judge_one_conflict(self, x, y):
        choice = []
        for i in self.all_conflict_set[x][y]:
            if i[0] != 0:
                choice.append(i[0])
            if len(set(choice)) == 9:
                return i[1]
        else:
            return None

    def judge_done(self):
        for i in self.column:
            for j in i:
                if j == 0:
                    return False
        return True

    def print_state(self):
        for i in self.column:
            print(i)
        return True


class BackJumpingCSP:
    queue = []
    step = 0
    answer = None
    finished = None
    conflict = None
    last = None

    def __init__(self, s):
        self.queue = [[s, [0, 0], 0]]
        self.finished = False

    def extend(self):
        i = self.queue.pop()
        self.last = i
        if i[0].judge_done():
            self.answer = i[0]
            self.finished = True

        for y in range(9):
            for x in range(9):
                if i[0].column[x][y] == 0:
                    if len(i[0].all_conflict_set[x][y]) >= 9:
                        if i[0].judge_one_conflict(x, y) is not None:
                            self.conflict = i[0].judge_one_conflict(x, y)
                            return False
                    for v in range(1, 10):
                        s = deepcopy(i[0])
                        s.set_value(x, y, v)
                        if s.judge_one(x, y):
                            self.queue.append([s, [x, y], v])
                    return True
        return True

    def sort(self):
        for i in range(len(self.queue)):
            for j in range(i, len(self.queue)):
                if self.queue[i][1][1] > self.queue[j][1][1]:
                    temp = self.queue[i]
                    self.queue[i] = self.queue[j]
                    self.queue[j] = temp
                elif self.queue[i][1][1] == self.queue[j][1][1]:
                    if self.queue[i][1][0] > self.queue[j][1][0]:
                        temp = self.queue[i]
                        self.queue[i] = self.queue[j]
                        self.queue[j] = temp
        return True

    def backjumping(self):
        queue = []
        for i in self.queue:
            if i[1][1] < self.conflict[1]:
                queue.append(i)
            elif (i[1][1] == self.conflict[1]) & (i[1][0] <= self.conflict[0]):
                queue.append(i)
        self.queue = queue
        self.conflict = None
        return True

    def run(self):
        while not self.finished:
            # print(self.queue)
            extend = self.extend()
            if not extend:
                self.backjumping()


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
s = BackJumpingSudoku()
s.init_state(Board)
p = BackJumpingCSP(s)
p.run()
if solve_sudoku(Board):
    print("Puzzle has been solved:")
    print_board(Board)
else:
    print("No Solution found")
