class ConnectionsGame {
  constructor(puzzle) {
    this.puzzle = puzzle; // {categories: [{name, difficulty, words}]}
    this.categories = puzzle.categories;
    this.wordToCategory = new Map(); // word -> category index
    this.remainingWords = shuffle of all 16 words (initial order maybe as given or shuffled)
    this.selected = [];
    this.mistakes = 0;
    this.maxMistakes = 4;
    this.solved = []; // category indices in solve order
    this.guessHistory = []; // arrays of difficulty indices or -1
    this.status = 'playing'; // 'playing' | 'won' | 'lost'
  }
  toggleSelect(word) -> {selected: bool, allowed: bool}
  deselectAll()
  shuffleRemaining()
  canSubmit()
  submitGuess() -> result object {type: 'correct'|'one-away'|'wrong', categoryIndex?, guessColors}
  isWon(), isLost(), isOver()
}