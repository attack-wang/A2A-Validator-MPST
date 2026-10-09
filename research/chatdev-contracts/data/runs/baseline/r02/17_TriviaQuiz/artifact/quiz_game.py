'''
quiz_game.py
Contains the QuizGame class, which drives an interactive quiz session:
asking questions, reading and validating user input, tracking the score
and producing a final report (with an optional answer review).
'''
import random
class QuizGame:
    """Runs an interactive trivia quiz over a list of Question objects."""
    def __init__(self, questions, shuffle_choices=False):
        """
        Args:
            questions (list): list of Question instances to ask.
            shuffle_choices (bool): shuffle MC choice order at runtime.
        """
        self.questions = list(questions)
        self.shuffle_choices = shuffle_choices
        self.results = []  # list of dicts with per-question outcome
    # ------------------------------------------------------------------ #
    # Score helpers
    # ------------------------------------------------------------------ #
    @property
    def total_questions(self):
        return len(self.questions)
    @property
    def correct_count(self):
        return sum(1 for r in self.results if r["is_correct"])
    @property
    def answered_count(self):
        return len(self.results)
    def get_score(self):
        """Return (correct, answered, total)."""
        return self.correct_count, self.answered_count, self.total_questions
    # ------------------------------------------------------------------ #
    # Game flow
    # ------------------------------------------------------------------ #
    def start(self, show_answers_after=False):
        """Run the full quiz loop, then display the final report."""
        if self.shuffle_choices:
            self._shuffle_all_choices()
        print("\n" + "=" * 60)
        print("              TRIVIA QUIZ - GOOD LUCK!")
        print("=" * 60)
        print(f"Questions: {self.total_questions}")
        print("Type your answer and press Enter. You may type")
        print("'skip' to skip a question (counts as incorrect).")
        print("-" * 60)
        for idx, question in enumerate(self.questions, start=1):
            self._ask_question(idx, question)
        self.display_results(show_answers=show_answers_after)
    def _shuffle_all_choices(self):
        """Shuffle the choices of every multiple-choice question."""
        for q in self.questions:
            if q.is_multiple_choice():
                correct = q.get_correct_answer()
                random.shuffle(q.choices)
    def _ask_question(self, number, question):
        """Present one question, read the answer and record the result."""
        print(f"\nQuestion {number} of {self.total_questions}")
        print("-" * 40)
        print(question.display(), end="")
        user_answer = input().strip()
        if user_answer.lower() == "skip":
            is_correct = False
            skipped = True
        else:
            is_correct = question.check_answer(user_answer)
            skipped = False
        if is_correct:
            print(">>> Correct!")
        elif skipped:
            print(">>> Skipped.")
        else:
            print(">>> Wrong.")
        self.results.append({
            "number": number,
            "question": question,
            "user_answer": None if skipped else user_answer,
            "is_correct": is_correct,
            "skipped": skipped,
        })
        # Live score line.
        correct, answered, total = self.get_score()
        print(f"[Score: {correct}/{answered} correct so far]")
    # ------------------------------------------------------------------ #
    # Reporting
    # ------------------------------------------------------------------ #
    def display_results(self, show_answers=False):
        """Print the final score summary and, optionally, the answer review."""
        correct, answered, total = self.get_score()
        percent = (correct / total * 100) if total else 0.0
        print("\n" + "=" * 60)
        print("                 QUIZ COMPLETED!")
        print("=" * 60)
        print(f"Total questions : {total}")
        print(f"Correct answers : {correct}")
        print(f"Score           : {percent:.1f}%")
        print("-" * 60)
        if correct == total and total > 0:
            print("Perfect score! Outstanding!")
        elif percent >= 70:
            print("Great job!")
        elif percent >= 40:
            print("Not bad - keep practicing!")
        else:
            print("Better luck next time!")
        if show_answers:
            self._print_answer_review()
        else:
            # Interactive prompt (only when running interactively).
            try:
                choice = input("\nShow correct answers for review? [y/N]: ").strip().lower()
            except EOFError:
                choice = "n"
            if choice in ("y", "yes"):
                self._print_answer_review()
    def _print_answer_review(self):
        """Print a detailed review of every question with correct answers."""
        print("\n" + "=" * 60)
        print("                ANSWER REVIEW")
        print("=" * 60)
        for r in self.results:
            q = r["question"]
            status = "CORRECT" if r["is_correct"] else ("SKIPPED" if r["skipped"] else "WRONG")
            print(f"\nQ{r['number']}. [{status}] ({q.topic}) {q.text}")
            if q.is_multiple_choice():
                print(q.format_choices())
            if r["user_answer"]:
                print(f"   Your answer   : {r['user_answer']}")
            else:
                print("   Your answer   : (skipped)")
            print(f"   Correct answer: {q.get_correct_answer()}")
            if q.explanation:
                print(f"   Explanation   : {q.explanation}")
        print("\n" + "=" * 60)