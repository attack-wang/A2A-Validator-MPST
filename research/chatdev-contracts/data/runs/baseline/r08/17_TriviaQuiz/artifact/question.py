'''
question.py
Defines the Question class, which represents a single trivia question.
Supports both multiple-choice and short-answer question types with
robust answer validation:
  - Multiple choice: accepts the correct option's letter (e.g. 'B'),
    its full text (e.g. 'Paris'), or a combined form (e.g. 'B. Paris').
    Text belonging to a NON-correct option is rejected.
  - Short answer: case-insensitive comparison with alternative
    accepted answers separated by '|' (e.g. "7|seven").
Also provides JSON (de)serialization for configurable question banks.
'''
class Question:
    """Represents a single trivia question (multiple-choice or short-answer)."""
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    def __init__(self, question_id, question_text, question_type, answer,
                 options=None, topic="General", explanation=""):
        """
        Initialize a Question instance.
        Args:
            question_id: Unique identifier for the question.
            question_text: The text of the question.
            question_type: Either "multiple_choice" or "short_answer".
            answer: The correct answer (letter for MCQ, text for short answer).
            options: List of answer options for multiple-choice questions.
            topic: The topic/category of the question.
            explanation: Optional explanation shown in the review.
        """
        self.question_id = question_id
        self.question_text = question_text
        self.question_type = question_type
        self.answer = answer
        self.options = options or []
        self.topic = topic
        self.explanation = explanation
    def is_multiple_choice(self):
        """Return True if this is a multiple-choice question."""
        return self.question_type == self.MULTIPLE_CHOICE
    def check_answer(self, user_answer):
        """
        Check whether the user's answer is correct.
        For multiple-choice questions, accepts the correct option's letter
        (e.g. 'B'), the option's text (e.g. 'Paris'), or a combined form
        (e.g. 'B. Paris'). Text of a non-correct option is rejected.
        For short-answer questions, performs a case-insensitive,
        whitespace-tolerant comparison and supports alternatives
        separated by '|'.
        Returns True if correct, False otherwise.
        """
        if user_answer is None:
            return False
        normalized = str(user_answer).strip()
        if not normalized:
            return False
        if self.is_multiple_choice():
            return self._check_multiple_choice(normalized)
        return self._check_short_answer(normalized)
    def _check_multiple_choice(self, normalized):
        """
        Validate a multiple-choice answer.
        Only the option referenced by self.answer (by letter or by text)
        is accepted; matching the text of any other option is incorrect.
        """
        answer_str = str(self.answer).strip()
        # Candidate forms of the user's input: the raw input plus the
        # input with a leading letter prefix (e.g. 'B. ') removed, so
        # combined entries like 'B. Paris' are understood.
        candidates = [normalized.lower()]
        stripped = self._extract_option_text(normalized)
        if stripped.lower() not in candidates:
            candidates.append(stripped.lower())
        # Direct match against the stored answer (letter or text).
        for candidate in candidates:
            if candidate == answer_str.lower():
                return True
        # Match against each option, but accept it only if that option
        # is the one the stored answer letter refers to.
        for option in self.options:
            option_str = str(option).strip()
            letter = option_str[:1].lower() if option_str and option_str[0].isalpha() else ""
            option_text = self._extract_option_text(option_str).lower()
            if any(candidate == letter or candidate == option_text
                   for candidate in candidates):
                if self._option_matches_answer(option_str):
                    return True
        return False
    def _option_matches_answer(self, option_str):
        """
        Return True if the given option string is the option referenced
        by self.answer (i.e. its leading letter equals the answer letter).
        """
        answer_letter = str(self.answer).strip().upper()
        option_letter = option_str[:1].upper() if option_str and option_str[0].isalpha() else ""
        return option_letter == answer_letter
    def _check_short_answer(self, normalized):
        """
        Validate a short-answer response (case-insensitive).
        Alternative accepted answers may be separated by '|',
        e.g. "7|seven" accepts both '7' and 'seven'.
        """
        accepted = [alt.strip().lower() for alt in str(self.answer).split("|")]
        return normalized.lower() in accepted
    @staticmethod
    def _extract_option_text(option):
        """
        Strip a leading letter prefix like 'A. ', 'B) ' or 'C:' from a
        string and return the remaining text. Handles both 'A. Text'
        and 'A.Text' forms; returns the input unchanged otherwise.
        """
        text = str(option).strip()
        if len(text) >= 2 and text[0].isalpha() and text[1] in (".", ")", ":"):
            remainder = text[2:].lstrip()
            return remainder if remainder else text
        return text
    def get_correct_answer_display(self):
        """Return a human-readable string of the correct answer."""
        if self.is_multiple_choice():
            letter = str(self.answer).strip().upper()
            for option in self.options:
                option_text = str(option).strip()
                if option_text[:1].upper() == letter:
                    return option_text
            return str(self.answer)
        return str(self.answer)
    def format_for_display(self):
        """Return a formatted string of the question with its options (if any)."""
        lines = [self.question_text]
        for option in self.options:
            lines.append("   " + str(option))
        return "\n".join(lines)
    def to_dict(self):
        """Serialize the question to a dictionary (JSON-friendly)."""
        data = {
            "id": self.question_id,
            "type": self.question_type,
            "question": self.question_text,
            "answer": self.answer,
            "topic": self.topic,
        }
        if self.options:
            data["options"] = list(self.options)
        if self.explanation:
            data["explanation"] = self.explanation
        return data
    @classmethod
    def from_dict(cls, data):
        """Build a Question instance from a dictionary (e.g. loaded from JSON)."""
        return cls(
            question_id=data.get("id"),
            question_text=data.get("question", ""),
            question_type=data.get("type", cls.SHORT_ANSWER),
            answer=data.get("answer", ""),
            options=data.get("options"),
            topic=data.get("topic", "General"),
            explanation=data.get("explanation", ""),
        )