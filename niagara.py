from copy import deepcopy
from itertools import repeat, product
from random import randrange

class RandomAgent:
	name = "Random"
	def getMove(self, state):
		moves = state.possibleMoves()
		return moves[randrange(1,len(moves))-1]

class HumanPlayer:
	def __init__(self, name):
		self.name = name

	def getMove(self, state):
		moves = state.possibleMoves()
		for i, m in enumerate(moves):
			print i, m
		return moves[input("Which move do you want to perform?")]

class Boat:
	position = 0
	stone = False

class PlayerState:
	bank = []
	boat = Boat()
	cards = [0,1,2,3,4,5,6] # 0 is weather
	curr_card = None

class Move:
	def __init__(self, dict):
		for key in dict:
			self.set(key,dict[key])

	direction = 0
	load = False
	after = False
	steal = False
	weather = 0

class State:
	weather = 0
	phase = 1
	curr_player = 0

	def __init__(self, n):
		self.player_states = list(repeat(PlayerState(), n))

	def possibleMoves(self):
		p = self.player_states[self.curr_player]
		if self.phase == 1:
			return p.cards
		else:
			moves = []

			# weather
			if p.curr_card == 0:
				if self.weather < 2:
				  moves.append(Move('weather', 1))
				if self.weather > -1:
					moves.append(Move({'weather': -1}))
		  # movement
			else:
				boat = p.boat
				for (direction, load, after, steal) in \
					product([1,-1], *[[True, False]]*3):

					distance = (p.curr_card - 2 * load) * direction

					# boat is on board
					if boat.position:
						if boat.load:
							# not enough points
							if p.curr_card < 2: continue
							# boat wants to load but is not at bay
							if boat.position + distance * (after) < 3: continue

						if steal:
							# not moving upwards
							if not distance < 0: continue

							# either there is a stone or its beeing loaded
							if boat.stone ^ load: continue

							victim = [p.boat for p in self.player_states if p.boat.position == boat.position + distance and p.boat.stone]
							if victim:
								# TODO: allow choosing victim
								steal = victim[0]
							else:
							  continue

						moves.append(Move({'direction': direction, 'load': load, 'after': after, 'steal': steal}))

			return moves

	def makeMove(self, move):
		p = self.player_states[self.curr_player]
		if not move in self.possibleMoves():
			raise Exception('invalid move')

		if self.phase == 1:
			p.curr_card = move
		else:
			p.cards.pop(p.curr_card)
			boat = p.boat

			if move.load:
				boat.stone = not boat.stone
				penalty += 2

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
		if self.curr_player == len(self.player_states):
			# TODO: rotate startplayer
			self.curr_player = 0
			if self.phase == 2:
				self.flow()
			self.phase = self.phase % 2 + 1

	def flow(self):
		for p in self.player_states:
			p.boat.position += self.weather

	def secure(self):
		copy = deepcopy(self)
		for p in copy.player_states:
			# TODO: here we want to remove the curr card to avoid cheating
			# but right now it has to be known for the current player to show possible moves
			# p.curr_card = None
			pass
		return copy

class Game:
	def __init__(self, players):
		self.players = players
		self.state = State(len(players))
		while True:
			for p in self.players:
				move = p.getMove(self.state.secure())
				print move
				self.state.makeMove(move)

Game([RandomAgent(), HumanPlayer("Human")]) # start game with 2 rnd players
