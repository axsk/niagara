from niagara import Game, Player, AgentRandom
from agenta import AgentDet
from itertools import combinations

agents = [AgentRandom(), AgentDet()]

repeats = 100

for (a,b) in combinations(agents,2):
	wins = 0
	rounds = 0
	for i in range (0, repeats):
		game = 0
		game = Game([a, b])
		game.run()
		if a in game.winners:
			wins += 1
		rounds += game.round

	print a.name + " vs " + b.name + ": " + `wins/repeats`
	print "average rounds: " + `rounds/repeats`