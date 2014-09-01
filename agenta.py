# alex agents
import pdb
from random import choice

class AgentDet:
    def __init__(self):
        self.name = "Det"

    def getMove(self, g):
        moves = g.possibleMoves()
        me  = g.players[g.curr_player]
        cmb = []
        if g.phase == 2:
            for i in range(0,2):
                boat = me.boats[i]
                mvs = moves[0]
                if boat.stone:
                    cmb.append(choice(filterMoves(mvs, [('direction', -1) , ('load', False)])))
                else:
                    f = filterMoves(mvs, [('load', True), ('direction', -1)], strict=True)
                    if f:
                        cmb.append(choice(f))
                    else:
                        cmb.append(choice(filterMoves(mvs, ('direction', 1))))
            return cmb 
        return choice(g.possibleMoves())

def filterMoves(ms, f, strict = False):
    if isinstance(f, tuple):
        fms = filter(lambda m: getattr(m,f[0])==f[1], ms)   
        return fms if fms or strict else ms
    else:
        q = [ms]
        q.extend(f)
        return reduce(lambda ms, f: filterMoves(ms, f, strict), q)
