'''
question.py
Data models for quiz questions.
Defines:
- normalize_text: helper that lowercases and collapses whitespace.
- Question: base class for a single trivia question.
- MultipleChoiceQuestion: question with lettered options (A, B, C, ...).
- ShortAnswerQuestion: free-text question with one or more accepted answers.
JSON question bank format (see question_bank.py for loading):
{
    "title": "My Quiz",
    "questions": [
        {
            "type": "multiple_choice",
            "topic": "Geography",
            "question": "What is the capital of France?",
            "options": ["London", "Paris", "Berlin", "Madrid"],
            "answer": "B"
        },
        {
            "type": "short_answer",
            "topic": "Science",
            "question": "What gas do plants absorb from the air?",
            "answer": ["carbon dioxide", "co2"]
        }
    ]
}
'''
def normalize_text(value):
    """Lowercase a string and collapse all internal whitespace."""
    return " ".join(str(value).strip().lower().split())
class Question:
    """Base class representing a single trivia question."""
    def __init__(self, text, topic="General", question_type="short_answer"):
        if not str(text).strip():
            raise ValueError("Question text cannot be empty.")
        self.text = str(text).strip()
        self.topic = str(topic).strip() or "General"
        self.question_type = question_type
    def is_correct(self, user_answer):
        """Return True if the user's answer is correct."""
        raise NotImplementedError("Subclasses must implement is_correct().")
    def prompt_text(self):
        """Full text displayed to the user when the question is asked."""
        return self.text
    def answer_prompt(self):
        """Hint shown next to the input prompt for this question type."""
        return "Your answer"
    def display_correct_answer(self):
        """Human-readable string of the correct answer (for the review)."""
        raise NotImplementedError("Subclasses must implement display_correct_answer().")
class MultipleChoiceQuestion(Question):
    """A multiple-choice question with lettered options."""
    def __init__(self, text, options, answer, topic="General"):
        super().__init__(text, topic, question_type="multiple_choice")
        if not isinstance(options, (list, tuple)) or len(options) < 2:
            raise ValueError(
                "Multiple-choice question needs at least 2 options: %s" % self.text
            )
        self.options = [str(option).strip() for option in options]
        self.answer_index = self._resolve_answer_index(answer)
    def _resolve_answer_index(self, answer):
        """Convert the configured answer (letter, number, or text) to a 0-based index."""
        if isinstance(answer, bool):
            raise ValueError(
                "Answer must be a letter, number, or option text, not a boolean: %s"
                % self.text
            )
        if isinstance(answer, int):
            index = answer - 1  # treat as 1-based option number
        else:
            text = str(answer).strip()
            if text.isdigit():
                index = int(text) - 1
            elif len(text) == 1 and text.isalpha():
                index = ord(text.upper()) - ord("A")
            else:
                index = None
                for i, option in enumerate(self.options):
                    if normalize_text(option) == normalize_text(text):
                        index = i
                        break
                if index is None:
                    raise ValueError(
                        "Answer %r does not match any option for question: %s"
                        % (answer, self.text)
                    )
        if not (0 <= index < len(self.options)):
            raise ValueError(
                "Answer %r is out of range for question: %s" % (answer, self.text)
            )
        return index
    def _parse_user_answer(self, user_answer):
        """Convert raw user input to a 0-based option index, or None if unparseable."""
        text = str(user_answer).strip()
        if not text:
            return None
        if text.isdigit():
            number = int(text)
            if 1 <= number <= len(self.options):
                return number - 1
            return None
        if len(text) == 1 and text.isalpha():
            index = ord(text.upper()) - ord("A")
            if 0 <= index < len(self.options):
                return index
            return None
        for i, option in enumerate(self.options):
            if normalize_text(option) == normalize_text(text):
                return i
        return None
    def is_correct(self, user_answer):
        index = self._parse_user_answer(user_answer)
        return index is not None and index == self.answer_index
    def prompt_text(self):
        lines = [self.text]
        for i, option in enumerate(self.options):
            lines.append("  %s) %s" % (chr(ord("A") + i), option))
        return "\n".join(lines)
    def answer_prompt(self):
        last_letter = chr(ord("A") + len(self.options) - 1)
        return "Your choice (A-%s, number, or option text)" % last_letter
    def display_correct_answer(self):
        return "%s) %s" % (
            chr(ord("A") + self.answer_index),
            self.options[self.answer_index],
        )
class ShortAnswerQuestion(Question):
    """A free-text question with one or more accepted answers (case-insensitive)."""
    def __init__(self, text, answer, topic="General"):
        super().__init__(text, topic, question_type="short_answer")
        if isinstance(answer, (list, tuple)):
            answers = list(answer)
        else:
            answers = [answer]
        self.accepted_answers = [
            normalize_text(a) for a in answers if str(a).strip()
        ]
        if not self.accepted_answers:
            raise ValueError(
                "Short-answer question needs at least one answer: %s" % self.text
            )
    def is_correct(self, user_answer):
        return normalize_text(user_answer) in self.accepted_answers
    def answer_prompt(self):
        return "Your answer"
    def display_correct_answer(self):
        return " / ".join(self.accepted_answers)