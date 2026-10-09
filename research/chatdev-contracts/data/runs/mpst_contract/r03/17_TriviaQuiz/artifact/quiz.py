"""Core quiz engine: question model, scoring, and result reporting."""
import json
import random


class Question:
    """A single trivia question (multiple-choice or short answer)."""

    def __init__(self, text, answer, choices=None, topic="General"):
        self.text = str(text)
        self.answer = str(answer).strip()
        self.choices = [str(c).strip() for c in choices] if choices else None
        self.topic = str(topic)

    def prompt(self):
        """Display the question and return the user's raw answer string."""
        print(f"[{self.topic}] {self.text}")
        if self.choices:
            for i, choice in enumerate(self.choices, 1):
                print(f"  {i}. {choice}")
            ask = "Your answer (number or text): "
        else:
            ask = "Your answer: "
        while True:
            raw = input(ask).strip()
            if raw:
                return raw
            print("Please enter an answer.")

    def is_correct(self, raw):
        """Case-insensitive check; numeric input may select a multiple-choice option.

        The raw guess is compared against the answer first, so a literal numeric
        answer is never misjudged by option-number remapping.
        """
        guess = raw.strip().lower()
        if guess == self.answer.lower():
            return True
        if self.choices and guess.isdigit():
            index = int(guess) - 1
            if 0 <= index < len(self.choices):
                return self.choices[index].lower() == self.answer.lower()
        return False


def build_questions(items):
    """Convert a list of question dictionaries into Question objects."""
    return [Question(item["text"], item["answer"],
                     item.get("choices"), item.get("topic", "General"))
            for item in items]


def load_json_bank(path):
    """Load a question bank from a JSON file (list of question objects)."""
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("Question bank JSON must be a list of question objects.")
    return build_questions(data)


class Quiz:
    """Runs questions, tracks the score, and reports results."""

    def __init__(self, questions, shuffle=False):
        self.questions = list(questions)
        if shuffle:
            random.shuffle(self.questions)
        self.results = []  # (number, question, raw_answer, correct)

    def run(self):
        print("=" * 40)
        print("            TRIVIA QUIZ")
        print("=" * 40)
        print(f"Answer {len(self.questions)} questions. Good luck!")
        for number, question in enumerate(self.questions, 1):
            print(f"\n--- Question {number} of {len(self.questions)} ---")
            try:
                raw = question.prompt()
            except EOFError:
                # Input stream closed (e.g. Ctrl-D / piped stdin exhausted):
                # stop asking questions gracefully and report what was answered.
                print("\nInput ended. Finishing the quiz early.")
                break
            except KeyboardInterrupt:
                print("\nInterrupted. Finishing the quiz early.")
                break
            correct = question.is_correct(raw)
            self.results.append((number, question, raw, correct))
            print("Correct!" if correct else "Incorrect.")

    def report(self, show_answers=False):
        total = len(self.results)
        score = sum(1 for _, _, _, ok in self.results if ok)
        print("\n" + "=" * 40)
        print("           QUIZ COMPLETE")
        print("=" * 40)
        print(f"Total correct answers: {score} / {total}")
        if show_answers:
            print("\n--- Answer Review ---")
            for number, question, raw, correct in self.results:
                status = "Correct" if correct else "Incorrect"
                print(f"\n{number}. [{status}] {question.text}")
                print(f"   Your answer:    {raw}")
                print(f"   Correct answer: {question.answer}")