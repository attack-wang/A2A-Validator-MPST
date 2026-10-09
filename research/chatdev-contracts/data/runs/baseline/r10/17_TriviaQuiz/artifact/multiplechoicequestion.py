class MultipleChoiceQuestion(Question):
    """A question with a fixed set of choices (answer by letter or text)."""
    LETTERS = "ABCDEFGH"
    def __init__(self, text, choices, answer, topic="General", points=1):
        super().__init__(text, answer, topic, points)
        self.choices = list(choices)
    def correct_letter(self):
        for index, choice in enumerate(self.choices):
            if self._normalize(choice) == self._normalize(self.answer):
                return self.LETTERS[index]
        return None
    def check_answer(self, user_answer):
        normalized = self._normalize(user_answer)
        letter = self.correct_letter()
        if letter and normalized == self._normalize(letter):
            return True                      # accepted letter, e.g. "B"
        return any(normalized == self._normalize(c) for c in self.choices) \
               or super().check_answer(user_answer)