'''
quiz_game.py
Defines the QuizGame class, the interactive controller that presents
questions, reads user answers, tracks the score, and displays final
results with an optional answer review. Quitting mid-quiz (entering
'q') is handled gracefully via return values instead of exceptions,
and all console output is ASCII-safe for maximum portability.
'''
from score_tracker import ScoreTracker
class QuizGame:
    """Runs an interactive trivia quiz session in the terminal."""
    QUIT_COMMAND = "q"
    def __init__(self, question_bank, score_tracker=None, show_answers_after=False):
        """
        Initialize the game.
        Args:
            question_bank: A QuestionBank instance providing the questions.
            score_tracker: A ScoreTracker instance (created if not supplied).
            show_answers_after: If True, display a full answer review at the end.
        """
        self.question_bank = question_bank
        self.score_tracker = score_tracker or ScoreTracker()
        self.show_answers_after = show_answers_after
    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #
    def start(self, questions):
        """Run the quiz over the provided list of Question objects."""
        if not questions:
            print("No questions available to start the quiz.")
            return
        print("=" * 60)
        print(f"  TRIVIA QUIZ: {self.question_bank.name}")
        print(f"  Questions: {len(questions)}")
        print("=" * 60)
        print("Instructions: type your answer and press Enter.")
        print("For multiple-choice questions you may enter the option")
        print("letter (e.g. B) or the option text. Type 'q' to quit.\n")
        quit_requested = False
        for number, question in enumerate(questions, start=1):
            if not self._ask_question(number, question):
                quit_requested = True
                break
        if quit_requested:
            print("\nQuiz ended early by user.")
        self.display_results()
    def _ask_question(self, number, question):
        """
        Present one question, read the answer, and record the result.
        Returns True to continue with the next question, or False if the
        user chose to quit the quiz early.
        """
        print("-" * 60)
        print(f"Question {number}: [{question.topic}]")
        print(question.format_for_display())
        user_answer = input("Your answer: ").strip()
        if user_answer.lower() == self.QUIT_COMMAND:
            return False
        is_correct = question.check_answer(user_answer)
        self.score_tracker.record_answer(question, user_answer, is_correct)
        if is_correct:
            print("Correct!")
        else:
            print("Incorrect.")
        return True
    # ------------------------------------------------------------------ #
    # Results
    # ------------------------------------------------------------------ #
    def display_results(self):
        """Display the final score and, optionally, the answer review."""
        print("\n" + "=" * 60)
        print("  QUIZ COMPLETE - FINAL RESULTS")
        print("=" * 60)
        print(f"  Total questions answered: {self.score_tracker.get_total_answered()}")
        print(f"  Total correct answers:    {self.score_tracker.get_correct_count()}")
        print(f"  Score: {self.score_tracker.get_summary()}")
        print("=" * 60)
        if self.show_answers_after:
            self.display_review()
    def display_review(self):
        """Show every question with the user's answer and the correct answer."""
        print("\n" + "-" * 60)
        print("  ANSWER REVIEW")
        print("-" * 60)
        for entry in self.score_tracker.get_review():
            question = entry["question"]
            status = "Correct" if entry["is_correct"] else "Incorrect"
            print(f"\nQ{entry['number']}. [{status}] {question.question_text}")
            if question.is_multiple_choice():
                for option in question.options:
                    print(f"      {option}")
            print(f"      Your answer:    {entry['user_answer'] or '(blank)'}")
            print(f"      Correct answer: {question.get_correct_answer_display()}")
            if question.explanation:
                print(f"      Info: {question.explanation}")