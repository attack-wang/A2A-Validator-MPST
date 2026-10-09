const rng = mulberry32(dayNumber + 12345);
const index = Math.floor(rng() * PUZZLES.length) % PUZZLES.length;