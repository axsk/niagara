from game import game as game

state = game()
state.addPlayer("player 1",None)
state.addPlayer("player 2",None)
print(state.possibleMoves(state.players[1])) 
