# alex agents
import pdb
from random import choice

class AgentDet:
	def __init__(self):
		self.name = "Det"

	def getMove(self, g):
		mvs = g.possibleMoves()
		me  = g.players[g.curr_player]
		
		if g.phase == 2:
			if me.boat.stone:
				return choice(filterMoves(mvs, [('direction', -1) , ('load', False)]))
			else:
				f = filterMoves(mvs, [('load', True), ('direction', -1)], strict=True)
				if f:
					return choice(f)
				else:
					return choice(filterMoves(mvs, ('direction', 1)))
		
		return choice(g.possibleMoves())

def filterMoves(ms, f, strict = False):
	if isinstance(f, tuple):
		fms = filter(lambda m: getattr(m,f[0])==f[1], ms)	
		return fms if fms or strict else ms
	else:
		q = [ms]
		q.extend(f)
		return reduce(lambda ms, f: filterMoves(ms, f, strict), q)