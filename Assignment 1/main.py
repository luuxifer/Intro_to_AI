import tkinter as tk
import copy
from dfs import *
import threading
import psutil

class MainApplication():
    def __init__(self, window):
        self.window = window
        self.grid_boxes = []
        self.btn = []
        self.feedback_solution = None
        self.setup_GUI()
        self.grid_value = [[1, 0, 0, 0, 7, 0, 3, 0, 0],
                        [0, 8, 0, 0, 2, 0, 7, 0, 0],
                        [3, 0, 0, 0, 8, 9, 0, 0, 4],
                        [8, 4, 0, 0, 0, 1, 9, 0, 3],
                        [0, 0, 3, 7, 0, 8, 5, 0, 0],
                        [9, 0, 1, 2, 0, 0, 0, 7, 8],
                        [7, 0, 0, 3, 5, 0, 0, 0, 9],
                        [0, 0, 9, 0, 4, 0, 0, 5, 0],
                        [0, 0, 4, 0, 1, 0, 0, 0, 2]]
        self.set_grid_GUI_from_value(self.grid_value)
        # self.get_grid_value_from_GUI()
        # self.reset_grid_colour()
        
    def setup_GUI(self):
        self.window.title("Sudoku")
        self.create_window()
        self.create_grid()
        self.create_btn()
        self.feedback_solution = tk.Label(self.window, text="")
        self.feedback_solution.grid(column=3, row=12, columnspan=2)

    def create_window(self):
        self.window.geometry('900x600')
        self.window.columnconfigure(0, minsize=20)
        self.window.rowconfigure(0, minsize=20)
        self.window.rowconfigure(10, minsize=20)
    
    def create_btn(self):
        rst_btn = tk.Button(self.window, text="Reset board", command=self.set_grid_GUI_from_value, font=('Ubuntu', 12), justify='center')
        rst_btn.grid(column=1, row=11, columnspan=2)
        new_btn = tk.Button(self.window, text="New board", command=self.new_board, font=('Ubuntu', 12), justify='center')
        new_btn.grid(column=3, row=11, columnspan=2)

        solve_btn = tk.Button(self.window, text="Solve board", command=self.solve_board, font=('Ubuntu', 12), justify='center')
        solve_btn.grid(column=5, row=11, columnspan=2) 

        check_btn = tk.Button(self.window, text="Check board", command=self.check_board, font=('Ubuntu', 12), justify='center')
        check_btn.grid(column=7, row=11, columnspan=2)

        self.btn = [rst_btn, new_btn, solve_btn, check_btn]

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

    def solve_board(self):
        self.btn_state(False)
        self.set_grid_GUI_from_value()
        board = copy.deepcopy(self.grid_value)
        solve_thread = threading.Thread(target=dfs_solver, args=(board, self), daemon=True)
        solve_thread.start()
    
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
    window = tk.Tk()
    MainApplication(window)
    
    window.mainloop()
    process = psutil.Process()
    print(process.memory_info().rss)  # in bytes 
