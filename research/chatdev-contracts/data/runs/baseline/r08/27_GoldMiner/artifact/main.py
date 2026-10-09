"""
main.py
Entry point and game orchestration for the Gold Miner game.
Wires together the settings, game_objects, claw, level and ui modules into
a runnable application. Implements the Game class that the other modules
depend on (game.objects, game.collect(), game.trigger_explosion(),
game.level_score, game.goal, game.time_left, game.level_number,
game.total_score, game.claw).
Game flow:
    * The claw swings back and forth; SPACE / left click launches it.
    * The claw grabs the first object it touches and reels it in; heavier
      objects take longer (weight-scaled reel speed).
    * Collected gold is credited immediately; reaching the level goal ends
      the level, running out of time ends the run.
    * TNT crates explode when grabbed, destroying everything nearby.
    * Each level tightens the timer, raises the goal and adds obstacles.
Controls:
    SPACE or left click : launch the claw / continue on overlay screens
    ESC or window close : quit the game
"""
import pygame
import settings
from claw import Claw
from level import make_level_plan, populate_objects
from ui import UI
# Seconds a TNT blast ring stays visible on screen.
EXPLOSION_DURATION = 0.5
class Game:
    """Owns the game state machine, scoring, timer and level flow."""
    STATE_PLAYING = "playing"
    STATE_LEVEL_COMPLETE = "level_complete"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        self.claw = Claw()
        self.ui = UI()
        self.running = True
        self.level_number = 1
        self.total_score = 0
        self.level_score = 0
        self.goal = 0
        self.time_left = 0.0
        self.objects = []
        self.state = self.STATE_PLAYING
        self.explosions = []  # active blast effects: {"x", "y", "t"}
        self.load_level(1)
    # ------------------------------------------------------------------
    # Level flow
    # ------------------------------------------------------------------
    def load_level(self, number):
        """(Re)build the level for the given number and reset per-level state."""
        plan = make_level_plan(number)
        self.level_number = plan.number
        self.goal = plan.goal
        self.time_left = float(plan.time_limit)
        self.level_score = 0
        self.objects = populate_objects(plan)
        self.explosions = []
        self.claw.reset()
        self.state = self.STATE_PLAYING
    # ------------------------------------------------------------------
    # API used by Claw / GameObjects
    # ------------------------------------------------------------------
    def collect(self, obj):
        """Credit a reeled-in object; end the level once the goal is met."""
        obj.alive = False
        self.level_score += obj.value
        self.total_score += obj.value
        if self.level_score >= self.goal:
            self.state = self.STATE_LEVEL_COMPLETE
    def trigger_explosion(self, tnt):
        """Destroy the TNT and every object inside the blast radius."""
        tnt.alive = False
        self.explosions.append({"x": tnt.x, "y": tnt.y, "t": EXPLOSION_DURATION})
        for obj in self.objects:
            if (obj.alive and obj is not tnt
                    and obj.distance_to(tnt.x, tnt.y) <= settings.TNT_BLAST_RADIUS):
                obj.alive = False
    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def handle_event(self, event):
        """Translate a pygame event into game actions."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_SPACE:
                self._confirm_or_launch()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._confirm_or_launch()
    def _confirm_or_launch(self):
        """SPACE / click: launch the claw while playing, advance screens otherwise."""
        if self.state == self.STATE_PLAYING:
            self.claw.launch()
        elif self.state == self.STATE_LEVEL_COMPLETE:
            self.load_level(self.level_number + 1)
        elif self.state == self.STATE_GAME_OVER:
            self.total_score = 0
            self.load_level(1)
    # ------------------------------------------------------------------
    # Per-frame update
    # ------------------------------------------------------------------
    def update(self, dt):
        """Advance the simulation by dt seconds."""
        self._update_explosions(dt)
        if self.state != self.STATE_PLAYING:
            return
        self.time_left = max(0.0, self.time_left - dt)
        if self.time_left <= 0.0:
            # Time up: meeting the goal still counts as a cleared level.
            self.state = (self.STATE_LEVEL_COMPLETE if self.level_score >= self.goal
                          else self.STATE_GAME_OVER)
            return
        self.claw.update(self)
    def _update_explosions(self, dt):
        """Age and prune TNT blast effects."""
        for blast in self.explosions:
            blast["t"] -= dt
        self.explosions = [blast for blast in self.explosions if blast["t"] > 0]
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def draw(self, surface):
        """Render one full frame: background, objects, claw, HUD, overlays."""
        self._draw_background(surface)
        for obj in self.objects:
            if obj.alive:
                obj.draw(surface)
        self._draw_miner(surface)
        self.claw.draw(surface)
        self._draw_explosions(surface)
        self.ui.draw_hud(surface, self)
        self.ui.draw_hint(surface, self)
        if self.state == self.STATE_LEVEL_COMPLETE:
            self.ui.draw_overlay(
                surface,
                f"Level {self.level_number} Cleared!",
                [f"Gold collected: {self.level_score} / {self.goal}",
                 f"Total gold: {self.total_score}",
                 "",
                 "SPACE / CLICK: next level"])
        elif self.state == self.STATE_GAME_OVER:
            self.ui.draw_overlay(
                surface,
                "Game Over",
                [f"You reached level {self.level_number}",
                 f"Total gold: {self.total_score}",
                 "",
                 "SPACE / CLICK: play again"])
    def _draw_background(self, surface):
        """Sky above the ground line, speckled dirt below it."""
        ground_y = settings.GROUND_Y
        surface.fill(settings.COLOR_SKY,
                     pygame.Rect(0, 0, settings.SCREEN_WIDTH, ground_y))
        surface.fill(settings.COLOR_DIRT,
                     pygame.Rect(0, ground_y, settings.SCREEN_WIDTH,
                                 settings.SCREEN_HEIGHT - ground_y))
        # Dirt speckles for texture.
        for i in range(0, settings.SCREEN_WIDTH, 60):
            pygame.draw.circle(surface, settings.COLOR_DIRT_DARK, (i + 20, ground_y + 45), 4)
            pygame.draw.circle(surface, settings.COLOR_DIRT_DARK, (i + 45, ground_y + 115), 3)
            pygame.draw.circle(surface, settings.COLOR_DIRT_DARK, (i + 10, ground_y + 195), 5)
            pygame.draw.circle(surface, settings.COLOR_DIRT_DARK, (i + 35, ground_y + 285), 4)
            pygame.draw.circle(surface, settings.COLOR_DIRT_DARK, (i + 55, ground_y + 375), 3)
        pygame.draw.line(surface, settings.COLOR_DIRT_DARK,
                         (0, ground_y), (settings.SCREEN_WIDTH, ground_y), 3)
    def _draw_miner(self, surface):
        """Simple miner figure and windlass at the claw's pivot."""
        px, py = settings.CLAW_PIVOT
        # Support post from the ground up to the pivot, plus the winch wheel.
        pygame.draw.line(surface, settings.COLOR_ROPE, (px, settings.GROUND_Y), (px, py), 5)
        pygame.draw.circle(surface, settings.COLOR_CLAW, (px, py), 11)
        pygame.draw.circle(surface, settings.COLOR_ROPE, (px, py), 11, 2)
        # Miner standing to the left of the winch, feet on the ground line.
        bx = px - 46
        pygame.draw.rect(surface, settings.COLOR_MINER, (bx - 10, settings.GROUND_Y - 32, 20, 32))
        pygame.draw.circle(surface, settings.COLOR_MINER, (bx, settings.GROUND_Y - 42), 9)
        pygame.draw.rect(surface, settings.COLOR_TNT_DARK, (bx - 11, settings.GROUND_Y - 56, 22, 7))
    def _draw_explosions(self, surface):
        """Expanding blast rings for recent TNT explosions."""
        for blast in self.explosions:
            progress = 1.0 - blast["t"] / EXPLOSION_DURATION  # 0 -> 1 over lifetime
            radius = int(settings.TNT_BLAST_RADIUS * progress)
            if radius > 2:
                pygame.draw.circle(surface, (255, 160, 40),
                                   (int(blast["x"]), int(blast["y"])), radius, 4)
                pygame.draw.circle(surface, (255, 220, 120),
                                   (int(blast["x"]), int(blast["y"])), max(2, radius // 2), 2)
def main():
    """Create the window, run the game loop and clean up afterwards."""
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    game = Game()
    while game.running:
        # Frame time in seconds; drives the countdown and effect timers.
        dt = clock.tick(settings.FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            else:
                game.handle_event(event)
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()
    pygame.quit()
if __name__ == "__main__":
    main()