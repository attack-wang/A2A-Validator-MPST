'''Question model classes for the trivia quiz program.'''
import config
from utils import normalize
class Question:
    '''Base class representing a single quiz question.
    The default answer check performs a normalized string comparison, so
    this class is fully usable on its own (no abstract placeholders).
    '''
    def __init__(self, text, answer, topic="General", points=1):
        '''Store the question text, canonical answer, topic, and point value.'''
        self.text = text
        self.answer = answer
        self.topic = topic
        self.points = points
    def check_answer(self, user_answer):
        '''Return True when the normalized user answer matches the answer.'''
        return normalize(user_answer) == normalize(self.answer)
    def display_question(self):
        '''Return the formatted question text shown to the user.'''
        return self.text
    def display_answer(self):
        '''Return the human-readable correct answer for the review screen.'''
        return self.answer
class MultipleChoiceQuestion(Question):
    '''A question that offers lettered choices (A, B, C, ...).'''
    def __init__(self, text, choices, answer, topic="General", points=1):
        '''Build the question, resolve the correct index, and validate choices.'''
        super().__init__(text, answer, topic, points)
        if not choices:
            raise ValueError("Multiple-choice question needs at least one choice.")
        self.choices = [str(choice) for choice in choices]
        self.correct_index = self._resolve_index(self.answer)
    def _resolve_index(self, answer):
        '''Map an answer like "B", "2", or full choice text to a 0-based index.'''
        given = str(answer).strip()
        # Interpret a single letter (A-H) as a choice label.
        if len(given) == 1 and given.upper() in config.CHOICE_LABELS:
            index = config.CHOICE_LABELS.index(given.upper())
            if index >= len(self.choices):
                raise ValueError("Answer '{}' has no matching choice.".format(given))
            return index
        # Interpret a plain number as a 1-based position.
        if given.isdigit():
            index = int(given) - 1
            if 0 <= index < len(self.choices):
                return index
            raise ValueError("Answer '{}' is out of range.".format(given))
        # Fall back to matching the full choice text (case-insensitive).
        target = normalize(given)
        for index, choice in enumerate(self.choices):
            if normalize(choice) == target:
                return index
        raise ValueError("Answer '{}' does not match any choice.".format(given))
    def check_answer(self, user_answer):
        '''Accept a letter, 1-based number, or full choice text as correct.'''
        given = str(user_answer).strip()
        # Single letter labels are matched directly against the correct index.
        if len(given) == 1 and given.upper() in config.CHOICE_LABELS:
            return config.CHOICE_LABELS.index(given.upper()) == self.correct_index
        # Plain numbers are treated as 1-based positions.
        if given.isdigit():
            return int(given) - 1 == self.correct_index
        # Otherwise compare the normalized text against the correct choice.
        return normalize(given) == normalize(self.choices[self.correct_index])
    def display_question(self):
        '''Return the question text followed by its lettered choices.'''
        lines = [self.text]
        for index, choice in enumerate(self.choices):
            label = config.CHOICE_LABELS[index]
            lines.append("  {}. {}".format(label, choice))
        return "\n".join(lines)
    def display_answer(self):
        '''Return the correct letter and its full choice text.'''
        label = config.CHOICE_LABELS[self.correct_index]
        return "{}. {}".format(label, self.choices[self.correct_index])
class ShortAnswerQuestion(Question):
    '''A question answered with free-form text plus optional alternatives.'''
    def __init__(self, text, answer, alternatives=None, topic="General", points=1):
        '''Build the question and store any accepted alternative answers.'''
        super().__init__(text, answer, topic, points)
        self.alternatives = [str(alt) for alt in (alternatives or [])]
    def check_answer(self, user_answer):
        '''Match the user input against the answer and all alternatives.'''
        given = normalize(user_answer)
        if given == normalize(self.answer):
            return True
        return any(given == normalize(alt) for alt in self.alternatives)
    def display_answer(self):
        '''Return the primary answer plus any alternatives in parentheses.'''
        if self.alternatives:
            return "{} (also accepted: {})".format(
                self.answer, ", ".join(self.alternatives))
        return self.answer