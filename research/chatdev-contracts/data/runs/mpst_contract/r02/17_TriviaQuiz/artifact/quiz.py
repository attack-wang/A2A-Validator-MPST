"""Quiz engine: asks questions, tracks score, summarizes and reviews results."""

import random


class Quiz:
    def __init__(self, questions, shuffle=False):
        self.questions = list(questions)
        if shuffle:
            random.shuffle(self.questions)
        self.score = 0
        self.results = []  # tuples of (question, user answer, correct flag)

    def run(self, input_fn=input, print_fn=print):
        total = len(self.questions)
        for number, question in enumerate(self.questions, start=1):
            print_fn(f"\nQuestion {number}/{total} [{question.topic}]")
            print_fn(question.text)
            if question.qtype == "mc":
                for letter, choice in zip("ABCDEFGH", question.choices):
                    print_fn(f"  {letter}) {choice}")
            answer = input_fn("Your answer: ").strip()
            while not answer:
                answer = input_fn("Please enter an answer: ").strip()
            correct = question.is_correct(answer)
            self.results.append((question, answer, correct))
            if correct:
                self.score += 1
                print_fn("Correct!")
            else:
                print_fn("Incorrect.")

    def summary(self):
        answered = len(self.results)
        percent = 100.0 * self.score / answered if answered else 0.0
        note = "" if answered == len(self.questions) else " (quiz ended early)"
        bar = "=" * 40
        return (f"\n{bar}\nQUIZ COMPLETE\n"
                f"Total correct answers: {self.score}/{answered} "
                f"({percent:.0f}%){note}\n{bar}")

    def review(self, print_fn=print):
        print_fn("\n--- Answer Review ---")
        for number, (question, answer, correct) in enumerate(self.results, start=1):
            status = "Correct" if correct else "Incorrect"
            print_fn(f"{number}. [{status}] {question.text}")
            print_fn(f"   Your answer: {answer}")
            print_fn(f"   Correct answer: {question.display_answer()}")