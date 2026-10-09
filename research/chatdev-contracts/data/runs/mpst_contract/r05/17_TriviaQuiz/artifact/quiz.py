import json
import string

LETTERS = string.ascii_uppercase


def normalize(text):
    return " ".join(str(text).strip().lower().split())


def questions_from_dicts(items):
    return [Question.from_dict(item) for item in items]


def load_bank(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    items = data["questions"] if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise ValueError("Question bank must be a list of questions or an object with a 'questions' list.")
    return questions_from_dicts(items)


class Question:
    def __init__(self, text, answer, choices=None, topic="general"):
        self.text = str(text)
        self.answers = [str(a) for a in (answer if isinstance(answer, list) else [answer])]
        self.choices = [str(c) for c in choices] if choices else None
        self.topic = str(topic)

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["answer"], data.get("choices"), data.get("topic", "general"))

    @property
    def is_multiple_choice(self):
        return bool(self.choices)

    def display(self):
        lines = [f"[{self.topic}] {self.text}"]
        if self.is_multiple_choice:
            lines.extend(f"  {letter}) {choice}" for letter, choice in zip(LETTERS, self.choices))
        return "\n".join(lines)

    def is_correct(self, user_answer):
        user = normalize(user_answer)
        if not user:
            return False
        accepted = [normalize(a) for a in self.answers]
        if self.is_multiple_choice and len(user) == 1 and user.upper() in LETTERS[: len(self.choices)]:
            return normalize(self.choices[LETTERS.index(user.upper())]) in accepted
        return user in accepted

    def correct_display(self):
        if self.is_multiple_choice:
            accepted = [normalize(a) for a in self.answers]
            for letter, choice in zip(LETTERS, self.choices):
                if normalize(choice) in accepted:
                    return f"{letter}) {choice}"
        return self.answers[0]


class Quiz:
    def __init__(self, questions, show_answers=False):
        self.questions = questions
        self.show_answers = show_answers
        self.score = 0
        self.results = []

    def run(self):
        if not self.questions:
            print("No questions available.")
            return
        print(f"Trivia Quiz - {len(self.questions)} questions. Enter your answer after each question.\n")
        for number, question in enumerate(self.questions, 1):
            print(f"Q{number}. {question.display()}")
            try:
                answer = input("Your answer: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nQuiz aborted.")
                break
            correct = question.is_correct(answer)
            self.score += int(correct)
            self.results.append((number, question, answer, correct))
            print("Correct!\n" if correct else f"Incorrect. The answer was: {question.correct_display()}\n")
        self.report()

    def report(self):
        asked = len(self.results)
        percent = 100.0 * self.score / asked if asked else 0.0
        print("=" * 40)
        print(f"Score: {self.score}/{asked} correct ({percent:.0f}%).")
        if self.show_answers and self.results:
            print("\nAnswer review:")
            for number, question, answer, correct in self.results:
                given = answer if answer else "(blank)"
                print(f"  Q{number}: {question.text}")
                print(f"     Your answer: {given} | Correct: {question.correct_display()}")