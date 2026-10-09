'''
ui.py
Console user-interface helpers: headers, prompts, feedback, and result
rendering for the trivia quiz program.
'''
import os
SEPARATOR = "=" * 62
THIN_SEPARATOR = "-" * 62
def clear_screen():
    """Clear the terminal (best effort across platforms)."""
    os.system("cls" if os.name == "nt" else "clear")
def print_header(title):
    """Print a prominent section header."""
    print()
    print(SEPARATOR)
    print(title.center(62))
    print(SEPARATOR)
def ask_yes_no(prompt, default=None):
    """Ask a yes/no question. Returns True for yes, False for no."""
    suffix = ""
    if default is True:
        suffix = " [Y/n] "
    elif default is False:
        suffix = " [y/N] "
    else:
        suffix = " [y/n] "
    while True:
        choice = input(prompt + suffix).strip().lower()
        if not choice and default is not None:
            return default
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("Please answer with 'y' or 'n'.")
def get_nonempty_input(prompt):
    """Keep prompting until the user enters non-empty text."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Input cannot be empty. Please try again.")
def print_question(index, total, question):
    """Display one question with its position in the quiz."""
    print()
    print(THIN_SEPARATOR)
    print(f"Question {index} of {total}   [{question.topic}]")
    print(THIN_SEPARATOR)
    print(question.display())
def print_feedback(is_correct, correct_answer=None):
    """Print immediate right/wrong feedback (correct answer hidden if None)."""
    if is_correct:
        print(">>> Correct!")
    else:
        print(">>> Incorrect.")
def print_results(correct, total):
    """Print the final score summary."""
    print_header("QUIZ COMPLETE")
    percentage = (correct / total * 100) if total else 0.0
    print(f"Total correct answers: {correct} out of {total} ({percentage:.1f}%)")
    if total and correct == total:
        print("Perfect score! Outstanding!")
    elif percentage >= 80:
        print("Great job!")
    elif percentage >= 50:
        print("Not bad — keep practicing!")
    else:
        print("Better luck next time!")
def print_answer_review(results):
    """Print a per-question review showing the correct answers."""
    print_header("ANSWER REVIEW")
    for i, result in enumerate(results, start=1):
        status = "Correct" if result["is_correct"] else "Wrong"
        marker = "✓" if result["is_correct"] else "✗"
        print(f"{i}. [{status}] {result['question_text']}")
        print(f"   Your answer  : {result['user_answer'] or '(no answer)'}")
        print(f"   Correct answer: {result['correct_answer']}")
        if result.get("explanation"):
            print(f"   Note: {result['explanation']}")
        print()