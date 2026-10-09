'''
main.py
Main entry point for the Sudoku puzzle game: builds the board and launches the GUI.
'''
import tkinter as tk
from game_gui import SudokuGUI
from sudoku_board import SudokuBoard
from sudoku_generator import SudokuGenerator
def main():
    """Create a medium puzzle, attach it to the GUI and run the main loop."""
    root = tk.Tk()
    puzzle, solution = SudokuGenerator.generate_puzzle('medium')
    board = SudokuBoard(puzzle, solution)
    app = SudokuGUI(root, board)  # keep a reference so the window stays alive
    root.mainloop()
if __name__ == '__main__':
    main()