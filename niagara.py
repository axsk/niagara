import pdb, traceback, sys
from copy import deepcopy
from itertools import product
from random import choice

class AgentRandom:
    def __init__(self):
        self.name = "Random"
    def getMove(self, game):
        return choice(game.possibleMoves())

class AgentHuman:
    def __init__(self):
        self.name = input("What is your name?")
    def getMove(self, game):
        moves = game.possibleMoves()
        print 'choose a move'
        for i, m in enumerate(moves):
            print "",i, m
        try:
            return moves[input('^')]
        except KeyboardInterrupt:
            raise
        except:
            return moves[0]

class Boat:
    def __init__(self):
        self.position = 0
        self.jewel = False
        self.branch = False

class Player:
    def __init__(self, agent):
        self.agent = agent
        self.bank = []
        self.boats = (Boat(), Boat())
        self.cards = [0, 1, 2, 3, 4, 5, 6]  # 0 is weather
        self.curr_card = None

class Move:
    def __init__(self, card=None, buyback=0, direction=0, load=False,
            after=False, steal=False, weather=0, branch=False):
        # phase 1
        self.card = card
        self.buyback = buyback
        # phase 2
        self.direction = direction
        self.load = load
        self.after = after
        self.steal = steal
        self.weather = weather
        self.branch = branch

    def __str__(self):
        if self.card != None:
            return (`self.card` if self.card>0 else "weather" +
                ("buyback" if self.buyback else "") )
        elif self.weather:
            return "weather " + ("+" if self.weather == 1 else "-")
        else:
            return (("up" if self.direction == -1 else "down") +
                (" load" if self.load else "") +
                (" after" if self.after else "") +
                (" steal" if self.steal else ""))

    # let Move()==Move() be true (comparison by values)
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Game:
    def __init__(self, agents):
        self.weather = 0
        self.phase = 1
        self.round = 1
        self.curr_player = 0
        self.players = []
        for agent in agents:
            self.players.append(Player(agent))
            self.players[-1].id = len(self.players)
        self.winners = []
        self.bay = [[]]*3 + [[i]*7 for i in range(3, 8)]

    def currPlayer(self):
        return self.players[self.curr_player]

    def sunkboats(self, player):
        return [boat for boat in player.boats if boat.position == None]

    def possibleMoves(self):
        if self.phase == 1:
            return self.possMoves1()
        else:
            return self.possMoves2()

    def possMoves1(self):
        p = self.currPlayer()
        moves = []
        nsb = len(self.sunkboats(p))
        for c in p.cards:
            if nsb == 0:
                moves.append(Move(card=c))
            elif nsb == 1:
                moves.append(Move(card=c))
                if len(p.bank):
                    moves.append(Move(card=c, buyback=1))
            elif nsb == 2:
                moves.append(Move(card=c, buyback=1))
                if len(p.bank):
                    moves.append(Move(card=c, buyback=2))
        return moves
    
    def possMoves2(self):
        p = self.currPlayer()
        doublemoves = []
        for boat in p.boats:
            moves = []
            # weather
            if p.curr_card == 0:
                if self.weather < 2:
                    move = Move()
                    move.weather = 1
                    moves.append(move)
                if self.weather > -1:
                    move = Move()
                    move.weather = -1
                    moves.append(move)
                return [moves, moves]

            # boat fell down
            if boat.position == None:
                doublemoves.append([Move()])
                continue

            # movement
            for (direction, load, after, steal) in \
                product([1,-1], *[[True, False]]*3):

                distance = (p.curr_card - (2 if load else 0)) * direction

                if load:
                    # not enough points
                    if p.curr_card < 2: continue
                    # boat wants to load but is not at bay
                    loadpos = boat.position + distance * (after)
                    if not (2 < loadpos < 8): continue
                    loads = ['unload'] if boat.jewel else set(self.bay[loadpos])
                else:
                    if after: continue
                    loads = [False]

                if steal:
                    continue # TODO: REMOVE HOTFIX
                    # not moving upwards
                    if not distance < 0: continue

                    # either there is a jewel or its beeing loaded
                    if boat.jewel ^ load: continue

                    vboats = [vboat for vboat in p.boats for p in self.players if vboat.position == boat.position + distance and vboat.jewel]
                    if vboats:
                        # TODO: allow choosing victim
                        steal = vboats[0]
                    else:
                        continue

                if boat.position < 6 and boat.position+distance >= 6:
                    branches = [1, 2]
                else:
                    branches = [0]

                for (l, b) in product(loads, branches):
                    moves.append(Move(direction=direction, load=l, after=after, steal=steal, branch=b))

            doublemoves.append(moves)
        return doublemoves

    def turn(self):
        if self.phase == 1:
            self.turn1()
        else:
            self.turn2()

    def turn1(self):
        p = self.currPlayer()
        move = p.agent.getMove1(self.secure())
        if not move in self.possMoves1(): raise Exception('invalid move')

        print p.agent.name + ": ", move

        p.curr_card = move.card
        sb = self.sunkboats(p)
        for i in range(0,move.buyback):
            sb[i].position = 0
            if len(p.bank): 
                jew = p.bank.pop()
                self.bay[jew].append(jew)
            print p.agent.name + " bought back"

        self.curr_player = (self.curr_player + 1) % len(self.players)

    def turn2(self):
        p = self.currPlayer()
        moves = p.agent.getMove2(self.secure())
        for move, poss in zip(moves, self.possMoves2()):
            if not move in poss: raise('invalid move')

        self.weather += moves[0].weather

        for move, boat in zip(moves, p.boats):
            if boat.position == None: continue
            print p.agent.name + ": ", move

            newpos = boat.position + move.direction * (p.curr_card - (2 if move.load else 0))
            loadpos = newpos if move.after else boat.position

            if move.load:
                if move.load == 'unload':
                    self.bay[loadpos] = boat.jewel
                    boat.jewel = False
                else:
                    boat.jewel = move.load
                    try:
                        self.bay[loadpos].remove(move.load)
                    except:
                        print "bug: donated jewel"
                print p.agent.name + " loaded " + `move.load`

            if move.direction:
                boat.position = newpos

                if boat.position < 0: boat.position = 0

                # add jewel to bank
                if boat.position == 0 and boat.jewel:
                    p.bank.append(boat.jewel)
                    boat.jewel = False
                    print p.agent.name + ' got a jewel'

            if move.steal:
                boat.jewel = move.steal.jewel
                move.steal.jewel = False
                print p.agent.name + ' stole a jewel'

            boat.branch = move.branch
        p.cards.remove(p.curr_card)
        self.curr_player = (self.curr_player + 1) % len(self.players)

    def ring(self):
        return (self.round - 1) % len(self.players)

    def playRound(self):

        self.printState()

        for i in [1, 2]:
            self.phase = i
            for j in range(0,len(self.players)):
                self.turn()

        # compute flow
        moves = [p.curr_card for p in self.players if p.curr_card]
        flow = (min(moves) if moves else 0) + self.weather
        flow = max(flow, 0)
        print "flowing " + `flow`

        # move boats
        for p in self.players:
            for boat in p.boats:
                if boat.position: boat.position += flow
                # correction for branches
                if boat.position > 5:
                    inact = (boat.branch - self.round) % 2
                    boat.position -= (boat.position - 5 + inact) // 2
                # sink boats
                if boat.position > 7:
                    boat.position = None
                    if boat.jewel: 
                        self.bay[boat.jewel].append(boat.jewel) 
                        boat.jewel = False
                    print p.agent.name + " fell down"

        # return cards
        if self.round % 7 == 0:
            for p in self.players:
                p.cards = [0, 1, 2, 3, 4, 5, 6]

        # determine winners
        self.winners = self.getWinners()

        # prepare next round
        self.round += 1
        self.curr_player = self.ring()

    def getWinners(self):
        winners = []
        for p in self.players:
            if (any(p.bank.count(i)==4 for i in [3,4,5,6,7])
                or set([3,4,5,6,7]).issubset(set(p.bank))
                or len(p.bank)>=7):
                winners.append(p.agent)
        return winners

    def printState(self):
    # underline player if he has a jewel
        t = ['bay  ','river','load ']
        for bay in range(0,8):
            tt = ['','','']
            for player in self.players:
                for boat in [b for b in player.boats if b.position == bay]:
                    tt[1] += `player.id`
                    tt[2] += `boat.jewel` if boat.jewel else ' '
            tt[0] = `len(self.bay[bay])`
            l = max(len(tt[0]), len(tt[1]))
            for i in range(0,3):
                tt[i] += ' ' * (l-len(tt[i]))
                t[i] += tt[i] + ' ' 
        print ''
        t[0] += 'R' + `self.round`
        t[1] += `[len(p.bank) for p in self.players]` 
        t[2] += '(~' + `self.weather` + '~)'
        for i in range(0,3):
            print t[i]
        print ''

    def secure(self):
        return self

    def run(self):
        while not self.winners:
            try:
                self.playRound()
            except KeyboardInterrupt:
                sys.exit()
            except:
                types, value, tb = sys.exc_info()
                traceback.print_exc()
                pdb.post_mortem(tb)
        for winner in self.winners:
            print winner.name + " won after " + `self.round` + " rounds"
        return self
