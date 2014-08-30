import pdb, traceback, sys
from copy import deepcopy
from itertools import product
from random import randrange

class AgentRandom:
	def getMove(self, game):
		moves = game.possibleMoves()
		return moves[randrange(1,len(moves))-1]

class AgentHuman:
	def getMove(self, game):
		moves = game.possibleMoves()
		for i, m in enumerate(moves):
			print i, m
		return moves[input("Which move do you want to perform?")]

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
		self.direction = 0
		self.load = False
		self.after = False
		self.steal = False
		self.weather = 0

	def __str__(self):
		return ("weather " + self.weather) if self.weather else (
			("up" if self.direction == 1 else "down") +
			(" load" if self.load else "") +
			(" after" if self.after else "") +
			(" steal" if self.steal else "") )

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

	def possibleMoves(self):
		p = self.players[self.curr_player]
		if self.phase == 1:
			return p.cards
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

	def makeMove(self, move):
		p = self.players[self.curr_player]
		if not move in self.possibleMoves():
			raise Exception('invalid move')

		if self.phase == 1:
			p.curr_card = move
		else:
			p.cards.remove(p.curr_card)
			boat = p.boat

			if move.load:
				boat.stone = not boat.stone

			if move.direction:
				boat.position += move.direction * (p.curr_card - 2 * move.load)

				if boat.position < 0: boat.position = 0

				if boat.position == 0 and boat.stone:
					p.bank.append(boat.stone)
					boat.stone = False
				if boat.position > 7:
					boat.position = None
					boat.stone = False

			if move.steal:
				boat.stone = move.steal.stone
				move.steal.stone = False

			self.weather += move.weather

		# next player
		self.curr_player += 1

		# last player moved
		if self.curr_player == len(self.players):
			# TODO: rotate startplayer
			self.curr_player = 0
			if self.phase == 1:
				self.phase = 2
			else:
				self.flow()
				self.phase = 1
				self.round += 1
				if self.round % 7 == 1:
					self.returnCards()

		print "round "+`self.round`+" phase "+`self.phase`+" player "+`self.curr_player+1`

	def flow(self):
		for p in self.players:
			if p.boat.position: p.boat.position += self.weather

	def returnCards(self):
		for p in self.players:
			p.cards = [0,1,2,3,4,5,6]

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
	game.players.append(Player("Human", AgentHuman()))
	game.players.append(Player("Random", AgentHuman()))
	while True:
		for player in game.players:
			move = player.agent.getMove(game.secure())
			print move
			game.makeMove(move)
except:
	tpes, value, tb = sys.exc_info()
	traceback.print_exc()
	pdb.post_mortem(tb)
