const DAILY_EPOCH_UTC = Date.UTC(2024, 0, 1);
const MS_PER_DAY = 24 * 60 * 60 * 1000;
function getUTCDateKey(date = new Date()) { return date.toISOString().slice(0, 10); }
function getDayNumber(date = new Date()) {
  return Math.floor((Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()) - DAILY_EPOCH_UTC) / MS_PER_DAY);
}
function getDailyPuzzleIndex(date = new Date()) {
  const d = getDayNumber(date);
  return ((d % PUZZLES.length) + PUZZLES.length) % PUZZLES.length;
}
function getDailyPuzzle(date = new Date()) { return PUZZLES[getDailyPuzzleIndex(date)]; }
/** mulberry32 PRNG */
function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function seededShuffle(array, rng) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}