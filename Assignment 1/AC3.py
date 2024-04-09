import time
from collections import deque, defaultdict

def AC3_solver_i(board, GUI=None):
    begin_time = time.time()
    solver = AC3SudokuSolver()
    solver.solveSudoku(board, GUI)
    end_time = time.time()

    if GUI:
        GUI.btn_state(True)

    time_to_solve = end_time - begin_time
    print (time_to_solve)
    return board

class CSP(object):
    def __init__(self, variables = [], adjList = {}, domains = {}) -> None:
        self.variables = variables
        self.adjList = adjList
        self.domains = domains

    def restore_domains(self, removals):
        for i in removals:
            self.domains[i] |= removals[i]

class SudokuCSP(CSP):
    def conflicts(self, r1, c1, val1, r2, c2, val2):
        k1 = r1 // 3 * 3 + c1 // 3
        k2 = r2 // 3 * 3 + c2 // 3
        return val1 == val2 and ( r1 == r2 or c1 == c2 or k1 == k2 )
    
class SudokuSolver(object):
    def __addEdge__(self, r_idx, c_idx, adjList):
        idx = r_idx // 3 * 3 + c_idx // 3
        for num in range(9):
            if num != r_idx:
                adjList[(r_idx, c_idx)].add((num, c_idx))
            if num != c_idx:
                adjList[(r_idx, c_idx)].add((r_idx, num))

            row = num // 3 + idx // 3 * 3
            col = num % 3 + idx % 3 * 3
            if row != r_idx or col != c_idx:
                adjList[(r_idx, c_idx)].add((row, col))

    def buildCspProblem(self, grid):
        adjList = defaultdict(set)
        # Graph constraints 
        for i in range(9):
            for j in range(9):
                self.__addEdge__(i, j, adjList)

        # Domains
        variables = []
        assigned = []
        domains = {}

        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    domains[(i, j)] = set(range(9))
                    variables.append((i, j))
                else:
                    domains[(i, j)] = set([int(grid[i][j]) - 1])
                    assigned.append((i, j))
        
        return SudokuCSP(variables, adjList, domains), assigned
    
def AC3(csp, queue = None, removals = defaultdict(set)):
    # Return False if there is no consistent assignment
    if queue is None:
        queue = [(Xt, X) for Xt in csp.adjList for X in csp.adjList[Xt]]
    # Queue of arcs of our concern
    while queue:
        # Xt --> Xh Delete from domain of Xt
        (Xt, Xh) = queue.pop()
        if remove_inconsistent_values(csp, Xt, Xh, removals):
            if not csp.domains[Xt]:
                return False
            # NOTE: Next two lines only for binary "!=" constraint
            elif len(csp.domains[Xt]) > 1:
                continue
            for X in csp.adjList[Xt]:
                if X != Xt:
                    queue.append((X, Xt))
    return True

def remove_inconsistent_values(csp: SudokuCSP, Xt, Xh, removals):
    revised = False

    for x in csp.domains[Xt].copy():
        for y in csp.domains[Xh]:
            if not csp.conflicts(*Xt, x, *Xh, y):
                break
            else:
                csp.domains[Xt].remove(x)
                removals[Xt].add(x)
                revised = True
    return revised

def makeArcQue(csp: SudokuCSP, Xs):
    return [(Xt, Xh) for Xh in Xs for Xt in csp.adjList[Xh]]


# Backtracking search with AC3 Maintaining Arc Consistency
class AC3SudokuSolver(SudokuSolver):
    def solveSudoku(self, board, GUI):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        # Build CSP problem
        csp, assigned = self.buildCspProblem(board)
        # Enforce AC3 on initial assignments
        AC3(csp, makeArcQue(csp, assigned))
        # If there's still uncertain choices
        uncertain = []
        for i in range(9):
            for j in range(9):
                if len(csp.domains[(i, j)]) > 1:
                    uncertain.append((i, j))
        # Search with backtracking
        self.backtrack(csp, uncertain, GUI)
        # Fill answer back to input table
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    assert len(csp.domains[(i, j)]) == 1
                    board[i][j] = str( csp.domains[(i, j)].pop() + 1 )
    
    def backtrack(self, csp, uncertain, GUI):
        if not uncertain:
            return True
        X = uncertain.pop()
        removals = defaultdict(set)
        for x in csp.domains[X]:
            domainX = csp.domains[X]
            csp.domains[X] = set([x])
            if GUI:
                GUI.update_single_grid_gui_square(X[0], X[1], "Green", x + 1)
                # GUI.window.update()
                # time.sleep(0.1) 
                # time.sleep(1)  # Adjust delay as neede

            if AC3(csp, makeArcQue(csp, [X]), removals):
                retval = self.backtrack(csp, uncertain, GUI)
                if retval:
                    return True
            if GUI:
                GUI.update_single_grid_gui_square(X[0], X[1], "Red")
                GUI.update_single_grid_gui_square(X[0], X[1], "Red", 0)
                # GUI.window.update()
                # time.sleep(0.1) 
                # time.sleep(1)  # Adjust delay as neede
            csp.restore_domains(removals)
            csp.domains[X] = domainX
        uncertain.append(X)
        return False
    

# def AC3_solver(board, GUI=None):
#     begin_time = time.time()
#     solver = AC3SudokuSolver()
#     solver.solveSudoku(board)
#     end_time = time.time()

#     if GUI:
#         GUI.btn_state(True)

#     time_to_solve = end_time - begin_time
#     print (time_to_solve)
#     return board

