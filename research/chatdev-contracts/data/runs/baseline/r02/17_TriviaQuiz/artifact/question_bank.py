'''
question_bank.py
Provides the QuestionBank class, responsible for loading, saving,
filtering and managing collections of Question objects.
Supported storage format: JSON files with the structure:
{
    "questions": [
        {
            "question": "What is the capital of France?",
            "type": "multiple_choice",
            "choices": ["London", "Paris", "Berlin", "Madrid"],
            "answer": "Paris",
            "topic": "Geography"
        },
        ...
    ]
}
"answer" may be a string or a list of acceptable strings (useful for
short-answer questions).
'''
import json
import os
import random
from question import Question
class QuestionBank:
    """Loads, stores, filters and saves trivia questions."""
    def __init__(self, questions=None):
        """Initialize the bank, optionally with an initial list of Questions."""
        self.questions = list(questions) if questions else []
    # ------------------------------------------------------------------ #
    # Loading / saving
    # ------------------------------------------------------------------ #
    @classmethod
    def from_json(cls, filepath):
        """Create a QuestionBank by loading questions from a JSON file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Question bank file not found: '{filepath}'")
        with open(filepath, "r", encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in '{filepath}': {exc}") from exc
        raw_questions = data.get("questions", []) if isinstance(data, dict) else data
        if not isinstance(raw_questions, list):
            raise ValueError(f"'{filepath}' does not contain a list of questions.")
        questions = []
        skipped = 0
        for i, item in enumerate(raw_questions, start=1):
            try:
                questions.append(Question.from_dict(item))
            except (ValueError, TypeError, AttributeError) as exc:
                skipped += 1
                print(f"  [warning] Skipping malformed question #{i}: {exc}")
        if skipped:
            print(f"  [info] Loaded {len(questions)} questions "
                  f"({skipped} malformed entries skipped).")
        return cls(questions)
    def to_json(self, filepath):
        """Save all questions in the bank to a JSON file."""
        payload = {"questions": [q.to_dict() for q in self.questions]}
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
    # ------------------------------------------------------------------ #
    # Management
    # ------------------------------------------------------------------ #
    def add_question(self, question):
        """Append a Question instance to the bank."""
        if not isinstance(question, Question):
            raise TypeError("add_question expects a Question instance.")
        self.questions.append(question)
    def get_topics(self):
        """Return a sorted list of the distinct topics in the bank."""
        return sorted({q.topic for q in self.questions})
    def get_questions(self, topic=None, count=None, shuffle=False):
        """
        Return a list of questions, optionally filtered and limited.
        Args:
            topic (str, optional): keep only questions of this topic
                (case-insensitive). None means all topics.
            count (int, optional): maximum number of questions to return.
            shuffle (bool): randomize question order before limiting.
        """
        pool = list(self.questions)
        if topic:
            wanted = topic.strip().lower()
            pool = [q for q in pool if q.topic.lower() == wanted]
        if shuffle:
            random.shuffle(pool)
        if count is not None:
            pool = pool[:max(0, count)]
        return pool
    def __len__(self):
        return len(self.questions)