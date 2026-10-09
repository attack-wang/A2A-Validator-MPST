/**
 * puzzles.js
 * Puzzle definitions for the Strands word-segmentation game.
 * Each puzzle contains:
 *  - id, title, theme, hint
 *  - strands: array of text fragments (each used exactly once across answers)
 *  - answers: array of { text, spangram } targets formed by concatenating strands
 */
const PUZZLES = [
  {
    id: 1,
    title: "Puzzle 1",
    theme: "Up in the Air",
    hint: "Look to the sky — things that fly, glow, or drift above us.",
    strands: ["BUT", "TER", "FLY", "SUN", "SET", "RAIN", "BOW", "STAR", "LIGHT"],
    answers: [
      { text: "BUTTERFLY", spangram: false },
      { text: "SUNSET", spangram: false },
      { text: "RAINBOW", spangram: false },
      { text: "STARLIGHT", spangram: true }
    ]
  },
  {
    id: 2,
    title: "Puzzle 2",
    theme: "In the Kitchen",
    hint: "Utensils and treats you'd find while baking up a storm.",
    strands: ["CUP", "CAKE", "SAUCE", "PAN", "TOOTH", "PICK", "ROLLING", "PIN"],
    answers: [
      { text: "CUPCAKE", spangram: false },
      { text: "SAUCEPAN", spangram: false },
      { text: "TOOTHPICK", spangram: false },
      { text: "ROLLINGPIN", spangram: true }
    ]
  },
  {
    id: 3,
    title: "Puzzle 3",
    theme: "Everyday Idioms",
    hint: "Common sayings — don't take them literally!",
    strands: ["BREAK", "A", "LEG", "ON", "CLOUD", "NINE", "HIT", "THE", "SACK", "PIECE", "OF", "CAKE"],
    answers: [
      { text: "BREAKALEG", spangram: false },
      { text: "ONCLOUDNINE", spangram: false },
      { text: "HITTHESACK", spangram: false },
      { text: "PIECEOFCAKE", spangram: true }
    ]
  },
  {
    id: 4,
    title: "Puzzle 4",
    theme: "Backyard Critters",
    hint: "Small creatures you might spot hopping, crawling, or gliding nearby.",
    strands: ["GOLD", "FISH", "DRAGON", "FLY", "LADY", "BUG", "BULL", "FROG", "EARTH", "WORM"],
    answers: [
      { text: "GOLDFISH", spangram: false },
      { text: "DRAGONFLY", spangram: false },
      { text: "LADYBUG", spangram: false },
      { text: "BULLFROG", spangram: false },
      { text: "EARTHWORM", spangram: true }
    ]
  }
];