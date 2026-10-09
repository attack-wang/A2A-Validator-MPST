"""Question bank loading, validation, and the built-in default bank.

JSON bank format (list of objects):
[
  {"topic": "Geography", "type": "multiple_choice",
   "question": "What is the capital of France?",
   "choices": ["London", "Paris", "Berlin", "Madrid"], "answer": "Paris"},
  {"topic": "Science", "type": "short_answer",
   "question": "Which planet is the Red Planet?", "answer": "Mars"}
]
"""

import json

from quiz import Question

REQUIRED_KEYS = ("topic", "type", "question", "answer")
VALID_TYPES = ("multiple_choice", "short_answer")

DEFAULT_QUESTIONS = [
    {
        "topic": "Geography",
        "type": "multiple_choice",
        "question": "What is the capital of France?",
        "choices": ["London", "Paris", "Berlin", "Madrid"],
        "answer": "Paris",
    },
    {
        "topic": "Science",
        "type": "short_answer",
        "question": "What gas do plants absorb from the atmosphere for photosynthesis?",
        "answer": "carbon dioxide",
    },
    {
        "topic": "History",
        "type": "multiple_choice",
        "question": "In which year did World War II end?",
        "choices": ["1918", "1939", "1945", "1950"],
        "answer": "1945",
    },
    {
        "topic": "Literature",
        "type": "short_answer",
        "question": "Who wrote the play 'Romeo and Juliet'?",
        "answer": "William Shakespeare",
    },
    {
        "topic": "Technology",
        "type": "multiple_choice",
        "question": "What does 'CPU' stand for?",
        "choices": [
            "Central Processing Unit",
            "Computer Personal Unit",
            "Central Program Utility",
            "Core Processing Utility",
        ],
        "answer": "Central Processing Unit",
    },
    {
        "topic": "Astronomy",
        "type": "short_answer",
        "question": "Which planet is known as the Red Planet?",
        "answer": "Mars",
    },
    {
        "topic": "Mathematics",
        "type": "short_answer",
        "question": "What is the value of 12 squared?",
        "answer": "144",
    },
    {
        "topic": "Music",
        "type": "multiple_choice",
        "question": "How many strings does a standard guitar have?",
        "choices": ["4", "5", "6", "7"],
        "answer": "6",
    },
]


def parse_bank(raw):
    """Convert and validate a raw list of question dictionaries into Question objects."""
    if not isinstance(raw, list) or not raw:
        raise ValueError("Question bank must be a non-empty JSON list of question objects.")
    questions = []
    for index, item in enumerate(raw, 1):
        if not isinstance(item, dict):
            raise ValueError(f"Question {index}: each entry must be an object.")
        missing = [key for key in REQUIRED_KEYS if key not in item]
        if missing:
            raise ValueError(f"Question {index}: missing field(s) {', '.join(missing)}.")
        qtype = str(item["type"]).strip().lower()
        if qtype not in VALID_TYPES:
            raise ValueError(f"Question {index}: type must be one of {VALID_TYPES}.")
        choices = item.get("choices", [])
        if qtype == "multiple_choice":
            if not isinstance(choices, list) or len(choices) < 2:
                raise ValueError(
                    f"Question {index}: multiple choice needs a 'choices' list with 2+ items."
                )
        else:
            choices = []
        questions.append(
            Question(
                topic=str(item["topic"]),
                text=str(item["question"]),
                qtype=qtype,
                answer=str(item["answer"]),
                choices=[str(choice) for choice in choices],
            )
        )
    return questions


def load_bank(path):
    """Load and validate a question bank from a JSON file."""
    with open(path, "r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return parse_bank(raw)