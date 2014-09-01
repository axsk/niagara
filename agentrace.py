from niagara import Game, Player, AgentRandom
from agenta import AgentDet
from itertools import combinations

agents = [Player('Random', AgentRandom()), Player('Det', AgentDet())]

repeats = 1

for (a,b) in combinations(agents,2):
	awins = 0
	for i in range (0, repeats):
		game = 0
		game = Game(players = [a, b])
		game.run()
		if a in game.winners:
			awins += 1
			
		print a.name + " vs " + b.name + ": " + `awins/repeats`
