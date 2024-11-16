import tkinter as tk
from tkinter import ttk


class TkinterApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("MongoDB Viewer")

        # Initialize variables
        self.input1_var = tk.StringVar()
        self.input2_var = tk.StringVar()
        self.choice1_var = tk.StringVar()
        self.choice2_var = tk.StringVar()
        self.choice3_var = tk.StringVar()

        self.setup_ui()

    def clear_fields(self):
        self.input1_var.set("")
        self.input2_var.set("")
        self.choice1_var.set("")
        self.choice2_var.set("")
        self.choice3_var.set("")
        self.validate_submit()

    def validate_submit(self):
        if self.input1_var.get() and self.input2_var.get() and self.choice1_var.get() and self.choice2_var.get() and self.choice3_var.get():
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)

    def setup_ui(self):
        # Header
        header_label = tk.Label(self.app, text="Header", font=(
            "Arial", 16, "bold"), anchor="w", justify="left")
        header_label.pack(pady=10, anchor="w", padx=20)

        # Description
        description_label = tk.Label(self.app, text="Description", font=(
            "Arial", 12), anchor="w", justify="left")
        description_label.pack(pady=5, anchor="w", padx=20)

        # Input fields container
        inputs_frame = tk.Frame(self.app)
        inputs_frame.pack(fill=tk.BOTH, padx=20, pady=10)

        # Input 1
        input1_label = tk.Label(inputs_frame, text="Input 1", font=(
            "Arial", 10), anchor="w", justify="left")
        input1_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        input1_entry = tk.Entry(inputs_frame, textvariable=self.input1_var)
        input1_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        input1_entry.bind("<KeyRelease>", lambda event: self.validate_submit())

        # Input 2
        input2_label = tk.Label(inputs_frame, text="Input 2", font=(
            "Arial", 10), anchor="w", justify="left")
        input2_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        input2_entry = tk.Entry(inputs_frame, textvariable=self.input2_var)
        input2_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        input2_entry.bind("<KeyRelease>", lambda event: self.validate_submit())

        inputs_frame.columnconfigure(0, weight=1)
        inputs_frame.columnconfigure(1, weight=1)

        # Dropdowns
        # Choice 1
        choice1_label = tk.Label(self.app, text="Choice 1", font=(
            "Arial", 10), anchor="w", justify="left")
        choice1_label.pack(pady=5, anchor="w", padx=20)
        choice1_dropdown = ttk.Combobox(
            self.app, textvariable=self.choice1_var, state="readonly")
        choice1_dropdown['values'] = ["Option 1", "Option 2", "Option 3"]
        choice1_dropdown.pack(pady=5, fill=tk.X, padx=20)
        choice1_dropdown.bind("<<ComboboxSelected>>",
                              lambda event: self.validate_submit())

        # Choice 2
        choice2_label = tk.Label(self.app, text="Choice 2", font=(
            "Arial", 10), anchor="w", justify="left")
        choice2_label.pack(pady=5, anchor="w", padx=20)
        choice2_dropdown = ttk.Combobox(
            self.app, textvariable=self.choice2_var, state="readonly")
        choice2_dropdown['values'] = ["Option 1", "Option 2", "Option 3"]
        choice2_dropdown.pack(pady=5, fill=tk.X, padx=20)
        choice2_dropdown.bind("<<ComboboxSelected>>",
                              lambda event: self.validate_submit())

        # Choice 3
        choice3_label = tk.Label(self.app, text="Choice 3", font=(
            "Arial", 10), anchor="w", justify="left")
        choice3_label.pack(pady=5, anchor="w", padx=20)
        choice3_dropdown = ttk.Combobox(
            self.app, textvariable=self.choice3_var, state="readonly")
        choice3_dropdown['values'] = ["Option 1", "Option 2", "Option 3"]
        choice3_dropdown.pack(pady=5, fill=tk.X, padx=20)
        choice3_dropdown.bind("<<ComboboxSelected>>",
                              lambda event: self.validate_submit())

        # Buttons
        buttons_frame = tk.Frame(self.app)
        buttons_frame.pack(pady=20, anchor="w")

        # Submit Button
        self.submit_button = tk.Button(
            buttons_frame, text="Submit", state=tk.DISABLED)
        self.submit_button.grid(row=0, column=0, padx=10)

        # Start Over Button
        startover_button = tk.Button(
            buttons_frame, text="Start Over", command=self.clear_fields)
        startover_button.grid(row=0, column=1, padx=10)

    def run(self):
        self.app.mainloop()


# Usage example in app.py
if __name__ == "__main__":
    app = TkinterApp()
    app.run()
