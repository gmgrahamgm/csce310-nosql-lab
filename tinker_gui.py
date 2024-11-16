import tkinter as tk
from tkinter import ttk
from mongodb_backend import Mongodb


class TkinterApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("MongoDB Viewer")

        self.mongodb = Mongodb()

        self.input1_var = tk.StringVar()
        self.input2_var = tk.StringVar()
        self.choice1_var = tk.StringVar()
        self.choice2_var = tk.StringVar()
        self.choice3_var = tk.StringVar()

        self.candidates = self.mongodb.get_all_candidates()

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

    def populate_choices(self, event=None):
        selected = {
            self.choice1_var.get(),
            self.choice2_var.get(),
            self.choice3_var.get()
        }
        available = [c for c in self.candidates if c not in selected]
        self.choice1_dropdown["values"] = available if not self.choice1_var.get() else [
            self.choice1_var.get()] + available
        self.choice2_dropdown["values"] = available if not self.choice2_var.get() else [
            self.choice2_var.get()] + available
        self.choice3_dropdown["values"] = available if not self.choice3_var.get() else [
            self.choice3_var.get()] + available

    def submit_ballot(self):
        voterID = self.input1_var.get()
        regPIN = self.input2_var.get()
        firstChoice = self.choice1_var.get()
        secondChoice = self.choice2_var.get()
        thirdChoice = self.choice3_var.get()

        self.mongodb.post_ballot(
            voterID, regPIN, firstChoice, secondChoice, thirdChoice)
        self.clear_fields()
        print("Ballot submitted successfully!")

    def setup_ui(self):
        # Header
        header_label = tk.Label(self.app, text="Voting Form", font=(
            "Arial", 16, "bold"), anchor="w", justify="left")
        header_label.pack(pady=10, anchor="w", padx=20)

        # Description
        description_label = tk.Label(self.app, text="Please enter your voter ID and registration PIN. These are found on the card that you were given by your local election agent.", font=(
            "Arial", 12), anchor="w", justify="left")
        description_label.pack(pady=5, anchor="w", padx=20)

        # Input fields container
        inputs_frame = tk.Frame(self.app)
        inputs_frame.pack(fill=tk.BOTH, padx=20, pady=10)

        # Input 1
        input1_label = tk.Label(inputs_frame, text="Voter ID", font=(
            "Arial", 10), anchor="w", justify="left")
        input1_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        input1_entry = tk.Entry(inputs_frame, textvariable=self.input1_var)
        input1_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        input1_entry.bind("<KeyRelease>", lambda event: self.validate_submit())

        # Input 2
        input2_label = tk.Label(inputs_frame, text="Registration PIN", font=(
            "Arial", 10), anchor="w", justify="left")
        input2_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        input2_entry = tk.Entry(inputs_frame, textvariable=self.input2_var)
        input2_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        input2_entry.bind("<KeyRelease>", lambda event: self.validate_submit())

        inputs_frame.columnconfigure(0, weight=1)
        inputs_frame.columnconfigure(1, weight=1)

        # Dropdowns
        # Choice 1
        choice1_label = tk.Label(self.app, text="First Choice", font=(
            "Arial", 10), anchor="w", justify="left")
        choice1_label.pack(pady=5, anchor="w", padx=20)
        self.choice1_dropdown = ttk.Combobox(
            self.app, textvariable=self.choice1_var, state="readonly")
        self.choice1_dropdown["values"] = self.candidates
        self.choice1_dropdown.pack(pady=5, fill=tk.X, padx=20)
        self.choice1_dropdown.bind(
            "<<ComboboxSelected>>", self.populate_choices)

        # Choice 2
        choice2_label = tk.Label(self.app, text="Second Choice", font=(
            "Arial", 10), anchor="w", justify="left")
        choice2_label.pack(pady=5, anchor="w", padx=20)
        self.choice2_dropdown = ttk.Combobox(
            self.app, textvariable=self.choice2_var, state="readonly")
        self.choice2_dropdown["values"] = self.candidates
        self.choice2_dropdown.pack(pady=5, fill=tk.X, padx=20)
        self.choice2_dropdown.bind(
            "<<ComboboxSelected>>", self.populate_choices)

        # Choice 3
        choice3_label = tk.Label(self.app, text="Third Choice", font=(
            "Arial", 10), anchor="w", justify="left")
        choice3_label.pack(pady=5, anchor="w", padx=20)
        self.choice3_dropdown = ttk.Combobox(
            self.app, textvariable=self.choice3_var, state="readonly")
        self.choice3_dropdown["values"] = self.candidates
        self.choice3_dropdown.pack(pady=5, fill=tk.X, padx=20)
        self.choice3_dropdown.bind(
            "<<ComboboxSelected>>", self.populate_choices)

        # Buttons
        buttons_frame = tk.Frame(self.app)
        buttons_frame.pack(pady=20, anchor="w")

        # Submit Button
        self.submit_button = tk.Button(
            buttons_frame, text="Submit", state=tk.DISABLED, command=self.submit_ballot)
        self.submit_button.grid(row=0, column=0, padx=10)

        # Start Over Button
        startover_button = tk.Button(
            buttons_frame, text="Start Over", command=self.clear_fields)
        startover_button.grid(row=0, column=1, padx=10)

        # Footer
        footer_label = tk.Label(self.app, text="After submitting your vote, please collect your ballot from the printer on your right and ensure that your ranked choices match your selections. After inspection, hand the printed ballot to the local election agent. Thank you for voting.", font=(
            "Arial", 12), anchor="w", justify="left")
        footer_label.pack(pady=5, anchor="w", padx=20)

    def run(self):
        self.app.mainloop()
