import os

from platformdirs import user_data_dir
import customtkinter as ctk

from controllers.main_controller import MainController
from database.database import init
from gui.main_window import CanvasConverterGui


def main() -> None:
    """
    Starts the application's main window and mainloop.
    """
    app_data_dir = user_data_dir("ms2canvas converter", "kiya2400")
    os.makedirs(app_data_dir, exist_ok=True)
    db_path = os.path.join(app_data_dir, "md2canvas.db")
    init(db_path)

    root = ctk.CTk()
    controller = MainController(root, db_path)

    root.mainloop()


if __name__ == "__main__":
    main()
