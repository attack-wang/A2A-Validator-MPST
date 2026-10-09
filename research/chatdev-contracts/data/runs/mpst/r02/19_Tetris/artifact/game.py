'''
game.py
Defines the Game class, which ties everything together.
The Game object owns the pygame window, the board, the current and next
tetrominoes, the score/level/lines counters, and the main loop that
processes input, applies gravity, updates state, and triggers rendering.
'''
import pygame
from settings import (FPS, INITIAL_DROP_INTERVAL, MIN_DROP_INTERVAL,
                      DROP_SPEEDUP_PER_LEVEL, LINES_PER_LEVEL,
                      LINE_SCORES, SOFT_DROP_POINTS, HARD_DROP_POINTS,
                      WALL_KICK_OFFSETS)
from board import Board
from tetromino import Tetromino
from renderer import Renderer
class Game:
    """Main Tetris application: state, input, gravity, scoring, loop."""
    # Key-repeat tuning for continuous movement while keys are held
    MOVE_DELAY = 170        # ms a key must be held before repeating starts
    MOVE_REPEAT = 50        # ms between horizontal repeats
    DOWN_REPEAT = 45        # ms between soft-drop repeats
    def __init__(self):
        """Initialise pygame, the window, the board and all game state."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.renderer = Renderer()
        self.board = Board()
        self.next_tetromino = Tetromino()
        self.current_tetromino = None
        self.score = 0
        self.level = 1
        self.lines = 0
        self.drop_interval = INITIAL_DROP_INTERVAL
        self.drop_timer = 0
        self.game_over = False
        self.paused = False
        self.running = True
        # Key-repeat state for continuous movement
        self.left_timer = 0
        self.right_timer = 0
        self.down_timer = 0
        self.spawn_piece()
    # ------------------------------------------------------------------
    # Piece management
    # ------------------------------------------------------------------
    def spawn_piece(self):
        """
        Bring the next tetromino into play and generate a new preview.
        If the new piece collides immediately the game is over because no
        more pieces can be placed on the board.
        """
        self.current_tetromino = self.next_tetromino
        self.current_tetromino.spawn_position(self.board.cols)
        self.next_tetromino = Tetromino()
        self.drop_timer = 0
        if self.board.is_game_over(self.current_tetromino):
            self.game_over = True
    # ------------------------------------------------------------------
    # Movement helpers (each returns True when the action succeeded)
    # ------------------------------------------------------------------
    def move_horizontal(self, dx):
        """Try to shift the current piece by dx columns."""
        if self.board.is_valid_position(self.current_tetromino, offset_x=dx):
            self.current_tetromino.x += dx
            return True
        return False
    def rotate(self, times):
        """
        Rotate the current piece, applying simple wall kicks so that
        rotations against walls or the stack still succeed when possible.
        """
        piece = self.current_tetromino
        candidate = piece.rotated_matrix(times)
        for offset in WALL_KICK_OFFSETS:
            if self.board.is_valid_position(piece, offset_x=offset, matrix=candidate):
                piece.matrix = candidate
                piece.x += offset
                return True
        return False
    def soft_drop(self):
        """Move the piece one row down; returns True on success."""
        if self.board.is_valid_position(self.current_tetromino, offset_y=1):
            self.current_tetromino.y += 1
            return True
        return False
    def hard_drop(self):
        """Instantly drop the piece to its lowest valid position and lock it."""
        distance = 0
        while self.soft_drop():
            distance += 1
        self.score += distance * HARD_DROP_POINTS
        self.lock_current_piece()
    def lock_current_piece(self):
        """Merge the piece into the board, clear lines and update scoring."""
        lockout = self.board.lock_piece(self.current_tetromino)
        cleared = self.board.clear_lines()
        self.update_score(cleared)
        if lockout:
            self.game_over = True
        else:
            self.spawn_piece()
    # ------------------------------------------------------------------
    # Scoring / progression
    # ------------------------------------------------------------------
    def update_score(self, lines_cleared):
        """
        Add points for cleared lines, update the lines counter and raise
        the level (which speeds up gravity) every LINES_PER_LEVEL lines.
        """
        if lines_cleared > 0:
            self.score += LINE_SCORES.get(lines_cleared, 800) * self.level
            self.lines += lines_cleared
            new_level = self.lines // LINES_PER_LEVEL + 1
            if new_level > self.level:
                self.level = new_level
                self.drop_interval = max(MIN_DROP_INTERVAL,
                                         INITIAL_DROP_INTERVAL
                                         - (self.level - 1) * DROP_SPEEDUP_PER_LEVEL)
    # ------------------------------------------------------------------
    # Gravity
    # ------------------------------------------------------------------
    def apply_gravity(self, dt):
        """
        Advance the automatic fall timer by dt milliseconds and drop the
        piece one row when the interval elapses. When the piece can no
        longer descend it is locked into the board.
        """
        if self.paused or self.game_over:
            return
        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval:
            self.drop_timer = 0
            if not self.soft_drop():
                self.lock_current_piece()
    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def handle_input(self, dt):
        """Process keyboard and window events for one frame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
        if self.paused or self.game_over:
            return
        # Continuous movement while keys are held (with key repeat delay)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.left_timer += dt
            if self.left_timer >= self.MOVE_DELAY:
                self.move_horizontal(-1)
                self.left_timer -= self.MOVE_REPEAT
        else:
            self.left_timer = 0
        if keys[pygame.K_RIGHT]:
            self.right_timer += dt
            if self.right_timer >= self.MOVE_DELAY:
                self.move_horizontal(1)
                self.right_timer -= self.MOVE_REPEAT
        else:
            self.right_timer = 0
        if keys[pygame.K_DOWN]:
            self.down_timer += dt
            if self.down_timer >= self.DOWN_REPEAT:
                if self.soft_drop():
                    self.score += SOFT_DROP_POINTS
                self.down_timer -= self.DOWN_REPEAT
        else:
            self.down_timer = 0
    def handle_keydown(self, key):
        """Dispatch a single key-press to the matching game action."""
        if key == pygame.K_ESCAPE:
            self.running = False
            return
        if self.game_over:
            if key == pygame.K_r:
                self.restart()
            return
        if key == pygame.K_p:
            self.paused = not self.paused
            return
        if self.paused:
            return
        if key == pygame.K_LEFT:
            self.move_horizontal(-1)
            self.left_timer = 0
        elif key == pygame.K_RIGHT:
            self.move_horizontal(1)
            self.right_timer = 0
        elif key == pygame.K_DOWN:
            if self.soft_drop():
                self.score += SOFT_DROP_POINTS
                self.drop_timer = 0
            self.down_timer = 0
        elif key == pygame.K_UP or key == pygame.K_x:
            self.rotate(1)
        elif key == pygame.K_z:
            self.rotate(3)
        elif key == pygame.K_SPACE:
            self.hard_drop()
    # ------------------------------------------------------------------
    # Restart / main loop
    # ------------------------------------------------------------------
    def restart(self):
        """Reset all state so a brand new game can start."""
        self.board.reset()
        self.next_tetromino = Tetromino()
        self.score = 0
        self.level = 1
        self.lines = 0
        self.drop_interval = INITIAL_DROP_INTERVAL
        self.drop_timer = 0
        self.game_over = False
        self.paused = False
        self.left_timer = 0
        self.right_timer = 0
        self.down_timer = 0
        self.spawn_piece()
    def run(self):
        """
        Main loop: tick the clock, process input, apply gravity, render.
        dt is the milliseconds elapsed since the previous frame.
        """
        while self.running:
            dt = self.clock.tick(FPS)
            self.handle_input(dt)
            self.apply_gravity(dt)
            self.renderer.draw(self)
        pygame.quit()