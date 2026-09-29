import json
import tkinter as tk
from gui.components.file_selector_dialog import FileSelectorDialog


class PreferencesDialog(tk.Toplevel):
    def __init__(self, parent, config_manager=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.title("Preferences")

        self.setup_config()
        self.setup_ui()

        self.transient(parent)
        self.grab_set()
        self.focus_set()
        parent.wait_window(self)

    def setup_config(self):
        self.config_data = None
        try:
            with open("../../user-config.json", "r", encoding="utf-8") as f:
                self.config_data = json.load(f)
        except FileNotFoundError:
            try:
                with open("../../default-config.json", "r", encoding="utf-8") as f:
                    self.config_data = json.load(f)
            except FileNotFoundError:
                print("Varning: Configuration files not found")

    def setup_ui(self):
        # Header
        tk.Label(self, text="Preferences:").grid(row=0, column=0, padx=20, pady=(20, 10), sticky=tk.W, columnspan=3)

        # Pages stylesheet input
        tk.Label(self, text="Stylesheet file for pages:").grid(row=1, column=0, sticky=tk.W, padx=(20, 0))
        self.style_var = tk.StringVar()
        entry = tk.Entry(self, width=50, textvariable=self.style_var)
        entry.grid(row=1, column=1, padx=(0, 5), sticky=tk.EW)
        btn_browse = tk.Button(self, text="Browse", command=FileSelectorDialog([("Stylesheet Files", "*.css")]).get_path)
        btn_browse.grid(row=1, column=2, padx=(0, 20))
