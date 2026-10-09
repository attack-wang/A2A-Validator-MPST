"""Configurable question banks: built-in defaults plus JSON file loading.

A bank entry is a dict with keys:
    topic   (optional str)   category label, defaults to "General"
    type    (optional str)   "mc" for multiple choice or "short" for short answer
    question (required str)  the question text
    choices (required for mc) list of answer options
    answer  (required str)   the correct answer
A JSON file may contain either a bare list of entries or {"questions": [...]}.
"""

import json

DEFAULT_BANK = [
    {"topic": "Geography", "type": "mc",
     "question": "What is the capital of Australia?",
     "choices": ["Sydney", "Melbourne", "Canberra", "Perth"],
     "answer": "Canberra"},
    {"topic": "Science", "type": "mc",
     "question": "Which planet is known as the Red Planet?",
     "choices": ["Venus", "Mars", "Jupiter", "Mercury"],
     "answer": "Mars"},
    {"topic": "Science", "type": "short",
     "question": "What gas do plants absorb from the atmosphere for photosynthesis?",
     "answer": "carbon dioxide"},
    {"topic": "History", "type": "mc",
     "question": "In which year did World War II end?",
     "choices": ["1943", "1944", "1945", "1946"],
     "answer": "1945"},
    {"topic": "History", "type": "short",
     "question": "Who was the first President of the United States?",
     "answer": "George Washington"},
    {"topic": "Literature", "type": "mc",
     "question": "Who wrote the play 'Romeo and Juliet'?",
     "choices": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
     "answer": "William Shakespeare"},
    {"topic": "Technology", "type": "short",
     "question": "What does 'CPU' stand for in computing?",
     "answer": "central processing unit"},
    {"topic": "Mathematics", "type": "mc",
     "question": "What is the value of 7 squared?",
     "choices": ["42", "49", "56", "64"],
     "answer": "49"},
]


def validate_entry(entry, position):
    if not isinstance(entry, dict):
        raise ValueError("entry %d must be an object" % position)
    if "question" not in entry or "answer" not in entry:
        raise ValueError("entry %d needs 'question' and 'answer' fields" % position)
    qtype = str(entry.get("type", "short")).lower()
    if qtype not in ("mc", "short"):
        raise ValueError("entry %d has invalid type %r (use 'mc' or 'short')"
                         % (position, entry.get("type")))
    if qtype == "mc" and len(entry.get("choices", [])) < 2:
        raise ValueError("entry %d is multiple choice but has fewer than 2 choices" % position)


def load_bank(path=None):
    """Return a question bank: the built-in default, or entries from a JSON file."""
    if path is None:
        return [dict(entry) for entry in DEFAULT_BANK]
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        data = data.get("questions", [])
    if not isinstance(data, list) or not data:
        raise ValueError("question bank file must contain a non-empty list of questions")
    for position, entry in enumerate(data, start=1):
        validate_entry(entry, position)
    return data