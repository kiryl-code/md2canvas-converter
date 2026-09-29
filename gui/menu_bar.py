import platform
import tkinter as tk
from gui.views.preferences import PreferencesDialog
from gui.views.help import HelpDialog

class MenuBar(tk.Menu):
    def __init__(self, parent, config_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.config_manager = config_manager

        if platform.system() == "Darwin":
            self.setup_mac()
        else:
            self.setup_default()

        self.setup_help()

    def setup_mac(self):
        self.parent.createcommand("tk::mac::ShowPreferences", self.on_preferences)

    def setup_default(self):
        edit_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Preferences...", command=self.on_preferences)

    def setup_help(self):
        help_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help", command=self.on_help)

    def on_preferences(self):
        PreferencesDialog(self.parent, self.config_manager)

    def on_help(self):
        HelpDialog(self.parent)