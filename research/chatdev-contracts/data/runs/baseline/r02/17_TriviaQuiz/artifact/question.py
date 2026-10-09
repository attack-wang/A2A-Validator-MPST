'''
question.py
Defines the Question class that models a single trivia question.
A question can be either:
  - "multiple_choice": has a list of choices, and the answer is one of them.
  - "short_answer": free-form text answer(s), compared case-insensitively.
'''
class Question:
    """Represents a single trivia question."""
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    LETTERS = "ABCDEFGH"  # labels used for multiple-choice options
    def __init__(self, text, qtype, answer, choices=None, topic="General", explanation=None):
        """
        Initialize a Question.
        Args:
            text (str): The question text.
            qtype (str): Either "multiple_choice" or "short_answer".
            answer (str or list): Correct answer. For short_answer, a list of
                acceptable answers may be provided.
            choices (list, optional): Choices for multiple-choice questions.
            topic (str, optional): Topic/category of the question.
            explanation (str, optional): Optional explanation of the answer.
        """
        self.text = str(text).strip()
        self.type = str(qtype).strip().lower()
        self.topic = str(topic).strip() if topic else "General"
        self.explanation = explanation
        # Normalize the answer into a list of acceptable answer strings.
        if isinstance(answer, (list, tuple)):
            self.answers = [str(a).strip() for a in answer]
        else:
            self.answers = [str(answer).strip()]
        # Normalize choices.
        self.choices = [str(c).strip() for c in choices] if choices else []
        # If an MC answer was stored as a letter label (e.g. "B"), resolve it
        # to the full choice text so answer checking stays consistent.
        if self.type == self.MULTIPLE_CHOICE and len(self.answers) == 1:
            ans = self.answers[0]
            if len(ans) == 1 and ans.upper() in self.LETTERS:
                idx = self.LETTERS.index(ans.upper())
                if idx < len(self.choices):
                    self.answers = [self.choices[idx]]
        self._validate()
    def _validate(self):
        """Validate the question configuration, raising ValueError on problems."""
        if not self.text:
            raise ValueError("Question text cannot be empty.")
        if self.type not in (self.MULTIPLE_CHOICE, self.SHORT_ANSWER):
            raise ValueError(
                f"Unsupported question type: '{self.type}'. "
                f"Use '{self.MULTIPLE_CHOICE}' or '{self.SHORT_ANSWER}'."
            )
        if not self.answers or all(not a for a in self.answers):
            raise ValueError("Question must have at least one correct answer.")
        if self.type == self.MULTIPLE_CHOICE and len(self.choices) < 2:
            raise ValueError("Multiple-choice questions need at least two choices.")
    def is_multiple_choice(self):
        """Return True if this is a multiple-choice question."""
        return self.type == self.MULTIPLE_CHOICE
    def is_short_answer(self):
        """Return True if this is a short-answer question."""
        return self.type == self.SHORT_ANSWER
    def get_correct_answer(self):
        """Return the primary (first) correct answer as a string."""
        return self.answers[0]
    def get_correct_letter(self):
        """Return the letter label of the correct choice for MC questions."""
        if not self.is_multiple_choice():
            return None
        target = self.get_correct_answer().lower()
        for letter, choice in zip(self.LETTERS, self.choices):
            if choice.lower() == target:
                return letter
        return None
    def check_answer(self, user_answer):
        """
        Check whether the user's answer is correct.
        For multiple-choice questions the user may reply either with the
        option letter (e.g. "b") or with the full choice text.
        For short-answer questions the comparison is case-insensitive and
        ignores surrounding whitespace.
        Returns True if correct, False otherwise.
        """
        if user_answer is None:
            return False
        candidate = str(user_answer).strip()
        if not candidate:
            return False
        if self.is_multiple_choice():
            # Letter match (case-insensitive).
            if len(candidate) == 1 and candidate.upper() in self.LETTERS:
                idx = self.LETTERS.index(candidate.upper())
                if idx < len(self.choices):
                    return self.choices[idx].lower() == self.get_correct_answer().lower()
            # Full-text match.
            return candidate.lower() == self.get_correct_answer().lower()
        # Short answer: compare against all acceptable answers.
        lowered = candidate.lower()
        return any(lowered == accepted.lower() for accepted in self.answers)
    def format_choices(self):
        """Return the multiple-choice options formatted as lettered lines."""
        lines = []
        for letter, choice in zip(self.LETTERS, self.choices):
            lines.append(f"  {letter}) {choice}")
        return "\n".join(lines)
    def display(self):
        """Return a human-readable string representing the question prompt."""
        header = f"[{self.topic}] "
        if self.is_multiple_choice():
            prompt = f"{header}{self.text}\n{self.format_choices()}"
            prompt += "\nYour answer (letter or full text): "
        else:
            prompt = f"{header}{self.text}\nYour answer: "
        return prompt
    def to_dict(self):
        """Serialize the question to a dictionary (for saving question banks)."""
        data = {
            "question": self.text,
            "type": self.type,
            "answer": self.answers if self.is_short_answer() and len(self.answers) > 1 else self.answers[0],
            "topic": self.topic,
        }
        if self.is_multiple_choice():
            data["choices"] = self.choices
        if self.explanation:
            data["explanation"] = self.explanation
        return data
    @classmethod
    def from_dict(cls, data):
        """Build a Question from a dictionary (e.g. loaded from JSON)."""
        return cls(
            text=data.get("question", ""),
            qtype=data.get("type", cls.SHORT_ANSWER),
            answer=data.get("answer", ""),
            choices=data.get("choices"),
            topic=data.get("topic", "General"),
            explanation=data.get("explanation"),
        )