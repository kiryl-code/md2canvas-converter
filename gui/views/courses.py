import customtkinter as ctk
import tkinter as tk

from models.course import Course


class CoursesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Kurser", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=32, pady=8, sticky="ew")

        self.courses_list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.courses_list_frame.grid(row=1, column=0, sticky="nsew")

        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=2, column=0, sticky="sew", pady=(0, 8))

        self.controls_frame.grid_columnconfigure(0, weight=1)


        self.add_course_button = ctk.CTkButton(self.controls_frame, text="Ny kurs", command=self.controller.create_course_on_click)
        self.add_course_button.grid(row=0, column=0, padx=8, pady=4, sticky="ew")

        self.import_button = ctk.CTkButton(self.controls_frame, text="Importera en kurs")
        self.import_button.grid(row=1, column=0, padx=8, pady=4, sticky="ew")

        self.archived_courses_button = ctk.CTkButton(self.controls_frame, text="Arkiverade kurser", command=self.controller.toggle_archived)
        self.archived_courses_button.grid(row=2, column=0, padx=8, pady=4, sticky="ew")

        self.file_converter_button = ctk.CTkButton(self.controls_frame, text="Konvertera en fil", command=self.controller.file_converter_on_click)
        self.file_converter_button.grid(row=3, column=0, padx=8, pady=4, sticky="ew")

        self.courses = []


    def render_courses(self, courses: list[Course], is_archived: bool = False) -> None:
        for widget in self.courses_list_frame.winfo_children():
            widget.destroy()
        self.courses.clear()

        self.title_label.configure(text="Arkiverade kurser" if is_archived else "Kurser")
        self.archived_courses_button.configure(text="Aktiva kurser" if is_archived else "Arkiverade kurser")

        for course in courses:
            course_frame = ctk.CTkFrame(self.courses_list_frame)
            course_frame.pack(padx=4, pady=4, fill="x")

            course_button = ctk.CTkButton(course_frame, text=course.course_code.upper(), fg_color="transparent", anchor="w")
            course_button.configure(command=lambda c=course.id, b=course_button: self.select_course(c,b))
            course_button.grid(row=0, column=0, padx=4, pady=4)
            course_button.course = course
            self.courses.append(course_button)

            options_button = ctk.CTkButton(course_frame, text="⋮", width=32, fg_color="transparent", command=lambda: self.show_course_actions_dropdown(options_button, course))
            options_button.grid(row=0, column=1, padx=4)

    def show_course_actions_dropdown(self, parent, course):
        self.course_actions_dropdown = tk.Menu(self, tearoff=0)
        self.course_actions_dropdown.add_command(label="Redigera", command=lambda: self.controller.create_course_on_click(course))
        self.course_actions_dropdown.add_separator()
        if course.is_archived:
            self.course_actions_dropdown.add_command(label="Återställa", command=lambda: self.controller.unarchive_course(course))
        else:
            self.course_actions_dropdown.add_command(label="Arkivera", command=lambda: self.controller.archive_course(course))

        parent.update_idletasks()
        x = parent.winfo_rootx()
        y = parent.winfo_rooty() + parent.winfo_height()
        self.course_actions_dropdown.tk_popup(x, y)

    def select_course(self, course_id, course_button):
        for b in self.courses:
            b.configure(fg_color="transparent")
        course_button.configure(fg_color=["#3a7ebf", "#1f538d"])
        self.controller.select_course(course_id)
