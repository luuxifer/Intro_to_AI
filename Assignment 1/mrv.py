import time
import heapq
from dataclasses import dataclass, field
from typing import List, Tuple
from utils import *
import tracemalloc

Sudoku = List[List[int]]


board = [[8,0,0,0,0,0,0,0,0],
          [0,0,3,6,0,0,0,0,0],
          [0,7,0,0,9,0,2,0,0],
          [0,5,0,0,0,7,0,0,0],
          [0,0,0,0,4,5,7,0,0],
          [0,0,0,1,0,0,0,3,0],
          [0,0,1,0,0,0,0,6,8],
          [0,0,8,5,0,0,0,1,0],
          [0,9,0,0,0,0,4,0,0]]
@dataclass(order=True)
class Node:
    """
    A class to represent a node in a Sudoku puzzle.
    """
    length: int
    domain: set = field(compare=False)
    indices: tuple = field(compare=False)


def domain(board: Sudoku, i: int, j: int) -> set:
    """
    Finds the domain of a cell in a Sudoku board.
    """
    full_domain = set(range(1, 10))

    row = set(board[i])

    col = {board[n][j] for n in range(9)}

    row_start, col_start = (i // 3) * 3, (j // 3) * 3
    grid = set()
    for a in range(3):
        for b in range(3):
            grid.add(board[row_start + a][col_start + b])

    return full_domain.difference(row | col | grid)


def mrv_indices(board: Sudoku) -> tuple:
    """
    Finds the minimal remaining values (MRV).
    """
    heap = list()
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                node_domain = domain(board, i, j)
                heapq.heappush(heap, Node(
                    len(node_domain), node_domain, (i, j)))
    node: Node = heapq.heappop(heap)
    return (node.indices[0], node.indices[1], node.domain)


def validate(board: Sudoku, i: int, j: int, x: int) -> bool:
    """
    Checks if a value x can be placed in the cell (i, j) of a Sudoku board without violating any constraints.
    """
    for n in range(9):
        if (board[i][n] == x) or (board[n][j] == x):
            return False

    row = (i // 3) * 3
    column = (j // 3) * 3
    for r in range(row, row+3):
        for c in range(column, column+3):
            if board[r][c] == x:
                return False
    return True


def solution(board: Sudoku) -> bool:
    """
    Checks if a Sudoku board is completely filled.
    """
    return all(all(row) for row in board)


def backtrack(board: Sudoku, GUI=None):
    """
    Solves a Sudoku puzzle using backtracking and constraint satisfaction.
    """
    if solution(board):
        return board

    i, j, domain = mrv_indices(board)
    for x in domain:
        if validate(board, i, j, x):
            board[i][j] = x
            if GUI:
                GUI.update_single_grid_gui_square(i, j, "Green", x)
            if backtrack(board, GUI):
                return board
            board[i][j] = 0
            if GUI:
                GUI.update_single_grid_gui_square(i, j, "Red", x)
                GUI.update_single_grid_gui_square(i, j, "Red", 0)

    return []


def print_sudoku(sudoku: Sudoku) -> None:
    """
    Prints a Sudoku puzzle in a visually appealing format.
    """
    for i, row in enumerate(sudoku):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(cell, end=" ")
        print()

def mrv_solver(board, GUI=None):
    memory_list = []
    begin_time = time.time()
    tracemalloc.start()
    solved_board = backtrack(board, GUI)
    memory_list.append(tracemalloc.get_traced_memory()[1])
    tracemalloc.stop()
    end_time = time.time()

    if GUI:
        GUI.btn_state(True)
    elapsed_time_seconds = end_time - begin_time
    return solved_board, elapsed_time_seconds, memory_list