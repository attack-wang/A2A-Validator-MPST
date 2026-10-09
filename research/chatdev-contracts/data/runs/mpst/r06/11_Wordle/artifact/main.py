Welcome banner
Show date, puzzle number maybe
loop:
  print board (history)
  print keyboard status
  prompt: "Enter guess (X attempts left):"
  read input; handle 'quit'/'exit' commands
  validate; on error, print error in red and continue (doesn't consume attempt)
  on valid: append, print colored row
  check win/lose
end: print win message with attempts, or reveal answer