'''
quiz.py
The quiz engine: presents questions one at a time, records answers,
tracks the running score, and produces final results with an optional
answer review.
Classes:
    Quiz -- stateful engine that walks a list of questions
'''
class Quiz:
    """Runs a trivia quiz over a list of questions and tracks results."""
    def __init__(self, questions, show_answers_at_end=True):
        self.questions = list(questions)
        self.show_answers_at_end = show_answers_at_end
        self.current_index = 0
        self.results = []
    # ----- state helpers -----
    @property
    def total_questions(self):
        return len(self.questions)
    @property
    def answered_count(self):
        return len(self.results)
    @property
    def score(self):
        return sum(1 for result in self.results if result["correct"])
    def has_next(self):
        return self.current_index < len(self.questions)
    def get_current_question(self):
        if self.has_next():
            return self.questions[self.current_index]
        return None
    # ----- answering -----
    def submit_answer(self, user_answer):
        """Grade and record the answer to the current question, then advance.
        Returns True when the answer was correct.
        """
        question = self.get_current_question()
        if question is None:
            raise RuntimeError("The quiz is already finished.")
        is_correct = question.check_answer(user_answer)
        self.results.append({
            "number": self.current_index + 1,
            "question": question,
            "user_answer": "" if user_answer is None else str(user_answer),
            "correct": is_correct,
        })
        self.current_index += 1
        return is_correct
    # ----- reporting -----
    def get_score_summary(self):
        """Return a formatted final score summary."""
        total = self.total_questions
        correct = self.score
        percent = (correct / total * 100.0) if total else 0.0
        lines = [
            "=" * 52,
            "QUIZ COMPLETE - FINAL RESULTS",
            "=" * 52,
            "Total questions : {}".format(total),
            "Correct answers : {}".format(correct),
            "Incorrect       : {}".format(total - correct),
            "Final score     : {:.1f}%".format(percent),
            "Grade           : {}".format(self._grade(percent)),
            "=" * 52,
        ]
        return "\n".join(lines)
    @staticmethod
    def _grade(percent):
        """Map a percentage score to a friendly letter grade."""
        if percent >= 90:
            return "A - Outstanding!"
        if percent >= 80:
            return "B - Great job!"
        if percent >= 70:
            return "C - Good effort."
        if percent >= 60:
            return "D - Keep practicing."
        return "F - Better luck next time!"
    def get_answer_review(self):
        """Return a formatted review listing the correct answer for every question."""
        lines = ["", "-" * 52, "ANSWER REVIEW", "-" * 52]
        for result in self.results:
            question = result["question"]
            status = "CORRECT  " if result["correct"] else "INCORRECT"
            lines.append("")
            lines.append("Q{} [{}] ({})".format(result["number"], status, question.topic))
            lines.append("    {}".format(question.question_text))
            lines.append("    Your answer    : {}".format(result["user_answer"] or "(no answer)"))
            lines.append("    Correct answer : {}".format(question.get_correct_answer_display()))
        lines.append("-" * 52)
        return "\n".join(lines)