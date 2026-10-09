"""Game orchestration: states, loop, input, difficulty, rendering.
Entry point for the Flappy Bird clone. Before importing any pygame-dependent
module, the runtime verifies that the required third-party package 'pygame'
is installed; if it is missing, a one-time automatic ``pip`` installation is
attempted and, should that fail, a clear manual-installation message is shown
instead of an opaque traceback.
"""
import sys
def _ensure_pygame():
    """Guarantee 'pygame' is importable, auto-installing it if necessary."""
    try:
        import pygame  # noqa: F401
        return
    except ImportError:
        pass
    print("The required module 'pygame' is not installed.")
    print("Attempting automatic installation with pip ...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        import pygame  # noqa: F401  # retry after installation
        print("pygame installed successfully.")
    except Exception as exc:
        print(f"Automatic installation failed: {exc}")
        print("Please install the dependencies manually with:")
        print("    pip install pygame numpy")
        sys.exit(1)
_ensure_pygame()
import os  # noqa: E402
import pygame  # noqa: E402
import settings as cfg  # noqa: E402
from bird import Bird  # noqa: E402
from pipe import PipeManager  # noqa: E402
from utils import draw_text, load_high_score, save_high_score, clamp  # noqa: E402
from sounds import SoundManager  # noqa: E402
STATE_START = "start"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
        pygame.display.set_caption(cfg.TITLE)
        self.clock = pygame.time.Clock()
        self.sounds = SoundManager()
        self.high_score_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")
        self.high_score = load_high_score(self.high_score_path)
        self.background = self._build_background()
        self.ground_offset = 0.0
        self.running = True
        self.reset()
        self.state = STATE_START
    ... (rest same as before)