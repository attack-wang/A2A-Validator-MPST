function getDaysSinceEpoch(date = new Date()) {
  const utc = Date.UTC(date.getFullYear(), date.getMonth(), date.getDate());
  return Math.floor(utc / 86400000);
}
function getDailyPuzzle(date = new Date()) {
  const day = getDaysSinceEpoch(date);
  return { puzzle: PUZZLES[day % PUZZLES.length], dayNumber: day, index: day % PUZZLES.length };
}