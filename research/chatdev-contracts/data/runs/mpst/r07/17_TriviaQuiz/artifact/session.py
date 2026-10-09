'''
session.py
Implements one complete trivia quiz session:
  - load_bank(): prompts for a JSON question bank file and loads it,
    retrying on missing/invalid files (configurable question banks).
  - prompt_for_topic(): lets the user pick a topic or all topics.
  - prompt_for_count(): lets the user choose how many questions to answer.
  - prompt_show_answers(): asks whether correct answers should be
    revealed in the review shown after the quiz.
  - run_session(): ties everything together -- loads the bank, gathers
    options, runs the Quiz, prints results and the optional answer review.
'''
import json
import sys
from question_bank import QuestionBank
from quiz import Quiz
def prompt_for_bank_file():
    """Prompt the user for the path to a question bank JSON file."""
    print("\n--- Question Bank Setup ---")
    filepath = input(
        "Enter the path to a question bank JSON file "
        "(press Enter for default 'questions.json'): "
    ).strip()
    if not filepath:
        filepath = "questions.json"
    return filepath
def load_bank():
    """
    Prompt for a question bank file and load it, retrying on errors.
    Returns:
        QuestionBank: A bank containing at least one question.
    """
    while True:
        filepath = prompt_for_bank_file()
        bank = QuestionBank()
        try:
            count = bank.load_from_json(filepath)
            if count == 0:
                print("The question bank contains no questions. Please try another file.")
                continue
            print(f"Loaded {count} question(s) from '{filepath}'.")
            return bank
        except FileNotFoundError:
            print(f"Error: file '{filepath}' does not exist. Please try again.")
        except json.JSONDecodeError:
            print(f"Error: '{filepath}' is not valid JSON. "
                  "Please fix it or choose another file.")
        except ValueError as exc:
            print(f"Error in question bank: {exc}")
            retry = input("Try a different file? (y/n): ").strip().lower()
            if retry != "y":
                sys.exit(1)
def prompt_for_topic(bank):
    """
    Prompt the user to select a topic.
    Args:
        bank (QuestionBank): The loaded question bank.
    Returns:
        str or None: The chosen topic, or None for all topics.
    """
    topics = bank.get_topics()
    print("\n--- Topic Selection ---")
    print("  0) All topics")
    for i, topic in enumerate(topics, start=1):
        print(f"  {i}) {topic}")
    while True:
        choice = input(f"Select a topic by number (0-{len(topics)}): ").strip()
        if choice == "0":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(topics):
            return topics[int(choice) - 1]
        print(f"Please enter a number between 0 and {len(topics)}.")
def prompt_for_count(available):
    """
    Prompt for how many questions to answer.
    Args:
        available (int): Number of questions available.
    Returns:
        int: Chosen question count (1..available).
    """
    while True:
        raw = input(
            f"How many questions would you like (1-{available}, "
            f"press Enter for all {available})? "
        ).strip()
        if not raw:
            return available
        if raw.isdigit() and 1 <= int(raw) <= available:
            return int(raw)
        print(f"Please enter a number between 1 and {available}.")
def prompt_show_answers():
    """
    Ask whether correct answers should be displayed after the quiz.
    Returns:
        bool: True to show correct answers in the post-quiz review.
    """
    while True:
        entry = input(
            "Display correct answers after the quiz? (y/n): "
        ).strip().lower()
        if entry in ("y", "yes"):
            return True
        if entry in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")
def run_session():
    """Run one full quiz session: setup, gameplay, results, review."""
    bank = load_bank()
    topic = prompt_for_topic(bank)
    available = bank.get_questions(topic=topic, shuffle=False)
    if not available:
        print("No questions available for the selected topic.")
        return
    count = prompt_for_count(len(available))
    show_answers = prompt_show_answers()
    selected = bank.get_questions(topic=topic, count=count)
    quiz = Quiz(selected, show_answers_after=show_answers)
    quiz.run()
    quiz.display_results()
    if show_answers:
        quiz.display_review()
    else:
        print("\nTip: choose 'y' at the start next time to review the correct answers.")