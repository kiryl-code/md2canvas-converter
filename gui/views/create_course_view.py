from tkinter import filedialog

import customtkinter as ctk

from models.course import Course


class CreateCourseView(ctk.CTkToplevel):
    def __init__(self, parent, on_save = None, course = None):
        super().__init__(parent)
        self.title("Lägga till ny kurs")
        self.center(self)
        self.course = course
        self.on_save = on_save
        self.is_archived_checkbox = None

        rows = 0

        self.course_code_label = ctk.CTkLabel(self, text="Kurskod")
        self.course_code_label.grid(row=rows, column=0, padx=(24, 8), pady=16, sticky="w")
        self.course_code_input = ctk.CTkEntry(self, placeholder_text="DV000G")
        self.course_code_input.grid(row=rows, column=1, columnspan=2, padx=(0, 24), pady=16, sticky="ew")

        rows += 1

        self.course_name_label = ctk.CTkLabel(self, text="Kursnamn")
        self.course_name_label.grid(row=rows, column=0, padx=(24, 8), pady=16, sticky="w")
        self.course_name_input = ctk.CTkEntry(self, placeholder_text="Programvaruteknik, introduktionskurs")
        self.course_name_input.grid(row=rows, column=1, columnspan=2, pady=16, padx=(0, 24), sticky="ew")

        rows += 1

        self.directory_label = ctk.CTkLabel(self, text="Kursmapp")
        self.directory_label.grid(row=rows, column=0, padx=(24, 8), pady=16, sticky="w")
        self.directory_input = ctk.CTkEntry(self)
        self.directory_input.grid(row=rows, column=1, pady=16, sticky="ew")
        self.directory_input_button = ctk.CTkButton(self, text="Bläddra...", width=86, command=self.browse)
        self.directory_input_button.grid(row=rows, column=2, padx=(8, 24), pady=16, sticky="ew")

        rows += 1

        if self.course:
            self.course_code_input.insert(0, self.course.course_code)
            self.course_name_input.insert(0, self.course.name)
            self.directory_input.insert(0, self.course.directory)

            self.is_archived_label = ctk.CTkLabel(self, text="Arkivera kurs")
            self.is_archived_label.grid(row=rows, column=0, padx=(24, 8), pady=16, sticky="w")
            self.is_archived_checkbox = ctk.CTkCheckBox(self, text="")
            self.is_archived_checkbox.grid(row=rows, column=1, padx=(0, 24), pady=16, sticky="ew")

            rows += 1

            self.is_archived_checkbox.set(self.course.is_archived)

        self.save_btn = ctk.CTkButton(self, text="Spara", command=self.save, width=86)
        self.save_btn.grid(row=rows, column=2, padx=(8, 24), pady=16, sticky="ew")

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

    def browse(self):
        dir_path = filedialog.askdirectory(title="Välj kursmapp")
        if dir_path:
            self.directory_input.delete(0, "end")
            self.directory_input.insert(0, dir_path)

    def save(self):
        course_code = self.course_code_input.get().strip().upper()
        name = self.course_name_input.get().strip()
        directory = self.directory_input.get().strip()
        is_archived = True if self.is_archived_checkbox and self.is_archived_checkbox.get() == 1 else False

        if course_code and name and directory:
            if self.course:
                self.course.course_code = course_code
                self.course.name = name
                self.course.directory = directory
                self.course.is_archived = is_archived
            else:
                 self.course = Course(course_code=course_code, name=name, directory=directory, is_archived=is_archived)
            self.on_save(self.course)
        self.destroy()
