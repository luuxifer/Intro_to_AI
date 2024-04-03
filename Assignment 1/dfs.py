import time
from random import randint, choice



def dfs_solver(board, GUI=None):
    begin_time = time.time()
    solved_board = dfs_solve(board, GUI)
    end_time = time.time()

    if GUI:
        GUI.btn_state(True)

    time_to_solve = end_time - begin_time
    return solved_board

# def dfs_solve(board, GUI):
#     if is_solve(board):
#         return board
#     f = open("output.txt", "x")
#     row, col = get_first_unfilled_square(board)
#     possible_solution = get_valid_set(board, row, col)
#     if possible_solution:
#         for number in possible_solution:
#             if GUI:
#                 GUI.update_single_grid_gui_square(row, col, "Green", number)
#                 # time.sleep(0.2)
#                 f.write(f"Add {number}\n")
#             board[row][col] = number
#             solved_board = dfs_solve(board, GUI)
#             if is_solve(solved_board):
#                 return solved_board
    
#     board[row][col] = 0
#     if(GUI):
#         GUI.update_single_grid_gui_square(row, col, "Red")
#         # time.sleep(0.2)
#         GUI.update_single_grid_gui_square(row, col, "Red", 0)
#         # time.sleep(0.2)

#     return board
STEP = 0
def dfs_solve(board, GUI):
    global STEP
    if is_solve(board):
        return board
    with open(r"D:\HCMUT\232\IntroductionToAI\MY_SUDOKU\output.txt", "a") as f:  # Open file in append mode
        row, col = get_first_unfilled_square(board)
        possible_solution = get_valid_set(board, row, col)
        if possible_solution:
            for number in possible_solution:
                if GUI:
                    GUI.update_single_grid_gui_square(row, col, "Green", number)
                    
                board[row][col] = number
                
                solved_board = dfs_solve(board, GUI)
                STEP += 1
                f.write(f"At step {STEP}: Add {number} at (row, col): {row, col}\n")# Write output to file
                
                if is_solve(solved_board):
                    return solved_board
        # STEP -= 1
        board[row][col] = 0
        if GUI:
            GUI.update_single_grid_gui_square(row, col, "Red")
            # f.write(f"At step {STEP}: Add {number} at (row, col): {row, col} but error\n")# Write output to file
            # STEP += 1
            GUI.update_single_grid_gui_square(row, col, "Red", 0)
            # f.write(f"At step {STEP}: Remove {number} at (row, col): {row, col}\n")# Write output to file
            # STEP += 1

    return board


def get_valid_set(board, row, col):
    return get_valid_numbers_in_row(board, row, col) & get_valid_numbers_in_column(board, row, col) & get_valid_numbers_in_subsquare(board, row, col)

def get_valid_numbers_in_row(board, row, col):
    valid_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for idx, val in enumerate(board[row]):
        if idx == col:
            continue
        else:
            if val in valid_numbers:
                valid_numbers.remove(val)
    return valid_numbers

def get_valid_numbers_in_column(board, row, col):
    valid_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for r_idx in range(9):
        if r_idx == row:
            continue
        else:
            if board[r_idx][col] in valid_numbers:
                valid_numbers.remove(board[r_idx][col])
    return valid_numbers

def get_valid_numbers_in_subsquare(board, row, col):
    valid_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    start_row = row // 3 * 3
    start_col = col // 3 * 3
    for r_idx in range(3):
        for c_idx in range(3):
            if start_row + r_idx == row and start_col + c_idx == col:
                continue
            else:
                if board[start_row + r_idx][start_col + c_idx] in valid_numbers:
                    valid_numbers.remove(board[start_row + r_idx][start_col + c_idx])
    return valid_numbers

def is_solve(board):
    """Checks if the board is completely filled with non zero numbers"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
    return True

def get_first_unfilled_square(board):
    for row in range(9):
        for col in range(9):
            if(board[row][col] == 0):
                return row, col

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