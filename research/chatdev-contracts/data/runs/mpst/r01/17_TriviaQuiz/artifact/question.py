'''
question.py
Defines the question models used by the trivia quiz application.
Classes:
    Question               - Base class for a single trivia question.
    MultipleChoiceQuestion - Question with lettered choices (A, B, C, ...).
    ShortAnswerQuestion    - Free-form question with accepted answer(s).
Every question supports:
    display()                -> text shown to the player
    check_answer(user_input) -> True/False
    format_correct_answer()  -> readable correct-answer string for reviews
'''
class Question:
    """Base class representing a single trivia question."""
    def __init__(self, text, answer, topic="General", explanation=""):
        """Store the question text, correct answer, topic, and explanation."""
        self.text = str(text).strip()
        self.answer = answer
        self.topic = str(topic).strip() or "General"
        self.explanation = str(explanation).strip()
    def display(self):
        """Return the question formatted for display to the player."""
        return self.text
    def check_answer(self, user_answer):
        """Return True when the player's answer is correct."""
        raise NotImplementedError("Subclasses must implement check_answer().")
    def format_correct_answer(self):
        """Return a human-readable string describing the correct answer."""
        return str(self.answer)
    def __str__(self):
        """Return the plain question text."""
        return self.text
class MultipleChoiceQuestion(Question):
    """A multiple-choice question whose choices are labelled A, B, C, ..."""
    LETTERS = "ABCDEFGHIJ"
    def __init__(self, text, choices, answer, topic="General", explanation=""):
        """Create a multiple-choice question.
        `answer` may be the full text of the correct choice, the choice's
        letter (e.g. "B"), or its 1-based number (e.g. "2").
        """
        super().__init__(text, answer, topic, explanation)
        self.choices = [str(choice).strip() for choice in choices]
    def display(self):
        """Return the question text plus its lettered choice list."""
        lines = [self.text]
        for index, choice in enumerate(self.choices):
            lines.append("  {}) {}".format(self.LETTERS[index], choice))
        return "\n".join(lines)
    def _answer_index(self):
        """Return the index of the correct choice, or None if unresolvable."""
        target = self._normalize(self.answer)
        for index, choice in enumerate(self.choices):
            if self._normalize(choice) == target:
                return index
        if len(target) == 1 and target in self.LETTERS[:len(self.choices)].lower():
            return self.LETTERS.lower().index(target)
        if target.isdigit():
            number = int(target)
            if 1 <= number <= len(self.choices):
                return number - 1
        return None
    def check_answer(self, user_answer):
        """Accept a letter (A-D), a 1-based number, or the full choice text."""
        index = self._answer_index()
        if index is None:
            return False
        guess = self._normalize(user_answer)
        if not guess:
            return False
        if len(guess) == 1 and guess in self.LETTERS[:len(self.choices)].lower():
            return self.LETTERS.lower().index(guess) == index
        if guess.isdigit():
            number = int(guess)
            if 1 <= number <= len(self.choices):
                return (number - 1) == index
            return False
        return self._normalize(self.choices[index]) == guess
    def format_correct_answer(self):
        """Return the correct choice as "B) Paris" when resolvable."""
        index = self._answer_index()
        if index is not None:
            return "{}) {}".format(self.LETTERS[index], self.choices[index])
        return str(self.answer)
    @staticmethod
    def _normalize(value):
        """Lower-case, trim, and collapse whitespace for comparisons."""
        return " ".join(str(value).strip().lower().split())
class ShortAnswerQuestion(Question):
    """A free-form question checked against one or more accepted answers."""
    def __init__(self, text, answer, topic="General", explanation="", accepted_answers=None):
        """Create a short-answer question.
        `accepted_answers` optionally lists every string that counts as
        correct; when omitted, only `answer` is accepted.
        """
        super().__init__(text, answer, topic, explanation)
        if accepted_answers:
            self.accepted_answers = [str(item) for item in accepted_answers]
        else:
            self.accepted_answers = [str(answer)]
    def display(self):
        """Return the question text with a free-form input hint."""
        return "{}\n  (Type your answer)".format(self.text)
    def check_answer(self, user_answer):
        """Case-insensitively compare the input with every accepted answer."""
        guess = self._normalize(user_answer)
        if not guess:
            return False
        return any(guess == self._normalize(accepted) for accepted in self.accepted_answers)
    def format_correct_answer(self):
        """Return all accepted answers joined with slashes."""
        return " / ".join(self.accepted_answers)
    @staticmethod
    def _normalize(value):
        """Lower-case, trim, and collapse whitespace for comparisons."""
        return " ".join(str(value).strip().lower().split())