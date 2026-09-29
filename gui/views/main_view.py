import customtkinter as ctk

from gui.views.assignments_view import AssignmentsView
from gui.views.evaluation_view import EvaluationView


class MainView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.grid(row=0, column=1, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.assignments = AssignmentsView(self, self.controller)
        self.assignments.grid(row=0, column=0, columnspan=2, padx=8, sticky="new")

        self.evaluation_frame = EvaluationView(self, self.controller)
        self.evaluation_frame.grid(row=1, column=0, columnspan=2, padx=8, pady=8, sticky="nsew")