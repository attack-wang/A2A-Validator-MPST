import random


class Question:
    """A single trivia question: multiple-choice ('mc') or short-answer ('sa')."""

    def __init__(self, qtype, text, answer, choices=None, topic="General"):
        self.qtype = qtype
        self.text = text
        self.answer = answer
        self.choices = choices or []
        self.topic = topic

    @staticmethod
    def _norm(value):
        return str(value).strip().lower()

    def _correct_index(self):
        """Resolve the index of the correct choice from the answer letter."""
        letter = self._norm(self.answer)[:1]
        if "a" <= letter <= "z":
            idx = ord(letter) - ord("a")
            if 0 <= idx < len(self.choices):
                return idx
        return -1

    def check(self, response):
        resp = self._norm(response)
        if self.qtype == "mc":
            idx = self._correct_index()
            if idx >= 0:
                # Only the correct choice's text (or its letter) is accepted.
                return resp == self._norm(self.choices[idx]) or resp == self._norm(self.answer)[:1]
            # Fallback: answer stored as full text rather than a letter.
            return resp == self._norm(self.answer)
        answers = self.answer if isinstance(self.answer, list) else [self.answer]
        return resp in {self._norm(a) for a in answers}

    def correct_text(self):
        if self.qtype == "mc" and self.choices:
            idx = self._correct_index()
            if idx >= 0:
                letter = chr(ord("a") + idx)
                return f"{letter.upper()}) {self.choices[idx]}"
        answers = self.answer if isinstance(self.answer, list) else [self.answer]
        return " / ".join(str(a) for a in answers)


class Quiz:
    """Runs a trivia session, tracks the score, and can review correct answers."""

    def __init__(self, questions, show_review=False, shuffle=False):
        self.questions = list(questions)
        if shuffle:
            random.shuffle(self.questions)
        self.show_review = show_review

    def _ask(self, prompt):
        try:
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\n(Quiz interrupted.)")
            return "q"

    def run(self):
        if not self.questions:
            print("No questions available in this bank.")
            return
        total = len(self.questions)
        print("=== Trivia Quiz ===")
        print(f"{total} questions. Type your answer and press Enter ('q' quits early).\n")
        score = 0
        results = []
        for number, q in enumerate(self.questions, 1):
            print(f"Question {number}/{total} [{q.topic}]")
            print(q.text)
            if q.qtype == "mc":
                for letter, choice in zip("ABCDE", q.choices):
                    print(f"  {letter}) {choice}")
            response = self._ask("Your answer: ").strip()
            if response.lower() == "q":
                break
            correct = q.check(response)
            results.append((q, response, correct))
            if correct:
                score += 1
                print("Correct!\n")
            else:
                print("Incorrect.\n")
        print("=== Quiz Complete ===")
        print(f"Total correct answers: {score} / {len(results)} answered ({total} in bank).")
        review = self.show_review
        if not review and results:
            review = self._ask("Display correct answers? (y/n): ").strip().lower() == "y"
        if review:
            print("\n--- Answer Review ---")
            for number, (q, response, correct) in enumerate(results, 1):
                status = "Correct" if correct else "Incorrect"
                print(f"{number}. [{status}] {q.text}")
                print(f"   Your answer: {response if response else '(blank)'}")
                print(f"   Correct answer: {q.correct_text()}")