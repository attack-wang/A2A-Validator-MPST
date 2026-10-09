class GuessValidator:
    def __init__(self, valid_words=None, word_length=5):
        self.valid_words = valid_words
        ...
    def validate(self, raw):
        # returns (ok, cleaned_or_error)