# alex agents
import pdb
from random import choice

class AgentHuman:
    def __init__(self):
        self.name = raw_input("What is your name?")
    def askMoves(self, moves):
        print 'choose a move'
        for i, m in enumerate(moves):
            print "", i, m
        try:
            return moves[int(raw_input('^'))]
        except KeyboardInterrupt:
            raise
        except:
            return moves[0]
    def getMove1(self, game):
        return self.askMoves(game.possibleMoves())
    def getMove2(self, game):
        poss = game.possibleMoves()
        return [self.askMoves(poss[0]), self.askMoves(poss[1])]

class AgentDet:
    def __init__(self):
        self.name = "Det"

    def getMove1(self, g):
        return choice(g.possibleMoves())

    def getMove2(self, g):
        moves = g.possibleMoves()
        me  = g.players[g.curr_player]
        cmb = []
        for i in range(0,2):
            boat = me.boats[i]
            mvs = moves[i]
            if boat.jewel:
                cmb.append(choice(filterMoves(mvs, [('direction', '==-1') , ('load', '==False')])))
            else:
                f = filterMoves(mvs, [('load', ''), ('direction', '==-1')], strict=True)
                if f:
                    cmb.append(choice(f))
                else:
                    cmb.append(choice(filterMoves(mvs, ('direction', '==1'))))
        return cmb 

def filterMoves(ms, f, strict = False):
    if isinstance(f, tuple):
        fms = filter(lambda m: eval('getattr(m,f[0])' + f[1]), ms)   
        return fms if fms or strict else ms
    else:
        q = [ms]
        q.extend(f)
        return reduce(lambda ms, f: filterMoves(ms, f, strict), q)
