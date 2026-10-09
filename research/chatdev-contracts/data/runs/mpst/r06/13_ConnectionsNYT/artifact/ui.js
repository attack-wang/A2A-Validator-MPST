class GameUI {
  constructor(game, callbacks) { ... }
  renderInitial()
  renderGrid()
  createTile(word)
  onTileClick(word)
  updateSelection()
  updateControls()
  renderMistakes()
  renderSolvedGroups()
  showToast(message, type)
  handleGuessResult(result)
  animateWrong(selectedWords)
  animateOneAway(selectedWords)
  revealGroup(categoryIndex)
  endGame(won)
  buildEmojiGrid()
  shareResult()
}