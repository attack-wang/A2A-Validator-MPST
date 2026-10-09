'''
game.py
Main game orchestrator: game loop, state machine (menu / playing / game
over), input handling, difficulty progression, collision checks and all
rendering. Built on tkinter (standard library only) so it runs without
any external packages such as pygame.
'''
import math
import random
import tkinter as tk
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FRAME_MS, TITLE,
    GROUND_HEIGHT, CEILING_MARGIN,
    BIRD_X, BIRD_RADIUS,
    PIPE_WIDTH, PIPE_SPACING,
    BASE_PIPE_SPEED, MAX_PIPE_SPEED, SPEED_INCREMENT,
    BASE_GAP_SIZE, MIN_GAP_SIZE, GAP_DECREMENT, GAP_VARIANCE, MAX_GAP_SHIFT,
    STATE_MENU, STATE_PLAYING, STATE_GAME_OVER,
    TEXT_WHITE, TEXT_SHADOW, TEXT_GOLD, OVERLAY_BLACK,
)
from bird import Bird
from pipe import Pipe
from utils import Background
RESTART_DELAY_FRAMES = 20   # ignore restart keys briefly after game over
class Game:
    """Flappy Bird game: owns the main loop, states, entities and rendering."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(TITLE)
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=SCREEN_WIDTH,
                                height=SCREEN_HEIGHT,
                                highlightthickness=0, bg="#78c7de")
        self.canvas.pack()
        # Key bindings (window-level events)
        self.root.bind("<KeyPress-space>", self._on_flap_key)
        self.root.bind("<KeyPress-Up>", self._on_flap_key)
        self.root.bind("<KeyPress-r>", self._on_restart_key)
        self.root.bind("<KeyPress-R>", self._on_restart_key)
        self.root.bind("<KeyPress-Escape>", self._on_quit)
        self.root.protocol("WM_DELETE_WINDOW", self._on_quit)
        self.font = ("Arial", 26, "bold")
        self.small_font = ("Arial", 13)
        self.background = Background()
        self.state = STATE_MENU
        self.restart_cooldown = 0
        self.menu_timer = 0
        self.best = 0
        self.reset()
    # ------------------------------------------------------------------ #
    # State management
    # ------------------------------------------------------------------ #
    def reset(self):
        """Reset every run-specific value (start of game and restarts)."""
        self.bird = Bird(BIRD_X, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.speed = BASE_PIPE_SPEED
        self.gap_size = BASE_GAP_SIZE
        self.background.reset()
    def update_difficulty(self):
        """Speed up and shrink gaps as the score grows (both capped)."""
        self.speed = min(BASE_PIPE_SPEED + self.score * SPEED_INCREMENT, MAX_PIPE_SPEED)
        self.gap_size = max(BASE_GAP_SIZE - self.score * GAP_DECREMENT, MIN_GAP_SIZE)
    def spawn_pipe(self):
        """Create a pipe just off the right edge with a random, bounded gap."""
        gap = max(MIN_GAP_SIZE, int(self.gap_size) + random.randint(-GAP_VARIANCE, GAP_VARIANCE))
        min_center = CEILING_MARGIN + gap // 2
        max_center = SCREEN_HEIGHT - GROUND_HEIGHT - CEILING_MARGIN - gap // 2
        gap_center = random.randint(min_center, max_center)
        # Limit the vertical jump compared to the previous pipe for fairness
        if self.pipes:
            prev = self.pipes[-1].gap_center
            gap_center = max(prev - MAX_GAP_SHIFT, min(prev + MAX_GAP_SHIFT, gap_center))
            gap_center = max(min_center, min(max_center, gap_center))
        self.pipes.append(Pipe(SCREEN_WIDTH + PIPE_WIDTH, gap_center, gap))
    # ------------------------------------------------------------------ #
    # Input
    # ------------------------------------------------------------------ #
    def _on_flap_key(self, event):
        """Space / Up: start, flap or restart depending on the state."""
        if self.state == STATE_MENU:
            self.state = STATE_PLAYING
            self.bird.flap()
        elif self.state == STATE_PLAYING:
            self.bird.flap()
        elif self.state == STATE_GAME_OVER and self.restart_cooldown == 0:
            self.reset()
            self.state = STATE_PLAYING
            self.bird.flap()
    def _on_restart_key(self, event):
        """R: restart from the game-over screen."""
        if self.state == STATE_GAME_OVER and self.restart_cooldown == 0:
            self.reset()
            self.state = STATE_PLAYING
    def _on_quit(self, event=None):
        """Escape or window close: exit cleanly."""
        self.root.destroy()
    # ------------------------------------------------------------------ #
    # Simulation
    # ------------------------------------------------------------------ #
    def update(self):
        """Advance the simulation by one frame."""
        if self.restart_cooldown > 0:
            self.restart_cooldown -= 1
        if self.state == STATE_MENU:
            # Idle bobbing bird and slowly drifting scenery
            self.menu_timer += 1
            self.bird.y = SCREEN_HEIGHT // 2 + math.sin(self.menu_timer * 0.06) * 8
            self.background.update(BASE_PIPE_SPEED * 0.4)
            return
        if self.state != STATE_PLAYING:
            return
        self.bird.update()
        # Distance-based spawning keeps PIPE_SPACING constant at any speed
        spawn_x = SCREEN_WIDTH + PIPE_WIDTH
        if not self.pipes or self.pipes[-1].x <= spawn_x - PIPE_SPACING:
            self.spawn_pipe()
        # Move pipes, award points for passes, drop off-screen pipes
        for pipe in self.pipes:
            pipe.update(self.speed)
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1
                self.update_difficulty()
        self.pipes = [p for p in self.pipes if not p.offscreen()]
        # Pipe collisions
        bird_rect = self.bird.rect
        for pipe in self.pipes:
            if pipe.collides(bird_rect):
                self.state = STATE_GAME_OVER
        # Ground collision
        if self.bird.y + BIRD_RADIUS >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.bird.y = SCREEN_HEIGHT - GROUND_HEIGHT - BIRD_RADIUS
            self.state = STATE_GAME_OVER
        # Ceiling clamp (soft: stop the bird, don't kill it)
        if self.bird.y - BIRD_RADIUS < 0:
            self.bird.y = BIRD_RADIUS
            self.bird.velocity = 0
        # Record best score and start the restart cooldown when a run ends
        if self.state == STATE_GAME_OVER:
            self.best = max(self.best, self.score)
            self.restart_cooldown = RESTART_DELAY_FRAMES
    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def _draw_text(self, text, font, color, center):
        """Draw centred text with a subtle drop shadow."""
        x, y = center
        self.canvas.create_text(x + 2, y + 2, text=text,
                                font=font, fill=TEXT_SHADOW)
        self.canvas.create_text(x, y, text=text, font=font, fill=color)
    def draw(self):
        """Render one full frame: background, pipes, bird, HUD, overlays."""
        self.canvas.delete("all")
        self.background.draw(self.canvas)
        for pipe in self.pipes:
            pipe.draw(self.canvas)
        self.bird.draw(self.canvas)
        self._draw_text(str(self.score), self.font, TEXT_WHITE,
                        (SCREEN_WIDTH // 2, 60))
        if self.state == STATE_MENU:
            self._draw_text("FLAPPY BIRD", self.font, TEXT_GOLD,
                            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
            self._draw_text("Press SPACE or UP to start", self.small_font,
                            TEXT_WHITE,
                            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self._draw_text("ESC to quit", self.small_font, TEXT_WHITE,
                            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        elif self.state == STATE_GAME_OVER:
            # Translucent dark overlay (stippled to approximate alpha)
            overlay = self.canvas.create_rectangle(
                0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                fill=OVERLAY_BLACK, outline="", stipple="gray50")
            self._draw_text("GAME OVER", self.font, TEXT_GOLD,
                            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
            self._draw_text("Score: {}".format(self.score), self.font,
                            TEXT_WHITE,
                            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            self._draw_text("Best: {}".format(self.best), self.font,
                            TEXT_WHITE,
                            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            if self.restart_cooldown == 0:
                self._draw_text("Press SPACE to play again", self.small_font,
                                TEXT_WHITE,
                                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #
    def run(self):
        """Start the fixed-timestep loop and the tkinter event loop."""
        self._tick()
        self.root.mainloop()
    def _tick(self):
        """One frame of update + render, rescheduled at ~FPS."""
        self.update()
        self.draw()
        self.root.after(FRAME_MS, self._tick)
def main():
    Game().run()
if __name__ == "__main__":
    main()