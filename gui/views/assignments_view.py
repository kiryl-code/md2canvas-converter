import customtkinter as ctk
import tkinter as tk


class AssignmentsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, height=42)
        self.controller = controller
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.assignments_tabs_container = ctk.CTkScrollableFrame(self, fg_color="transparent", orientation="horizontal", height=42)
        self.assignments_tabs_container.grid(row=0, column=0, sticky="nsew", padx=(4, 0), pady=0)
        self.assignments_tabs_container._scrollbar.grid_forget()
        self.assignments_tabs_container._parent_canvas.rowconfigure(0, weight=1)

        self.add_button = ctk.CTkButton(self, text="+", width=42, height=42, command=self.controller.create_assignment_on_click)
        self.add_button.grid(row=0, column=1)

        self.assignments_buttons = []

    def render_assignments(self, assignments, selected_assignment: int | None = None):
        for widget in self.assignments_tabs_container.winfo_children():
            widget.destroy()

        for assignment in assignments:
            btn_color = ("#3a7ebf", "#1f538d")
            assignment_button_frame = ctk.CTkFrame(self.assignments_tabs_container, fg_color="transparent")
            assignment_button_frame.pack(side="left", padx=(2, 4), expand=True, pady=(0, 4))

            assignment_button = ctk.CTkButton(assignment_button_frame, text=assignment.name, fg_color="transparent", width=0, command=lambda a=assignment: self.controller.select_assignment(a.id))
            assignment_button.grid(row=0, column=0, padx=0, pady=0)
            assignment_button.assignment = assignment

            options_button = ctk.CTkButton(assignment_button_frame, text="⋮", fg_color="transparent", width=4, height=24, command=lambda btn=assignment_button, a=assignment: self.show_assignment_actions_dropdown(btn, a))
            options_button.grid(row=0, column=1, padx=(0, 4))

            self.assignments_buttons.append(assignment_button)

    def show_assignment_actions_dropdown(self, button, assignment):
        self.assignment_actions_dropdown = tk.Menu(self, tearoff=0)
        self.assignment_actions_dropdown.add_command(label="Redigera", command=lambda: self.controller.create_assignment_on_click(assignment))
        # self.assignment_actions_dropdown.add_command(label="Radera", command=lambda: self.controller.delete_assignment(assignment.id))

        button.update_idletasks()
        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()
        self.assignment_actions_dropdown.tk_popup(x, y)