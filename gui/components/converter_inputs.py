import tkinter as tk
from gui.components.file_selector import FileSelectorComponent
from utils import globals


class ConverterInputs(tk.Frame):
    """
    Contains input and output widgets
    that can be used in convertor views.
    Provides links to the input and output
    paths through ``input_path`` and ``output_path``.
    """

    def __init__(self, parent: tk.Frame | tk.Tk):
        """
        Constructs a frame with widgets for selecting input file
        and output directory.
        :param parent: parent widget or window
        """
        super().__init__(parent)
        self.input_selector = FileSelectorComponent(self, "Input file", globals.FILETYPE_MARKDOWN)
        self.output_selector = FileSelectorComponent(self, "Output path")
        self.input_selector.pack(fill="x")
        self.output_selector.pack(fill="x")
        self.input_path = self.input_selector.path
        self.output_path = self.output_selector.path
