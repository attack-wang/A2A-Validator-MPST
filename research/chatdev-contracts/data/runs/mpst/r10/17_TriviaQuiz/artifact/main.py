'''
main.py
Entry point for the trivia quiz program. Launches the interactive
console application.
'''
from app import QuizApp
def main():
    app = QuizApp()
    app.run()
if __name__ == "__main__":
    main()