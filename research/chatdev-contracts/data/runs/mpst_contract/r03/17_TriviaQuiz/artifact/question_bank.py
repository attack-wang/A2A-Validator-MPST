"""Configurable question banks.

The built-in DEFAULT_BANK is used when no JSON file is supplied. To use a
custom bank, create a JSON file containing a list of objects with keys:
  "text"    (str, required):  the question text
  "answer"  (str, required):  the correct answer
  "choices" (list, optional): multiple-choice options
  "topic"   (str, optional):  category label
"""
from quiz import build_questions, load_json_bank

DEFAULT_BANK = [
    {"text": "What is the capital of France?", "answer": "Paris", "topic": "Geography"},
    {"text": "Which planet is known as the Red Planet?", "answer": "Mars", "topic": "Science"},
    {"text": "How many continents are there on Earth?", "answer": "7", "topic": "Geography"},
    {"text": "Who wrote the play 'Romeo and Juliet'?", "answer": "William Shakespeare",
     "topic": "Literature"},
    {"text": "What is the largest mammal in the world?", "answer": "Blue whale", "topic": "Science"},
    {"text": "What does 'HTTP' stand for?", "answer": "HyperText Transfer Protocol",
     "topic": "Technology"},
    {"text": "In which year did World War II end?", "answer": "1945", "topic": "History"},
    {"text": "What is the chemical symbol for gold?", "answer": "Au", "topic": "Science"},
    {"text": "Which language has the most native speakers worldwide?",
     "answer": "Mandarin Chinese",
     "choices": ["English", "Spanish", "Mandarin Chinese", "Hindi"], "topic": "Language"},
    {"text": "What is 12 x 12?", "answer": "144",
     "choices": ["124", "144", "148", "121"], "topic": "Math"},
]


def get_questions(bank_path=None):
    """Return Question objects from a JSON file, or the built-in default bank."""
    if bank_path:
        return load_json_bank(bank_path)
    return build_questions(DEFAULT_BANK)