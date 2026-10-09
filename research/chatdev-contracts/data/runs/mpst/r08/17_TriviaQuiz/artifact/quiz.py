'''
quiz.py
Quiz engine: presents questions, collects user answers, tracks score,
displays results and optional answer review.
'''
import random
from questions import MultipleChoiceQuestion
class Quiz:
    """Runs one pass over a question bank, tracking the user's answers."""
    def __init__(self, bank, input_func=input, output_func=print, shuffle=False):
        self.bank = bank
        self.questions = bank.get_questions()
        if shuffle:
            random.shuffle(self.questions)
        self.user_answers = []
        self.results = []  # list of dicts: number, question, user_answer, correct
        self.input_func = input_func
        self.output_func = output_func
    def run(self):
        """Present every question, collect answers and return (correct, total)."""
        self.output_func("")
        self.output_func("=" * 60)
        self.output_func("Quiz: %s" % self.bank.name)
        if self.bank.description:
            self.output_func(self.bank.description)
        self.output_func("%d questions. Good luck!" % len(self.questions))
        self.output_func("=" * 60)
        for i, q in enumerate(self.questions, 1):
            self.output_func("")
            self.output_func("Question %d of %d [%s]" % (i, len(self.questions), q.topic))
            self.output_func(q.display())
            answer = self._prompt_answer(q)
            correct = q.check_answer(answer)
            self.user_answers.append(answer)
            self.results.append({
                "number": i,
                "question": q,
                "user_answer": answer,
                "correct": correct,
            })
        return self.score()
    def _prompt_answer(self, q):
        """Prompt until the user enters a non-empty answer."""
        if isinstance(q, MultipleChoiceQuestion):
            hint = "Your answer (letter, option number or option text)"
        else:
            hint = "Your answer"
        while True:
            answer = self.input_func("%s: " % hint)
            text = str(answer).strip()
            if text:
                return text
            self.output_func("Please enter a non-empty answer.")
    def score(self):
        """Return (number correct, total answered)."""
        correct = sum(1 for r in self.results if r["correct"])
        return correct, len(self.results)
    def display_results(self):
        """Show the final score with a simple percentage bar."""
        correct, total = self.score()
        percentage = (100.0 * correct / total) if total else 0.0
        self.output_func("")
        self.output_func("=" * 60)
        self.output_func("Results for %s" % self.bank.name)
        self.output_func("=" * 60)
        self.output_func(
            "You answered %d out of %d questions correctly (%.1f%%)."
            % (correct, total, percentage)
        )
        bar_width = 30
        filled = int(round(bar_width * correct / total)) if total else 0
        self.output_func("[" + "#" * filled + "." * (bar_width - filled) + "]")
    def display_review(self):
        """Show each question with the user's answer and the correct answer."""
        self.output_func("")
        self.output_func("=" * 60)
        self.output_func("Answer Review")
        self.output_func("=" * 60)
        for r in self.results:
            q = r["question"]
            self.output_func("")
            self.output_func("Q%d [%s] %s" % (r["number"], q.topic, q.text))
            self.output_func("  Your answer:    %s" % (r["user_answer"] or "(blank)"))
            self.output_func("  Correct answer: %s" % q.format_correct_answer())
            self.output_func("  Result: %s" % ("CORRECT" if r["correct"] else "WRONG"))