import tkinter as tk

class HelpDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Help")
        tk.Label(self, text="Help information for Markdown -> Canvas converter.").pack(pady=20, padx=40)
        self.resizable(width=False, height=False)