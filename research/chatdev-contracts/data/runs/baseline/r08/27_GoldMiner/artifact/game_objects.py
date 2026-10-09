"""
game_objects.py
Collectible objects that populate the mine: gold nuggets, diamonds,
rocks, bones and TNT crates.
Every object knows its value (gold added to the score when collected),
its weight (which controls how long the claw takes to reel it in) and
its radius (used for drawing and collision detection).
"""
import math
import random
import pygame
import settings
class GameObject:
    """Base class for anything the claw can grab in the mine."""
    def __init__(self, x, y, spec):
        """
        Create an object at (x, y) from a spec dictionary containing
        name / value / weight / radius entries (see settings.py).
        """
        self.x = x
        self.y = y
        self.name = spec["name"]
        self.value = spec["value"]
        self.weight = spec["weight"]
        self.radius = spec["radius"]
        self.alive = True  # False once collected or destroyed
    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------
    def distance_to(self, px, py):
        """Euclidean distance from the object's centre to a point."""
        return math.hypot(px - self.x, py - self.y)
    def contains_point(self, px, py):
        """True if the point lies inside the object's bounding circle."""
        return self.distance_to(px, py) <= self.radius
    def overlaps(self, other, margin=6):
        """True if this object's circle overlaps another object's."""
        return self.distance_to(other.x, other.y) < self.radius + other.radius + margin
    # ------------------------------------------------------------------
    # Behaviour hooks
    # ------------------------------------------------------------------
    def on_grabbed(self, game):
        """Called when the claw grabs this object. Default: nothing special."""
        return None
    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw(self, surface):
        """Draw the object; subclasses override _draw_body."""
        self._draw_body(surface)
    def _draw_body(self, surface):
        """Fallback rendering: a simple circle."""
        pygame.draw.circle(surface, settings.COLOR_GOLD,
                           (int(self.x), int(self.y)), self.radius)
class Gold(GameObject):
    """A gold nugget. Small / medium / large variants via the spec."""
    def _draw_body(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        # Lumpy nugget: main circle plus a couple of highlight bumps.
        pygame.draw.circle(surface, settings.COLOR_GOLD, (cx, cy), r)
        pygame.draw.circle(surface, settings.COLOR_GOLD, (cx - r // 2, cy - r // 3), max(3, r // 2))
        pygame.draw.circle(surface, settings.COLOR_GOLD, (cx + r // 2, cy - r // 4), max(3, r // 3))
        pygame.draw.circle(surface, settings.COLOR_GOLD_DARK, (cx, cy), r, 2)
        # Sparkle
        pygame.draw.line(surface, (255, 255, 255),
                         (cx - r // 3, cy - r // 3), (cx - r // 6, cy - r // 6), 2)
class Diamond(GameObject):
    """High-value, light gem: quick to reel in, big payoff."""
    def _draw_body(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        top = (cx, cy - r)
        bottom = (cx, cy + r)
        left = (cx - r, cy)
        right = (cx + r, cy)
        pygame.draw.polygon(surface, settings.COLOR_DIAMOND, [top, right, bottom, left])
        pygame.draw.polygon(surface, settings.COLOR_DIAMOND_DARK, [top, right, bottom, left], 2)
        pygame.draw.line(surface, (255, 255, 255), top, left, 2)
class Rock(GameObject):
    """Heavy, nearly worthless stone. Pure obstacle — slows you down."""
    def _draw_body(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        pygame.draw.circle(surface, settings.COLOR_ROCK, (cx, cy), r)
        pygame.draw.circle(surface, settings.COLOR_ROCK_DARK, (cx, cy), r, 2)
        # A few cracks / shading dots
        pygame.draw.line(surface, settings.COLOR_ROCK_DARK,
                         (cx - r // 2, cy - r // 4), (cx, cy + r // 4), 2)
        pygame.draw.line(surface, settings.COLOR_ROCK_DARK,
                         (cx, cy + r // 4), (cx + r // 3, cy - r // 6), 2)
class Bone(GameObject):
    """Almost worthless junk the claw can still get stuck reeling in."""
    def _draw_body(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        # Shaft
        pygame.draw.line(surface, settings.COLOR_BONE,
                         (cx - r, cy), (cx + r, cy), max(3, r // 2))
        # Knobs at both ends
        for sx in (-1, 1):
            pygame.draw.circle(surface, settings.COLOR_BONE,
                               (cx + sx * r, cy - r // 3), max(3, r // 2))
            pygame.draw.circle(surface, settings.COLOR_BONE,
                               (cx + sx * r, cy + r // 3), max(3, r // 2))
class TNT(GameObject):
    """Explosive crate: grabbing it destroys it and everything nearby,
    and the claw snaps back empty."""
    def on_grabbed(self, game):
        """Explode: remove nearby objects (including self) and notify the game."""
        game.trigger_explosion(self)
        return "explosion"
    def _draw_body(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        rect = pygame.Rect(cx - r, cy - r, 2 * r, 2 * r)
        pygame.draw.rect(surface, settings.COLOR_TNT, rect)
        pygame.draw.rect(surface, settings.COLOR_TNT_DARK, rect, 2)
        # White "TNT" band
        band = pygame.Rect(cx - r, cy - r // 3, 2 * r, max(6, 2 * r // 3))
        pygame.draw.rect(surface, (240, 240, 240), band)
        # Fuse
        pygame.draw.line(surface, (80, 60, 40), (cx, cy - r), (cx + r // 2, cy - r - 8), 3)
        pygame.draw.circle(surface, (255, 160, 40), (cx + r // 2, cy - r - 10), 4)