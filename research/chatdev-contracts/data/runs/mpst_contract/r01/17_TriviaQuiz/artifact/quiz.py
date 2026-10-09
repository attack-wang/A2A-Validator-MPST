"""Core quiz engine: question model, answer checking, scoring, and review."""

import json
import random
import re


def normalize(text):
    return re.sub(r"\s+", " ", str(text).strip().lower())


def read_answer(prompt_text):
    """Read one line of user input; return None on EOF (closed stdin)."""
    try:
        return input(prompt_text)
    except EOFError:
        return None
    except KeyboardInterrupt:
        return None


class Question:
    def __init__(self, topic, text, answer, choices=None, qtype="mc"):
        self.topic = topic
        self.text = text
        self.choices = choices or []
        self.qtype = qtype
        self.answer = answer
        self.user_answer = None
        self.correct = False

    @classmethod
    def from_dict(cls, data):
        qtype = data.get("type", "mc")
        if qtype == "mc":
            return cls(data.get("topic", "General"), data["question"],
                       data["answer"], data.get("choices", []), "mc")
        answers = data["answer"] if isinstance(data["answer"], list) else [data["answer"]]
        return cls(data.get("topic", "General"), data["question"], answers, None, "sa")

    def check(self, raw):
        self.user_answer = raw.strip()
        guess = normalize(raw)
        if self.qtype == "mc":
            for i, choice in enumerate(self.choices):
                if guess == normalize(choice) or guess == chr(65 + i).lower():
                    self.correct = normalize(choice) == normalize(self.answer)
                    return self.correct
            self.correct = False
        else:
            self.correct = any(guess == normalize(a) for a in self.answer)
        return self.correct

    def prompt(self, index):
        lines = ["Q%d [%s] %s" % (index, self.topic, self.text)]
        if self.qtype == "mc":
            for i, choice in enumerate(self.choices):
                lines.append("  %s) %s" % (chr(65 + i), choice))
        return "\n".join(lines)

    def display_answer(self):
        if self.qtype == "mc":
            return self.answer
        return " / ".join(self.answer)


class Quiz:
    def __init__(self, questions, shuffle=False, limit=None, show_answers=False):
        self.questions = questions
        if shuffle:
            random.shuffle(self.questions)
        if limit is not None and limit > 0:
            self.questions = self.questions[:limit]
        self.show_answers = show_answers
        self.score = 0

    def run(self):
        total = len(self.questions)
        print("=" * 60)
        print("TRIVIA QUIZ  -  %d questions (mc = multiple choice, sa = short answer)" % total)
        print("=" * 60)
        for i, q in enumerate(self.questions, 1):
            print()
            print(q.prompt(i))
            raw = None
            while True:
                raw = read_answer("Your answer: ")
                if raw is None:
                    break
                if raw.strip():
                    break
                print("Please enter an answer.")
            if raw is None:
                print()
                print("Input stream ended; scoring answers given so far.")
                break
            if q.check(raw):
                self.score += 1
                print("Correct!")
            else:
                print("Wrong.")
        self.report()

    def report(self):
        total = len(self.questions)
        pct = (100.0 * self.score / total) if total else 0.0
        print()
        print("=" * 60)
        print("QUIZ COMPLETE")
        print("Total questions : %d" % total)
        print("Correct answers : %d" % self.score)
        print("Final score     : %d/%d (%.0f%%)" % (self.score, total, pct))
        print("=" * 60)
        if self.show_answers:
            print()
            print("ANSWER REVIEW")
            for i, q in enumerate(self.questions, 1):
                status = "CORRECT" if q.correct else "WRONG  "
                yours = q.user_answer if q.user_answer is not None else "(no answer)"
                print("%d. [%s] %s" % (i, status, q.text))
                print("   Your answer    : %s" % yours)
                print("   Correct answer : %s" % q.display_answer())


def load_bank(path):
    """Load a JSON question bank: a list of question objects,
    or an object with a 'questions' key holding that list."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    items = data.get("questions", data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise ValueError("question bank must be a list of question objects "
                         "or an object with a 'questions' list.")
    for i, item in enumerate(items, 1):
        if not isinstance(item, dict):
            raise ValueError("question #%d is not an object (got %s)."
                             % (i, type(item).__name__))
    return [Question.from_dict(item) for item in items]