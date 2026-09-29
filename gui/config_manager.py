import json
from tkinter import BooleanVar, StringVar


class ConfigManager:
    def __init__(self, config_path="user-config.json", default_path="default-config.json"):
        self.path = config_path
        self.default_path = default_path
        self.config = self.load_config()

        self.page_styles = StringVar(value=self.config.get("page_style"))
        self.feedback_style = StringVar(value=self.config.get("feedback_style"))
        self.syntax_highlight = StringVar(value=self.config.get("syntax_highlight"))
        self.run_gui = BooleanVar(value=self.config.get("run_gui"))

    def load_config(self) -> dict:
        # TODO: move this logic from gui?
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Create user-config if there is no one
            # and apply default settings
            try:
                with open(self.default_path, "r") as f:
                    default_config = json.load(f)

                    with open(self.path, "w") as cf:
                        json.dump(default_config, cf)
                        return self.load_config()
            except (FileNotFoundError, json.JSONDecodeError) as e:
                raise e
