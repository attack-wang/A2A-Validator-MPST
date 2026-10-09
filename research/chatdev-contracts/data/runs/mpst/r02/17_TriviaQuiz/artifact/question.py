'''
question.py
Defines the question data model for the trivia quiz.
Classes:
    Question               -- base class for a single quiz question.
    MultipleChoiceQuestion -- a question with lettered choices (A, B, C, ...).
    ShortAnswerQuestion    -- a free-form text answer question.
Answer checking is tolerant: comparison is case-insensitive, ignores
leading/trailing whitespace, and collapses internal whitespace runs.
Multiple acceptable answers may be supplied (e.g. ["Mars", "the red planet"]).
Revision notes:
    - Restored the full class definitions that were missing from the shipped
      file (it previously contained only the module docstring, which would
      have caused an ImportError once question_bank.py was repaired).
    - MultipleChoiceQuestion accepts the answer either as choice text or as
      a zero-based index into the choices list (e.g. "answer": 1 in JSON),
      resolving the index to the choice text before validation.
    - check_answer safely rejects empty input before the letter check.
    - All feedback strings are ASCII-only for cp1252 console safety.
'''
import re
class Question:
    """Base class for a single quiz question."""
    type_name = "question"
    def __init__(self, text, answer, topic="General", explanation=""):
        text = str(text).strip()
        if not text:
            raise ValueError("question text must not be empty")
        self.text = text
        self.topic = str(topic)
        self.explanation = str(explanation)
        if isinstance(answer, str):
            acceptable = [answer]
        elif isinstance(answer, list):
            acceptable = [str(a).strip() for a in answer if str(a).strip()]
        else:
            acceptable = [str(answer)]
        if not acceptable:
            raise ValueError("at least one acceptable answer is required")
        self.acceptable_answers = acceptable
    @staticmethod
    def _normalize(value):
        """Lowercase, trim, and collapse internal whitespace runs."""
        return re.sub(r"\s+", " ", str(value).strip()).lower()
    def check_answer(self, user_answer):
        """Tolerant comparison of the user's answer against acceptable answers."""
        if user_answer is None:
            return False
        candidate = self._normalize(user_answer)
        if not candidate:
            return False
        return candidate in {self._normalize(a) for a in self.acceptable_answers}
    def correct_answer_display(self):
        """Human-readable string of the correct answer(s) for the review."""
        return " / ".join(self.acceptable_answers)
    def display(self):
        """Return the text shown to the user for this question."""
        return self.text
class MultipleChoiceQuestion(Question):
    """A question that presents lettered choices (A, B, C, ...)."""
    type_name = "multiple_choice"
    def __init__(self, text, choices, answer, topic="General", explanation=""):
        if not isinstance(choices, list) or len(choices) < 2:
            raise ValueError("Multiple choice questions need at least 2 choices.")
        self.choices = [str(choice).strip() for choice in choices]
        # If the answer was supplied as a zero-based index, resolve it to text
        # BEFORE calling the base constructor so normalization/validation and
        # correct_answer_display() work uniformly.
        if isinstance(answer, int) and not isinstance(answer, bool):
            if not (0 <= answer < len(self.choices)):
                raise ValueError(
                    f"answer index {answer} is out of range for "
                    f"{len(self.choices)} choices"
                )
            answer = self.choices[answer]
        super().__init__(text, answer, topic, explanation)
    def display(self):
        """Show the question text followed by lettered choices."""
        lines = [self.text]
        for index, choice in enumerate(self.choices):
            lines.append(f"  {chr(ord('A') + index)}) {choice}")
        return "\n".join(lines)
    def check_answer(self, user_answer):
        """Accept either a choice letter (e.g. 'B') or the full choice text."""
        if user_answer is None:
            return False
        candidate = str(user_answer).strip()
        if not candidate:
            return False
        if len(candidate) == 1 and candidate.isalpha():
            index = ord(candidate.lower()) - ord("a")
            if 0 <= index < len(self.choices):
                normalized_choice = self._normalize(self.choices[index])
                return normalized_choice in {
                    self._normalize(a) for a in self.acceptable_answers
                }
            return False
        return super().check_answer(candidate)
class ShortAnswerQuestion(Question):
    """A free-form text answer question."""
    type_name = "short_answer"