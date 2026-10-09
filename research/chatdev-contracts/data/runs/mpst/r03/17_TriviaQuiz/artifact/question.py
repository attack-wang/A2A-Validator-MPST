'''
question.py
Defines the Question model classes used by the trivia quiz program.
Classes:
    Question               - Base class representing a single quiz question.
    MultipleChoiceQuestion - A question with lettered options (A, B, C, ...).
    ShortAnswerQuestion    - A question answered with free-form text.
Each question knows how to:
    * render itself for display,
    * validate a user's answer (with sensible normalization),
    * expose its correct answer and an optional explanation.
'''
class Question:
    """Base class for a trivia question."""
    def __init__(self, question_text, correct_answer, topic="General",
                 explanation="", question_type="short_answer"):
        self.question_text = question_text
        self.correct_answer = correct_answer
        self.topic = topic
        self.explanation = explanation
        self.question_type = question_type
    @staticmethod
    def normalize(text):
        """Normalize a text answer for comparison: trim, lower-case, collapse spaces."""
        if text is None:
            return ""
        return " ".join(str(text).strip().lower().split())
    def display(self):
        """Return the question text formatted for display."""
        return self.question_text
    def check_answer(self, user_answer):
        """Return True if the user's answer matches the correct answer."""
        return self.normalize(user_answer) == self.normalize(self.correct_answer)
    def get_correct_answer(self):
        """Return a human-readable string of the correct answer."""
        return str(self.correct_answer)
    def __str__(self):
        return f"[{self.topic}] {self.question_text}"
class MultipleChoiceQuestion(Question):
    """A multiple-choice question with lettered options."""
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def __init__(self, question_text, options, correct_answer, topic="General",
                 explanation=""):
        super().__init__(question_text, correct_answer, topic, explanation,
                         question_type="multiple_choice")
        self.options = list(options)
    def display(self):
        """Return the question text plus its lettered options."""
        lines = [self.question_text]
        for i, option in enumerate(self.options):
            lines.append(f"  {self.LETTERS[i]}) {option}")
        return "\n".join(lines)
    def check_answer(self, user_answer):
        """Accept either the option letter (e.g. 'B') or the full option text."""
        answer = self.normalize(user_answer)
        if not answer:
            return False
        # Match by letter
        if len(answer) == 1 and answer.isalpha():
            index = self.LETTERS.index(answer.upper())
            if 0 <= index < len(self.options):
                return self.normalize(self.options[index]) == self.normalize(self.correct_answer)
        # Match by full text
        return answer == self.normalize(self.correct_answer)
    def get_correct_answer(self):
        """Return the correct answer with its letter, e.g. 'B) Paris'."""
        for i, option in enumerate(self.options):
            if self.normalize(option) == self.normalize(self.correct_answer):
                return f"{self.LETTERS[i]}) {option}"
        return str(self.correct_answer)
class ShortAnswerQuestion(Question):
    """A free-form short-answer question, optionally with accepted alternatives."""
    def __init__(self, question_text, correct_answer, alternatives=None,
                 topic="General", explanation=""):
        super().__init__(question_text, correct_answer, topic, explanation,
                         question_type="short_answer")
        self.alternatives = list(alternatives or [])
    def check_answer(self, user_answer):
        """Accept the correct answer or any listed alternative."""
        answer = self.normalize(user_answer)
        accepted = [self.normalize(self.correct_answer)] + \
                   [self.normalize(a) for a in self.alternatives]
        return answer != "" and answer in accepted
    def get_correct_answer(self):
        """Return the correct answer, noting any accepted alternatives."""
        if self.alternatives:
            return f"{self.correct_answer} (also accepted: {', '.join(self.alternatives)})"
        return str(self.correct_answer)