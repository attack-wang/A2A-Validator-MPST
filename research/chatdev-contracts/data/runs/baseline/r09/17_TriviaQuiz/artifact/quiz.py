'''
quiz.py
Runs an interactive trivia quiz session: presents each question, reads and
validates the user's answer, tracks the running score, and reports the final
results (with an optional answer review).
'''
class Quiz:
    """Plays one session of the trivia quiz over a list of questions."""
    def __init__(self, questions, show_correct_answers=True):
        self.questions = list(questions)
        self.show_correct_answers = show_correct_answers
        self.user_answers = []
        self.score = 0
    def run(self):
        """Execute the full question-and-answer loop."""
        total = len(self.questions)
        if total == 0:
            print("No questions available for this quiz.")
            return 0
        print("=" * 60)
        print("        WELCOME TO THE TRIVIA QUIZ!")
        print("=" * 60)
        print(f"You will be asked {total} question(s).")
        print("For multiple-choice questions, type the letter (e.g. 'b')")
        print("or the full answer text. Press Ctrl+C to quit early.\n")
        for index, question in enumerate(self.questions, start=1):
            self.ask_question(question, index, total)
        self.display_results()
        return self.score
    def ask_question(self, question, index, total):
        """Present one question, collect an answer, and update the score."""
        print("-" * 60)
        print(f"Question {index} of {total}  [{question.topic}]")
        print(question.display())
        answer = self.get_user_answer()
        correct = question.is_correct(answer)
        self.user_answers.append((question, answer, correct))
        if correct:
            self.score += 1
            print("✔ Correct!")
        else:
            print("✘ Incorrect.")
        print(f"Running score: {self.score}/{index}\n")
    @staticmethod
    def get_user_answer():
        """Prompt until the user supplies a non-empty answer."""
        while True:
            answer = input("Your answer: ").strip()
            if answer:
                return answer
            print("Please enter an answer (it cannot be blank).")
    def display_results(self):
        """Show the final score and, optionally, the answer review."""
        total = len(self.questions)
        percent = (self.score / total * 100) if total else 0.0
        print("=" * 60)
        print("                 QUIZ COMPLETE!")
        print("=" * 60)
        print(f"Total correct answers: {self.score} out of {total} ({percent:.1f}%)")
        if self.score == total and total > 0:
            print("Perfect score — outstanding work!")
        elif percent >= 70:
            print("Great job!")
        elif percent >= 40:
            print("Not bad — keep practicing!")
        else:
            print("Better luck next time!")
        if self.show_correct_answers:
            self.display_answer_review()
    def display_answer_review(self):
        """Print a per-question review of user answers vs correct answers."""
        print("\n" + "-" * 60)
        print("ANSWER REVIEW")
        print("-" * 60)
        for index, (question, answer, correct) in enumerate(self.user_answers, start=1):
            status = "Correct" if correct else "Incorrect"
            print(f"\n{index}. [{status}] {question.text}")
            print(f"   Your answer:    {answer if answer else '(no answer)'}")
            print(f"   Correct answer: {question.answer}")
            if question.explanation:
                print(f"   Info: {question.explanation}")