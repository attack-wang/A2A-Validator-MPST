'''
score_tracker.py
Records the outcome of every question asked during a quiz and produces the
final score summary and answer review.
'''
class ScoreTracker:
    """Tracks per-question results and computes the final score."""
    def __init__(self):
        """Initialize an empty result list."""
        self._results = []
    def record(self, question, user_answer, is_correct):
        """Record the outcome of one question."""
        self._results.append({
            "question": question,
            "user_answer": user_answer,
            "is_correct": is_correct,
        })
    @property
    def total(self):
        """Total number of recorded questions."""
        return len(self._results)
    @property
    def correct(self):
        """Number of correctly answered questions."""
        return sum(1 for r in self._results if r["is_correct"])
    @property
    def incorrect(self):
        """Number of incorrectly answered questions."""
        return self.total - self.correct
    def percentage(self):
        """Return the percentage of correct answers (0.0 if nothing recorded)."""
        if self.total == 0:
            return 0.0
        return 100.0 * self.correct / self.total
    def summary(self):
        """Return a one-line score summary."""
        pct = self.percentage()
        return f"Score: {self.correct} out of {self.total} correct ({pct:.1f}%)."
    def review_lines(self):
        """Return human-readable lines reviewing every question and answer."""
        lines = []
        for i, r in enumerate(self._results, 1):
            q = r["question"]
            status = "[CORRECT]" if r["is_correct"] else "[WRONG]  "
            lines.append(f"{i}. {status} {q.text}")
            lines.append(f"   Your answer: {r['user_answer']}")
            lines.append(f"   Correct answer: {q.correct_answer_display}")
            if q.explanation:
                lines.append(f"   Info: {q.explanation}")
        return lines