import sys
from dataclasses import dataclass
@dataclass
class Strand:
    """A single piece of text the player can use in a merge."""
    sid: int
    text: str
# Each puzzle: a name, a list of Strand objects, and a list of target
# words/phrases. Every strand's text must be used exactly once, and the
# concatenation of merged strands must equal a target.
PUZZLES = [
    {
        "name": "Garden Bloom",
        "strands": [
            Strand(0, "SUN"),
            Strand(1, "FLOW"),
            Strand(2, "ER"),
            Strand(3, "ROSE"),
            Strand(4, "BUD"),
            Strand(5, "TULIP"),
        ],
        "targets": ["SUNFLOWER", "ROSEBUD", "TULIP"],
    },
    {
        "name": "Night Sky",
        "strands": [
            Strand(0, "STAR"),
            Strand(1, "LIGHT"),
            Strand(2, "MOON"),
            Strand(3, "BEAM"),
            Strand(4, "COMET"),
            Strand(5, "TAIL"),
        ],
        "targets": ["STARLIGHT", "MOONBEAM", "COMETTAIL"],
    },
    {
        "name": "Coffee Break",
        "strands": [
            Strand(0, "ESPRESSO"),
            Strand(1, "MOCHA"),
            Strand(2, "LATTE"),
            Strand(3, "CUP"),
            Strand(4, "CAKE"),
            Strand(5, "CUPCAKE"),
        ],
        "targets": ["ESPRESSOCUP", "MOCHACAKE", "LATTECUPCAKE"],
    },
]