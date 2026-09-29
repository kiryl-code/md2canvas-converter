from tkinter import filedialog

import customtkinter as ctk

from models.assignment import Assignment
from models.course import Course


class FeedbackPreview(ctk.CTkToplevel):
    def __init__(self, parent, feedback, on_save=None):
        super().__init__(parent)
        self.title("Förhandsgranskning")
        self.center(self)
        self.on_save = on_save
        self.feedback = feedback

        rows = 0

        self.preview_text_box = ctk.CTkTextbox(self, height=512)
        self.preview_text_box.grid(row=rows, column=0, padx=8, pady=8, sticky="nsew")

        rows += 1

        self.save_btn = ctk.CTkButton(self, text="Spara", command=self.save)
        self.save_btn.grid(row=rows, column=0, padx=8, pady=8, sticky="ew")

        self.preview_text_box.insert("0.0", feedback)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
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
        if not self.on_save:
            return
        else:
            feedback = self.preview_text_box.get("0.0", "end").strip()
            self.on_save(feedback)
        self.destroy()
