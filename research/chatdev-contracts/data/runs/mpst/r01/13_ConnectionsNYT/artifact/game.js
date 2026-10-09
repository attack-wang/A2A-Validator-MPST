class Game {
  static MAX_MISTAKES = 4;
  constructor(puzzle, dayNumber) {
    this.puzzle = puzzle;
    this.dayNumber = dayNumber;
    this.maxMistakes = 4;
    this.mistakesMade = 0;
    this.solvedGroups = [];
    this.guessHistory = []; // {correct, oneAway}
    this.status = 'playing';
    const rng = mulberry32((dayNumber * 2654435761) >>> 0);
    this.remainingWords = seededShuffle(this.allWords(), rng);
    this.selected = new Set();
    this.listeners = [];
  }
  allWords() { return this.puzzle.categories.flatMap(c => c.words); }
  addChangeListener(fn) { this.listeners.push(fn); }
  notify() { this.listeners.forEach(fn => fn(this)); }
  toggleWord(word) {
    if (this.status !== 'playing') return false;
    if (!this.remainingWords.includes(word)) return false;
    if (this.selected.has(word)) { this.selected.delete(word); this.notify(); return true; }
    if (this.selected.size >= 4) return false;
    this.selected.add(word); this.notify(); return true;
  }
  clearSelection() { if (this.selected.size) { this.selected.clear(); this.notify(); } }
  shuffleRemaining() {
    // Fisher-Yates with Math.random; keep selection
    const arr = this.remainingWords;
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    this.notify();
  }
  findMatchingCategory(words) {
    const set = new Set(words);
    return this.puzzle.categories.find(c => c.words.length === set.size && c.words.every(w => set.has(w))) || null;
  }
  countNearMatches(words) {
    const set = new Set(words);
    let best = 0;
    for (const c of this.puzzle.categories) {
      if (this.solvedGroups.includes(c)) continue;
      const overlap = c.words.filter(w => set.has(w)).length;
      if (overlap > best) best = overlap;
    }
    return best;
  }
  submitGuess() {
    if (this.status !== 'playing' || this.selected.size !== 4) return null;
    const words = [...this.selected];
    const cat = this.findMatchingCategory(words);
    if (cat) {
      this.solvedGroups.push(cat);
      this.remainingWords = this.remainingWords.filter(w => !this.selected.has(w));
      this.selected.clear();
      this.guessHistory.push({ correct: true, oneAway: false });
      if (this.solvedGroups.length === 4) this.status = 'won';
      this.notify();
      return { correct: true, category: cat };
    }
    this.mistakesMade++;
    const near = this.countNearMatches(words);
    const oneAway = near === 3;
    this.guessHistory.push({ correct: false, oneAway });
    if (this.mistakesMade >= this.maxMistakes) this.status = 'lost';
    this.notify();
    return { correct: false, oneAway };
  }
  getMistakesRemaining() { return this.maxMistakes - this.mistakesMade; }
  isGameOver() { return this.status !== 'playing'; }
  revealRemainingGroups() {
    // group remaining words by true category
    const remaining = new Set(this.remainingWords);
    return this.puzzle.categories
      .filter(c => !this.solvedGroups.includes(c))
      .map(c => ({ name: c.name, difficulty: c.difficulty, words: c.words.filter(w => remaining.has(w)) }));
  }
  serialize() {
    return {
      dayNumber: this.dayNumber,
      status: this.status,
      mistakesMade: this.mistakesMade,
      solvedGroups: this.solvedGroups.map(c => c.name),
      remainingWords: [...this.remainingWords],
      guessHistory: [...this.guessHistory],
    };
  }
  static deserialize(obj, puzzle, dayNumber) {
    if (!obj || typeof obj !== 'object') return null;
    if (obj.dayNumber !== dayNumber) return null;
    if (obj.status !== 'playing') return null; // finished games start fresh? Actually if finished, we might want to show results. Hmm.
    ...
  }
}