import timeit
import heapq
from dataclasses import dataclass, field
from typing import List, Tuple
from utils import *

Sudoku = List[List[int]]

test: Sudoku = [[8,0,0,0,0,0,0,0,0],
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

    Attributes
    ----------
    length : int
        The length of the domain of the node.
    domain : set
        The set of possible values for the given node.
    indices : tuple
        The row and column indices of the node in the Sudoku puzzle.
    """
    length: int
    domain: set = field(compare=False)
    indices: tuple = field(compare=False)


def domain(board: Sudoku, i: int, j: int) -> set:
    """
    Finds the domain of a cell in a Sudoku board.

    Parameters
    ----------
    board: Sudoku
        A 9x9 list representing the Sudoku puzzle.
    i: int
        The row index of the cell.
    j: int
        The column index of the cell.

    Returns
    -------
    set
        The set of possible values for the given cell.
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

    Parameters
    ----------
    board: Sudoku
        A 9x9 list representing the Sudoku puzzle.

    Returns
    -------
    tuple
        A tuple containing the row index, column index, and domain of the MRV cell.
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

    Parameters
    ----------
    board: Sudoku
        A 9x9 list representing the Sudoku puzzle.
    i: int
        The row index of the cell.
    j: int
        The column index of the cell.
    x: int
        The value to be checked for placement in the cell (i, j).

    Returns
    -------
    bool
        True if the value x can be placed in the cell (i, j), False otherwise.
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

    Parameters
    ----------
    board: Sudoku
        A 9x9 list representing the Sudoku puzzle.

    Returns
    -------
    bool
        True if the Sudoku board is completely filled, False otherwise.
    """
    return all(all(row) for row in board)


def backtrack(board: Sudoku):
    """
    Solves a Sudoku puzzle using backtracking and constraint satisfaction.

    Parameters
    ----------
    board: Sudoku
        A 9x9 list representing the Sudoku puzzle.

    Returns
    -------
    Sudoku or List
        A 9x9 list representing the solved Sudoku puzzle.
    """
    if solution(board):
        return board

    i, j, domain = mrv_indices(board)
    for x in domain:
        if validate(board, i, j, x):
            board[i][j] = x
            if backtrack(board):
                return board
            board[i][j] = 0

    return []


def print_sudoku(sudoku: Sudoku) -> None:
    """
    Prints a Sudoku puzzle in a visually appealing format.

    Parameters
    ----------
    sudoku: list
        A 9x9 list representing the Sudoku puzzle.
    """
    for i, row in enumerate(sudoku):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(cell, end=" ")
        print()


if __name__ == "__main__":

    start = timeit.default_timer()
    _backtrack = backtrack(test)
    stop = timeit.default_timer()

    print()
    print_sudoku(_backtrack)
    print()
    print(f"Execution time: {format_time(stop - start)}")