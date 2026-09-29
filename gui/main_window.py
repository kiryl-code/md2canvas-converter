import customtkinter as ctk
import tkinter as tk

from gui.components.converter_inputs import ConverterInputs
from converter.converter import convert
from gui.views.courses import CoursesView
from gui.views.main_view import MainView


class CanvasConverterGui(ctk.CTkFrame):
    """
    Application's main window.
    """

    def __init__(self, root, controller):
        """
        Starts the application's main window.
        """
        super().__init__(root, fg_color="transparent")

        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.courses_panel = CoursesView(self, self.controller)
        self.courses_panel.grid(row=0, column=0, sticky="nsew", padx=(4,0), pady=(0, 8))

        self.main_area = MainView(self, self.controller)
        self.main_area.grid(row=0, column=1, sticky="nsew")


        # self.inputs_panel = ConverterInputs(self)
        # self.inputs_panel.pack(fill="x")
        #
        # self.convert_button = tk.Button(self, text="Convert", command=self.convert)
        # self.convert_button.pack()

        root.config(padx=8, pady=8)
        self.setup_window(root)

    def set_controller(self, controller):
        self.controller = controller

    def setup_window(self, root) -> None:
        """
        Sets up the application's main window by setting
        name and dimensions.
        """
        root.title("Markdown -> Canvas converter")
        root.update_idletasks()
        root.minsize(width=900, height=600)
        width = root.winfo_width()
        height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        root.geometry(f"+{x}+{y}")

    def convert(self) -> None:
        """
        A method that invokes when the user clicks "Convert" button.
        Calls conversion logic.
        """
        convert(self.inputs_panel.input_path.get(), self.inputs_panel.output_path.get(), "styles/kiya-pages-style.css")





if __name__ == "__main__":
    main()
