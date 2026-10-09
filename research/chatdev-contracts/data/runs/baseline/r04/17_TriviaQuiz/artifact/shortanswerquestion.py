class ShortAnswerQuestion(Question):
    """A trivia question that expects a free-form (typed) answer."""
    def display(self):
        """Return the question text with a short-answer prompt hint."""
        return "{}\n  (Type your answer)".format(self.text)