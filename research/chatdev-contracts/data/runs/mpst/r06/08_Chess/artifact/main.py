print welcome + help
loop:
  print board
  status: whose turn, check warning, last move SAN
  if game over: print result, break
  prompt: "White to move (e.g. 'e2e4' or 'Nf3'): " — wait, task says formal notation like Ke8. Prompt: "White to move: "
  read input
  commands: quit/exit, undo, help, style, moves (list legal moves in SAN?), board
  try parse_move → make_move → print "Played: Nf3" 
  except ValueError as e: print error, continue (same player retries)