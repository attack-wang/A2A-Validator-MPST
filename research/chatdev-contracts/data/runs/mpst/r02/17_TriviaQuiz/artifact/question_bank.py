'''
question_bank.py
Loads and manages a configurable bank of quiz questions from a JSON file.
Expected JSON schema:
{
    "questions": [
        {
            "type": "multiple_choice",
            "topic": "Geography",
            "question": "What is the capital of France?",
            "choices": ["London", "Paris", "Berlin", "Madrid"],
            "answer": "Paris",            // choice text ...
            "answer": 1,                  // ... or a zero-based choice index
            "explanation": "Optional explanation shown with the answers."
        },
        {
            "type": "short_answer",
            "topic": "Science",
            "question": "Which planet is known as the Red Planet?",
            "answer": ["Mars", "the red planet"],
            "explanation": "Optional explanation."
        }
    ]
}
Revision notes (fix for reported SyntaxError):
    - The shipped file contained ONLY the body of the multiple-choice branch
      of the question factory, so the "return" at line 5 sat at module top
      level -> SyntaxError: 'return' outside function (raised at import time
      from main.py line 22, aborting the whole program).
    - Restored the complete module: imports, the QuestionBankError exception
      imported by main.py, and the full QuestionBank class, with the orphaned
      fragment now properly enclosed (and indented) inside _build_question().
'''
import json
import random
from question import MultipleChoiceQuestion, ShortAnswerQuestion
class QuestionBankError(Exception):
    """Raised when a question bank file cannot be loaded or parsed."""
class QuestionBank:
    """Holds quiz questions loaded from a JSON file."""
    def __init__(self, questions=None):
        self.questions = list(questions) if questions else []
    def __len__(self):
        return len(self.questions)
    @classmethod
    def load_from_json(cls, path):
        """Load and validate a question bank from a JSON file."""
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except FileNotFoundError:
            raise QuestionBankError(f"file not found: {path}")
        except json.JSONDecodeError as exc:
            raise QuestionBankError(f"invalid JSON in '{path}': {exc}")
        except OSError as exc:
            raise QuestionBankError(f"cannot read '{path}': {exc}")
        if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
            raise QuestionBankError(
                f"'{path}' must contain a top-level object with a 'questions' list."
            )
        questions = []
        for number, item in enumerate(data["questions"], start=1):
            try:
                questions.append(cls._build_question(item))
            except (ValueError, TypeError, KeyError) as exc:
                raise QuestionBankError(
                    f"invalid question #{number} in '{path}': {exc}"
                )
        return cls(questions)
    @staticmethod
    def _build_question(item):
        """Build a Question object from one JSON dictionary entry."""
        if not isinstance(item, dict):
            raise ValueError("each question must be a JSON object")
        text = item.get("question")
        if not text:
            raise ValueError("missing required field 'question'")
        answer = item.get("answer")
        if answer is None or answer == "":
            raise ValueError("missing required field 'answer'")
        topic = str(item.get("topic", "General"))
        explanation = str(item.get("explanation", ""))
        q_type = str(item.get("type", "short_answer")).strip().lower()
        if q_type in ("multiple_choice", "multiple choice", "mc"):
            choices = item.get("choices")
            if not isinstance(choices, list) or len(choices) < 2:
                raise ValueError("'choices' must be a list with at least 2 options")
            return MultipleChoiceQuestion(
                text=str(text), choices=choices, answer=answer,
                topic=topic, explanation=explanation
            )
        if q_type in ("short_answer", "short answer", "sa"):
            if isinstance(answer, str):
                answer = [answer]
            if not isinstance(answer, list) or not answer:
                raise ValueError(
                    "'answer' must be a string or a non-empty list of strings"
                )
            return ShortAnswerQuestion(
                text=str(text), answer=answer,
                topic=topic, explanation=explanation
            )
        raise ValueError(f"unknown question type: '{q_type}'")
    def get_topics(self):
        """Return a sorted list of the topics present in the bank."""
        return sorted({question.topic for question in self.questions})
    def get_questions(self, topics=None, count=None, shuffle=True):
        """Select questions, optionally filtered by topic, shuffled and limited."""
        pool = list(self.questions)
        if topics:
            wanted = {str(t).strip().lower() for t in topics if str(t).strip()}
            if wanted:
                pool = [q for q in pool if q.topic.lower() in wanted]
        if shuffle:
            random.shuffle(pool)
        if count is not None:
            pool = pool[:count]
        return pool