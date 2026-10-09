'''
questions.py
Defines the question model classes for the trivia quiz program.
Classes:
    Question               -- base class for all question types
    MultipleChoiceQuestion -- question with lettered choices (A, B, C, ...)
    ShortAnswerQuestion    -- question answered with free-form text
'''
class Question:
    """Base class representing a single trivia question."""
    def __init__(self, question_text, answer, topic="General", question_type="short_answer"):
        self.question_text = str(question_text)
        self.answer = answer
        self.topic = str(topic)
        self.question_type = question_type
    def display(self):
        """Return the question text formatted for display to the user."""
        return self.question_text
    def check_answer(self, user_answer):
        """Return True when the user's answer is correct."""
        raise NotImplementedError("Subclasses must implement check_answer().")
    def get_correct_answer_display(self):
        """Return a human-readable string showing the correct answer."""
        return str(self.answer)
    @staticmethod
    def normalize(text):
        """Normalize text for comparison: trim, lowercase, collapse whitespace."""
        return " ".join(str(text).strip().lower().split())
class MultipleChoiceQuestion(Question):
    """A trivia question that offers lettered multiple-choice options."""
    LETTERS = "ABCDEFGH"
    def __init__(self, question_text, choices, answer, topic="General"):
        super().__init__(question_text, answer, topic, question_type="multiple_choice")
        self.choices = [str(choice) for choice in choices]
        self._letter_map = {letter.lower(): index
                            for index, letter in enumerate(self.LETTERS[:len(self.choices)])}
    def display(self):
        """Return the question text with its lettered choice list."""
        lines = [self.question_text]
        for index, choice in enumerate(self.choices):
            lines.append("  {}) {}".format(self.LETTERS[index], choice))
        return "\n".join(lines)
    def _resolve_choice_index(self, value):
        """Map a letter, 1-based number, or choice text to a choice index."""
        text = self.normalize(value)
        if not text:
            return None
        if len(text) == 1 and text in self._letter_map:
            return self._letter_map[text]
        if text.isdigit():
            number = int(text)
            if 1 <= number <= len(self.choices):
                return number - 1
        for index, choice in enumerate(self.choices):
            if self.normalize(choice) == text:
                return index
        return None
    def check_answer(self, user_answer):
        """Accept a letter (A/B/C/...), a 1-based number, or the choice text."""
        if user_answer is None:
            return False
        correct_index = self._resolve_choice_index(self.answer)
        user_index = self._resolve_choice_index(user_answer)
        if correct_index is not None and user_index is not None:
            return user_index == correct_index
        # Fallback: plain text comparison (e.g. answer stored as exact text).
        return self.normalize(user_answer) == self.normalize(self.answer)
    def get_correct_answer_display(self):
        """Show the correct choice with its letter, e.g. 'B) Paris'."""
        index = self._resolve_choice_index(self.answer)
        if index is not None:
            return "{}) {}".format(self.LETTERS[index], self.choices[index])
        return str(self.answer)
class ShortAnswerQuestion(Question):
    """A trivia question answered with free-form text."""
    def __init__(self, question_text, answer, topic="General", alternatives=None):
        super().__init__(question_text, answer, topic, question_type="short_answer")
        self.alternatives = [self.normalize(alt) for alt in (alternatives or [])]
    def check_answer(self, user_answer):
        """Case-insensitive comparison, honouring optional alternative answers."""
        if user_answer is None:
            return False
        text = self.normalize(user_answer)
        if not text:
            return False
        return text == self.normalize(self.answer) or text in self.alternatives