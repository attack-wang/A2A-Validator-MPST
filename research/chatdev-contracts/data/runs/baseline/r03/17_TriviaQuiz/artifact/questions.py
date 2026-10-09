'''
Question model classes: base Question, MultipleChoiceQuestion,
ShortAnswerQuestion.
Each subclass knows how to display itself and how to check a user's
answer. Answer comparison is case-insensitive and ignores surrounding
punctuation/whitespace.
'''
import re
class Question:
    """Base class representing a single trivia question."""
    def __init__(self, text, answer, topic="General", explanation=None):
        self.text = text.strip()
        self.answer = answer
        self.topic = topic
        self.explanation = explanation
    def display_text(self):
        return self.text
    def check_answer(self, user_answer):
        raise NotImplementedError("Subclasses must implement check_answer")
    def correct_answer_display(self):
        return str(self.answer)
    @staticmethod
    def _normalize(text):
        """Normalize a string for comparison: lowercase, collapse whitespace, strip punctuation."""
        text = str(text).lower().strip()
        text = re.sub(r'\s+', ' ', text)
        text = text.strip(' .!?,;:"\'()-')
        return text
class MultipleChoiceQuestion(Question):
    """A question with a fixed set of options; user picks one."""
    LETTERS = "ABCDEFGHIJ"
    def __init__(self, text, options, answer, topic="General", explanation=None):
        super().__init__(text, answer, topic, explanation)
        self.options = [str(opt) for opt in options]
        # Resolve answer: could be index (int or numeric str) or option text
        self._resolve_answer()
    def _resolve_answer(self):
        ans = self.answer
        # numeric index?
        if isinstance(ans, int) or (isinstance(ans, str) and ans.strip().isdigit()):
            idx = int(ans)
            if 0 <= idx < len(self.options):
                self.answer = self.options[idx]
                return
        # text match?
        normalized = self._normalize(ans)
        for opt in self.options:
            if self._normalize(opt) == normalized:
                self.answer = opt
                return
        raise ValueError(f"Answer '{ans}' does not match any option for question: {self.text}")
    def display_text(self):
        lines = [self.text]
        for i, opt in enumerate(self.options):
            lines.append(f"  {self.LETTERS[i]}) {opt}")
        return "\n".join(lines)
    def check_answer(self, user_answer):
        user = str(user_answer).strip()
        # Letter choice
        if len(user) == 1 and user.upper() in self.LETTERS[:len(self.options)]:
            idx = self.LETTERS.index(user.upper())
            return self._normalize(self.options[idx]) == self._normalize(self.answer)
        # Number choice (1-based)
        if user.isdigit():
            idx = int(user) - 1
            if 0 <= idx < len(self.options):
                return self._normalize(self.options[idx]) == self._normalize(self.answer)
        # Full text
        return self._normalize(user) == self._normalize(self.answer)
    def correct_answer_display(self):
        idx = next(i for i, o in enumerate(self.options)
                   if self._normalize(o) == self._normalize(self.answer))
        return f"{self.LETTERS[idx]}) {self.answer}"
class ShortAnswerQuestion(Question):
    """A question answered by typing text; comparison is case-insensitive."""
    def __init__(self, text, answer, topic="General", explanation=None, alternatives=None):
        super().__init__(text, answer, topic, explanation)
        self.alternatives = [str(a) for a in (alternatives or [])]
    def check_answer(self, user_answer):
        user = self._normalize(user_answer)
        if not user:
            return False
        acceptable = [self._normalize(self.answer)] + [self._normalize(a) for a in self.alternatives]
        return user in acceptable
    def correct_answer_display(self):
        if self.alternatives:
            return f"{self.answer} (also accepted: {', '.join(self.alternatives)})"
        return self.answer