import customtkinter as ctk
import tkinter as tk

from models.criteria import Criteria


class CriteriaComponent(ctk.CTkFrame):
    def __init__(self, parent, criteria: Criteria, controller):
        super().__init__(parent)

        self.controller = controller
        self.status_var = ctk.StringVar(value=criteria.pass_text)

        self.grid_columnconfigure(1, weight=1)

        options_button = ctk.CTkButton(self, text="⋮", width=32, fg_color="transparent",
                                       command=lambda: self.show_criteria_actions_dropdown(criteria))
        options_button.grid(row=0, column=0, padx=4, pady=8, sticky="w")

        self.criteria_text = ctk.CTkLabel(self, text=criteria.criteria, justify="left")
        # self.criteria_text.bind("<Configure>", lambda e: self.criteria_text.configure(wraplength=self.criteria_text.winfo_width()))
        self.criteria_text.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        self.criteria_checkbox = ctk.CTkSwitch(self, variable=self.status_var, onvalue=criteria.pass_text, offvalue=criteria.fail_text, text="", width=36)
        self.criteria_checkbox.grid(row=0, column=2, padx=8, pady=8, sticky="e")

        self.bind("<Configure>", self.update_text_wrap)

    def update_text_wrap(self, event):
        available_width = event.width - 120

        if available_width > 20:
            self.criteria_text.configure(wraplength=available_width)

    def get_criteria_evaluation_text(self):
        return self.status_var.get()

    def show_criteria_actions_dropdown(self, criteria):
        self.criteria_actions_dropdown = tk.Menu(self, tearoff=0)
        self.criteria_actions_dropdown.add_command(label="Redigera", command=lambda: self.controller.create_criteria_on_click(criteria))
        # self.criteria_actions_dropdown.add_command(label="Radera", command=lambda: self.controller.delete_criteria_on_click(criteria.id))

        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.criteria_actions_dropdown.tk_popup(x, y)

    def get_value(self):
        return self.status_var.get()