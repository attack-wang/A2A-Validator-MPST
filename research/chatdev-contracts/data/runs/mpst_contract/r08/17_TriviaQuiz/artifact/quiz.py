"""Core quiz engine: questions, answer checking, scoring, and review."""

import random

LETTERS = "abcdefghij"


class Question:
    """A single trivia question (multiple-choice or short answer)."""

    def __init__(self, topic, qtype, text, choices, answer):
        self.topic = topic
        self.qtype = qtype
        self.text = text
        self.choices = list(choices)
        self.answer = answer

    @classmethod
    def from_dict(cls, data):
        qtype = str(data.get("type", "short")).lower()
        if qtype not in ("mc", "short"):
            raise ValueError("question type must be 'mc' or 'short', got %r" % data.get("type"))
        text = str(data["question"]).strip()
        if not text:
            raise ValueError("question text cannot be empty")
        answer = str(data["answer"]).strip()
        if not answer:
            raise ValueError("answer cannot be empty")
        choices = [str(c).strip() for c in data.get("choices", []) if str(c).strip()]
        if qtype == "mc":
            if len(choices) < 2:
                raise ValueError("multiple-choice question needs at least 2 choices")
            if answer not in choices:
                choices.append(answer)
        return cls(str(data.get("topic", "General")), qtype, text, choices, answer)

    @staticmethod
    def _norm(value):
        return " ".join(str(value).lower().split())

    def is_correct(self, response):
        if self.qtype == "mc":
            choice = self.match_choice(response)
            return choice is not None and self._norm(choice) == self._norm(self.answer)
        return self._norm(response) == self._norm(self.answer)

    def match_choice(self, response):
        """Return the choice matching full text first, then a letter (a, b, c...)."""
        resp = str(response).strip()
        for choice in self.choices:
            if self._norm(choice) == self._norm(resp):
                return choice
        letter = resp.lower()
        if len(letter) == 1 and letter in LETTERS and LETTERS.index(letter) < len(self.choices):
            return self.choices[LETTERS.index(letter)]
        return None

    def display(self, index):
        kind = "multiple choice" if self.qtype == "mc" else "short answer"
        lines = ["Q%d [%s - %s] %s" % (index, self.topic, kind, self.text)]
        if self.qtype == "mc":
            for letter, choice in zip(LETTERS, self.choices):
                lines.append("   %s) %s" % (letter, choice))
            lines.append("   (enter a letter or the full answer)")
        return "\n".join(lines)


class Quiz:
    """Runs a quiz over a list of Question objects and tracks the score."""

    def __init__(self, questions, shuffle=False):
        self.questions = list(questions)
        if shuffle:
            random.shuffle(self.questions)
        self.results = {}  # Question -> (raw_response, correct_bool)

    def _ask(self, question):
        while True:
            try:
                response = input("Your answer: ").strip()
            except EOFError:
                return None
            if response:
                return response
            print("Please enter a non-empty answer (or press Ctrl+C to quit).")

    def run(self):
        print("=== Trivia Quiz ===")
        print("Answer every question, then press Enter. Ctrl+C stops early.")
        total = len(self.questions)
        try:
            for index, question in enumerate(self.questions, start=1):
                print()
                print(question.display(index))
                response = self._ask(question)
                if response is None:
                    print("\nInput ended early; finishing the quiz now.")
                    break
                correct = question.is_correct(response)
                self.results[question] = (response, correct)
                print("Correct!" if correct else "Incorrect.")
        except KeyboardInterrupt:
            print("\nQuiz stopped early by user.")
        answered = len(self.results)
        score = sum(1 for _, ok in self.results.values() if ok)
        print("\n=== Results ===")
        print("Answered: %d of %d" % (answered, total))
        print("Total correct answers: %d" % score)
        if answered:
            print("Score: %.1f%%" % (100.0 * score / answered))
        return score

    def review(self):
        """Print the full answer key next to the user's responses."""
        print("\n=== Answer Review ===")
        if not self.questions:
            print("No questions available.")
            return
        for index, question in enumerate(self.questions, start=1):
            response, correct = self.results.get(question, ("", None))
            if correct is None:
                status = "SKIPPED"
            elif correct:
                status = "CORRECT"
            else:
                status = "WRONG"
            print("Q%d [%s] %s" % (index, status, question.text))
            print("   Your answer: %s" % (response if response else "(not answered)"))
            print("   Correct answer: %s" % question.answer)