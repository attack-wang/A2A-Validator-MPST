'''
config.py
Loads program settings from settings.json and provides safe defaults.
Class:
    Config - Reads settings.json (falling back to built-in defaults when the
             file is missing or malformed) and exposes the settings as
             attributes consumed by main.py:
                 show_answers_after_quiz - whether to review answers at the end
                 shuffle_questions       - whether to shuffle question order
                 banks_directory         - folder containing *.json banks
                 default_bank            - preselected bank filename
             Also resolves the absolute path to the banks directory.
'''
import json
import os
DEFAULT_SETTINGS = {
    "show_answers_after_quiz": True,
    "shuffle_questions": True,
    "banks_directory": "banks",
    "default_bank": "general_knowledge.json",
}
class Config:
    """Loads settings.json (falling back to defaults) and exposes
    settings as attributes used by main.py."""
    def __init__(self, settings_file="settings.json"):
        base = os.path.dirname(os.path.abspath(__file__))
        self.settings_file = os.path.join(base, settings_file)
        settings = dict(DEFAULT_SETTINGS)
        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                settings.update(loaded)
        except (OSError, json.JSONDecodeError):
            pass  # missing or malformed settings.json -> use defaults
        self.show_answers_after_quiz = bool(settings["show_answers_after_quiz"])
        self.shuffle_questions = bool(settings["shuffle_questions"])
        self.banks_directory = str(settings["banks_directory"])
        self.default_bank = str(settings["default_bank"])
    def banks_path(self):
        """Absolute path to the question-bank directory."""
        if os.path.isabs(self.banks_directory):
            return self.banks_directory
        base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, self.banks_directory)