"""Core quiz engine: Question model, question-bank loading, and quiz runner."""
import json
import random


class Question:
    def __init__(self, text, answer, choices=None, topic="General"):
        self.text = str(text).strip()
        self.answer = str(answer).strip()
        self.choices = [str(c).strip() for c in choices] if choices else None
        self.topic = topic

    def is_multiple_choice(self):
        return bool(self.choices)

    def check(self, response):
        resp = " ".join(str(response).strip().lower().split())
        ans = " ".join(self.answer.lower().split())
        if self.is_multiple_choice():
            if len(resp) == 1 and resp.isalpha():
                idx = ord(resp) - ord("a")
                if 0 <= idx < len(self.choices):
                    return " ".join(self.choices[idx].lower().split()) == ans
                return False
            return resp == ans
        return resp == ans

    def correct_display(self):
        if self.is_multiple_choice():
            for i, choice in enumerate(self.choices):
                if choice.lower() == self.answer.lower():
                    return f"{chr(ord('a') + i)}) {self.answer}"
        return self.answer


def questions_from_dicts(data):
    return [
        Question(item["question"], item["answer"],
                 item.get("choices"), item.get("topic", "General"))
        for item in data
    ]


def load_bank(path):
    """Load a JSON question bank: a list of objects with keys 'question',
    'answer', optional 'choices' (list of strings) and optional 'topic'."""
    with open(path, "r", encoding="utf-8") as fh:
        return questions_from_dicts(json.load(fh))


class Quiz:
    def __init__(self, questions, shuffle=False):
        self.questions = list(questions)
        self.shuffle = shuffle
        self.results = []  # tuples: (Question, response, is_correct)

    def run(self, prompt=input, echo=print):
        if self.shuffle:
            random.shuffle(self.questions)
        count = len(self.questions)
        for i, q in enumerate(self.questions, 1):
            echo(f"\nQuestion {i} of {count} [{q.topic}]: {q.text}")
            if q.is_multiple_choice():
                for j, choice in enumerate(q.choices):
                    echo(f"  {chr(ord('a') + j)}) {choice}")
                response = prompt("Your answer (letter or text): ")
            else:
                response = prompt("Your answer: ")
            correct = q.check(response)
            self.results.append((q, response.strip(), correct))
            echo("Correct!" if correct else "Incorrect.")
        return self.score()

    def score(self):
        correct = sum(1 for _, _, ok in self.results if ok)
        return correct, len(self.results)

    def review(self, echo=print):
        echo("\n===== Answer Review =====")
        for i, (q, response, ok) in enumerate(self.results, 1):
            echo(f"{i}. {'Correct' if ok else 'Wrong'} - {q.text}")
            echo(f"   Your answer: {response if response else '(blank)'}")
            echo(f"   Correct answer: {q.correct_display()}")