'''
question_bank.py
Loading, validation and discovery of question banks.
A question bank is a JSON file with the structure:
    {
      "name": "General Knowledge",
      "description": "Optional description shown in the bank menu.",
      "questions": [
        {
          "type": "multiple_choice",
          "question": "What is the capital of France?",
          "options": ["London", "Paris", "Berlin", "Madrid"],
          "answer": "Paris",
          "topic": "Geography"
        },
        {
          "type": "short_answer",
          "question": "What planet is known as the Red Planet?",
          "answer": "Mars",
          "alternatives": ["the mars"],
          "topic": "Astronomy"
        }
      ]
    }
"answer" for multiple-choice questions may be the option text (recommended),
the option letter ("B") or a zero-based option index (1).
'''
import json
import os
import sys
from questions import MultipleChoiceQuestion, ShortAnswerQuestion
class QuestionBankError(Exception):
    """Raised when a question bank file is missing, unreadable or invalid."""
class QuestionBank:
    """An immutable-by-convention collection of questions loaded from JSON."""
    def __init__(self, name, description="", questions=None, source_path=None):
        self.name = str(name)
        self.description = str(description or "")
        self.questions = list(questions or [])
        self.source_path = source_path
    @classmethod
    def from_file(cls, path):
        """Load and validate a question bank from a JSON file."""
        path = os.fspath(path)
        if not os.path.isfile(path):
            raise QuestionBankError("Question bank file not found: %s" % path)
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise QuestionBankError("Invalid JSON in %s: %s" % (path, exc))
        except OSError as exc:
            raise QuestionBankError("Cannot read %s: %s" % (path, exc))
        if not isinstance(data, dict):
            raise QuestionBankError("%s must contain a JSON object." % path)
        name = data.get("name") or os.path.splitext(os.path.basename(path))[0].replace("_", " ").title()
        description = data.get("description", "")
        raw_questions = data.get("questions")
        if not isinstance(raw_questions, list) or not raw_questions:
            raise QuestionBankError("%s must contain a non-empty 'questions' list." % path)
        questions = [cls._build_question(item, path, position)
                     for position, item in enumerate(raw_questions, start=1)]
        return cls(name=name, description=description, questions=questions, source_path=path)
    @staticmethod
    def _build_question(item, path, position):
        where = "%s, question %d" % (path, position)
        if not isinstance(item, dict):
            raise QuestionBankError("%s: each question must be a JSON object." % where)
        text = item.get("question")
        if not isinstance(text, str) or not text.strip():
            raise QuestionBankError("%s: missing or empty 'question' text." % where)
        if "answer" not in item:
            raise QuestionBankError("%s: missing 'answer'." % where)
        topic = item.get("topic") or "General"
        qtype = str(item.get("type", "short_answer")).strip().lower()
        if qtype in ("multiple_choice", "multiple-choice", "mc", "choice"):
            options = item.get("options")
            if not isinstance(options, list) or len(options) < 2:
                raise QuestionBankError("%s: multiple-choice questions need at least two 'options'." % where)
            try:
                return MultipleChoiceQuestion(text, options, item["answer"], topic=topic)
            except ValueError as exc:
                raise QuestionBankError("%s: %s" % (where, exc))
        elif qtype in ("short_answer", "short-answer", "short", "text"):
            alternatives = item.get("alternatives")
            if alternatives is not None and not isinstance(alternatives, list):
                alternatives = [alternatives]
            return ShortAnswerQuestion(text, item["answer"], alternatives=alternatives, topic=topic)
        else:
            raise QuestionBankError("%s: unknown question type %r (use 'multiple_choice' or 'short_answer')." % (where, qtype))
    def get_questions(self):
        """Return a shallow copy of the question list."""
        return list(self.questions)
    def __len__(self):
        return len(self.questions)
    def __repr__(self):
        return "QuestionBank(name=%r, questions=%d)" % (self.name, len(self.questions))
def discover_banks(directory):
    """Load every valid *.json question bank found in `directory`.
    Invalid files are skipped with a warning printed to stderr.
    Returns a list of QuestionBank objects sorted by name.
    """
    banks = []
    if not os.path.isdir(directory):
        return banks
    for filename in sorted(os.listdir(directory)):
        if not filename.lower().endswith(".json"):
            continue
        path = os.path.join(directory, filename)
        try:
            banks.append(QuestionBank.from_file(path))
        except QuestionBankError as exc:
            print("Warning: skipping %s (%s)" % (path, exc), file=sys.stderr)
    banks.sort(key=lambda bank: bank.name.lower())
    return banks