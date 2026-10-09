'''
question.py
Defines the Question class: a single trivia question that can be either
multiple-choice or short-answer. Handles validation, answer checking
(case-insensitive, tolerant of punctuation/spacing), display formatting
and conversion from JSON dictionary entries.
'''
import re
class Question:
    """A single trivia question (multiple-choice or short-answer)."""
    VALID_TYPES = ("multiple_choice", "short_answer")
    TYPE_ALIASES = {
        "multiple_choice": "multiple_choice",
        "multiplechoice": "multiple_choice",
        "mc": "multiple_choice",
        "choice": "multiple_choice",
        "short_answer": "short_answer",
        "shortanswer": "short_answer",
        "short": "short_answer",
        "sa": "short_answer",
        "text": "short_answer",
    }
    def __init__(self, text, q_type, answer, choices=None, explanation="", topic="General", accept=None):
        q_type = self._canonical_type(q_type)
        if q_type not in self.VALID_TYPES:
            raise ValueError(f"Unknown question type: {q_type!r}")
        if not str(text).strip():
            raise ValueError("Question text must not be empty.")
        if not str(answer).strip():
            raise ValueError("Answer must not be empty.")
        if q_type == "multiple_choice":
            if not choices or len(choices) < 2:
                raise ValueError("Multiple-choice questions need at least two choices.")
            self.choices = [str(choice) for choice in choices]
        else:
            self.choices = []
        self.text = str(text).strip()
        self.q_type = q_type
        self.answer = str(answer).strip()
        self.explanation = str(explanation or "").strip()
        self.topic = str(topic or "General").strip() or "General"
        alternates = [str(a) for a in accept] if accept else []
        self.accepted_answers = [self.answer] + alternates
    @classmethod
    def _canonical_type(cls, q_type):
        """Map free-form type strings onto the two supported question types."""
        key = str(q_type or "short_answer").strip().casefold()
        key = re.sub(r"[\s-]+", "_", key)
        return cls.TYPE_ALIASES.get(key, key)
    @classmethod
    def from_dict(cls, entry):
        """Build a Question from a dictionary (one entry of a JSON bank)."""
        if not isinstance(entry, dict):
            raise TypeError("Question entry must be a JSON object.")
        return cls(
            text=entry.get("question", ""),
            q_type=entry.get("type", "short_answer"),
            answer=entry.get("answer", ""),
            choices=entry.get("choices"),
            explanation=entry.get("explanation", ""),
            topic=entry.get("topic", "General"),
            accept=entry.get("accept"),
        )
    @staticmethod
    def _normalize(text):
        """Lowercase and strip everything except letters and digits."""
        return re.sub(r"[^a-z0-9]+", "", str(text).casefold())
    def is_correct(self, user_answer):
        """Return True if the user's answer matches an accepted answer.
        For multiple-choice questions the choice letter (e.g. 'B') is also
        accepted as long as it points at the correct choice.
        """
        normalized = self._normalize(user_answer)
        if not normalized:
            return False
        if any(self._normalize(accepted) == normalized for accepted in self.accepted_answers):
            return True
        if self.q_type == "multiple_choice" and len(normalized) == 1 and normalized.isalpha():
            index = ord(normalized) - ord("a")
            if 0 <= index < len(self.choices):
                selected = self._normalize(self.choices[index])
                return any(self._normalize(accepted) == selected for accepted in self.accepted_answers)
        return False
    def display(self):
        """Return the question text plus the numbered choices (if any)."""
        lines = [self.text]
        if self.q_type == "multiple_choice":
            for index, choice in enumerate(self.choices):
                lines.append(f"  {chr(ord('A') + index)}) {choice}")
        return "\n".join(lines)
    def correct_answer_display(self):
        """Human-readable string of the correct answer, with letter for MC."""
        if self.q_type == "multiple_choice":
            for index, choice in enumerate(self.choices):
                if any(self._normalize(accepted) == self._normalize(choice) for accepted in self.accepted_answers):
                    return f"{chr(ord('A') + index)}) {choice}"
        return str(self.answer)