'''Main game class: state machine, level flow, rendering and input.'''
import math
import random
import pygame
import audio
from claw import Claw
from objects import GameObject
from hud import draw_hud, draw_center_message, draw_progress_bar
from settings import (WIDTH, HEIGHT, FPS, SKY_BLUE, DIRT_BROWN, DIRT_DARK,
                      BLACK, WHITE, GOLD, GREEN, RED, CYAN, ORANGE, GRAY_DARK,
                      HUD_HEIGHT, SURFACE_Y, MINE_TOP, MINE_LEFT, MINE_RIGHT,
                      MINE_BOTTOM, PIVOT, OBJECT_STATS, TNT_BLAST_RADIUS,
                      get_level_config)
class GoldMinerGame:
    """Gold Miner: time the claw, grab valuables, hit the level target."""
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gold Miner")
        self.clock = pygame.time.Clock()
        self.fonts = {
            'big': pygame.font.Font(None, 56),
            'medium': pygame.font.Font(None, 36),
            'small': pygame.font.Font(None, 28),
            'tiny': pygame.font.Font(None, 22),
        }
        self.sounds = audio.init_sounds()
        self.claw = Claw()
        self.state = 'level_intro'
        self.level = 1
        self.score = 0
        self.load_level(1)
    # ------------------------------------------------------------------ setup
    def load_level(self, level):
        """(Re)build all per-level state from the level configuration."""
        config = get_level_config(level)
        self.config = config
        self.target = config['target']
        self.time_left = config['time_limit']
        self.objects = self.generate_objects(config)
        self.claw.reset()
        self.claw.swing_speed = config['swing_speed']
        self.claw.extend_speed = config['extend_speed']
        self.level_score = 0  # gold collected during this level only
        self.state = 'level_intro'
    def generate_objects(self, config):
        """Place objects randomly in the mine area without overlap."""
        placed = []
        for kind, count in config['counts'].items():
            r = OBJECT_STATS[kind]['radius']
            for _ in range(count):
                for attempt in range(200):
                    x = random.randint(MINE_LEFT + r, MINE_RIGHT - r)
                    y = random.randint(MINE_TOP + r, MINE_BOTTOM - r)
                    if all(math.hypot(x - o.x, y - o.y) >= r + o.radius + 6
                           for o in placed):
                        placed.append(GameObject(kind, x, y))
                        break
        return placed
    # ------------------------------------------------------------------ events
    def on_deliver(self):
        """Bank the object the claw just reeled in."""
        obj = self.claw.attached
        if obj is None:
            return
        self.claw.attached = None
        if obj in self.objects:
            self.objects.remove(obj)
        self.score += obj.value
        self.level_score += obj.value
        if obj.kind in ('small_gold', 'medium_gold', 'large_gold', 'diamond', 'mystery'):
            audio.play(self.sounds, 'deliver')
        else:
            audio.play(self.sounds, 'miss')  # worthless rock/bone clunk
    def explode_tnt(self):
        """The grabbed TNT blows up: it and nearby objects are destroyed."""
        tnt = self.claw.attached
        if tnt is None:
            return
        self.claw.attached = None
        if tnt in self.objects:
            self.objects.remove(tnt)
        destroyed = []
        for obj in list(self.objects):
            if math.hypot(obj.x - tnt.x, obj.y - tnt.y) <= TNT_BLAST_RADIUS:
                self.objects.remove(obj)
                destroyed.append(obj)
        audio.play(self.sounds, 'boom')
    # ------------------------------------------------------------------ flow
    def complete_level(self):
        self.state = 'level_clear'
        audio.play(self.sounds, 'deliver')
    def game_over(self):
        self.state = 'game_over'
        audio.play(self.sounds, 'boom')
    def next_level(self):
        self.level += 1
        self.load_level(self.level)
    def restart(self):
        self.level = 1
        self.score = 0
        self.load_level(1)
    # ------------------------------------------------------------------ loop
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
    def handle_events(self):
        """Process the event queue. Returns False to quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.confirm()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == 'playing':
                    self.claw.launch()
                else:
                    self.confirm()
        return True
    def confirm(self):
        """SPACE/ENTER: advance menus or launch the claw."""
        if self.state == 'level_intro':
            self.state = 'playing'
        elif self.state == 'playing':
            self.claw.launch()
        elif self.state == 'level_clear':
            self.next_level()
        elif self.state == 'game_over':
            self.restart()
    def update(self, dt):
        if self.state == 'playing':
            self.time_left -= dt
            event = self.claw.update(dt, self.objects)
            if event == 'tnt':
                self.explode_tnt()
            elif event == 'deliver':
                self.on_deliver()
            elif event == 'miss':
                audio.play(self.sounds, 'miss')
            elif event == 'grab':
                audio.play(self.sounds, 'grab')
            # check end conditions (per-level target, not total score)
            if self.level_score >= self.target:
                self.complete_level()
            elif self.time_left <= 0:
                self.time_left = 0
                self.game_over()
    # ------------------------------------------------------------------ draw
    def draw(self):
        self.screen.fill(SKY_BLUE)
        self.draw_ground()
        for obj in self.objects:
            obj.draw(self.screen)
        self.claw.draw(self.screen)
        draw_hud(self.screen, self.fonts, self.level, self.score, self.target,
                 self.time_left, self.level_score)
        if self.state == 'level_intro':
            draw_center_message(self.screen, self.fonts['big'], [
                ('Level %d' % self.level, GOLD),
                ('Target: %d gold  |  Time: %d s' % (self.target, int(self.config['time_limit'])), WHITE),
                ('Press SPACE to start', CYAN),
            ])
        elif self.state == 'level_clear':
            draw_center_message(self.screen, self.fonts['big'], [
                ('Level %d cleared!' % self.level, GREEN),
                ('Total score: %d' % self.score, WHITE),
                ('Press SPACE for level %d' % (self.level + 1), CYAN),
            ])
        elif self.state == 'game_over':
            draw_center_message(self.screen, self.fonts['big'], [
                ('Game Over', RED),
                ('Reached level %d with %d gold' % (self.level, self.score), WHITE),
                ('Press SPACE to retry', CYAN),
            ])
        pygame.display.flip()
    def draw_ground(self):
        """Sky, grass line, dirt and the miner's wooden frame."""
        # dirt
        pygame.draw.rect(self.screen, DIRT_BROWN, (0, SURFACE_Y, WIDTH, HEIGHT - SURFACE_Y))
        pygame.draw.rect(self.screen, DIRT_DARK, (0, SURFACE_Y, WIDTH, 8))
        # darker band at the bottom
        pygame.draw.rect(self.screen, DIRT_DARK, (0, MINE_BOTTOM, WIDTH, HEIGHT - MINE_BOTTOM))
        # wooden frame above the pulley
        pygame.draw.polygon(self.screen, DIRT_DARK, [
            (PIVOT[0] - 46, SURFACE_Y), (PIVOT[0] + 46, SURFACE_Y), (PIVOT[0], PIVOT[1] - 26)])
        pygame.draw.circle(self.screen, BLACK, PIVOT, 9)