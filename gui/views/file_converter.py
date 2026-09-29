from tkinter import filedialog

import customtkinter as ctk

from utils.globals import FILETYPE_MARKDOWN


class FileConverter(ctk.CTkToplevel):
    def __init__(self, parent, on_convert):
        super().__init__(parent)
        self.parent = parent
        self.title("Konvertera en fil")
        self.on_convert = on_convert

        self.file_input_label = ctk.CTkLabel(self, text="Välj en fil")
        self.file_input_label.grid(column=0, row=0, pady=16, padx=(24,8), sticky="w")
        self.file_input = ctk.CTkEntry(self)
        self.file_input.grid(column=1, row=0, pady=16, padx=(0,8), sticky="ew")
        self.file_input_button = ctk.CTkButton(self, text="Bläddra...", width=86, command=self.browse_input)
        self.file_input_button.grid(column=2, row=0, pady=16, padx=(0,24), sticky="ew")

        self.directory_output_label = ctk.CTkLabel(self, text="Välj export mapp")
        self.directory_output_label.grid(column=0, row=1, pady=16, padx=(24, 8), sticky="w")
        self.directory_output = ctk.CTkEntry(self)
        self.directory_output.grid(column=1, row=1, pady=16, padx=(0,8), sticky="ew")
        self.directory_output_button = ctk.CTkButton(self, text="Bläddra...", width=86, command=self.browse_output)
        self.directory_output_button.grid(column=2, row=1, pady=16, padx=(0,24), sticky="ew")

        self.convert_button = ctk.CTkButton(self, text="Konvertera", width=86, command=lambda: self.on_convert(self.file_input.get().strip(), self.directory_output.get().strip()))
        self.convert_button.grid(column=2, row=2, pady=16, padx=(0,24), sticky="ew")

        self.grid_columnconfigure(1, weight=1)
        self.center(parent)
        self.grab_set()

    def center(self, root):
        self.minsize(width=500, height=140)
        width = root.winfo_width()
        height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"+{x}+{y}")

    def browse_input(self):
        file_path = filedialog.askopenfilename(filetypes=FILETYPE_MARKDOWN)
        if file_path:
            self.file_input.delete(0, "end")
            self.file_input.insert(0, file_path)

    def browse_output(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.directory_output.delete(0, "end")
            self.directory_output.insert(0, dir_path)
