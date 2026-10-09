'''
score_tracker.py
Defines the ScoreTracker class, which records each answered question,
maintains running totals, and produces final results and a review list.
'''
class ScoreTracker:
    """Tracks correct answers and detailed results for a quiz session."""
    def __init__(self):
        self.records = []  # list of dicts: question, user_answer, is_correct
    def record_answer(self, question, user_answer, is_correct):
        """Record the outcome of a single answered question."""
        self.records.append({
            "question": question,
            "user_answer": user_answer,
            "is_correct": is_correct,
        })
    def get_correct_count(self):
        """Return the number of correctly answered questions."""
        return sum(1 for record in self.records if record["is_correct"])
    def get_total_answered(self):
        """Return the total number of questions answered."""
        return len(self.records)
    def get_percentage(self):
        """Return the score as a percentage (0.0 - 100.0), or 0.0 if empty."""
        if not self.records:
            return 0.0
        return (self.get_correct_count() / self.get_total_answered()) * 100.0
    def get_summary(self):
        """Return a human-readable summary line, e.g. '7/10 correct (70.0%)'."""
        return (f"{self.get_correct_count()}/{self.get_total_answered()} correct "
                f"({self.get_percentage():.1f}%)")
    def get_review(self):
        """
        Return a list of review entries for every answered question,
        used to display the correct answers after the quiz.
        """
        review = []
        for index, record in enumerate(self.records, start=1):
            question = record["question"]
            review.append({
                "number": index,
                "question": question,
                "user_answer": record["user_answer"],
                "is_correct": record["is_correct"],
            })
        return review