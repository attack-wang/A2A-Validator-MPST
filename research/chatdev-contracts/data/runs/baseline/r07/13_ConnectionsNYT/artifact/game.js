const DIFFICULTY_NAMES = ['yellow', 'green', 'blue', 'purple'];
const MAX_MISTAKES = 4;
const STORAGE_PREFIX = 'daily-connections';
class ConnectionsGame {
  constructor(puzzle, dateKey) {
    this.puzzle = puzzle;
    this.dateKey = dateKey;
    this.categories = puzzle.categories.map(c => ({ name: c.name, difficulty: c.difficulty, words: [...c.words] }));
    this.wordToCategory = new Map();
    this.categories.forEach(cat => cat.words.forEach(w => this.wordToCategory.set(w, cat)));
    this.initState();
    this.loadState();
  }
  initState() {
    this.allWords = this.categories.flatMap(c => c.words);
    this.displayOrder = this.shuffleArray([...this.allWords]);
    this.selected = [];
    this.solved = []; // category names in solve order
    this.mistakesRemaining = MAX_MISTAKES;
    this.gameOver = false;
  }
  shuffleArray(arr) { Fisher-Yates }
  get unsolvedWords() {
    const solvedWords = new Set(this.solvedCategoryWords());
    return this.displayOrder.filter(w => !solvedWords.has(w));
  }
  solvedCategoryWords() {
    return this.solved.flatMap(name => this.categories.find(c => c.name === name).words);
  }
  selectWord(word) {
    if (this.gameOver) return false;
    const idx = this.selected.indexOf(word);
    if (idx >= 0) { this.selected.splice(idx, 1); return true; }
    if (this.selected.length >= 4) return false;
    if (this.solvedCategoryWords().includes(word)) return false;
    this.selected.push(word);
    return true;
  }
  deselectAll() { this.selected = []; }
  shuffle() {
    const solvedWords = new Set(this.solvedCategoryWords());
    const remaining = this.displayOrder.filter(w => !solvedWords.has(w));
    this.displayOrder = [...this.solvedCategoryWords(), ...this.shuffleArray(remaining)]; 