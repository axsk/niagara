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
        self.stone = False

class Player:
    def __init__(self, agent):
        self.agent = agent
        self.bank = []
        self.boats = (Boat(), Boat())
        self.cards = [0,1,2,3,4,5,6] # 0 is weather
        self.curr_card = None

class Move:
    def __init__(self, card=None, buyback=0):
        # phase 1
        self.card = card
        self.buyback = buyback
        # phase 2
        self.direction = None
        self.load = False
        self.after = False
        self.steal = False
        self.weather = 0

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
        return self.__str__() == other.__str__()

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

    def sunkboats(self, player):
        return [boat for boat in player.boats if boat.position == None]

    def possibleMoves(self):
        p = self.players[self.curr_player]
        # phase 1
        if self.phase == 1:
            moves = []
            nsb = len(self.sunkboats(p))
            for c in p.cards:
                if nsb == 0:
                    moves.append(Move(card=c))
                elif nsb == 1:
                    moves.append(Move(card=c))
                    if len(p.bank):
                        moves.append(Move(card=c, buyback=1))
                elif sunkboats == 2:
                    moves.append(Move(card=c, buyback=1))
                    if len(p.bank):
                        moves.append(Move(card=c, buyback=2))
            return moves

        # phase 2
        else:
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
                    doublemoves.append(moves)
                    doublemoves.append(moves)
                    break
                # movement
                else:
                    for (direction, load, after, steal) in \
                        product([1,-1], *[[True, False]]*3):

                        distance = (p.curr_card - 2 * load) * direction

                        # boat is on board
                        if boat.position != None:
                            if load:
                                # not enough points
                                if p.curr_card < 2: continue
                                # boat wants to load but is not at bay
                                if boat.position + distance * (after) < 3: continue
                            else:
                                if after: continue

                            if steal:
                                # not moving upwards
                                if not distance < 0: continue

                                # either there is a stone or its beeing loaded
                                if boat.stone ^ load: continue

                                victim = [vboat for vboat in p.boats for p in self.players if vboat.position == boat.position + distance and vboat.stone]
                                if victim:
                                    # TODO: allow choosing victim
                                    steal = victim[0]
                                else:
                                    continue
                            move = Move()
                            move.direction = direction
                            move.load = load
                            move.after = after
                            move.steal = steal
                            moves.append(move)
                        else:
                            moves.append(Move())
                doublemoves.append(moves)
            return doublemoves

    def turn(self):
        p = self.players[self.curr_player]
        move = p.agent.getMove(self.secure())
        if type(move) == list:
            for mv, pos in zip(move, self.possibleMoves()):
                if not (mv in pos or mv in move): 
                    raise Exception('invalid move')
        else:
            if not move in self.possibleMoves():
                raise Exception('invalid move')

        print p.agent.name + ": ", move

        if self.phase == 1:
            p.curr_card = move.card
            sb = self.sunkboats(p)
            for i in range(0,move.buyback):
                sb[i].position = 0
                if len(p.bank): p.bank.pop()
                print p.agent.name + " bought back"

        else:
            moves = move
            self.weather += move[0].weather
            p.cards.remove(p.curr_card)
            for move, boat in zip(moves, p.boats):
                if move.load:
                    boat.stone = not boat.stone
                    print p.agent.name + ( " " if boat.stone else " un" ) + "loaded a stone"

                if move.direction:
                    boat.position += move.direction * (p.curr_card - 2 * move.load)

                    if boat.position < 0: boat.position = 0

                    # add stone to bank
                    if boat.position == 0 and boat.stone:
                        p.bank.append(boat.stone)
                        boat.stone = False
                        print p.agent.name + ' got a stone'

                if move.steal:
                    boat.stone = move.steal.stone
                    move.steal.stone = False
                    print p.agent.name + ' stole a stone'


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
        flow = min(moves) if moves else 0 + self.weather
        flow = max(flow, 0)
        print "flowing " + `flow`

        # move boats
        for p in self.players:
            boat = p.boats[0]
            if boat.position: boat.position += flow
            # sink boats
            if boat.position > 7:
                boat.position = None
                boat.stone = False
                print p.agent.name + " fell down"

        # return cards
        if self.round % 7 == 0:
            for p in self.players:
                p.cards = [0,1,2,3,4,5,6]

        # determine winners
        self.winners = [p for p in self.players if len(p.bank) == 2]

        # prepare next round
        self.round += 1
        self.curr_player = self.ring()

    def printState(self):
    # underline player if he has a stone
        def markstone(str, boat):
            return '\033[4m' + `str` + '\033[0m' if boat.stone else `str`
        text = ''
        for bay in range(0,8):
            baytext = ""
            for player in self.players:
                for boat in player.boats:
                    baytext += markstone(player.id, boat) if boat.position == bay else ""
            baytext = baytext if baytext else 'o'
            text += baytext + ' '
        print ''
        print text + '(~' + `self.weather` + '~)'
        print ''

    def secure(self):
        copy = deepcopy(self)
        for p in copy.players: pass
            # TODO: here we want to remove the curr card to avoid cheating
            # but right now it has to be known for the current player to show possible moves
            # p.curr_card = None
            # p.agent = None
        return copy

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
        print self.winners[0].agent.name + " won after " + `self.round` + " rounds"
        return self
