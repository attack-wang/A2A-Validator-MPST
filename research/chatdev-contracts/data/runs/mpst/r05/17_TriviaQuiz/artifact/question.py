'''
question.py
Defines the Question model used by the trivia quiz program.
A Question can be either a multiple-choice question (with a fixed set of
choices) or a short-answer question (free-form text answer). The class is
responsible for validating its own data and for checking whether a user's
answer is correct.
'''
import re
class Question:
    """Represents a single trivia question."""
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    VALID_TYPES = (MULTIPLE_CHOICE, SHORT_ANSWER)
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def __init__(self, text, question_type, correct_answer, choices=None, topic="General", explanation=None):
        """Create and validate a Question instance."""
        self.text = str(text).strip()
        self.question_type = str(question_type).strip().lower()
        self.topic = str(topic).strip() if topic else "General"
        self.explanation = explanation
        # Normalize correct answer into a tuple of acceptable answers.
        if isinstance(correct_answer, (list, tuple)):
            self.correct_answers = tuple(str(a) for a in correct_answer)
        else:
            self.correct_answers = (str(correct_answer),)
        if self.question_type == self.MULTIPLE_CHOICE:
            if not choices:
                raise ValueError(
                    f"Multiple-choice question {self.text!r} requires a 'choices' list."
                )
            self.choices = [str(c) for c in choices]
        else:
            self.choices = []
        self.validate()
    def validate(self):
        """Validate question data; canonicalize letter answers to choice text."""
        if not self.text:
            raise ValueError("Question text cannot be empty.")
        if self.question_type not in self.VALID_TYPES:
            raise ValueError(
                f"Invalid question type: {self.question_type!r}. "
                f"Valid types: {', '.join(self.VALID_TYPES)}"
            )
        if not self.correct_answers or any(not str(a).strip() for a in self.correct_answers):
            raise ValueError(
                f"Question {self.text!r} must define at least one non-empty correct answer."
            )
        if self.question_type == self.MULTIPLE_CHOICE:
            if len(self.choices) < 2:
                raise ValueError(
                    f"Multiple-choice question {self.text!r} needs at least two choices."
                )
            if len(self.choices) > len(self.LETTERS):
                raise ValueError(
                    f"Multiple-choice questions support at most {len(self.LETTERS)} choices."
                )
            # The correct answer must be a letter in range or match one of the choices.
            idx = self._resolve_choice_index(self.correct_answers[0])
            if idx is None:
                raise ValueError(
                    f"Correct answer {self.correct_answers[0]!r} does not match any "
                    f"choice or letter for question {self.text!r}."
                )
            # Canonicalize a letter answer (e.g. "B") to the full choice text so
            # that check_answer works for banks written either way.
            if len(self.correct_answers[0].strip()) == 1:
                self.correct_answers = (self.choices[idx],) + self.correct_answers[1:]
        else:
            # Short-answer questions ignore any stray 'choices' field.
            self.choices = []
    def _normalize(self, value):
        """Lowercase, collapse whitespace, and strip surrounding punctuation."""
        text = str(value).strip().lower()
        text = re.sub(r"\s+", " ", text)
        return text.strip(" .,!?;:\"'`-_*")
    def _resolve_choice_index(self, user_input):
        """Map a letter ('a'-'z') or exact choice text to a choice index; None if no match."""
        text = self._normalize(user_input)
        if len(text) == 1:
            idx = self.LETTERS.lower().find(text)
            if 0 <= idx < len(self.choices):
                return idx
        for i, choice in enumerate(self.choices):
            if self._normalize(choice) == text:
                return i
        return None
    def check_answer(self, user_answer):
        """Return True if the user's answer is correct."""
        if user_answer is None:
            return False
        normalized = self._normalize(user_answer)
        if self.question_type == self.MULTIPLE_CHOICE:
            # Accept a letter or the full choice text.
            resolved = self._resolve_choice(user_answer)
            return resolved is not None and self._normalize(resolved) in [
                self._normalize(a) for a in self.correct_answers
            ]
        return any(self._normalize(a) == normalized for a in self.correct_answers)
    def _resolve_choice(self, user_input):
        """Return the choice matching a letter or full text input; None if no match."""
        idx = self._resolve_choice_index(user_input)
        if idx is not None:
            return self.choices[idx]
        return None
    def format_choices(self):
        """Return the choices formatted as 'A) text' lines."""
        lines = []
        for i, choice in enumerate(self.choices):
            lines.append(f"  {self.LETTERS[i]}) {choice}")
        return "\n".join(lines)
    @property
    def correct_answer_display(self):
        """Human-readable correct answer, e.g. 'C) Canberra' or 'au'."""
        if self.question_type == self.MULTIPLE_CHOICE:
            idx = self._resolve_choice_index(self.correct_answers[0])
            if idx is not None:
                return f"{self.LETTERS[idx]}) {self.choices[idx]}"
        return " / ".join(self.correct_answers)
    def __str__(self):
        """Return the question text."""
        return self.text