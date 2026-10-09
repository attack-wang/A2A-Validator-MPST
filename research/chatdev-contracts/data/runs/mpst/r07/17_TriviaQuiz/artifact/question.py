'''
question.py
Defines the Question class, which represents a single trivia question.
Supports two question types:
  - multiple_choice: a question with a list of choices (A, B, C, ...)
  - short_answer: a free-form text answer
Answers are compared case-insensitively and whitespace-trimmed.
Multiple-choice questions accept either the choice letter (e.g. "B")
or the full choice text.
'''
class Question:
    """Represents a single trivia question."""
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    VALID_TYPES = (MULTIPLE_CHOICE, SHORT_ANSWER)
    def __init__(self, question_text, question_type, answer, choices=None, topic="General"):
        """
        Create and validate a Question instance.
        Args:
            question_text (str): The question text.
            question_type (str): "multiple_choice" or "short_answer".
            answer (str or list): The correct answer. A list means several
                acceptable answers (useful for short-answer questions).
            choices (list or None): Choice strings for multiple-choice
                questions (displayed as A) B) C) ...).
            topic (str): Category label; defaults to "General".
        Raises:
            ValueError: If the type is unknown, a multiple-choice question
                lacks a valid choices list, or the answer is empty.
        """
        question_type = str(question_type).strip().lower()
        if question_type not in self.VALID_TYPES:
            raise ValueError(
                f"Unknown question type '{question_type}'. "
                f"Expected one of: {', '.join(self.VALID_TYPES)}."
            )
        if question_type == self.MULTIPLE_CHOICE:
            if choices is None or not isinstance(choices, list) or not choices:
                raise ValueError(
                    "Multiple-choice questions require a non-empty 'choices' list."
                )
            if len(choices) < 2:
                raise ValueError(
                    "Multiple-choice questions require at least two choices."
                )
        self.text = str(question_text).strip()
        self.type = question_type
        self.topic = str(topic).strip() or "General"
        self.choices = [str(choice).strip() for choice in choices] if choices else None
        # Normalize accepted answers: lowercase and trimmed for comparison.
        if isinstance(answer, list):
            self.answers = [str(a).strip().lower() for a in answer if str(a).strip()]
        else:
            self.answers = [str(answer).strip().lower()]
        if not self.answers:
            raise ValueError("Question must have a non-empty 'answer'.")
        self.raw_answer = answer
    def format_question(self):
        """
        Render the question text, with lettered choices for multiple choice.
        Returns:
            str: The formatted question, ready to display.
        """
        lines = [self.text]
        if self.type == self.MULTIPLE_CHOICE and self.choices:
            for index, choice in enumerate(self.choices):
                lines.append(f"  {chr(ord('A') + index)}) {choice}")
        return "\n".join(lines)
    def check_answer(self, user_answer):
        """
        Check whether the user's answer is correct.
        Comparison is case-insensitive and ignores surrounding whitespace.
        Multiple-choice questions accept either the choice letter (e.g.
        "B", "b)") or the full choice text. Short-answer questions accept
        any of the configured acceptable answers.
        Args:
            user_answer (str): The answer entered by the user.
        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        if user_answer is None:
            return False
        candidate = str(user_answer).strip().lower()
        if not candidate:
            return False
        if self.type == self.MULTIPLE_CHOICE and self.choices:
            # Accept the choice letter, optionally followed by ")" or ".".
            letter = candidate.rstrip(").:").strip()
            if len(letter) == 1 and "a" <= letter <= "z":
                index = ord(letter) - ord("a")
                if not 0 <= index < len(self.choices):
                    return False
                chosen = self.choices[index].strip().lower()
                # Correct if the chosen choice is an accepted answer, or
                # if the answer key itself was given as a choice letter.
                return chosen in self.answers or letter in self.answers
            # Accept the full choice text or any accepted answer text.
            if candidate in self.answers:
                return True
            return any(candidate == choice.strip().lower() for choice in self.choices)
        # Short answer: compare against all accepted answers.
        return candidate in self.answers
    def correct_answer_text(self):
        """
        Return a human-readable string of the correct answer for the review.
        Returns:
            str: The correct answer (lettered choice text for multiple choice).
        """
        if self.type == self.MULTIPLE_CHOICE and self.choices:
            for index, choice in enumerate(self.choices):
                if choice.strip().lower() in self.answers:
                    return f"{chr(ord('A') + index)}) {choice}"
            # Fallback: the answer key may itself be a choice letter.
            for accepted in self.answers:
                if len(accepted) == 1 and "a" <= accepted <= "z":
                    index = ord(accepted) - ord("a")
                    if 0 <= index < len(self.choices):
                        return f"{chr(ord('A') + index)}) {self.choices[index]}"
        if isinstance(self.raw_answer, list):
            return " / ".join(str(a) for a in self.raw_answer)
        return str(self.raw_answer)