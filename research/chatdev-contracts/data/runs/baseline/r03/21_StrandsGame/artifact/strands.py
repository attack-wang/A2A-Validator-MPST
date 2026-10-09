'''
strands.py
Strands — a word-segmentation puzzle game.
Players are presented with a board of numbered text strands (fragments).
By entering strand IDs, the player merges fragments in the chosen order;
if the concatenation forms a meaningful word or phrase from the puzzle's
target list, the merge is accepted and feedback is shown (NYT-Strands
style). The game is complete when every target word/phrase has been
formed and all strands are consumed.
Usage:
    python strands.py
Commands:
    <ids>   merge strands, e.g.  06 04 01
    found   list words found so far
    hint    reveal the first strand of an unfound word
    board   redraw the board
    q       quit the game
'''