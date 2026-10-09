'''
question.py
Defines the trivia question model: a base Question class plus
MultipleChoiceQuestion and ShortAnswerQuestion subclasses, and a factory
(question_from_dict) that builds question objects from JSON dictionaries.
'''
import random
import re
class Question:
    """Base class for all trivia questions."""
    def __init__(self, text, answer, topic="General", explanation=""):
        self.text = str(text)
        self.answer = str(answer)
        self.topic = str(topic)
        self.explanation = str(explanation)
    @staticmethod
    def normalize(value):
        """Lowercase, strip, and collapse whitespace for fair comparison."""
        return re.sub(r"\s+", " ", str(value).strip().lower())
    def display(self):
        """Return the question text (subclasses add formatting)."""
        return self.text
    def is_correct(self, user_answer):
        """Return True if the normalized answer matches."""
        return self.normalize(user_answer) == self.normalize(self.answer)
class MultipleChoiceQuestion(Question):
    """A question with lettered choices, answered by letter or full text."""
    def __init__(self, text, choices, answer, topic="General", explanation=""):
        super().__init__(text, answer, topic, explanation)
        self.choices = [str(c) for c in choices]
    def display(self):
        """Render the question plus lettered choices (a, b, c, ...)."""
        lines = [self.text]
        for i, choice in enumerate(self.choices):
            lines.append(f"   {chr(ord('a') + i)}) {choice}")
        return "\n".join(lines)
    def shuffle_choices(self):
        """Randomly reorder the choices (the answer text stays valid)."""
        random.shuffle(self.choices)
    def is_correct(self, user_answer):
        """Accept 'b', 'b)', 'b.', or the full answer text."""
        normalized = self.normalize(user_answer)
        if not normalized:
            return False
        letter = normalized[0]
        if len(normalized) <= 3 and letter.isalpha() and normalized[1:2] in ("", ")", "."):
            index = ord(letter.lower()) - ord("a")
            if 0 <= index < len(self.choices):
                return self.normalize(self.choices[index]) == self.normalize(self.answer)
        return normalized == self.normalize(self.answer)
class ShortAnswerQuestion(Question):
    """A free-text question with a primary answer plus acceptable alternatives."""
    def __init__(self, text, answer, acceptable_answers=None, topic="General", explanation=""):
        super().__init__(text, answer, topic, explanation)
        self.acceptable_answers = [str(a) for a in (acceptable_answers or [])]
    def is_correct(self, user_answer):
        """Match against the primary answer and all acceptable alternatives."""
        normalized = self.normalize(user_answer)
        if not normalized:
            return False
        return normalized == self.normalize(self.answer) or any(
            normalized == self.normalize(a) for a in self.acceptable_answers
        )
def question_from_dict(data):
    """Build a Question subclass instance from a JSON dictionary."""
    if not isinstance(data, dict):
        raise ValueError("Each question must be a JSON object.")
    qtype = str(data.get("type", "short_answer")).strip().lower()
    text = data.get("question")
    if not text or not str(text).strip():
        raise ValueError("Question is missing its 'question' text.")
    topic = str(data.get("topic", "General"))
    explanation = str(data.get("explanation", ""))
    if qtype in ("multiple_choice", "multiple-choice", "mc"):
        choices = data.get("choices")
        if not isinstance(choices, list) or len(choices) < 2:
            raise ValueError(f"Multiple-choice question '{text}' needs at least 2 choices.")
        answer = data.get("answer")
        if answer is None or not str(answer).strip():
            raise ValueError(f"Multiple-choice question '{text}' is missing an answer.")
        if str(answer).strip() not in [str(c).strip() for c in choices]:
            raise ValueError(f"Answer for '{text}' must be one of its choices.")
        return MultipleChoiceQuestion(str(text), [str(c) for c in choices], str(answer), topic, explanation)
    elif qtype in ("short_answer", "short-answer", "sa"):
        answer = data.get("answer")
        if answer is None or not str(answer).strip():
            raise ValueError(f"Short-answer question '{text}' is missing an answer.")
        acceptable = data.get("acceptable_answers", [])
        if not isinstance(acceptable, list):
            raise ValueError(f"'acceptable_answers' for '{text}' must be a list.")
        return ShortAnswerQuestion(str(text), str(answer), [str(a) for a in acceptable], topic, explanation)
    else:
        raise ValueError(f"Unknown question type '{qtype}'.")