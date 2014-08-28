from copy import deepcopy
from itertools import repeat
from random import randrange

class RandomAgent:
	name = "Random"
	def getMove(self, state):
		moves = state.possibleMoves()
		return moves[randrange(1,len(moves))-1]

class PlayerState:
	bank = []
	boat_pos = [0, 0]
	boat_load = [None, None]
	cards = [0,1,2,3,4,5,6] # 0 is weather
	curr_card = None

class State:
	weather = 0
	phase = 1
	curr_player = 0

	def __init__(self, n):
		self.player_states = list(repeat(PlayerState(), n))

	def possibleMoves(self):
		cps = self.player_states[self.curr_player]
		if self.phase == 1:
			return cps.cards
		else:
			# TODO!!!
			poss_moves = []
			return poss_moves

	def move(self, move):
		cps = self.player_states[self.curr_player]
		if not move in self.possibleMoves():
			raise Exception('unvalid move')

		if self.phase == 1:
			cps.curr_card = move
		else:
			penalty = 0      
			cps.cards.pop(cps.curr_card)

			# TODO: care about order ln/ud
			if 'l' in move: # load
				cps.boat_load[1] = True
				penalty = 2           
			elif 'n' in move: # unload
				cps.boat_load[1] = False
				penalty = 2   

			if 'u' in move: # up
				cps.boat_pos[1] -= cps.curr_card - penalty
				# check for steal
			elif 'd' in move: # down
				cps.boat_pos[1] += cps.curr_card - penalty

			if move == '+':
				self.weather += 1
			elif move == '-':
				self.weather -= 1
		
		self.curr_player += 1
		if self.curr_player == len(self.player_states):
			self.curr_player = 0
			if self.phase == 2:
				self.flow()
			self.phase = self.phase % 2 + 1
				
	def flow(self):
		for p in self.player_states
			p.boat_pos += self.weather

	def secure(self):
		copy = deepcopy(self)
		for p in copy.player_states:
			p.curr_card = None
		return copy

class Game:
	def __init__(self, players):
		self.players = players
		self.state = State(len(players))
		while True:
			for p in self.players:
				move = p.getMove(self.state.secure())
				print move
				self.state.move(move)

Game([RandomAgent(), RandomAgent()]) # start game with 2 rnd players
