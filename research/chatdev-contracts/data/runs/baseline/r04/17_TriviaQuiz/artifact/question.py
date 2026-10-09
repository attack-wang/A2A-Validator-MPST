'''
question.py
Defines the question model classes used by the trivia quiz program.
Classes:
    Question -- base class representing a single quiz question
    MultipleChoiceQuestion -- a question displayed with lettered choices
    ShortAnswerQuestion -- a question expecting a free-form typed answer
'''
def normalize_text(value):
    """Return a canonical, comparison-friendly version of the given text."""
    if value is None:
        return ""
    return " ".join(str(value).strip().lower().split())
class Question:
    """Base class representing a single trivia question."""
    def __init__(self, text, answers, topic="General"):
        """
        Initialize a question.
        Args:
            text (str): The question text shown to the user.
            answers (str or list): Acceptable answer(s); any one counts as correct.
            topic (str): Topic/category the question belongs to.
        """
        self.text = str(text)
        if isinstance(answers, (list, tuple, set)):
            self.answers = [str(answer) for answer in answers]
        else:
            self.answers = [str(answers)]
        self.topic = str(topic)
    def display(self):
        """Return the text that should be shown to the user for this question."""
        return self.text
    def check_answer(self, user_answer):
        """Return True when the user's answer matches an accepted answer."""
        candidate = normalize_text(user_answer)
        if not candidate:
            return False
        return any(candidate == normalize_text(correct) for correct in self.answers)
    def correct_answer_text(self):
        """Return a human-readable string listing the correct answer(s)."""
        return " / ".join(self.answers)
class MultipleChoiceQuestion(Question):
    """A trivia question that offers a fixed list of lettered choices."""
    LETTERS = "ABCDEFGHIJ"
    def __init__(self, text, choices, answers, topic="General"):
        """
        Initialize a multiple-choice question.
        Args:
            text (str): The question text shown to the user.
            choices (list): The answer options displayed to the user.
            answers (str or list): Acceptable answer(s) (choice text or letter).
            topic (str): Topic/category the question belongs to.
        """
        super().__init__(text, answers, topic)
        self.choices = [str(choice) for choice in choices]
    def _letter_for(self, choice_text):
        """Return the display letter for a given choice text, or None."""
        normalized = normalize_text(choice_text)
        for index, choice in enumerate(self.choices):
            if normalize_text(choice) == normalized:
                if index < len(self.LETTERS):
                    return self.LETTERS[index]
                return str(index + 1)
        return None
    def _choice_for_letter(self, letter):
        """Return the choice text matching the given display letter, or None."""
        normalized = normalize_text(letter)
        for index, choice in enumerate(self.choices):
            display_letter = self.LETTERS[index] if index < len(self.LETTERS) else str(index + 1)
            if normalize_text(display_letter) == normalized:
                return choice
        return None
    def display(self):
        """Return the question text followed by its lettered choices."""
        lines = [self.text]
        for index, choice in enumerate(self.choices):
            letter = self.LETTERS[index] if index < len(self.LETTERS) else str(index + 1)
            lines.append("  {}) {}".format(letter, choice))
        return "\n".join(lines)
    def check_answer(self, user_answer):
        """
        Return True when the user's answer is correct.
        The user may reply with the choice letter (e.g. 'b'), the full choice
        text (e.g. 'Paris'), or any case/spacing variant of either. This also
        works when the bank stores the answer as a letter instead of text.
        """
        candidate = normalize_text(user_answer)
        if not candidate:
            return False
        for correct in self.answers:
            normalized_correct = normalize_text(correct)
            if candidate == normalized_correct:
                return True
            # Accept the letter when the stored answer is the choice text.
            letter = self._letter_for(normalized_correct)
            if letter is not None and candidate == normalize_text(letter):
                return True
            # Accept the choice text when the stored answer is a letter.
            choice_text = self._choice_for_letter(normalized_correct)
            if choice_text is not None and candidate == normalize_text(choice_text):
                return True
        # Also accept the letter of a choice whose text matches an answer.
        for choice in self.choices:
            letter = self._letter_for(choice)
            if letter is not None and candidate == normalize_text(letter):
                if any(normalize_text(choice) == normalize_text(correct) for correct in self.answers):
                    return True
        return False
    def correct_answer_text(self):
        """Return the correct answer(s) annotated with their choice letters."""
        labeled = []
        for correct in self.answers:
            normalized = normalize_text(correct)
            letter = self._letter_for(normalized)
            if letter is not None:
                labeled.append("{} ({})".format(correct, letter))
                continue
            choice_text = self._choice_for_letter(normalized)
            if choice_text is not None:
                labeled.append("{} ({})".format(choice_text, self._letter_for(choice_text)))
            else:
                labeled.append(correct)
        return " / ".join(labeled)
class ShortAnswerQuestion(Question):
    """A trivia question that expects a free-form (typed) answer."""
    def display(self):
        """Return the question text with a short-answer prompt hint."""
        return "{}\n  (Type your answer)".format(self.text)