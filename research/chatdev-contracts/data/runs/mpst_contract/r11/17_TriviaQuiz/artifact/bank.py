"""Question bank utilities and the built-in default bank.

Custom banks are JSON files, either a list of question objects or an
object with a "questions" list. Each question object supports:

    text     (str, required): the question text
    answer   (str, required): the correct answer
    choices  (list of str, optional): enables multiple-choice mode
    topic    (str, optional): topic label, defaults to "General"

Example:
    [
        {"text": "What is 2 + 2?", "answer": "4",
         "choices": ["3", "4", "5"], "topic": "Math"}
    ]
"""
import json

DEFAULT_BANK = [
    {"text": "What is the capital of France?", "answer": "Paris", "topic": "Geography"},
    {"text": "Which planet is known as the Red Planet?", "answer": "Mars", "topic": "Science"},
    {"text": "How many continents are on Earth?", "answer": "7",
     "choices": ["5", "6", "7", "8"], "topic": "Geography"},
    {"text": "Who wrote the play 'Romeo and Juliet'?", "answer": "William Shakespeare",
     "topic": "Literature"},
    {"text": "What is the chemical symbol for gold?", "answer": "Au", "topic": "Science"},
    {"text": "In which year did World War II end?", "answer": "1945", "topic": "History"},
    {"text": "What is the largest animal on Earth?", "answer": "Blue whale",
     "choices": ["African elephant", "Blue whale", "Giraffe", "Orca"], "topic": "Animals"},
    {"text": "What is 12 multiplied by 8?", "answer": "96", "topic": "Math"},
    {"text": "Which gas do plants absorb from the atmosphere for photosynthesis?",
     "answer": "Carbon dioxide",
     "choices": ["Oxygen", "Nitrogen", "Carbon dioxide", "Helium"], "topic": "Science"},
    {"text": "What is the longest river in Africa?", "answer": "Nile", "topic": "Geography"},
]


def validate_entry(entry, index):
    if not isinstance(entry, dict):
        raise ValueError(f"Question {index}: expected a JSON object.")
    if "text" not in entry or "answer" not in entry:
        raise ValueError(f"Question {index}: missing required 'text' or 'answer'.")
    choices = entry.get("choices")
    if choices is not None and (not isinstance(choices, list) or len(choices) < 2):
        raise ValueError(f"Question {index}: 'choices' must be a list with at least 2 options.")
    return entry


def load_bank(path):
    """Load and validate a JSON question bank file."""
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        data = data.get("questions")
    if not isinstance(data, list) or not data:
        raise ValueError("Question bank must be a non-empty list of questions.")
    return [validate_entry(entry, number) for number, entry in enumerate(data, 1)]