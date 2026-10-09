class ShortAnswerQuestion(Question):
    """A free-form short-answer question, optionally with accepted alternatives."""
    def __init__(self, question_text, correct_answer, alternatives=None, topic="General", explanation=""):
        super().__init__(question_text, correct_answer, topic, explanation, question_type="short_answer")
        self.alternatives = list(alternatives or [])
    def check_answer(self, user_answer):
        answer = self.normalize(user_answer)
        accepted = [self.normalize(self.correct_answer)] + [self.normalize(a) for a in self.alternatives]
        return answer in accepted and answer != ""
    def get_correct_answer(self):
        if self.alternatives:
            return f"{self.correct_answer} (also accepted: {', '.join(self.alternatives)})"
        return str(self.correct_answer)