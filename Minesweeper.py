import numpy as np

class Tile:
	def __init__(self):
		self.mines = 0
		self.is_mine = False
		self.is_revealed = False
		self.is_flagged = False

	def __repr__(self):
		return '1' if self.is_revealed else '0'

class Board:
	def __init__(self, n, m, num_mines):
		self.grid = [[Tile() for i in range(m)]  for i in range(n)]
		# 0 - empty unrevealed
		# 1 - empty revealed
		# 2 - mine
		# 3 - flag
		self.n = n
		self.m = m
		self.num_tiles = self.n * self.m
		self.num_mines = num_mines
		self.tiles_remaining = self.num_tiles-self.num_mines

	def get_tile(self, pos):
		return self.grid[pos[0]][pos[1]]

	def generate_mines(self, inital_pos):
		current_mines = 0
		no_mine_area = self.get_neighbors(inital_pos)
		if self.num_tiles - len(no_mine_area) < self.num_mines:
			self.num_mines = self.num_tiles - len(no_mine_area)
		while current_mines < self.num_mines:
			i = np.random.randint(self.n)
			j = np.random.randint(self.m)
			if (i, j) in no_mine_area or self.is_mine((i,j)):
				continue
			self.grid[i][j].is_mine = True
			current_mines += 1

	def is_blank(self, pos):
		return not self.is_mine(pos) and not self.is_revealed(pos) and not self.is_flagged(pos)

	def is_revealed(self, pos):
		return self.get_tile(pos).is_revealed

	def is_mine(self, pos):
		return self.get_tile(pos).is_mine

	def is_flagged(self, pos):
		return self.get_tile(pos).is_flagged

	def is_won(self):
		return self.tiles_remaining == 0

	def get_neighbors(self, pos):
		neighbors = []
		for i in range(pos[0]-1, pos[1]+2):
			for j in range(pos[0]-1, pos[1]+2):
				if i < 0 or i >= self.n:
					break
				if j < 0 or j >= self.m:
					continue
				neighbors.append((i,j))
		return neighbors

	def reveal_tile(self, pos):
		neighbors = self.get_neighbors(pos)
		for neighbor in neighbors:
			if self.is_blank(neighbor) and self.get_tile(neighbor).mines == 0:
				self.grid[neighbor[0]][neighbor[1]].is_revealed = True
				self.tiles_remaining -= 1
				if self.is_won():
					self.won_game()
				self.reveal_tile(neighbor)

	def won_game(self):
		pass

	def lost_game(self):
		pass

	def __str__(self):
		s = ''
		for row in self.grid:
			s += str(row) + '\n'
		return s

def main():
	b = Board(10, 10, 30)
	b.generate_mines((5,5))
	print(b)
	b.reveal_tile((5,5))
	print(b)

if __name__ == '__main__':
	main()