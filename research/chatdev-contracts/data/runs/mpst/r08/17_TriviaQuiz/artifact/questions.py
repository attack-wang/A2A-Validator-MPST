'''
questions.py
Defines the question model used by the trivia quiz program.
Classes:
    Question -- abstract base class representing a single trivia question.
    MultipleChoiceQuestion -- a question that offers lettered options (A, B, C, ...).
    ShortAnswerQuestion -- a free-form question answered with a word or phrase.
Each question knows how to:
    * render itself for display (display),
    * validate a user's answer (check_answer),
    * describe its correct answer (format_correct_answer).
'''
class Question:
    """Base class for all trivia questions."""
    def __init__(self, text, answer, topic="General"):
        if not str(text).strip():
            raise ValueError("Question text must not be empty.")
        self.text = str(text).strip()
        self.answer = answer
        self.topic = str(topic) if topic else "General"
    # -- interface ---------------------------------------------------------
    def check_answer(self, user_answer):
        """Return True if user_answer is correct, else False."""
        raise NotImplementedError("Subclasses must implement check_answer().")
    def display(self):
        """Return the question text (and options, if any) as a string."""
        raise NotImplementedError("Subclasses must implement display().")
    def format_correct_answer(self):
        """Return a human-readable string of the correct answer."""
        raise NotImplementedError("Subclasses must implement format_correct_answer().")
    # -- helpers -----------------------------------------------------------
    @staticmethod
    def _normalize(value):
        """Lowercase, trim and collapse internal whitespace."""
        return " ".join(str(value).strip().lower().split())
class MultipleChoiceQuestion(Question):
    """A question with a fixed list of options, answered by letter, number or text."""
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def __init__(self, text, options, answer, topic="General"):
        super().__init__(text, answer, topic)
        if not options or len(options) < 2:
            raise ValueError(
                "A multiple-choice question needs at least two options: %r" % self.text
            )
        self.options = [str(option).strip() for option in options]
        self.correct_index = self._resolve_answer(answer)
    def _resolve_answer(self, answer):
        """Map the configured answer (letter, number or text) to an option index."""
        if isinstance(answer, bool):
            raise ValueError("Answer must be a letter, number or option text, not a boolean.")
        if isinstance(answer, int):
            index = answer
        else:
            text = str(answer).strip()
            if not text:
                raise ValueError("Answer must not be empty.")
            if len(text) == 1 and text.isalpha():
                index = self.LETTERS.find(text.upper())
            elif text.isdigit():
                index = int(text) - 1  # 1-based option number
            else:
                index = None
                for i, option in enumerate(self.options):
                    if self._normalize(option) == self._normalize(text):
                        index = i
                        break
        if index is None or not (0 <= index < len(self.options)):
            raise ValueError(
                "Answer %r does not match any option of question: %s" % (answer, self.text)
            )
        return index
    def check_answer(self, user_answer):
        """Accept the option letter (A-D), the option number (1-based) or the option text."""
        text = str(user_answer).strip()
        if not text:
            return False
        if len(text) == 1 and text.isalpha():
            index = self.LETTERS.find(text.upper())
            if index < 0 or index >= len(self.options):
                return False  # letter outside the offered range -> wrong, not error
            return index == self.correct_index
        if text.isdigit():
            index = int(text) - 1
            if 0 <= index < len(self.options):
                return index == self.correct_index
            return False
        return self._normalize(text) == self._normalize(self.options[self.correct_index])
    def display(self):
        lines = [self.text]
        for i, option in enumerate(self.options):
            lines.append("  %s) %s" % (self.LETTERS[i], option))
        return "\n".join(lines)
    def format_correct_answer(self):
        return "%s) %s" % (self.LETTERS[self.correct_index], self.options[self.correct_index])
class ShortAnswerQuestion(Question):
    """A free-form question; the answer is compared case-insensitively."""
    def __init__(self, text, answer, alternatives=None, topic="General"):
        super().__init__(text, answer, topic)
        alternatives = alternatives or []
        if isinstance(alternatives, str):
            alternatives = [alternatives]
        self.alternatives = [str(a) for a in alternatives]
    def _accepted_answers(self):
        return [self.answer] + list(self.alternatives)
    def check_answer(self, user_answer):
        normalized = self._normalize(user_answer)
        if not normalized:
            return False
        return any(self._normalize(acc) == normalized for acc in self._accepted_answers())
    def display(self):
        return self.text
    def format_correct_answer(self):
        return str(self.answer)