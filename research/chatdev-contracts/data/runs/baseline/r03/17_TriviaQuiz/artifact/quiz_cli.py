'''
Command-line interface for the Trivia Quiz application.
Handles all user interaction: selecting a question bank, choosing
options (topic, number of questions, feedback), running the quiz loop,
showing final results and the optional answer review.
Typing "quit" at any prompt exits the quiz early.
'''
import glob
import os
from question_bank import QuestionBank, QuestionBankError
from quiz import Quiz
QUESTION_BANK_DIR = "question_banks"
class QuitQuiz(Exception):
    '''Raised when the user chooses to leave the quiz early.'''
class QuizCLI:
    '''Text-based user interface driving the whole quiz experience.'''
    def __init__(self, input_func=input, output_func=print):
        self._input = input_func
        self._print = output_func
    # ------------------------------------------------------------------
    # Low-level input helpers
    # ------------------------------------------------------------------
    def _ask(self, prompt):
        '''Read one line of input; convert EOF or 'quit' into QuitQuiz.'''
        try:
            raw = self._input(prompt)
        except EOFError:
            raise QuitQuiz
        if raw.strip().lower() == "quit":
            raise QuitQuiz
        return raw.strip()
    def _ask_yes_no(self, prompt, default=False):
        '''Ask a yes/no question; returns True for yes.'''
        suffix = " (Y/n): " if default else " (y/N): "
        while True:
            raw = self._ask(prompt + suffix).lower()
            if raw == "":
                return default
            if raw in ("y", "yes"):
                return True
            if raw in ("n", "no"):
                return False
            self._print("Please answer 'y' or 'n'.")
    def _ask_int(self, prompt, default, minimum, maximum):
        '''Ask for an integer within an inclusive range; empty = default.'''
        while True:
            raw = self._ask(prompt)
            if raw == "":
                return default
            if raw.isdigit():
                value = int(raw)
                if minimum <= value <= maximum:
                    return value
            self._print(f"Please enter a number between {minimum} and {maximum}.")
    # ------------------------------------------------------------------
    # Main flow
    # ------------------------------------------------------------------
    def run(self):
        '''Main entry: pick a bank, configure the quiz, run it, show results.'''
        self._print("=" * 60)
        self._print("        Welcome to the Trivia Quiz!")
        self._print("=" * 60)
        self._print("(Type 'quit' at any prompt to exit early.)")
        try:
            bank = self._select_bank()
            questions = self._configure_quiz(bank)
            if not questions:
                self._print("No questions matched your selection.")
                return
            feedback = self._ask_yes_no("Show feedback immediately after each answer?", default=False)
            quiz = Quiz(questions, immediate_feedback=feedback)
            try:
                self._run_quiz(quiz)
            except QuitQuiz:
                self._print("\nQuiz ended early.")
            if quiz.total_answered > 0:
                self._show_results(quiz)
                if self._ask_yes_no("\nWould you like to review the correct answers?", default=True):
                    self._show_review(quiz)
            else:
                self._print("\nNo questions were answered.")
        except QuestionBankError as e:
            self._print(f"Error: {e}")
        except QuitQuiz:
            pass
        self._print("\nThanks for playing! Goodbye.")
    def _select_bank(self):
        '''List JSON banks in QUESTION_BANK_DIR and let the user choose one.'''
        files = sorted(glob.glob(os.path.join(QUESTION_BANK_DIR, "*.json")))
        if not files:
            raise QuestionBankError(f"No question bank files (*.json) found in '{QUESTION_BANK_DIR}'.")
        self._print("\nAvailable question banks:")
        for i, f in enumerate(files, 1):
            self._print(f"  {i}. {os.path.splitext(os.path.basename(f))[0]}")
        while True:
            raw = self._ask("Select a question bank (number): ")
            if raw.isdigit() and 1 <= int(raw) <= len(files):
                return QuestionBank.load(files[int(raw) - 1])
            self._print(f"Please enter a number between 1 and {len(files)}.")
    def _configure_quiz(self, bank):
        '''Ask for topic and number of questions; return the selected questions.'''
        topics = bank.get_topics()
        self._print(f"\nLoaded '{bank.name}' with {len(bank)} questions.")
        self._print(f"Topics: all, {', '.join(topics)}")
        topic = None
        while True:
            raw = self._ask("Choose a topic (or press Enter for 'all'): ")
            if raw == "" or raw.lower() == "all":
                break
            if raw.lower() in [t.lower() for t in topics]:
                topic = raw
                break
            self._print("Unknown topic. Try again.")
        max_count = len(bank.get_questions(topic=topic, shuffle=False))
        count = self._ask_int(f"How many questions? (1-{max_count}, Enter for {max_count}): ",
                              default=max_count, minimum=1, maximum=max_count)
        return bank.get_questions(topic=topic, count=count, shuffle=True)
    def _run_quiz(self, quiz):
        '''Present each question, read the user's answer, submit it.'''
        while quiz.has_next():
            question = quiz.current_question()
            self._print("\n" + "-" * 60)
            self._print(f"Question {quiz.total_answered + 1} of {len(quiz.questions)} [{question.topic}]")
            self._print(question.display_text())
            answer = self._ask("Your answer (or 'quit' to exit): ")
            correct = quiz.submit_answer(answer)
            if quiz.immediate_feedback:
                self._print("Correct!" if correct else
                            f"Sorry, the correct answer was: {question.correct_answer_display()}")
                if question.explanation:
                    self._print(f"Info: {question.explanation}")
    def _show_results(self, quiz):
        '''Display the final score, percentage and per-topic breakdown.'''
        score, total = quiz.final_score()
        self._print("\n" + "=" * 60)
        self._print("QUIZ COMPLETE!")
        self._print(f"You answered {score} out of {total} questions correctly ({quiz.percentage():.1f}%).")
        breakdown = quiz.topic_breakdown()
        if len(breakdown) > 1:
            self._print("\nTopic breakdown:")
            for topic, stats in sorted(breakdown.items()):
                self._print(f"  {topic}: {stats['correct']}/{stats['total']}")
    def _show_review(self, quiz):
        '''Show every answered question with the user's answer and the correct one.'''
        self._print("\n" + "=" * 60)
        self._print("ANSWER REVIEW")
        self._print("=" * 60)
        for i, r in enumerate(quiz.results, 1):
            q = r["question"]
            self._print(f"\n{i}. [{'CORRECT' if r['correct'] else 'INCORRECT'}] {q.display_text()}")
            self._print(f"   Your answer: {r['user_answer']}")
            if not r["correct"]:
                self._print(f"   Correct answer: {q.correct_answer_display()}")
            if q.explanation:
                self._print(f"   Explanation: {q.explanation}")