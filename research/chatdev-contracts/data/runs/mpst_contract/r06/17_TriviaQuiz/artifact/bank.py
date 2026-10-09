"""Question bank loading.

Built-in default bank, or load a custom JSON file:
[
  {"topic": "Geography", "type": "mc", "question": "...",
   "options": ["A text", "B text", "C text", "D text"], "answer": 1},
  {"topic": "Math", "type": "short", "question": "...",
   "answer": "56", "accept": ["fifty-six"]}
]
"answer" for "mc" is the zero-based index of the correct option.
"accept" (optional) lists extra accepted spellings for short answers.
"""
import json

from quiz import Question

DEFAULT_BANK = [
    {"topic": "Geography", "type": "mc", "question": "What is the capital of France?",
     "options": ["London", "Paris", "Berlin", "Madrid"], "answer": 1},
    {"topic": "Science", "type": "mc", "question": "Which planet is known as the Red Planet?",
     "options": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": 1},
    {"topic": "Science", "type": "mc", "question": "What gas do plants absorb from the atmosphere?",
     "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": 2},
    {"topic": "History", "type": "mc", "question": "In which year did World War II end?",
     "options": ["1943", "1944", "1945", "1946"], "answer": 2},
    {"topic": "Math", "type": "short", "question": "What is 7 x 8?",
     "answer": "56", "accept": ["fifty-six"]},
    {"topic": "Literature", "type": "short", "question": "Who wrote 'Romeo and Juliet'?",
     "answer": "shakespeare", "accept": ["william shakespeare"]},
    {"topic": "Technology", "type": "short", "question": "What does 'CPU' stand for?",
     "answer": "central processing unit"},
    {"topic": "Geography", "type": "short", "question": "What is the largest ocean on Earth?",
     "answer": "pacific", "accept": ["pacific ocean"]},
]

_MC_TYPES = {"mc", "multiple", "multiple_choice", "choice"}


def _build(entry):
    if not isinstance(entry, dict) or "question" not in entry:
        raise ValueError("each entry must be an object with a 'question' field")
    qtype = str(entry.get("type", "mc")).lower()
    topic = str(entry.get("topic", "General"))
    if qtype in _MC_TYPES:
        options = list(entry.get("options") or [])
        answer = int(entry["answer"])
        if not options or not (0 <= answer < len(options)):
            raise ValueError("multiple-choice needs 'options' and an 'answer' index in range")
        return Question(entry["question"], "mc", answer, options=options, topic=topic)
    if "answer" not in entry:
        raise ValueError("short-answer needs an 'answer' field")
    accepts = [str(a) for a in (entry.get("accept") or [])]
    return Question(entry["question"], "short", str(entry["answer"]),
                    accepts=accepts, topic=topic)


def load_bank(path=None):
    if path:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = DEFAULT_BANK
    if isinstance(data, dict):
        data = data.get("questions", [])
    if not isinstance(data, list) or not data:
        raise ValueError("question bank must be a non-empty JSON list of question objects")
    questions = []
    for i, entry in enumerate(data, 1):
        try:
            questions.append(_build(entry))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid question entry #{i}: {exc}") from exc
    return questions