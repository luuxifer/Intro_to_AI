    import tkinter as tk
    from tkinter import messagebox
    import threading
    import copy

    def solve_board():
        if option1_var.get() and option2_var.get():
            messagebox.showwarning("Multiple Options Selected", "Please select only one option to run the task.")
        elif not option1_var.get() and not option2_var.get():
            messagebox.showwarning("No Option Selected", "Please select one option to run the task.")
        else:
            # Run the selected algorithm
            if option1_var.get():
                algorithm = "Algorithm 1"
                # Call the function for Algorithm 1
                algorithm_1_function()
            elif option2_var.get():
                algorithm = "Algorithm 2"
                # Call the function for Algorithm 2
                algorithm_2_function()

    def algorithm_1_function():
        # Implement your code for Algorithm 1 here
        messagebox.showinfo("Algorithm 1", "Running Algorithm 1")

    def algorithm_2_function():
        # Implement your code for Algorithm 2 here
        messagebox.showinfo("Algorithm 2", "Running Algorithm 2")

    # Create the main window
    root = tk.Tk()
    root.title("Task Runner")

    # Variables to track the state of checkboxes
    option1_var = tk.BooleanVar()
    option2_var = tk.BooleanVar()

    # Function to enable/disable the run button based on checkbox state
    def check_runnable():
        if option1_var.get() != option2_var.get():
            run_button.config(state=tk.NORMAL)
        else:
            run_button.config(state=tk.DISABLED)

    # Checkboxes for options
    option1_checkbox = tk.Checkbutton(root, text="Algorithm 1", variable=option1_var, command=check_runnable)
    option1_checkbox.pack()

    option2_checkbox = tk.Checkbutton(root, text="Algorithm 2", variable=option2_var, command=check_runnable)
    option2_checkbox.pack()

    # Button to run the task
    run_button = tk.Button(root, text="Run Task", command=solve_board, state=tk.DISABLED)
    run_button.pack()

    root.mainloop()
