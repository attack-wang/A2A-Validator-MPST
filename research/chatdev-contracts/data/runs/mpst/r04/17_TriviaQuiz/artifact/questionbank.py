import json
import os
import random
from question import Question
class QuestionBank:
    """A named collection of Question objects loaded from a JSON file."""
    def __init__(self, name="Untitled Bank", questions=None):
        self.name = name
        self.questions = list(questions) if questions else []
    @classmethod
    def load_from_json(cls, path):
        """Load a question bank from a JSON file."""
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise ValueError(f"'{path}' is not a valid JSON file: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError(f"'{path}' must contain a JSON object with 'name' and 'questions'.")
        name = data.get("name") or os.path.splitext(os.path.basename(path))[0].title()
        raw_questions = data.get("questions")
        if not isinstance(raw_questions, list) or not raw_questions:
            raise ValueError(f"'{path}' does not contain any questions (expected a non-empty 'questions' list).")
        questions = []
        for index, entry in enumerate(raw_questions, start=1):
            try:
                questions.append(Question.from_dict(entry))
            except ValueError as exc:
                raise ValueError(f"Question #{index} in '{path}' is invalid: {exc}") from exc
        return cls(name=name, questions=questions)
    def add_question(self, question):
        if not isinstance(question, Question):
            raise TypeError("add_question expects a Question instance.")
        self.questions.append(question)
    def topics(self):
        return sorted({q.topic for q in self.questions})
    def filter_by_topic(self, topic):
        wanted = str(topic).strip().lower()
        return [q for q in self.questions if q.topic.lower() == wanted]
    def select(self, topic=None, count=None, shuffle=False):
        questions = list(self.questions)
        if topic:
            questions = self.filter_by_topic(topic)
        if shuffle:
            random.shuffle(questions)
        if count is not None:
            if count <= 0:
                raise ValueError("--num-questions must be a positive integer.")
            questions = questions[:count]
        return questions
    def __len__(self):
        return len(self.questions)