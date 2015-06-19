from game import Game
from agentbasic import AgentHuman, AgentRule
from itertools import combinations
import sys

availableAgents = {'human': AgentHuman, 'rule': AgentRule}
agents=[]

for arg in sys.argv[1:]:
    agents.append(availableAgents[arg]())

for i, agent in enumerate(agents):
    agent.name = 'P'+`i+1`+' '+agent.name

repeats = 10
wins = 0
rounds = 0
for i in range (0, repeats):
    game = 0
    game = Game(agents)
    game.run()
    if a in game.winners:
        wins += 1
    rounds += game.round
print ""
print "result after " + `repeats` + " runs:"
print a.name + " vs " + b.name + ": " + `float(wins)/repeats`
print "average rounds: " + `rounds/repeats`
