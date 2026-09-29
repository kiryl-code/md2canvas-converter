from tkinter import filedialog

import customtkinter as ctk

from models.assignment import Assignment
from models.course import Course


class CreateAssignmentView(ctk.CTkToplevel):
    def __init__(self, parent, course_id, on_save = None, assignment = None):
        super().__init__(parent)
        self.title("Lägga till ny uppgift")
        self.center(self)
        self.assignment = assignment
        self.course_id = course_id
        self.on_save = on_save

        rows = 0

        self.assignment_name_label = ctk.CTkLabel(self, text="Namn")
        self.assignment_name_label.grid(row=rows, column=0, padx=(24, 8), pady=16, sticky="w")
        self.assignment_name_input = ctk.CTkEntry(self, placeholder_text="Laboration 1")
        self.assignment_name_input.grid(row=rows, column=1, columnspan=1, padx=(0, 24), pady=(16,8), sticky="ew")

        rows += 1

        self.assignment_introduction_label = ctk.CTkLabel(self, text="Inledning")
        self.assignment_introduction_label.grid(row=rows, column=0, padx=(24, 8), pady=(8,0), sticky="w")

        rows += 1

        self.assignment_introduction_variable_tip = ctk.CTkLabel(self, text="Variabler: {{name}} {{grade}}")
        self.assignment_introduction_variable_tip.grid(row=rows, column = 0, columnspan=2, padx=(24, 8), pady=(0,8), sticky="w")

        rows += 1

        self.assignment_introduction_input = ctk.CTkTextbox(self, height=128)
        self.assignment_introduction_input.grid(row=rows, column=0, columnspan=2, pady=(4, 8), padx=24, sticky="ew")

        rows += 1

        self.save_btn = ctk.CTkButton(self, text="Spara", command=self.save, width=86)
        self.save_btn.grid(row=rows, column=1, padx=24, pady=(8, 16), sticky="e")

        self.add_criteria_btn = ctk.CTkButton(self, text="Lägg till kriterium")
        self.add_criteria_btn.grid(row=rows, column=0, padx=24, pady=(8, 16), sticky="w")

        if self.assignment:
            self.assignment_name_input.delete(0)
            self.assignment_introduction_input.delete("0.0", "end")
            self.assignment_name_input.insert(0, self.assignment.name)
            self.assignment_introduction_input.insert("0.0", self.assignment.introduction_template)

        self.grid_columnconfigure(1, weight=1)
        self.grab_set()

    def center(self, root):
        root.minsize(width=400, height=240)
        width = root.winfo_width()
        height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        root.geometry(f"+{x}+{y}")

    def save(self):
        assignment_name = self.assignment_name_input.get().strip().capitalize()
        assignment_intro = self.assignment_introduction_input.get("0.0", "end").strip()

        if not assignment_name and assignment_intro:
            return
        if not self.assignment:
            self.assignment = Assignment(course_id=self.course_id, name=assignment_name, introduction_template=assignment_intro)
        else:
            self.assignment.name = assignment_name
            self.assignment.introduction_template = assignment_intro

        self.on_save(self.assignment)
        self.destroy()
