"""Small shared helpers: color manipulation and polygon point generation."""
import math
def clamp_color(v):
    return max(0, min(255, int(v)))
def darken(color, factor):
    r, g, b = color
    return (clamp_color(r * factor), clamp_color(g * factor), clamp_color(b * factor))
def lighten(color, factor):
    r, g, b = color
    return (clamp_color(r + (255 - r) * (factor - 1)), ...) 