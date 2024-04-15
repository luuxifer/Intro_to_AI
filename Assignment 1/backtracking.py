import time
from random import randint, choice
from collections import defaultdict
from datetime import timedelta


def dfs_solver(board, GUI=None):
    begin_time = time.time()
    solved_board = backtracking(board, 0, 0, GUI)
    end_time = time.time()

    if GUI:
        GUI.btn_state(True)

    time_to_solve = end_time - begin_time
    print(time_to_solve)

    # Convert the elapsed time to a timedelta object
    elapsed_time_delta = timedelta(seconds=time_to_solve)
    # Format the elapsed time as a string in HH:MM:SS format
    elapsed_time_str = str(elapsed_time_delta)

    return solved_board, elapsed_time_str

def is_solve(board):
    """Checks if the board is completely filled with non zero numbers"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
    return True

def print_solution(board):
    for row in board:
        print(row)

def generate_new_board():
    """Randomly generates a seed for a board, then solves the board and randomly removes numbers"""
    new_board = [[0] * 9 for i in range(9)]
    possible_numbers = [1,2,3,4,5,6,7,8,9]
    row = randint(0,8)
    for col in range(9):
        value = choice(possible_numbers)
        possible_numbers.remove(value)
        new_board[row][col] = value

    new_board, _ = dfs_solver(new_board, None)

    for row in range(9):
        num_squares_to_delete = randint(7,9)
        for _ in range(num_squares_to_delete):
            col = randint(0,8)
            new_board[row][col] = 0

    return new_board

def is_valid(grid, r: int, c: int, k: int) -> bool:
    not_in_row = k not in grid[r]
    not_in_col = k not in [grid[i][c] for i in range(9)]
    r_box = r // 3 * 3
    c_box = c // 3 * 3
    not_in_box = k not in [grid[i][j] for i in range(r_box, r_box + 3) for j in range(c_box, c_box + 3)]
    return not_in_row and not_in_col and not_in_box

def backtracking(grid, r=0, c=0, GUI=None):
    if r == 9:
        return grid  # Return the solved board when all rows have been filled

    elif c == 9:
        return backtracking(grid, r + 1, 0, GUI)

    elif grid[r][c] != 0:
        return backtracking(grid, r, c + 1, GUI)

    else:
        for k in range(1, 10):
            if is_valid(grid, r, c, k):
                grid[r][c] = k
                if GUI:
                    GUI.update_single_grid_gui_square(r, c, "Green", k)
                solution = backtracking(grid, r, c + 1, GUI)
                if solution:
                    return solution  # Return the solution if found
                grid[r][c] = 0
                if GUI:
                    GUI.update_single_grid_gui_square(r, c, "Red", k)
                    GUI.update_single_grid_gui_square(r, c, "Red", 0)
        return None  # Return None if no solution is found


    