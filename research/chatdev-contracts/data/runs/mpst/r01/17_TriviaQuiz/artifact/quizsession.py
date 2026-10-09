'''
quizsession.py
The quiz engine: presents questions, validates input, tracks the score,
and produces a final results report with an optional answer review.
'''
from question import MultipleChoiceQuestion
class QuizSession:
    """Runs one pass through a list of questions while tracking the score."""
    QUIT_WORDS = ("q", "quit", "exit")
    def __init__(self, questions, show_answers_after=False, instant_feedback=False):
        """Store the questions and the display options for this session."""
        self.questions = list(questions)
        self.show_answers_after = show_answers_after
        self.instant_feedback = instant_feedback
        self.results = []  # list of dicts: question, user_answer, is_correct
    @property
    def correct_count(self):
        """Number of correctly answered questions so far."""
        return sum(1 for result in self.results if result["is_correct"])
    @property
    def answered_count(self):
        """Number of questions answered so far."""
        return len(self.results)
    def run(self, io):
        """Present every question, collect answers, then show the results."""
        io.print_message()
        io.print_message("Starting the quiz! Answer each question below.")
        io.print_message("Type 'quit' at any prompt to finish early.")
        io.print_message("-" * 60)
        for number, question in enumerate(self.questions, start=1):
            io.print_message()
            io.print_message("Question {} of {} [{}]".format(number, len(self.questions), question.topic))
            io.print_message(question.display())
            prompt = self._prompt_for(question)
            user_answer = io.ask(prompt)
            while not user_answer:
                io.print_message("Please enter an answer (or 'quit' to stop).")
                user_answer = io.ask(prompt)
            if user_answer.lower() in self.QUIT_WORDS:
                io.print_message("Stopping the quiz early...")
                break
            is_correct = question.check_answer(user_answer)
            self.results.append({"question": question, "user_answer": user_answer, "is_correct": is_correct})
            if self.instant_feedback:
                io.print_message("Correct!" if is_correct else "Incorrect.")
        io.print_message()
        io.print_message(self.results_report())
        if self.show_answers_after:
            io.print_message()
            io.print_message(self.answer_review())
        return self.correct_count
    def _prompt_for(self, question):
        """Build the input prompt appropriate to the question type."""
        if isinstance(question, MultipleChoiceQuestion):
            return "Your answer (letter, number, or full text): "
        return "Your answer: "
    def results_report(self):
        """Return the final score summary as a multi-line string."""
        total = len(self.questions)
        answered = self.answered_count
        correct = self.correct_count
        percent = int(round(100.0 * correct / answered)) if answered else 0
        lines = [
            "=" * 60,
            "QUIZ RESULTS",
            "=" * 60,
            "Questions presented: {}".format(total),
            "Questions answered:  {}".format(answered),
            "Correct answers:     {} / {}".format(correct, answered),
            "Score:               {}%".format(percent),
        ]
        if correct == answered and answered > 0:
            lines.append("Perfect score - outstanding!")
        elif percent >= 80:
            lines.append("Great job!")
        elif percent >= 50:
            lines.append("Not bad - keep practicing!")
        elif answered > 0:
            lines.append("Keep studying and try again!")
        lines.append("=" * 60)
        return "\n".join(lines)
    def answer_review(self):
        """Return a detailed review showing correct answers, if requested."""
        lines = ["ANSWER REVIEW", "-" * 60]
        for number, result in enumerate(self.results, start=1):
            question = result["question"]
            marker = "CORRECT" if result["is_correct"] else "INCORRECT"
            lines.append("{}. [{}] {}".format(number, marker, question.text))
            lines.append("   Your answer:    {}".format(result["user_answer"]))
            lines.append("   Correct answer: {}".format(question.format_correct_answer()))
            if question.explanation:
                lines.append("   Info:           {}".format(question.explanation))
        return "\n".join(lines)