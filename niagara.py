import pdb, traceback, sys
from copy import deepcopy
from itertools import product
from random import randrange

class AgentRandom:
	def getMove(self, game):
		moves = game.possibleMoves()
		return moves[randrange(0,len(moves))]

class AgentHuman:
	def getMove(self, game):
		me = game.players[game.curr_player]
		moves = game.possibleMoves()
		print "you are standing at "+`me.boat.position`
		for i, m in enumerate(moves):
			print " ",i, m
		try:
			return moves[input(" Which move do you want to perform?")]
		except KeyboardInterrupt:
				raise
		except:
			return moves[0]

class Boat:
	def __init__(self):
		self.position = 0
		self.stone = False

class Player:
	def __init__(self, name, agent):
		self.name = name
		self.agent = agent
		self.bank = []
		self.boat = Boat()
		self.cards = [0,1,2,3,4,5,6] # 0 is weather
		self.curr_card = None

class Move:
	def __init__(self):
		# phase 1
		self.card = None
		self.buyback = False
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
		return self.__dict__ == other.__dict__

class Game:
	def __init__(self):
		self.weather = 0
		self.phase = 1
		self.round = 1
		self.curr_player = 0
		self.players = []
		self.winners = []

	def possibleMoves(self):
		p = self.players[self.curr_player]
		if self.phase == 1:
			moves = []
			for c in p.cards:
				move = Move()
				move.card = c
				# force buyback
				if p.boat.position == None:
					move.buyback = True
				moves.append(move)
			return moves

		else:
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
			# movement
			else:
				boat = p.boat
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

							victim = [p.boat for p in self.players if p.boat.position == boat.position + distance and p.boat.stone]
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

			return moves

	def turn(self):
		p = self.players[self.curr_player]
		move = p.agent.getMove(game.secure())
		if not move in self.possibleMoves():
			raise Exception('invalid move')

		print "moving " + p.name + ": ", move

		if self.phase == 1:
			p.curr_card = move.card
			if move.buyback:
				p.boat.position = 0
				try: a.pop()
				except: pass

		else:
			p.cards.remove(p.curr_card)
			boat = p.boat

			if move.load:
				boat.stone = not boat.stone

			if move.direction:
				boat.position += move.direction * (p.curr_card - 2 * move.load)

				if boat.position < 0: boat.position = 0

				# add stone to bank
				if boat.position == 0 and boat.stone:
					p.bank.append(boat.stone)
					boat.stone = False

			if move.steal:
				boat.stone = move.steal.stone
				move.steal.stone = False

			self.weather += move.weather

		# next player
		self.curr_player += 1
		self.curr_player = self.curr_player % len(self.players)

		# last player moved
		if self.curr_player == self.ring():
			if self.phase == 1:
				self.phase = 2
			else:
				self.endRound()
				self.phase = 1
				self.round += 1
				self.curr_player = self.ring()

		print "round "+`self.round`+" phase "+`self.phase`+" player "+`self.players[self.curr_player].name`

	def ring(self):
		return (self.round - 1) % len(self.players)

	def endRound(self):
		# flow river
		moves = [p.curr_card for p in self.players if p.curr_card]
		flow = min(moves) if moves else 0 + self.weather
		flow = max(flow, 0)
		print "flowing " + `flow`
		print ""
		for p in self.players:
			# move boats
			if p.boat.position: p.boat.position += flow
			# sink boats
			if p.boat.position > 7:
				p.boat.position = None
				p.boat.stone = False

		# return cards
		if self.round % 7 == 0:
			for p in self.players:
				p.cards = [0,1,2,3,4,5,6]

		# determine winners
		self.winners = [p for p in self.players if len(p.bank)]

	def secure(self):
		copy = deepcopy(self)
		for p in copy.players: pass
			# TODO: here we want to remove the curr card to avoid cheating
			# but right now it has to be known for the current player to show possible moves
			# p.curr_card = None
			# p.agent = None
		return copy

try:
	game = Game()
	game.players.append(Player("Random 1", AgentRandom()))
	game.players.append(Player("Random 2", AgentRandom()))
	while not game.winners:
		game.turn()
	print game.winners[0].name
except KeyboardInterrupt:
	sys.exit()
except:
	tpes, value, tb = sys.exc_info()
	traceback.print_exc()
	pdb.post_mortem(tb)
