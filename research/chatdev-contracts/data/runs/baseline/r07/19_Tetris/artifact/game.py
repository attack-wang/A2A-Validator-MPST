'''
game.py
Core game logic and main loop for Tetris.
The Game class owns the board, the current/next pieces, the score, level
and speed progression. It handles keyboard input (movement with DAS
auto-repeat, rotation with simple wall kicks, soft/hard drop), locks
pieces, clears completed lines, updates the score and detects game over.
'''
import pygame
from settings import (WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COLS,
                      FALL_INTERVAL_START, FALL_INTERVAL_MIN,
                      FALL_INTERVAL_STEP, LINES_PER_LEVEL, LINE_SCORES,
                      SOFT_DROP_SCORE, HARD_DROP_SCORE,
                      MOVE_REPEAT_DELAY, MOVE_REPEAT_INTERVAL)
from board import Board
from tetromino import Tetromino, PieceBag
from renderer import Renderer
class Game:
    """Owns the game state, the fixed-timestep loop, input handling,
    scoring and level/speed progression."""
    def __init__(self):
        pygame.init()  # idempotent; also safe when Game is used directly
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.board = Board()
        self.bag = PieceBag()
        self.reset()
    # ------------------------------------------------------------- lifecycle
    def reset(self):
        """Start (or restart) a round with a clean board and fresh state."""
        self.board.reset()
        self.bag = PieceBag()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.state = 'playing'           # 'playing' | 'paused' | 'game_over'
        self.next_key = self.bag.next()  # must exist before spawn_next()
        self.current_piece = self.spawn_next()
        self.fall_timer = 0              # ms accumulated toward next auto drop
        self.held_dir = None             # 'left' | 'right' | None (DAS state)
        self.repeat_timer = 0            # ms until next held horizontal repeat
        self.soft_drop_timer = 0         # ms until next held soft-drop repeat
    def fall_interval(self):
        """Milliseconds per automatic drop; shrinks as the level rises."""
        return max(FALL_INTERVAL_MIN,
                   FALL_INTERVAL_START - (self.level - 1) * FALL_INTERVAL_STEP)
    def spawn_next(self):
        """Create the next piece centred at the top of the board.
        Sets state to 'game_over' when the spawn position is blocked."""
        piece = Tetromino(self.next_key)
        piece.x = (COLS - piece.width) // 2
        piece.y = 0
        self.next_key = self.bag.next()
        if not self.board.is_valid_position(piece):
            self.state = 'game_over'
        return piece
    # -------------------------------------------------------------- movement
    def try_move(self, dx, dy):
        """Apply a translation if legal; returns True on success."""
        if self.board.is_valid_position(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False
    def try_rotate(self, clockwise=True):
        """Rotate the piece with simple wall kicks: try the plain rotation
        first, then small offsets so pieces can rotate next to walls or
        the stack. Returns True if any orientation fit."""
        piece = self.current_piece
        rotated = piece.rotated_cw() if clockwise else piece.rotated_ccw()
        kicks = ((0, 0), (-1, 0), (1, 0), (0, -1), (-2, 0), (2, 0))
        for dx, dy in kicks:
            if self.board.is_valid_position(piece, dx, dy, rotated):
                if clockwise:
                    piece.rotate_cw()
                else:
                    piece.rotate_ccw()
                piece.x += dx
                piece.y += dy
                return True
        return False
    def soft_drop(self):
        """Move one row down manually, awarding a point per cell."""
        if self.try_move(0, 1):
            self.score += SOFT_DROP_SCORE
            return True
        return False
    def hard_drop(self):
        """Instantly drop to the landing position, then lock the piece."""
        distance = 0
        while self.try_move(0, 1):
            distance += 1
        self.score += distance * HARD_DROP_SCORE
        self.lock_current()
    def lock_current(self):
        """Merge the piece into the board, clear completed lines, update
        score/level/speed and spawn the next piece."""
        if self.board.lock_piece(self.current_piece):
            self.state = 'game_over'
            return
        cleared = self.board.full_rows()
        if cleared:
            self.board.clear_rows(cleared)
            self.score += LINE_SCORES[len(cleared)]
            self.lines += len(cleared)
            self.level = 1 + self.lines // LINES_PER_LEVEL
        self.fall_timer = 0
        self.current_piece = self.spawn_next()
    # ----------------------------------------------------------------- input
    def handle_event(self, event):
        """React to a single pygame event (keyboard presses only)."""
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_p:  # pause toggle works in any state
            if self.state == 'playing':
                self.state = 'paused'
            elif self.state == 'paused':
                self.state = 'playing'
            return
        if self.state == 'game_over' and event.key == pygame.K_r:
            self.reset()
            return
        if self.state != 'playing':
            return
        if event.key == pygame.K_LEFT:
            self.try_move(-1, 0)
            self.held_dir = 'left'
            self.repeat_timer = MOVE_REPEAT_DELAY
        elif event.key == pygame.K_RIGHT:
            self.try_move(1, 0)
            self.held_dir = 'right'
            self.repeat_timer = MOVE_REPEAT_DELAY
        elif event.key == pygame.K_DOWN:
            self.soft_drop()
            self.soft_drop_timer = MOVE_REPEAT_DELAY
        elif event.key == pygame.K_UP:
            self.try_rotate(clockwise=True)
        elif event.key == pygame.K_z:
            self.try_rotate(clockwise=False)
        elif event.key == pygame.K_SPACE:
            self.hard_drop()
    def handle_held_keys(self, dt):
        """DAS-style auto-repeat for held left/right and soft drop."""
        if self.state != 'playing':
            return
        keys = pygame.key.get_pressed()
        left, right = keys[pygame.K_LEFT], keys[pygame.K_RIGHT]
        if left and not right:
            direction = -1
        elif right and not left:
            direction = 1
        else:
            direction = 0
        if direction == 0:
            self.held_dir = None
        elif self.held_dir == ('left' if direction < 0 else 'right'):
            # Key was already held: count down, then repeat at interval.
            self.repeat_timer -= dt
            if self.repeat_timer <= 0:
                self.try_move(direction, 0)
                self.repeat_timer = MOVE_REPEAT_INTERVAL
        else:
            # New direction pressed: remember it, delay before repeating.
            self.held_dir = 'left' if direction < 0 else 'right'
            self.repeat_timer = MOVE_REPEAT_DELAY
        if keys[pygame.K_DOWN]:
            self.soft_drop_timer -= dt
            if self.soft_drop_timer <= 0:
                self.soft_drop()
                self.soft_drop_timer = MOVE_REPEAT_INTERVAL
        else:
            self.soft_drop_timer = 0
    # ------------------------------------------------------------------ loop
    def update(self, dt):
        """Advance the simulation by dt milliseconds."""
        if self.state != 'playing':
            return
        self.handle_held_keys(dt)
        self.fall_timer += dt
        while self.state == 'playing':
            interval = self.fall_interval()
            if self.fall_timer < interval:
                break
            self.fall_timer -= interval
            if not self.try_move(0, 1):
                self.lock_current()
    def run(self):
        """Main loop: process events, update, render, at FPS."""
        while True:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                self.handle_event(event)
            self.update(dt)
            self.renderer.draw(self)
            pygame.display.flip()