'''
question_bank.py
Loads and manages collections of trivia questions from JSON question-bank
files. The JSON format is:
{
  "title": "My Trivia Bank",
  "questions": [
    {
      "type": "multiple_choice",          // or "short_answer"
      "question": "What is ...?",
      "choices": ["A text", "B text"],    // required for multiple_choice
      "answer": "B text",                 // choice text or letter for MC;
                                          // string or list of strings for short_answer
      "topic": "Science",                 // optional
      "explanation": "Because ..."        // optional, shown in the answer review
    }
  ]
}
'''
import json
import random
from question import Question
class QuestionBank:
    """A collection of trivia questions loaded from a JSON file."""
    def __init__(self, questions=None, title="Trivia Quiz", source=None):
        """Build a bank from an optional list of Question objects."""
        self.title = title
        self.source = source
        self._questions = []
        for question in questions or []:
            self.add_question(question)
    @classmethod
    def from_json(cls, path):
        """Load a question bank from a JSON file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Could not parse '{path}' as JSON: {exc}") from exc
        except OSError as exc:
            raise OSError(f"Could not read question bank file '{path}': {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError(f"Question bank '{path}' must be a JSON object.")
        title = data.get("title", "Trivia Quiz")
        raw_questions = data.get("questions", [])
        if not isinstance(raw_questions, list):
            raise ValueError(f"'questions' in '{path}' must be a list.")
        bank = cls(title=title, source=path)
        for position, raw in enumerate(raw_questions, start=1):
            bank.add_question(cls._build_question(raw, position))
        return bank
    @staticmethod
    def _build_question(raw, position):
        """Convert one raw JSON entry into a validated Question object."""
        if not isinstance(raw, dict):
            raise ValueError(f"Question #{position} must be a JSON object.")
        try:
            return Question(
                text=raw.get("question", ""),
                question_type=raw.get("type", Question.SHORT_ANSWER),
                correct_answer=raw.get("answer"),
                choices=raw.get("choices"),
                topic=raw.get("topic", "General"),
                explanation=raw.get("explanation"),
            )
        except ValueError as exc:
            raise ValueError(f"Question #{position}: {exc}") from exc
    def add_question(self, question):
        """Append a Question to the bank."""
        if not isinstance(question, Question):
            raise TypeError("add_question expects a Question instance.")
        self._questions.append(question)
    def __len__(self):
        """Return the number of questions in the bank."""
        return len(self._questions)
    def __iter__(self):
        """Iterate over the questions in bank order."""
        return iter(self._questions)
    def topics(self):
        """Return a sorted list of unique topics."""
        return sorted({q.topic for q in self._questions})
    def topic_counts(self):
        """Return a dict mapping each topic to its question count."""
        counts = {}
        for q in self._questions:
            counts[q.topic] = counts.get(q.topic, 0) + 1
        return counts
    def select(self, topic=None, shuffle=False, limit=None):
        """Return questions filtered by topic, optionally shuffled and limited."""
        questions = list(self._questions)
        if topic:
            wanted = topic.strip().lower()
            questions = [q for q in questions if q.topic.lower() == wanted]
        if shuffle:
            random.shuffle(questions)
        if limit is not None:
            if limit <= 0:
                raise ValueError("--limit must be a positive integer.")
            questions = questions[:limit]
        return questions