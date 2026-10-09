"""Question model and configurable question-bank loading for the trivia quiz."""

import json

DEFAULT_BANK = [
    {"type": "mc", "topic": "Geography", "text": "What is the capital of Australia?",
     "choices": ["Sydney", "Canberra", "Melbourne", "Perth"], "answer": "B"},
    {"type": "short", "topic": "Science",
     "text": "What gas do plants absorb from the atmosphere for photosynthesis?",
     "answer": "carbon dioxide"},
    {"type": "mc", "topic": "History", "text": "In which year did World War II end?",
     "choices": ["1943", "1944", "1945", "1946"], "answer": "C"},
    {"type": "short", "topic": "Literature",
     "text": "Who wrote the play 'Romeo and Juliet'?", "answer": "Shakespeare"},
    {"type": "mc", "topic": "Science", "text": "What is the chemical symbol for gold?",
     "choices": ["Go", "Gd", "Au", "Ag"], "answer": "C"},
    {"type": "short", "topic": "Technology", "text": "What does 'CPU' stand for?",
     "answer": "central processing unit"},
]


class Question:
    """A single trivia question: multiple-choice ('mc') or short-answer ('short')."""

    def __init__(self, text, qtype, answer, choices=None, topic="General"):
        self.text = text
        self.qtype = qtype
        self.answer = answer
        self.choices = choices or []
        self.topic = topic

    @staticmethod
    def _normalize(value):
        return " ".join(str(value).lower().split())

    def is_correct(self, response):
        resp = str(response).strip()
        if self.qtype == "mc":
            if resp.upper() == self.answer:
                return True
            correct_text = self.choices[ord(self.answer) - ord("A")]
            return self._normalize(resp) == self._normalize(correct_text)
        return self._normalize(resp) == self._normalize(self.answer)

    def display_answer(self):
        if self.qtype == "mc":
            return f"{self.answer}) {self.choices[ord(self.answer) - ord('A')]}"
        return self.answer


def _build_question(item, index):
    if not isinstance(item, dict):
        raise ValueError(f"Question {index}: expected an object")
    qtype = str(item.get("type", "short")).strip().lower()
    if qtype not in ("mc", "short"):
        raise ValueError(f"Question {index}: unknown type '{qtype}' (use 'mc' or 'short')")
    text = str(item.get("text", "")).strip()
    if not text:
        raise ValueError(f"Question {index}: missing 'text'")
    topic = str(item.get("topic", "General"))
    answer = item.get("answer")
    if qtype == "mc":
        choices = [str(choice) for choice in item.get("choices", [])]
        if not 2 <= len(choices) <= 8:
            raise ValueError(f"Question {index}: 'mc' needs between 2 and 8 choices")
        letter = str(answer).strip().upper() if answer is not None else ""
        if len(letter) != 1 or not "A" <= letter <= chr(ord("A") + len(choices) - 1):
            raise ValueError(f"Question {index}: 'answer' must be a letter A-"
                             f"{chr(ord('A') + len(choices) - 1)}")
        return Question(text, "mc", letter, choices, topic)
    if answer is None or not str(answer).strip():
        raise ValueError(f"Question {index}: missing 'answer'")
    return Question(text, "short", str(answer).strip(), None, topic)


def load_bank(path=None):
    """Load questions from a JSON file, or the built-in bank when path is None.

    Accepts either a top-level list of question objects or {"questions": [...]}.
    """
    if path is None:
        items = DEFAULT_BANK
    else:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        items = data.get("questions") if isinstance(data, dict) else data
        if not isinstance(items, list):
            raise ValueError("Bank file must be a list of questions or {'questions': [...]}")
    return [_build_question(item, i + 1) for i, item in enumerate(items)]