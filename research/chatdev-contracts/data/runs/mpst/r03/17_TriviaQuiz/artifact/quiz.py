'''
quiz.py
Core quiz engine: runs a session of questions, captures user answers,
tracks the score, and produces the final results and optional answer review.
Class:
    Quiz - Manages a list of questions and the flow of one quiz session.
'''
from ui import print_question, print_feedback, get_nonempty_input, print_results, print_answer_review
class Quiz:
    """Runs one quiz session over a list of Question objects."""
    def __init__(self, questions, show_answers_after=False):
        if not questions:
            raise ValueError("A quiz needs at least one question.")
        self.questions = list(questions)
        self.show_answers_after = show_answers_after
        self.results = []          # per-question result records
        self.correct_count = 0
    def run(self):
        """Present every question, collect answers, and track the score."""
        total = len(self.questions)
        self.results = []
        self.correct_count = 0
        for index, question in enumerate(self.questions, start=1):
            print_question(index, total, question)
            user_answer = get_nonempty_input("Your answer: ")
            is_correct = question.check_answer(user_answer)
            self.record_answer(question, user_answer, is_correct)
            print_feedback(is_correct)
        return self.correct_count
    def record_answer(self, question, user_answer, is_correct):
        """Store the outcome of one answered question."""
        if is_correct:
            self.correct_count += 1
        self.results.append({
            "question_text": question.question_text,
            "topic": question.topic,
            "user_answer": user_answer,
            "correct_answer": question.get_correct_answer(),
            "explanation": question.explanation,
            "is_correct": is_correct,
        })
    def get_score(self):
        """Return (correct, total)."""
        return self.correct_count, len(self.questions)
    def display_results(self):
        """Show the total number of correct answers."""
        correct, total = self.get_score()
        print_results(correct, total)
    def display_answer_review(self):
        """Show the per-question review with correct answers (if enabled)."""
        if self.show_answers_after and self.results:
            print_answer_review(self.results)