import itertools
import random

class RandomAgent:
	name = "Random"
	def getMove(self, state):
		moves = state.possibleMoves()
		return moves[random.randrange(1,len(moves))]


class PlayerState:
	bank = []
	boat_pos = [0, 0]
	boat_load = [None, None]
	cards = [0, 1, 2, 3, 4, 5, 6] # 0 is weather
	curr_card = None

class State:
	weather = 0
	phase = 1
	curr_player = 1

	def __init__(self, n):
		self.player_states = list(itertools.repeat(PlayerState(), n))

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
			cps.cards.remove(move)
		elif move>0:
			penalty = 0      
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
		else: 
			#weather
			pass
		
		self.curr_player += 1
		if self.curr_player > len(self.player_states):
			self.curr_player = 1
			self.phase = self.phase % 2 + 1
				
	def turn(self):
		# move boats
		return None		


class Game:
	def __init__(self, players):
		self.players = players
		self.state = State(len(players))
		while True:
			for p in self.players:
				self.state.move(p.getMove(self.state))

Game([RandomAgent(), RandomAgent()]) # start game with 2 rnd players
