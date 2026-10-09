'''
Daily Connections - a daily word-grouping puzzle game.
HOW TO PLAY
-----------
Sixteen words are presented in a 4x4 grid.  Every word belongs to exactly
one of four hidden categories.  Select any four words and press "Submit"
to guess a category.  A correct guess removes those words from the grid
and reveals the category name together with a colour that codes its
difficulty:
    yellow  - easiest
    green   - easy
    blue    - tricky
    purple  - hardest
An incorrect guess costs one of your four allowed mistakes; after the
fourth mistake the game ends and every remaining group is revealed.
Words are deliberately chosen so that some of them seem to fit more than
one category - but only one correct solution exists.
A new puzzle is selected automatically every day (the puzzle is chosen
deterministically from today's date, so everybody plays the same puzzle
on the same day).
Run with:  python daily_connections.py
Requires:  Python 3.x (standard library only - tkinter ships with Python).
'''