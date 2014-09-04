from niagara import Game
from agentbasic import AgentHuman, AgentDet
from itertools import combinations

agents = [AgentDet(), AgentDet()]
agents[0].name = 'p1'
agents[1].name = 'p2'
repeats = 10

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
    print ""
    print "result after " + `repeats` + " runs:"
    print a.name + " vs " + b.name + ": " + `float(wins)/repeats`
    print "average rounds: " + `rounds/repeats`
