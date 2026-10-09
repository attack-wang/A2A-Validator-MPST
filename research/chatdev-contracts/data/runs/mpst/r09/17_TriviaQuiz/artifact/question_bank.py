'''
question_bank.py
Loads, validates, and stores a collection of Question objects from a
JSON question-bank file. This makes the quiz's question set fully
configurable: users can edit the JSON file (or point the program at a
different one) without touching any code.
Expected JSON schema:
{
  "questions": [
    {
      "type": "multiple_choice" | "short_answer",
      "topic": "Geography",              (optional, default "General")
      "question": "What is the capital of France?",
      "choices": ["Paris", "London"],    (required for multiple_choice)
      "answer": "Paris"                  (string or list of accepted answers)
    },
    ...
  ]
}
'''
import json
import os
from question import Question
class QuestionBank:
    """A configurable collection of trivia questions."""
    def __init__(self, questions=None):
        self._questions = list(questions) if questions else []
    # ---------- loading ----------
    @classmethod
    def from_json_file(cls, path):
        """Create a QuestionBank from a JSON file. Raises FileNotFoundError
        or ValueError with a helpful message on problems."""
        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"Question bank file not found: '{path}'"
            )
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Could not parse '{path}' as JSON: {exc}"
            ) from exc
        if not isinstance(data, dict) or "questions" not in data:
            raise ValueError(
                f"Invalid question bank format in '{path}': "
                "top-level object must contain a 'questions' list."
            )
        raw_questions = data["questions"]
        if not isinstance(raw_questions, list) or not raw_questions:
            raise ValueError(
                f"Invalid question bank format in '{path}': "
                "'questions' must be a non-empty list."
            )
        questions = []
        for index, entry in enumerate(raw_questions, start=1):
            try:
                questions.append(cls._build_question(entry))
            except (ValueError, KeyError, TypeError) as exc:
                raise ValueError(
                    f"Problem with question #{index} in '{path}': {exc}"
                ) from exc
        return cls(questions)
    @staticmethod
    def _build_question(entry):
        """Convert one raw JSON dict into a validated Question."""
        if not isinstance(entry, dict):
            raise ValueError("each question must be a JSON object")
        question_type = entry.get("type", Question.SHORT_ANSWER)
        text = entry.get("question") or entry.get("text")
        if text is None:
            raise ValueError("missing required field 'question'")
        answer = entry.get("answer")
        if answer is None:
            raise ValueError("missing required field 'answer'")
        choices = entry.get("choices")
        topic = entry.get("topic", "General")
        return Question(
            text=text,
            question_type=question_type,
            answer=answer,
            choices=choices,
            topic=topic,
        )
    # ---------- access ----------
    def add_question(self, question):
        self._questions.append(question)
    def get_questions(self):
        return list(self._questions)
    def __len__(self):
        return len(self._questions)