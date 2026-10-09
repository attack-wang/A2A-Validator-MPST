'''
main.py
Program entry point for the trivia quiz.
Wires together configuration, question-bank loading, user prompts, and the
Quiz engine into a complete interactive console session.
'''
import json
import os
import sys
from config import Config
from question_bank import QuestionBank, list_bank_files
from quiz import Quiz
from ui import ask_yes_no, clear_screen, print_header
def choose_bank(config):
    """Display available question banks and return the user's chosen bank."""
    bank_files = list_bank_files(config.banks_path())
    if not bank_files:
        raise FileNotFoundError(
            f"No question bank (*.json) files found in '{config.banks_path()}'.")
    # Preselect the bank named in config.default_bank, if configured.
    default_index = 0
    for i, path in enumerate(bank_files):
        if os.path.basename(path).lower() == config.default_bank.lower():
            default_index = i
            break
    print_header("CHOOSE A QUESTION BANK")
    for i, path in enumerate(bank_files, start=1):
        print(f"  {i}) {os.path.splitext(os.path.basename(path))[0]}")
    while True:
        raw = input(f"Select a bank (1-{len(bank_files)}) [{default_index + 1}]: ").strip()
        if not raw:
            raw = str(default_index + 1)
        if raw.isdigit() and 1 <= int(raw) <= len(bank_files):
            path = bank_files[int(raw) - 1]
            try:
                bank = QuestionBank.load_from_json(path)
            except (ValueError, json.JSONDecodeError, OSError) as exc:
                print(f"Could not load that bank: {exc}")
                continue
            if len(bank) == 0:
                print("That bank contains no questions. Pick another.")
                continue
            print(f"Loaded '{bank.name}' with {len(bank)} questions.")
            return bank
        print("Invalid choice. Enter a number from the list.")
def choose_topic(bank):
    """Display the bank's topics and return the chosen topic (None = all)."""
    topics = bank.topics
    print_header("CHOOSE A TOPIC")
    print("  0) All topics")
    for i, topic in enumerate(topics, start=1):
        print(f"  {i}) {topic}")
    while True:
        raw = input(f"Select a topic (0-{len(topics)}) [0]: ").strip()
        if not raw:
            return None
        if raw.isdigit() and 0 <= int(raw) <= len(topics):
            return None if int(raw) == 0 else topics[int(raw) - 1]
        print("Invalid choice. Enter a number from the list.")
def choose_question_count(available):
    """Ask how many questions to play; returns an int in 1..available."""
    while True:
        raw = input(f"How many questions? (1-{available}) [{available}]: ").strip()
        if not raw:
            return available
        if raw.isdigit() and 1 <= int(raw) <= available:
            return int(raw)
        print(f"Please enter a number between 1 and {available}.")
def run_session(config):
    """Run one complete quiz session."""
    bank = choose_bank(config)
    topic = choose_topic(bank)
    questions = bank.get_questions(topic=topic, shuffle=config.shuffle_questions)
    count = choose_question_count(len(questions))
    questions = questions[:count]
    quiz = Quiz(questions, show_answers_after=config.show_answers_after_quiz)
    quiz.run()
    quiz.display_results()
    quiz.display_answer_review()
def main():
    """Program entry point."""
    config = Config()
    clear_screen()
    print_header("TRIVIA QUIZ")
    print("Answer each question by typing your answer and pressing Enter.")
    print("For multiple-choice questions you may type the option letter (e.g. B)")
    print("or the full option text.")
    while ask_yes_no("\nStart a quiz?", default=True):
        try:
            run_session(config)
        except KeyboardInterrupt:
            print("\nQuiz interrupted.")   # return to menu instead of exiting
        except (FileNotFoundError, ValueError) as exc:
            print(f"\n{exc}")
    print("\nThanks for playing! Goodbye.")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)