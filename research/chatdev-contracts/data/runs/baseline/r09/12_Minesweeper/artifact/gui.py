'''
GUI module for the Minesweeper game using tkinter.
Contains the MinesweeperGUI class responsible for rendering the board,
handling mouse input (left click to reveal, right click to flag),
displaying the mine counter and timer, and switching difficulty levels.
'''
import tkinter as tk
from tkinter import messagebox
from board import Board
from config import ...