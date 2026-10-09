class ShortAnswerQuestion(Question):
    """A free-form question checked against one or more accepted answers."""
    def __init__(self, text, answer, topic="General", explanation="", accepted_answers=None):
        super().__init__(text, answer, topic, explanation)
        if accepted_answers:
            self.accepted_answers = [str(a) for a in accepted_answers]
        else:
            self.accepted_answers = [str(answer)]
    def display(self):
        return f"{self.text}\n  (Type your answer)"
    def check_answer(self, user_answer):
        normalized = self._normalize(user_answer)
        if not normalized:
            return False
        return any(normalized == self._normalize(acc) for acc in self.accepted_answers)
    def format_correct_answer(self):
        return " / ".join(self.accepted_answers)
    @staticmethod
    def _normalize(value):
        return " ".join(str(value).strip().lower().split())