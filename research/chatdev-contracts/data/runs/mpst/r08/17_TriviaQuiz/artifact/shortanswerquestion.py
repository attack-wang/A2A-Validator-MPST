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