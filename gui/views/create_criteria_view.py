import customtkinter as ctk

from models.criteria import Criteria


class CreateCriteriaView(ctk.CTkToplevel):
    def __init__(self, parent, assignment_id, criteria=None, on_save=None):
        super().__init__(parent)
        self.title("Nytt kriterium")
        self.center(self)
        self.assignment_id = assignment_id
        self.criteria = criteria
        self.on_save = on_save
        self.grid_columnconfigure(0, weight=1)

        rows = 0

        self.criteria_label = ctk.CTkLabel(self, text="Moment / kriterium")
        self.criteria_label.grid(row=rows, column=0, padx=24, pady=16, sticky="w")

        rows += 1

        self.criteria_input = ctk.CTkTextbox(self, height=128)
        self.criteria_input.grid(rows=rows, column=0, padx=24, pady=(4, 8), sticky="ew")

        rows += 1

        self.pass_label = ctk.CTkLabel(self, text="Text vid godkänt")
        self.pass_label.grid(row=rows, column=0, padx=24, pady=(8, 4), sticky="w")

        rows += 1

        self.pass_input = ctk.CTkTextbox(self, height=128)
        self.pass_input.grid(row=rows, column=0, padx=24, pady=(4, 8), sticky="ew")

        rows += 1

        self.fail_label = ctk.CTkLabel(self, text="Text vid komplettering")
        self.fail_label.grid(row=rows, column=0, padx=24, pady=(8, 4), sticky="w")

        rows += 1

        self.fail_input = ctk.CTkTextbox(self, height=128)
        self.fail_input.grid(row=rows, column=0, padx=24, pady=(4, 8), sticky="ew")

        rows += 1

        self.save_btn = ctk.CTkButton(self, text="Spara", command=self.save)
        self.save_btn.grid(row=rows, column=0, padx=24, pady=(4, 8), sticky="e")

        if self.criteria:
            self.criteria_input.insert("0.0", self.criteria.criteria)
            self.pass_input.insert("0.0", self.criteria.pass_text)
            self.fail_input.insert("0.0", self.criteria.fail_text)

        self.grab_set()

    def save(self):
        criteria = self.criteria_input.get("0.0", "end").strip()
        pass_text = self.pass_input.get("0.0", "end").strip()
        fail_text = self.fail_input.get("0.0", "end").strip()

        if not self.on_save:
            return

        if not (criteria and pass_text and fail_text):
            return
        else:
            if self.criteria:
                self.criteria.criteria = criteria
                self.criteria.pass_text = pass_text
                self.criteria.fail_text = fail_text
                self.on_save(self.criteria)
            else:
                criteria = Criteria(assignment_id=self.assignment_id, criteria=criteria, pass_text=pass_text,
                                    fail_text=fail_text)
                self.on_save(criteria)
        self.destroy()

    def center(self, root):
        root.minsize(width=400, height=240)
        width = root.winfo_width()
        height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        root.geometry(f"+{x}+{y}")
