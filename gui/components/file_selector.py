import tkinter as tk
from gui.components.file_selector_dialog import FileSelectorDialog


class FileSelectorComponent(tk.Frame):
    """
    A component for selecting a file. Includes label, input and a button
    for browsing and selecting a file from file explorer.
    """

    def __init__(self, parent: tk.Frame | tk.Tk, label_text: str, filetype: list[tuple[str, str]] | None = None):
        """
        Initializes the component.
        :param parent: a parent widget
        :param label_text: a text to display in the label
        :param filetype: define which file type should be selectable through the :class:`FileSelectorDialog`. Defaults
        to ``None``, which means directory selection.
        """

        super().__init__(parent)
        self.button = None
        self.input = None
        self.label = None

        self.parent = parent
        self.label_text = label_text
        self.filetype = filetype
        self.path = tk.StringVar()
        self.construct_gui()

    def construct_gui(self) -> None:
        """
        Initializes GUI of component.
        """

        self.config(padx=16)

        self.label = tk.Label(self, text=self.label_text)
        self.label.config(pady=8, padx=16)
        self.label.pack(side="left", fill="x", anchor="w")

        self.input = tk.Entry(self, textvariable=self.path)
        self.input.pack(side="left", fill="x", expand=True, anchor="center")
        self.input.bind("<Escape>", lambda e: self.focus_set())

        self.button = tk.Button(self, text="Browse...", command=self.browse)
        self.button.config(padx=16)
        self.button.pack(side="right", fill="x", anchor="e")

    def browse(self) -> None:
        """
        Creates new :class:`FileSelectorDialog` which allows the user
        to choose a path.
        """

        file_selector_dialog = FileSelectorDialog(self.filetype)
        selected_path = file_selector_dialog.get_path(self.path.get())
        if selected_path:
            self.path.set(selected_path)
