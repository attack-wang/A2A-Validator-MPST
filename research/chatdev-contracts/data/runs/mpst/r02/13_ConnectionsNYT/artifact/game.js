class Game {
  constructor(puzzle, seed) {
    this.puzzle = puzzle;
    this.seed = seed;
    this.wordToGroup = {};
    puzzle.groups.forEach(g => g.words.forEach(w => { this.wordToGroup[w] = g; }));
    const allWords = puzzle.groups.flatMap(g => g.words);
    this.words = seededShuffle(allWords, seed);
    this.selected = [];
    this.solvedGroups = [];
    this.mistakes = 0;
    this.maxMistakes = 4;
    this.status = 'playing';
  }
  toggleWord(word) {
    if (this.status !== 'playing') return { selected: false, allowed: false };
    const idx = this.selected.indexOf(word);
    if (idx !== -1) {
      this.selected.splice(idx, 1);
      return { selected: false, allowed: true };
    }
    if (this.selected.length >= 4) return { selected: false, allowed: false };
    this.selected.push(word);
    return { selected: true, allowed: true };
  }
  isSelected(word) { return this.selected.includes(word); }
  canSelect() { return this.selected.length < 4 && this.status === 'playing'; }
  shuffleWords() {
    this.words = seededShuffle(this.remainingWords(), this.seed + this.mistakes * 31 + this.solvedGroups.length * 7 + Date.now() % 1000);
    // Hmm, for shuffle we want it to actually change each time. Use a random seed.
  }
  ...
}