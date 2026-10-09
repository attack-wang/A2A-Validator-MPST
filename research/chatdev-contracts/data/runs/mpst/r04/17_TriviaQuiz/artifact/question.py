'''
question.py
Question model for the trivia quiz program.
Defines the Question class, which validates question data, checks user
answers (case- and punctuation-insensitive), deserializes questions from
JSON dictionaries, and provides display helpers for the answer review.
'''
import random
import re
class Question:
    """A single trivia question, either multiple-choice or short-answer."""
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    VALID_TYPES = (MULTIPLE_CHOICE, SHORT_ANSWER)
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def __init__(self, text, question_type, correct_answers, options=None,
                 topic="General", explanation="", question_id=None):
        if question_type not in self.VALID_TYPES:
            raise ValueError(
                f"Invalid question type '{question_type}'. "
                f"Expected one of: {', '.join(self.VALID_TYPES)}"
            )
        if not text or not str(text).strip():
            raise ValueError("Question text must not be empty.")
        if not correct_answers or not [a for a in correct_answers if str(a).strip()]:
            raise ValueError("Question must have at least one correct answer.")
        self.text = str(text).strip()
        self.question_type = question_type
        self.correct_answers = [str(a).strip() for a in correct_answers if str(a).strip()]
        self.topic = str(topic).strip() or "General"
        self.explanation = str(explanation).strip()
        self.question_id = question_id if question_id is not None else ""
        self.options = []
        if question_type == self.MULTIPLE_CHOICE:
            if not options or len(options) < 2:
                raise ValueError("Multiple-choice questions need at least two options.")
            self.options = [str(o).strip() for o in options]
            normalized_options = {self._normalize(o) for o in self.options}
            if not any(self._normalize(a) in normalized_options for a in self.correct_answers):
                raise ValueError(
                    f"Multiple-choice question '{self.text[:50]}...' has correct "
                    "answers that do not match any option."
                )
        self._normalized_correct = [self._normalize(a) for a in self.correct_answers]
    @classmethod
    def from_dict(cls, data):
        """Create a Question instance from a single JSON object."""
        if not isinstance(data, dict):
            raise ValueError(
                f"Question entry must be a JSON object, got: {type(data).__name__}."
            )
        question_type = data.get("type", data.get("question_type"))
        if question_type is None:
            raise ValueError(
                f"Question is missing the required 'type' field: {data.get('text', data)!r}"
            )
        text = data.get("text")
        correct = data.get("correct_answers", data.get("answer"))
        if isinstance(correct, str):
            correct = [correct]
        return cls(
            text=text,
            question_type=question_type,
            correct_answers=correct,
            options=data.get("options"),
            topic=data.get("topic", "General"),
            explanation=data.get("explanation", ""),
            question_id=data.get("id"),
        )
    @staticmethod
    def _normalize(value):
        """Lower-case, strip punctuation and collapse whitespace for fair comparison."""
        text = str(value).strip().lower()
        text = re.sub(r"[^\w\s]", "", text)
        return re.sub(r"\s+", " ", text)
    @staticmethod
    def _letter_index(answer):
        """Map 'a'-'z' or '1'-'99' to a 0-based option index; None otherwise."""
        if len(answer) == 1 and "a" <= answer <= "z":
            return ord(answer) - ord("a")
        if answer.isdigit():
            return int(answer) - 1
        return None
    def check_answer(self, user_answer):
        """Return True when the user's answer matches an accepted correct answer."""
        if user_answer is None:
            return False
        answer = str(user_answer).strip()
        if not answer:
            return False
        if self.question_type == self.MULTIPLE_CHOICE:
            index = self._letter_index(answer.lower())
            if index is not None and 0 <= index < len(self.options):
                return self._normalize(self.options[index]) in self._normalized_correct
        return self._normalize(answer) in self._normalized_correct
    def copy_with_shuffled_options(self):
        """Return a copy of this multiple-choice question with options in random order."""
        if self.question_type != self.MULTIPLE_CHOICE:
            return self
        options = list(self.options)
        random.shuffle(options)
        return Question(
            self.text,
            self.question_type,
            self.correct_answers,
            options=options,
            topic=self.topic,
            explanation=self.explanation,
            question_id=self.question_id,
        )
    @property
    def correct_answer_display(self):
        """Readable string of the correct answer(s) for the review screen."""
        if self.question_type == self.MULTIPLE_CHOICE:
            parts = [
                f"{self.LETTERS[i]}) {option}"
                for i, option in enumerate(self.options)
                if self._normalize(option) in self._normalized_correct
            ]
            return "; ".join(parts) if parts else "; ".join(self.correct_answers)
        return " or ".join(self.correct_answers)