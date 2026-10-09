'''
question_bank.py
Loads and manages collections of questions from JSON question-bank files.
Classes:
    QuestionBankError: Raised when a question bank file is invalid.
    QuestionBank: Holds a list of Question objects and provides filtering,
                  shuffling and selection utilities.
Functions:
    build_question(raw): Convert a raw dictionary into a Question instance.
'''
import json
import random
from question import MultipleChoiceQuestion, ShortAnswerQuestion
class QuestionBankError(Exception):
    """Raised when a question bank file cannot be parsed or is invalid."""
def build_question(raw):
    """Convert a raw question dictionary into a Question instance."""
    if not isinstance(raw, dict):
        raise QuestionBankError("Each question must be a JSON object.")
    q_type = str(raw.get("type", "short_answer")).strip().lower()
    text = raw.get("question")
    answer = raw.get("answer")
    topic = raw.get("topic", "General")
    points = raw.get("points", 1)
    if not text or answer is None:
        raise QuestionBankError(f"Question missing 'question' or 'answer' field: {raw}")
    try:
        points = int(points)
    except (TypeError, ValueError):
        raise QuestionBankError(f"Invalid 'points' value: {points!r}")
    if q_type in ("multiple_choice", "multiple-choice", "mc"):
        choices = raw.get("choices")
        if not isinstance(choices, list) or len(choices) < 2:
            raise QuestionBankError(f"Multiple-choice question needs at least 2 choices: {text}")
        return MultipleChoiceQuestion(text, choices, answer, topic, points)
    if q_type in ("short_answer", "short-answer", "sa"):
        alternatives = raw.get("alternatives", [])
        if not isinstance(alternatives, list):
            raise QuestionBankError(f"'alternatives' must be a list: {text}")
        return ShortAnswerQuestion(text, answer, alternatives, topic, points)
    raise QuestionBankError(f"Unknown question type: {q_type}")
class QuestionBank:
    """A collection of questions loaded from a JSON file."""
    def __init__(self, questions=None, source=""):
        self.questions = list(questions or [])
        self.source = source
    @classmethod
    def load(cls, path):
        """Load a question bank from a JSON file."""
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except FileNotFoundError:
            raise QuestionBankError(f"Question bank file not found: {path}")
        except json.JSONDecodeError as exc:
            raise QuestionBankError(f"Invalid JSON in {path}: {exc}")
        except OSError as exc:
            raise QuestionBankError(f"Cannot read question bank {path}: {exc}")
        if isinstance(data, dict):
            raw_questions = data.get("questions", [])
        elif isinstance(data, list):
            raw_questions = data
        else:
            raise QuestionBankError(f"Question bank must be a JSON object or list: {path}")
        if not isinstance(raw_questions, list):
            raise QuestionBankError(f"'questions' must be a list in {path}")
        questions = []
        for index, raw in enumerate(raw_questions, start=1):
            try:
                questions.append(build_question(raw))
            except QuestionBankError as exc:
                raise QuestionBankError(f"Question #{index} in {path}: {exc}")
        if not questions:
            raise QuestionBankError(f"No questions found in {path}")
        return cls(questions, source=path)
    def topics(self):
        """Return a sorted list of the topics present in the bank."""
        return sorted({q.topic for q in self.questions})
    def filter_by_topic(self, topic):
        """Return a new QuestionBank containing only questions of a topic."""
        if not topic or str(topic).lower() == "all":
            return self
        filtered = [q for q in self.questions if q.topic.lower() == str(topic).lower()]
        return QuestionBank(filtered, source=self.source)
    def select(self, count=None, shuffle=False):
        """Return the list of questions to use, optionally shuffled and limited."""
        questions = list(self.questions)
        if shuffle:
            random.shuffle(questions)
        if count is not None:
            if count < 1:
                raise QuestionBankError("Question count must be at least 1.")
            questions = questions[:count]
        if not questions:
            raise QuestionBankError("No questions selected for the quiz.")
        return questions