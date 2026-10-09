'''
question_bank.py
Loads trivia questions from JSON question-bank files and builds the set of
questions used for a quiz session.
'''
import json
import os
import random
from question import question_from_dict, MultipleChoiceQuestion
class QuestionBankError(Exception):
    """Raised when a question bank file cannot be read or parsed."""
class QuestionBank:
    """A collection of questions loaded from one or more JSON bank files."""
    def __init__(self):
        self.questions = []
        self.bank_names = []
    def load_file(self, path):
        """Load all questions from a single JSON question-bank file."""
        if not os.path.exists(path):
            raise QuestionBankError(f"Question bank file not found: '{path}'")
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise QuestionBankError(f"'{path}' is not valid JSON: {exc}") from exc
        except OSError as exc:
            raise QuestionBankError(f"Could not read '{path}': {exc}") from exc
        if isinstance(data, dict):
            name = str(data.get("name", os.path.basename(path)))
            raw_questions = data.get("questions", [])
        elif isinstance(data, list):
            name = os.path.basename(path)
            raw_questions = data
        else:
            raise QuestionBankError(f"'{path}' must contain a JSON object or list.")
        if not isinstance(raw_questions, list):
            raise QuestionBankError(f"'questions' in '{path}' must be a list.")
        loaded = 0
        for i, item in enumerate(raw_questions, start=1):
            try:
                self.questions.append(question_from_dict(item))
                loaded += 1
            except ValueError as exc:
                raise QuestionBankError(f"'{path}' question #{i}: {exc}") from exc
        self.bank_names.append(name)
        return loaded
    def load_files(self, paths):
        """Load every question bank listed in `paths`; returns total loaded."""
        total = 0
        for path in paths:
            total += self.load_file(path)
        return total
    def available_topics(self):
        """Return a sorted list of the distinct topics across all questions."""
        return sorted({q.topic for q in self.questions})
    def build_quiz(self, count=0, topics=None, shuffle_questions=True, shuffle_choices=True):
        """Select and prepare the questions for one quiz session."""
        selected = list(self.questions)
        if topics:
            wanted = {t.strip().lower() for t in topics}
            selected = [q for q in selected if q.topic.strip().lower() in wanted]
        if not selected:
            return []
        if shuffle_questions:
            random.shuffle(selected)
        if count and count > 0:
            selected = selected[:count]
        if shuffle_choices:
            for q in selected:
                if isinstance(q, MultipleChoiceQuestion):
                    q.shuffle_choices()
        return selected