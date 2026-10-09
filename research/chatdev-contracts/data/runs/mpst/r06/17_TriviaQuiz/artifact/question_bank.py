'''
question_bank.py
Loads and manages a collection of questions from a JSON question bank file.
Expected JSON format:
{
    "title": "My Quiz",
    "questions": [
        {
            "type": "multiple_choice",
            "question": "What is the capital of France?",
            "choices": ["London", "Paris", "Berlin", "Madrid"],
            "answer": "Paris",
            "explanation": "Paris has been France's capital since ...",
            "topic": "Geography"
        },
        {
            "type": "short_answer",
            "question": "What is 7 x 8?",
            "answer": "56",
            "topic": "Math"
        }
    ]
}
'''
import json
import os
import random
from question import Question
class QuestionBank:
    """Loads trivia questions from a JSON file and manages the question pool."""
    def __init__(self, filepath):
        self.filepath = filepath
        self.title = "Trivia Quiz"
        self.questions = []
    def load(self):
        """Read and parse the JSON question bank. Returns the list of questions."""
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(f"Question bank file not found: {self.filepath}")
        try:
            with open(self.filepath, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Question bank '{self.filepath}' is not valid JSON: {exc}")
        if not isinstance(data, dict):
            raise ValueError("Question bank root must be a JSON object.")
        self.title = str(data.get("title", "Trivia Quiz"))
        raw_questions = data.get("questions", [])
        if not isinstance(raw_questions, list) or not raw_questions:
            raise ValueError("Question bank must contain a non-empty 'questions' list.")
        self.questions = []
        errors = []
        for index, entry in enumerate(raw_questions, start=1):
            try:
                self.questions.append(Question.from_dict(entry))
            except (ValueError, TypeError) as exc:
                errors.append(f"  - question #{index}: {exc}")
        if errors:
            raise ValueError(
                "Question bank contains invalid entries:\n" + "\n".join(errors)
            )
        return self.questions
    def topics(self):
        """Return a sorted list of the distinct topics in the bank."""
        return sorted({q.topic for q in self.questions})
    def filter_by_topic(self, topic):
        """Keep only questions matching the given topic (case-insensitive)."""
        if topic:
            wanted = topic.strip().casefold()
            self.questions = [q for q in self.questions if q.topic.casefold() == wanted]
            if not self.questions:
                raise ValueError(f"No questions found for topic: {topic!r}")
    def shuffle(self):
        """Randomize the order of the questions."""
        random.shuffle(self.questions)
    def __len__(self):
        return len(self.questions)