import tkinter as tk

from gui.components.converter_inputs import ConverterInputs
from converter.converter import convert


class CanvasConverterGui(tk.Tk):
    """
    Application's main window.
    """

    def __init__(self):
        """
        Starts the application's main window.
        """
        super().__init__()

        self.inputs_panel = ConverterInputs(self)
        self.inputs_panel.pack(fill="x")

        self.convert_button = tk.Button(self, text="Convert", command=self.convert)
        self.convert_button.pack()

        self.config(padx=8, pady=16)
        self.setup_window()

    def setup_window(self) -> None:
        """
        Sets up the application's main window by setting
        title and dimensions.
        """
        self.title("Markdown -> Canvas converter")
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"+{x}+{y}")

    def convert(self) -> None:
        """
        A method that invokes when the user clicks "Convert" button.
        Calls conversion logic.
        """
        convert(self.inputs_panel.input_path.get(), self.inputs_panel.output_path.get(), "styles/kiya-pages-style.css")


def main() -> None:
    """
    Starts the application's main window and mainloop.
    """
    app = CanvasConverterGui()
    app.mainloop()


if __name__ == "__main__":
    main()
