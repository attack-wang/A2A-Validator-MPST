"""Quiz engine: question model, answer checking, scoring, and review."""
import random


class Question:
    """A single trivia question, either multiple-choice or short-answer."""

    def __init__(self, text, answer, choices=None, topic="General"):
        self.text = str(text)
        self.answer = str(answer)
        self.choices = [str(c) for c in choices] if choices else None
        self.topic = str(topic)

    @property
    def is_multiple_choice(self):
        return bool(self.choices)

    @staticmethod
    def normalize(value):
        return " ".join(str(value).strip().lower().split())

    def check(self, response):
        return self.normalize(response) == self.normalize(self.answer)

    def accept_choice(self, response):
        """Translate a choice letter (a/b/c/...) into the choice text."""
        if not self.is_multiple_choice:
            return response
        resp = str(response).strip()
        if len(resp) == 1 and resp.isalpha():
            index = ord(resp.upper()) - ord("A")
            if 0 <= index < len(self.choices):
                return self.choices[index]
        return response

    def correct_letter(self):
        if not self.is_multiple_choice:
            return None
        target = self.normalize(self.answer)
        for index, choice in enumerate(self.choices):
            if self.normalize(choice) == target:
                return chr(ord("A") + index)
        return None

    def prompt(self):
        lines = [self.text]
        if self.is_multiple_choice:
            lines.extend(f"  {chr(ord('A') + i)}) {choice}"
                         for i, choice in enumerate(self.choices))
            lines.append("  (enter a letter or the full answer)")
        else:
            lines.append("  (short answer)")
        return "\n".join(lines)


class Quiz:
    """Runs a quiz session, tracks the score, and reports results."""

    def __init__(self, questions, shuffle=False, show_answers=False,
                 input_fn=input, output_fn=print):
        self.questions = [self._as_question(q) for q in questions]
        if shuffle:
            random.shuffle(self.questions)
        self.show_answers = show_answers
        self._input = input_fn
        self._print = output_fn
        self.results = []  # list of (question, response, was_correct)

    @staticmethod
    def _as_question(item):
        if isinstance(item, Question):
            return item
        if isinstance(item, dict):
            return Question(item["text"], item["answer"],
                            item.get("choices"), item.get("topic", "General"))
        raise TypeError(f"Unsupported question entry: {item!r}")

    def run(self):
        self._print("=" * 55)
        self._print("TRIVIA QUIZ".center(55))
        self._print("=" * 55)
        self._print(f"{len(self.questions)} questions. Type 'q' to quit early.")
        for number, question in enumerate(self.questions, 1):
            self._print(f"\nQuestion {number} of {len(self.questions)} "
                        f"[{question.topic}]")
            self._print(question.prompt())
            try:
                response = self._input("Your answer: ").strip()
            except EOFError:
                self._print("\nNo more input available; quiz ended early.")
                break
            except KeyboardInterrupt:
                self._print("\nQuiz interrupted by user.")
                break
            if response.lower() in ("q", "quit"):
                self._print("\nQuiz ended early by user.")
                break
            response = question.accept_choice(response)
            correct = question.check(response)
            self.results.append((question, response, correct))
            self._print("Correct!" if correct else "Incorrect.")
        self.report()

    def score(self):
        return sum(1 for _, _, correct in self.results if correct)

    def report(self):
        total = len(self.results)
        score = self.score()
        self._print("\n" + "=" * 55)
        self._print(f"QUIZ COMPLETE: {score} out of {total} correct")
        if total:
            self._print(f"Score: {score / total * 100:.0f}%")
        if self.show_answers and self.results:
            self._print("\nAnswer review " + "-" * 40)
            for number, (question, response, correct) in enumerate(self.results, 1):
                mark = "Correct" if correct else "Wrong"
                self._print(f"{number}. [{mark}] {question.text}")
                self._print(f"   Your answer: {response}")
                if not correct:
                    letter = question.correct_letter()
                    answer = f"{letter}) {question.answer}" if letter else question.answer
                    self._print(f"   Correct answer: {answer}")