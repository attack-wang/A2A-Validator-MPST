'''
config.py
Defines QuizConfig, which loads, validates, and stores all user-configurable
settings for the trivia quiz program (question bank files, number of
questions, shuffling behaviour, and whether correct answers are revealed
after the quiz).
'''
import json
import os
DEFAULT_CONFIG = {
    "question_bank_files": [
        "question_banks/general.json",
        "question_banks/science.json",
    ],
    "question_count": 0,          # 0 means "use every available question"
    "topics": [],                  # empty list means "all topics"
    "shuffle_questions": True,
    "shuffle_choices": True,
    "show_correct_answers": True,
}
class ConfigError(Exception):
    """Raised when the configuration file is invalid."""
class QuizConfig:
    """Holds all settings that control how a quiz session runs."""
    def __init__(self, **overrides):
        settings = dict(DEFAULT_CONFIG)
        settings.update({k: v for k, v in overrides.items() if v is not None})
        self.question_bank_files = list(settings["question_bank_files"])
        try:
            self.question_count = int(settings["question_count"])
        except (TypeError, ValueError):
            raise ConfigError("'question_count' must be an integer.")
        self.topics = list(settings["topics"])
        self.shuffle_questions = bool(settings["shuffle_questions"])
        self.shuffle_choices = bool(settings["shuffle_choices"])
        self.show_correct_answers = bool(settings["show_correct_answers"])
    @classmethod
    def load(cls, path):
        """Create a QuizConfig from a JSON file, falling back to defaults."""
        if not os.path.exists(path):
            return cls()
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            raise ConfigError(f"Could not read config file '{path}': {exc}") from exc
        if not isinstance(data, dict):
            raise ConfigError(f"Config file '{path}' must contain a JSON object.")
        unknown = set(data) - set(DEFAULT_CONFIG)
        if unknown:
            raise ConfigError(f"Unknown config keys: {', '.join(sorted(unknown))}")
        return cls(**data)
    def summary(self):
        """Return a human-readable summary of current settings."""
        return "\n".join([
            "Quiz configuration:",
            f"  Question banks:       {', '.join(self.question_bank_files)}",
            f"  Question count:       {self.question_count or 'all'}",
            f"  Topics:               {', '.join(self.topics) if self.topics else 'all'}",
            f"  Shuffle questions:    {self.shuffle_questions}",
            f"  Shuffle choices:      {self.shuffle_choices}",
            f"  Show correct answers: {self.show_correct_answers}",
        ])