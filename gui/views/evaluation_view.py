import platform

import customtkinter as ctk

from gui.components.criteria_component import CriteriaComponent


class EvaluationView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        root_window = self.winfo_toplevel()
        root_window.bind_all("<MouseWheel>", self._on_mouse_scroll)
        root_window.bind_all("<Button-4>", self._on_mouse_scroll) # För Linux
        root_window.bind_all("<Button-5>", self._on_mouse_scroll) # För Linux

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        student_credentials_frame = ctk.CTkFrame(self, fg_color="transparent")
        student_credentials_frame.grid_columnconfigure(4, weight=1)
        student_credentials_frame.grid(row=0, column=0, padx=8, pady=8, sticky="ew")

        student_credentials_frame_gap = 24

        # student id
        self.student_id_label = ctk.CTkLabel(student_credentials_frame, text="Student-ID")
        self.student_id_label.grid(row=0, column=0, padx=(4, 8), pady=0, sticky="ew")
        self.student_id_input = ctk.CTkEntry(student_credentials_frame, placeholder_text="abcd1234")
        self.student_id_input.grid(row=0, column=1, padx=(0, 0), pady=0, sticky="ew")

        # student namn
        self.student_name_label = ctk.CTkLabel(student_credentials_frame, text="Namn")
        self.student_name_label.grid(row=0, column=3, padx=(student_credentials_frame_gap, 8), pady=0, sticky="ew")
        self.student_name_input = ctk.CTkEntry(student_credentials_frame)
        self.student_name_input.grid(row=0, column=4, padx=(0, 0), pady=0, sticky="ew")

        # Betyg
        self.grade_label = ctk.CTkLabel(student_credentials_frame, text="Betyg")
        self.grade_label.grid(row=0, column=5, padx=(student_credentials_frame_gap, 8), pady=0, sticky="ew")
        self.grade_input = ctk.CTkEntry(student_credentials_frame, width=64)
        self.grade_input.grid(row=0, column=6, padx=(0, 0), pady=0, sticky="ew")

        # Bedömning
        self.criteria_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.criteria_container.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.criteria_container.grid_columnconfigure(0, weight=1)

        # Övriga kommentarer
        self.free_comment_label = ctk.CTkLabel(self, text="Övriga kommentarer")
        self.free_comment_label.grid(row=2, column=0, padx=8, pady=0, sticky="w")
        self.free_comment_input = ctk.CTkTextbox(self, height=84)
        self.free_comment_input.grid(row=3, column=0, padx=8, pady=0, sticky="nsew", columnspan=2)

        # Buttons
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=4, column=0, padx=2, pady=4, sticky="we", columnspan=2)
        self.controls_frame.grid_columnconfigure(1, weight=1)

        self.add_criteria_button = ctk.CTkButton(self.controls_frame, text="Lägg till kriterium", command=self.controller.create_criteria_on_click)
        self.add_criteria_button.grid(row=0, column=0, padx=8, pady=4, sticky="e")

        self.next_button = ctk.CTkButton(self.controls_frame, text="Nästa student", command=self.reset)
        self.next_button.grid(row=0, column=1, padx=8, pady=4, sticky="e")

        self.preview_button = ctk.CTkButton(self.controls_frame, text="Spara och förhandsgranska", command=self.preview)
        self.preview_button.grid(row=0, column=2, padx=8, pady=4, sticky="e")

        self.export_button = ctk.CTkButton(self.controls_frame, text="Exportera", command=self.export)
        self.export_button.grid(row=0, column=3, padx=8, pady=4, sticky="e")

        self.criteria_widgets = {}
        self.criteria_evaluation = {}

    def render_criteria(self, criteria_list):
        for widget in self.criteria_container.winfo_children():
            widget.destroy()
        self.criteria_widgets.clear()

        if not criteria_list:
            criteria_not_found_label = ctk.CTkLabel(self.criteria_container,
                                                    text="Inga kriterier tilldagda för denna uppgift")
            criteria_not_found_label.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        rows = 0

        for criteria in criteria_list:
            criteria_frame = CriteriaComponent(self.criteria_container, criteria, self.controller)
            criteria_frame.grid(row=rows, column=0, sticky="ew", columnspan=2)
            self.criteria_widgets[criteria.id] = criteria_frame
            rows += 1

    def reset(self):
        self.student_id_input.delete(0, "end")
        self.student_name_input.delete(0, "end")
        self.grade_input.delete(0, "end")
        self.free_comment_input.delete("0.0", "end")
        self.render_criteria([])
        self.controller.reset_feedback()

    def preview(self):
        criteria_data = []
        for criteria, widget in self.criteria_widgets.items():
            criteria_data.append(widget.get_value())
        student_name = self.student_name_input.get()
        grade = self.grade_input.get()
        additional_comment = self.free_comment_input.get("0.0", "end")
        self.controller.preview_feedback_on_click(criteria_data, student_name, grade, additional_comment)

    def export(self):
        student_id = self.student_id_input.get()
        self.controller.export_feedback_on_click(student_id)

    def _on_mouse_scroll(self, event):
        if not self.winfo_ismapped():
            return

        canvas = self.criteria_container._parent_canvas

        if platform.system() == "Windows":
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Darwin":
            canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")