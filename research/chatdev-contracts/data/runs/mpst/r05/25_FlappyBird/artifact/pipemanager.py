from pipemanager import PipeManager
from sounds import build_sounds
from storage import load_best, save_best
from ui import draw_text
# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_DYING = 2
STATE_GAMEOVER = 3
BEST_FILE = "best_score.dat"  # no, that's in storage.py