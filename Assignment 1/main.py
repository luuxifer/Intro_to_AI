import tkinter as tk
import copy
from dfs import *
from tkinter import ttk 
import threading
from ac3 import AC3SudokuSolver, AC3_solver
from mrv import mrv_solver
import tkinter.messagebox as messagebox
from utils import * 

class MainApplication():
    def __init__(self, window):
        self.window = window
        self.grid_boxes = []
        self.btn = []
        self.feedback_solution = None
        self.setup_GUI()
        self.grid_value = hard
        self.set_grid_GUI_from_value(self.grid_value)
        # self.get_grid_value_from_GUI()
        # self.reset_grid_colour()

        # Define a class-level variable to store the currently selected algorithm
        self.selected_algorithm = None
        
    def setup_GUI(self):
        self.window.title("Sudoku")
        # self.window.configure(bg="#BEF6F2")
        self.create_window()
        self.create_grid()
        self.create_btn()
        self.create_checklist()
        self.create_table()
        self.feedback_solution = tk.Label(self.window, text="")
        self.feedback_solution.grid(column=3, row=12, columnspan=2)

    def create_window(self):
        self.window.geometry('1400x600')
        for col in range(30):
            self.window.columnconfigure(col, weight=1, minsize=20)
        self.window.rowconfigure(10, minsize=20)
    
    def create_btn(self):
            style = ttk.Style()
            style.configure('Custom.TButton', foreground='black', background='#4CAF50', font=('Ubuntu', 12))

            rst_btn = ttk.Button(self.window, text="Reset board", command=self.set_grid_GUI_from_value, style='Custom.TButton')
            rst_btn.grid(column=1, row=11, columnspan=2)

            new_btn = ttk.Button(self.window, text="New board", command=self.new_board, style='Custom.TButton')
            new_btn.grid(column=3, row=11, columnspan=2)

            solve_btn = ttk.Button(self.window, text="Solve board", command=self.solve_board, style='Custom.TButton')
            solve_btn.grid(column=5, row=11, columnspan=2)

            check_btn = ttk.Button(self.window, text="Check board", command=self.check_board, style='Custom.TButton')
            check_btn.grid(column=7, row=11, columnspan=2)

            self.btn = [rst_btn, new_btn, solve_btn, check_btn]

    def show_warning(self, message):
        messagebox.showwarning("Warning", message)

    def create_checklist(self):
        option1_var = tk.BooleanVar()
        option2_var = tk.BooleanVar()
        option3_var = tk.BooleanVar()

        # Header label
        header_label = tk.Label(self.window, text="Choose algorithm", font=('Ubuntu', 14))
        header_label.grid(row=1, column=11, columnspan=9)  # Adjust row and column as needed

        # Create the first checkbox
        algo_1 = tk.Checkbutton(self.window, text="DFS", variable=option1_var, command=lambda: self.update_selected_algorithm("DFS"), font=('Ubuntu', 12), justify='center')
        algo_1.grid(row=2, column=11)  # Adjust row and column as needed
        
        # Create the second checkbox
        algo_2 = tk.Checkbutton(self.window, text="AC3", variable=option2_var, command=lambda: self.update_selected_algorithm("AC3"), font=('Ubuntu', 12), justify='center')
        algo_2.grid(row=2, column=15)  # Adjust row and column as needed

        # Create the third checkbox
        algo_3 = tk.Checkbutton(self.window, text="MRV", variable=option3_var, command=lambda: self.update_selected_algorithm("MRV"), font=('Ubuntu', 12), justify='center')
        algo_3.grid(row=2, column=19)  # Adjust row and column as needed

        # Assign the BooleanVars to instance variables for later access
        self.option1_var = option1_var
        self.option2_var = option2_var
        self.option3_var = option3_var

    def create_table(self):
        # Update the "Strategy" label font settings
        label = tk.Label(self.window, text="STRATEGY", font=('Ubuntu', 14, 'bold'))  # Increased size and bold
        label.grid(row=6, column=11)

        label = tk.Label(self.window, text="DFS", font=('Ubuntu'))  # Increased size and bold
        label.grid(row=7, column=11)

        label = tk.Label(self.window, text="AC3", font=('Ubuntu'))  # Increased size and bold
        label.grid(row=8, column=11)

        label = tk.Label(self.window, text="MRV", font=('Ubuntu'))  # Increased size and bold
        label.grid(row=9, column=11)

        label = tk.Label(self.window, text="ELAPSED TIME", font=('Ubuntu', 14, 'bold'))  # Increased size and bold
        label.grid(row=6, column=15)

        self.elapsed_time_label_dfs = tk.Label(self.window, text="0", font=('Ubuntu', 12))
        self.elapsed_time_label_dfs.grid(row=7, column=15)

        self.elapsed_time_label_ac3 = tk.Label(self.window, text="0", font=('Ubuntu', 12))
        self.elapsed_time_label_ac3.grid(row=8, column=15)

        self.elapsed_time_label_mrv = tk.Label(self.window, text="0", font=('Ubuntu', 12))
        self.elapsed_time_label_mrv.grid(row=9, column=15)

        label = tk.Label(self.window, text="MEMORY", font=('Ubuntu', 14, 'bold'))  # Increased size and bold
        label.grid(row=6, column=19)

        self.mem_dfs = tk.Label(self.window, text="0", font=('Ubuntu', 12))
        self.mem_dfs.grid(row=7, column=19)

        self.mem_ac3 = tk.Label(self.window, text="0", font=('Ubuntu', 12))
        self.mem_ac3.grid(row=8, column=19)

        self.mem_mrv = tk.Label(self.window, text="0", font=('Ubuntu', 12))
        self.mem_mrv.grid(row=9, column=19)


        
    def create_grid(self):
        for row in range(9):
            self.grid_boxes.append([])
            for col in range(9):
                input_box = Grid(self.window, width=3, font=('Ubuntu', 28), justify='center')
                input_box.configure(highlightbackground="red", highlightcolor="red")
                pady = (10, 0) if row % 3 == 0 else 0
                padx = (10, 0) if col % 3 == 0 else 0
                input_box.grid(column=col + 1, row=row + 1, padx=padx, pady=pady)
                self.grid_boxes[row].append(input_box)
    
    def set_grid_GUI_from_value(self, grid = None):
        if grid is None:
            grid = self.grid_value
        
        for r_idx, _ in enumerate(self.grid_boxes):
            for c_idx, c_val in enumerate(self.grid_boxes[r_idx]):
                value = grid[r_idx][c_idx]
                if(value != 0):
                    c_val.set(value)
                    c_val.config(state='readonly')
                else:
                    c_val.set('')
                    c_val.config(state='normal')

    def get_grid_value_from_GUI(self):
        board = []
        for r_idx, row in enumerate(self.grid_boxes):
            board.append([])
            for col in row:
                value = col.get()
                board[r_idx].append(int(value)) if value != "" else board[r_idx].append(0)
        return board

    def new_board(self):
        """Generates a new list of values to fill the grid squares and sets the GUI to this new list"""
        self.grid_value = generate_new_board()
        self.set_grid_GUI_from_value(self.grid_value)
        # self.reset_grid_colour()

    def check_board(self):
        board = self.get_grid_value_from_GUI()
        if is_solve(board):
            self.feedback_solution.config(text='You Win!!!', fg='Green')
        else:
            self.feedback_solution.config(text='Incorrect Solution', fg='Red')

    # def solve_board(self):
    #     self.btn_state(False)
    #     self.set_grid_GUI_from_value()
    #     board = copy.deepcopy(self.grid_value)
    #     solve_thread = threading.Thread(target=dfs_solver, args=(board, self), daemon=True)
    #     solve_thread.start()

    def update_selected_algorithm(self, algorithm):
        self.selected_algorithm = algorithm
        
    def solve_board(self):
        # Kiểm tra xem có giải thuật nào được chọn không
        if not self.selected_algorithm:
            self.show_warning("Please select an algorithm!")
            return

        # Kiểm tra xem có nhiều hơn một giải thuật được chọn không
        selected_algorithms = [self.option1_var.get(), self.option2_var.get(), self.option3_var.get()]
        if sum(selected_algorithms) != 1:
            self.show_warning("Please select exactly one algorithm!")
            return

        self.btn_state(False)
        self.set_grid_GUI_from_value()
        board = copy.deepcopy(self.grid_value)

        if self.selected_algorithm == "DFS":
            # Define a function to solve the Sudoku puzzle using DFS in a separate thread
            def solve_sudoku_thread():
                solved_board, elapsed_time_str, mem = dfs_solver(board, self)
                self.set_grid_GUI_from_value(solved_board)
                self.elapsed_time_label_dfs.config(text=f"{format_time(elapsed_time_str)}")
                self.mem_dfs.config(text=f"{mem}")
                self.btn_state(True)  # Enable buttons after solving

            # Create and start the thread
            solve_thread = threading.Thread(target=solve_sudoku_thread, daemon=True)
            solve_thread.start()

        elif self.selected_algorithm == "AC3":
            # Define a function to solve the Sudoku puzzle using AC3 in a separate thread
            def solve_sudoku_thread():
                solved_board, elapsed_time_str, mem = AC3_solver(board, self)
                self.set_grid_GUI_from_value(solved_board)
                self.elapsed_time_label_ac3.config(text=f"{format_time(elapsed_time_str)}")
                self.mem_ac3.config(text=f"{mem}")
                self.btn_state(True)  # Enable buttons after solving
            
            # Create and start the thread
            solve_thread = threading.Thread(target=solve_sudoku_thread, daemon=True)
            solve_thread.start()
            self.selected_algorithm = None  # Reset selected algorithm

        elif self.selected_algorithm == "MRV":
            # Define a function to solve the Sudoku puzzle using MRV in a separate thread
            # Replace this with your MRV solver function
            def solve_sudoku_thread():
                solved_board, elapsed_time_str, mem = mrv_solver(board, self)
                self.set_grid_GUI_from_value(solved_board)
                self.elapsed_time_label_mrv.config(text=f"{format_time(elapsed_time_str)}")
                self.mem_mrv.config(text=f"{mem}")
                self.btn_state(True)  # Enable buttons after solving

            # Create and start the thread
            solve_thread = threading.Thread(target=solve_sudoku_thread, daemon=True)
            solve_thread.start()
            self.selected_algorithm = None  # Reset selected algorithm

    # def solve_board(self):
    #     self.btn_state(False)
    #     self.set_grid_GUI_from_value()
    #     board = copy.deepcopy(self.grid_value)
        
    #     # Define a function to solve the Sudoku puzzle in a separate thread
    #     def solve_sudoku_thread():
    #         solver = AC3SudokuSolver()
    #         solver.solveSudoku(board)
    #         self.set_grid_GUI_from_value(board)
    #         self.btn_state(True)  # Enable buttons after solving
        
    #     # Create and start the thread
    #     solve_thread = threading.Thread(target=solve_sudoku_thread, daemon=True)
    #     solve_thread.start()
    
    def copy_grid_values(self):
    # Tạo một bản sao của lưới
        copied_grid = []
        for row in self.grid_boxes:
            copied_row = []
            for value in row:
                copied_row.append(value)
            copied_grid.append(copied_row)
        return copied_grid


    def update_single_grid_gui_square(self, row, col, colour, value=None):
        """Updates the colour and value of a single square in the grid GUI"""
        self.grid_boxes[row][col].config(fg=colour)
        if value is not None:
            if value == 0:
                value = ""
            self.grid_boxes[row][col].set(value)

    def btn_state(self, clickable):
        for btn in self.btn:
            btn.config(state=tk.NORMAL if clickable else tk.DISABLED)

class Grid(tk.Entry):
    def __init__(self, master = None, **kwargs):
        self.value = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.value, **kwargs)
        self.cur_value = ''
        self.value.trace('w', self.valid_input)
        self.get = self.value.get
        self.set = self.value.set   

    def valid_input(self, *args):
        value = self.get()
        if not value:
            self.set("")
        elif value.isdigit() and len(value) < 2 and value != '0':
                self.cur_value = self.get()
        else:
            self.set(self.cur_value)


if __name__ == "__main__":
    # window = tk.Tk()
    # MainApplication(window)
    
    # window.mainloop()
    # process = psutil.Process()
    # print(process.memory_info().rss)  # in bytes 
    # puzzle = [[8,0,0,0,0,0,0,0,0],
    #       [0,0,3,6,0,0,0,0,0],
    #       [0,7,0,0,9,0,2,0,0],
    #       [0,5,0,0,0,7,0,0,0],
    #       [0,0,0,0,4,5,7,0,0],
    #       [0,0,0,1,0,0,0,3,0],
    #       [0,0,1,0,0,0,0,6,8],
    #       [0,0,8,5,0,0,0,1,0],
    #       [0,9,0,0,0,0,4,0,0]]
    # start = time.time()
    # dfs_solver(puzzle)
    # end = time.time()
    # print(end-start)
    window = tk.Tk()
    MainApplication(window)
    
    window.mainloop()
