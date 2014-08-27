class player:
	bank = []
	boats = [0, 0]
	cards = [0, 1, 2, 3, 4, 5, 6]
	name = ""
	handle = None
	def __init__(self, name, handle):
		self.name = name
		self.handle = handle

class game:
	players = []
	weather = 0
	phase = 1
	def addPlayer(self, name, handle):
		self.players.append(player(name,handle))
	def possibleMoves(self, player):
		if self.phase == 1:
			return player.cards
		else:
			return 0
	def run(self):
		# phase 1
		for p in players:
			p.getCard()
		# phase 2
		for p in players:
			p.getMove()
