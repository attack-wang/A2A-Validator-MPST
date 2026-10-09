'''
question_bank.py
Loads and manages configurable question banks from JSON files.
Class:
    QuestionBank - Holds a named collection of Question objects and provides
                   loading from JSON, topic filtering, and shuffling.
Expected JSON format:
    {
        "name": "General Knowledge",
        "questions": [
            {
                "type": "multiple_choice",
                "topic": "Geography",
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "answer": "Paris",
                "explanation": "Paris has been France's capital since..."
            },
            {
                "type": "short_answer",
                "topic": "Science",
                "question": "What gas do plants absorb?",
                "answer": "Carbon dioxide",
                "alternatives": ["CO2"],
                "explanation": "..."
            }
        ]
    }
'''
import json
import os
import random
from question import MultipleChoiceQuestion, ShortAnswerQuestion, Question
class QuestionBank:
    """A named collection of questions loaded from a JSON file."""
    def __init__(self, name, questions=None):
        self.name = name
        self.questions = list(questions or [])
    def __len__(self):
        return len(self.questions)
    @property
    def topics(self):
        """Sorted list of unique topics in this bank."""
        return sorted({q.topic for q in self.questions})
    def add_question(self, question):
        self.questions.append(question)
    def get_questions(self, topic=None, shuffle=False, limit=None):
        """Return questions, optionally filtered by topic, shuffled, and limited."""
        pool = self.questions
        if topic:
            pool = [q for q in pool if q.topic.lower() == topic.lower()]
        pool = list(pool)
        if shuffle:
            random.shuffle(pool)
        if limit is not None:
            pool = pool[:max(0, limit)]
        return pool
    @classmethod
    def load_from_json(cls, filepath):
        """Load a QuestionBank from a JSON file. Raises ValueError on bad data."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        name = data.get("name", os.path.splitext(os.path.basename(filepath))[0])
        bank = cls(name)
        for i, item in enumerate(data.get("questions", [])):
            try:
                bank.questions.append(cls._build_question(item))
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Invalid question at index {i} in '{filepath}': {exc}") from exc
        return bank
    @staticmethod
    def _build_question(item):
        """Convert a JSON dict into the appropriate Question subclass."""
        qtype = str(item.get("type", "short_answer")).strip().lower()
        text = item["question"]
        answer = item["answer"]
        topic = item.get("topic", "General")
        explanation = item.get("explanation", "")
        if qtype in ("multiple_choice", "multiple-choice", "mc"):
            options = item["options"]
            if not isinstance(options, list) or len(options) < 2:
                raise ValueError("multiple-choice questions need at least 2 options")
            return MultipleChoiceQuestion(text, options, answer, topic, explanation)
        elif qtype in ("short_answer", "short-answer", "sa"):
            return ShortAnswerQuestion(text, answer, item.get("alternatives"), topic, explanation)
        else:
            raise ValueError(f"unknown question type '{qtype}'")
def list_bank_files(directory):
    """Return sorted paths of all .json files in a directory."""
    if not os.path.isdir(directory):
        return []
    return [os.path.join(directory, f) for f in sorted(os.listdir(directory)) if f.lower().endswith(".json")]