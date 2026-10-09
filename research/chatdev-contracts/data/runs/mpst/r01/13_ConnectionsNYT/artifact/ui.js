class UI {
  constructor(game, opts) { this.game = game; ... cache DOM elements ... }
  init() { render everything, bind events }
  renderGrid() { build tiles for game.remainingWords; mark selected }
  renderSolvedGroups() { for each solved group, a banner with color }
  updateMistakes() { dots }
  setMessage(text, tone) { auto-clear after timeout for transient messages }
  handleSubmit() { ... }
  handleCorrect(category) { animate: mark tiles, then after animation move to solved, re-render }
  handleIncorrect(oneAway) { shake selected tiles, update dots, message }
  handleShuffle() { re-render with pop animation }
  revealRemainingGroups() { for lost game }
  showModal(won) { build results grid + share text }
  buildShareText() { emoji squares per guess? We don't track guess history in detail... }
}