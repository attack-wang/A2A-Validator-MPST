'''
Crossword Puzzle — Console Application
======================================
A crossword puzzle game that:
1. Shows a grid of squares ('#' = black/block square, '.' = empty square)
   together with numbered clues for the ACROSS and DOWN entries.
2. Lets the user enter a word by typing the clue number and direction,
   e.g.  "1 across"  or  "3 down", followed by the word itself.
3. Validates every entry:
   - the word length must match the entry's length;
   - every letter must match the letters already placed by crossing
     words (conflicts are reported row/column by row/column).
4. Confirms completion: as soon as all entries are filled correctly the
   program congratulates the user and prints the solved grid.
In-game commands
----------------
  <number> <across|down>    start filling an entry, e.g. "1 across"
  grid                      redraw the current grid
  clues                     show all clues again
  check                     report the status of every entry
  clear <number> <dir>      erase a previously placed word
  reveal <number> <dir>     fill in the correct answer for one entry
  reset                     wipe the whole board
  help                      show the command list
  quit                      leave the game
'''