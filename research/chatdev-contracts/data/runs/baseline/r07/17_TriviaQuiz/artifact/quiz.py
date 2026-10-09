'''
quiz.py
Core quiz engine.
Defines:
- QuizAborted: exception raised when the quiz cannot continue because the
  input stream is closed (EOF) or the user interrupts the session.
- _read_answer: safe input helper that converts EOFError/KeyboardInterrupt
  into QuizAborted so piped or automated (non-TTY) runs terminate cleanly.
- QuizGame: runs a quiz session over a QuestionBank, tracks per-question
  results and the running score, and renders the final summary and the
  optional correct-answer review.
EOF/interrupt handling:
- Every user input goes through _read_answer(); on EOF or Ctrl+C the
  QuizAborted exception propagates out of run() while all answers recorded
  so far remain in self.results, letting the caller show partial results.
'''
import random
class QuizAborted(Exception):
    """Raised when the quiz cannot continue (EOF on stdin or user interrupt)."""
def _read_answer(prompt):
    """Read one stripped line of user input; convert EOF/interrupt to QuizAborted."""
    try:
        return input(prompt).strip()
    except EOFError:
        raise QuizAborted("Input stream closed (EOF).")
    except KeyboardInterrupt:
        raise QuizAborted("Interrupted by user.")
class QuizGame:
    """Runs an interactive quiz session and tracks per-question results."""
    def __init__(self, bank, shuffle=False):
        """Store the question bank, optionally shuffle question order, init results."""
        self.bank = bank
        self.questions = list(bank.questions)
        if shuffle:
            random.shuffle(self.questions)
        self.results = []  # each entry: {"question", "user_answer", "is_correct"}
    def run(self):
        """Game loop: ask every question in order and record the answers.
        Raises QuizAborted if the input stream is exhausted or interrupted;
        answers recorded so far stay in self.results for partial reporting.
        """
        total = len(self.questions)
        print("\n=== %s ===" % self.bank.title)
        print("Answer all %d questions. Good luck!\n" % total)
        for number, question in enumerate(self.questions, start=1):
            self._ask_question(number, total, question)
    def _ask_question(self, number, total, question):
        """Prompt one question, re-prompting until a non-empty answer is given.
        Uses _read_answer() so EOF/interrupt exits the re-prompt loop via
        QuizAborted instead of crashing with an unhandled EOFError.
        """
        print("-" * 40)
        print("Question %d of %d  [%s]" % (number, total, question.topic))
        print(question.prompt_text())
        while True:
            answer = _read_answer("%s: " % question.answer_prompt())
            if answer:
                break
            print("Please enter a non-empty answer.")
        correct = question.is_correct(answer)
        self.results.append(
            {"question": question, "user_answer": answer, "is_correct": correct}
        )
        print("Correct!\n" if correct else "Incorrect.\n")
    @property
    def score(self):
        """Number of correctly answered questions."""
        return sum(1 for r in self.results if r["is_correct"])
    def display_results(self):
        """Print the final summary: totals, percentage, and a grade message."""
        total = len(self.results)
        correct = self.score
        percentage = (correct / total * 100.0) if total else 0.0
        print("=" * 40)
        print("QUIZ COMPLETE!")
        print("=" * 40)
        print("Total questions: %d" % total)
        print("Correct answers: %d" % correct)
        print("Incorrect:       %d" % (total - correct))
        print("Score: %.1f%%" % percentage)
        print(self._grade_message(percentage))
    @staticmethod
    def _grade_message(percentage):
        """Map a score percentage to an encouraging message."""
        if percentage >= 90:
            return "Outstanding! You're a trivia master!"
        if percentage >= 70:
            return "Great job!"
        if percentage >= 50:
            return "Not bad — keep practicing!"
        return "Better luck next time!"
    def display_answers(self):
        """Print the answer review: user answer vs. correct answer per question."""
        print("-" * 40)
        print("ANSWER REVIEW")
        print("-" * 40)
        for number, result in enumerate(self.results, start=1):
            q = result["question"]
            print("%d. [%s] %s" % (number, q.topic, q.text))
            print("   Your answer:    %s" % result["user_answer"])
            print("   Correct answer: %s" % q.display_correct_answer())
            print("   Result: %s" % ("Correct" if result["is_correct"] else "Incorrect"))