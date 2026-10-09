'''
question_bank.py
Loads and manages collections of questions ("question banks") stored as
JSON files. A bank file looks like:
    {
      "name": "General Knowledge",
      "questions": [
        {"type": "multiple_choice", "topic": "Geography", ...},
        {"type": "short_answer", "topic": "Science", ...}
      ]
    }
The QuestionBank can filter questions by topic and/or limit their number,
which makes the quiz fully configurable from the command line.
'''
import json
import os
import random
from question import Question
class QuestionBank:
    """A named, ordered collection of Question objects loaded from JSON."""
    def __init__(self, name="Question Bank", questions=None):
        self.name = name
        self.questions = list(questions or [])
    @classmethod
    def from_json_file(cls, path):
        """Load a bank from a JSON file, validating its basic structure."""
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
            raise ValueError(
                f"{path} is not a valid question bank file: expected a JSON object "
                "with a 'questions' list."
            )
        name = data.get("name") or os.path.splitext(os.path.basename(path))[0]
        questions = []
        for position, item in enumerate(data["questions"], start=1):
            if not isinstance(item, dict):
                raise ValueError(f"{path}: question #{position} is not a JSON object.")
            try:
                questions.append(Question.from_dict(item))
            except ValueError as exc:
                raise ValueError(f"{path}: question #{position}: {exc}") from exc
        if not questions:
            raise ValueError(f"{path} contains no questions.")
        return cls(name=name, questions=questions)
    def topics(self):
        """Return the distinct topics of this bank, in first-seen order."""
        seen = []
        for q in self.questions:
            if q.topic not in seen:
                seen.append(q.topic)
        return seen
    def filter(self, topics=None, count=None, shuffle=False, rng=None):
        """Select questions by topic, optionally shuffled and/or truncated."""
        selected = self.questions
        if topics:
            wanted = {str(t).lower() for t in topics}
            selected = [q for q in selected if q.topic.lower() in wanted]
        selected = list(selected)
        if shuffle:
            (rng or random).shuffle(selected)
        if count is not None:
            if count <= 0:
                raise ValueError("--num must be a positive integer.")
            selected = selected[:count]
        return selected
    def to_json_file(self, path):
        """Write this bank back to a JSON file (useful for authoring banks)."""
        data = {"name": self.name, "questions": [q.to_dict() for q in self.questions]}
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)