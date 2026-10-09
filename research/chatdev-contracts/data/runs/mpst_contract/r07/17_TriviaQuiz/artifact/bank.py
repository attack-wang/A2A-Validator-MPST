import json

from quiz import Question

DEFAULT_BANK = [
    {"type": "mc", "topic": "Geography", "question": "What is the capital of France?",
     "choices": ["London", "Paris", "Berlin", "Madrid"], "answer": "B"},
    {"type": "mc", "topic": "Science", "question": "Which planet is known as the Red Planet?",
     "choices": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": "B"},
    {"type": "mc", "topic": "History", "question": "In which year did World War II end?",
     "choices": ["1943", "1944", "1945", "1946"], "answer": "C"},
    {"type": "sa", "topic": "Math", "question": "What is 7 x 8?", "answer": ["56"]},
    {"type": "sa", "topic": "Literature", "question": "Who wrote the play 'Romeo and Juliet'?",
     "answer": ["shakespeare", "william shakespeare"]},
    {"type": "sa", "topic": "Science", "question": "What is the chemical symbol for gold?",
     "answer": ["au"]},
]


def load_bank(path):
    """Load and validate a JSON question bank file, returning Question objects."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list) or not data:
        raise ValueError("Question bank must be a non-empty JSON list of question objects.")
    questions = []
    for index, item in enumerate(data, 1):
        qtype = str(item.get("type", "sa")).strip().lower()
        if qtype not in ("mc", "sa"):
            raise ValueError(f"Question {index}: unknown type '{qtype}' (use 'mc' or 'sa').")
        text = item.get("question")
        answer = item.get("answer")
        if not text or answer is None or answer == "":
            raise ValueError(f"Question {index}: missing 'question' or 'answer' field.")
        choices = item.get("choices") or []
        if qtype == "mc":
            if len(choices) < 2:
                raise ValueError(f"Question {index}: multiple-choice needs at least 2 choices.")
            letter = str(answer).strip().lower()[:1]
            if not ("a" <= letter <= "e") or (ord(letter) - ord("a")) >= len(choices):
                raise ValueError(f"Question {index}: 'answer' must be a valid choice letter.")
        questions.append(Question(qtype, str(text), answer,
                                  [str(c) for c in choices],
                                  str(item.get("topic", "General"))))
    return questions


def get_questions(path=None):
    """Return Question objects from a JSON bank file, or the built-in default bank."""
    if path:
        return load_bank(path)
    return [Question(str(q["type"]), q["question"], q["answer"], q.get("choices"),
                     q.get("topic", "General")) for q in DEFAULT_BANK]