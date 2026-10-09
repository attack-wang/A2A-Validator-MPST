    def check_answer(self, user_answer):
        normalized = self._normalize(user_answer)
        letter = self.correct_letter()
        if letter and normalized == self._normalize(letter):
            return True                      # accepted letter, e.g. "B"
        return any(normalized == self._normalize(c) for c in self.choices) \
               or super().check_answer(user_answer)