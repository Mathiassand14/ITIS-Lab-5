# Grid World game

# Import libraries used for this program
 

import numpy as np
#from Demos.SystemParametersInfo import new_h, new_y
from numpy.f2py.crackfortran import parameterpattern


class GridWorld():
	# Rendering?
	
	rendering = False
	
	# Images
	filenames = ['person.png', 'key.png', 'door.png', 'death.png']
	
	images = None
	
	# Colors
	goodColor = (30, 192, 30)
	badColor = (192, 30, 30)
	pathColor = (225, 220, 225)
	wallColor = (157, 143, 130)
	pygame_on = True

	pygame = None

	def __init__(self, state=None, pygame_on = True) :
		self.pygame_on = pygame_on
		if self.pygame_on:
			import pygame
			self.pygame = pygame
			self.pygame.init()
		self.reward = 0
		if state is None:
			self.x, self.y, self.has_key, self.board, self.score = self.new_game()
		else:
			x, y, has_key, board, score = state
			self.x, self.y, self.has_key, self.board, self.score = x, y, has_key, board.copy(), score
			
		
		if self.pygame_on:
			self.images = [self.pygame.image.load(file) for file in self.filenames]
		
		
		
	def get_state(self):
		return self.x, self.y, self.has_key
		
	def step(self, action):
		# Move character
		if not self.game_over(self.x, self.y, self.has_key, self.board):
			self.x, self.y, self.has_key, self.board, self.score, self.reward = self.move(self.x, self.y, self.has_key, self.board, self.score, action)
		
		# return observation, reward, done
		done = self.game_over(self.x, self.y, self.has_key, self.board)
		return (self.x, self.y, self.has_key), self.reward, done
		
	def render(self):
		if self.pygame_on:
			if not self.rendering:
				self.init_render()
				
				
			# Clear the screen
			self.screen.fill((187,173,160))
			
			border = 3
			
			if self.pygame_on:
				self.pygame.draw.rect(self.screen, (187,173,160), self.pygame.Rect(100,0,600,600))
			for i in range(10):
				for j in range(10):
					val = self.board[i,j]
					col = self.wallColor if val & 8 else self.pathColor
					
					self.pygame.draw.rect(self.screen, col, self.pygame.Rect(100+60*i+border,60*j+border,
						                                                        60-2*border, 60-2*border))
					if val>0:
						x = 105 + 60*i
						y = 5 + 60*j
						if val & 4:
							self.screen.blit(self.images[2], (x, y))
						if val & 2:
							self.screen.blit(self.images[1], (x, y))
						if val & 1:
							if self.game_over(self.x, self.y, self.has_key, self.board) and not self.won(self.x, self.y, self.has_key, self.board):
								self.screen.blit(self.images[3], (x, y))
							else:
								self.screen.blit(self.images[0], (x, y))
							
						
				
			
			text = self.scorefont.render("{:}".format(self.score), True, (0,0,0))
			self.screen.blit(text, (790-text.get_width(), 10))
			
			# Draw game over or you won
			if self.game_over(self.x, self.y, self.has_key, self.board):
				if self.won(self.x, self.y, self.has_key, self.board):
					msg = 'Congratulations!'
					col = self.goodColor
				else:
					msg = 'Game over!'
					col = self.badColor
				text = self.bigfont.render(msg, True, col)
				textpos = text.get_rect(centerx=self.background.get_width()/2)
				textpos.top = 300
				self.screen.blit(text, textpos)
	
			# Display
			self.pygame.display.flip()

	def reset(self):
		self.x, self.y, self.has_key, self.board, self.score = self.new_game()

	def close(self):
		if self.pygame_on:
			self.pygame.quit()
		
		
		
	def init_render(self):
		if self.pygame_on:
			self.screen = self.pygame.display.set_mode([800, 600])
			self.pygame.display.set_caption('Grid World')
			self.background = self.pygame.Surface(self.screen.get_size())
			self.rendering = True
			self.clock = self.pygame.time.Clock()
	
			# Set up game
			self.bigfont = self.pygame.font.Font(None, 80)
			self.scorefont = self.pygame.font.Font(None, 30)
			
	@staticmethod
	def game_over(x, y, has_key, board):
		# Are we on a death square?
		if board[x,y] & 8:
			return True
		
		# Are we on the door with the key?
		# Are we on the door with the key?
		if board[x,y] & 4 and not np.any(board & 2):
			return True
		
		return False
	
	@staticmethod
	def won(x, y, has_key, board):
		# Are we on the door with the key?
		if board[x,y] & 4 and not np.any(board & 2):
			return True
		
		return False
		
		
	def move(self, x, y, has_key, board, score, direction='left'):
		new_x, new_y = x, y
		if direction=='left':
			if x>0:
				new_x = x-1
			
		elif direction=='right':
			if x<9:
				new_x = x+1
			
		elif direction=='up':
			if y>0:
				new_y = y-1
			
		elif direction=='down':
			if y<9:
				new_y = y+1
			
		reward = -1
		
		# Update position
		board[x,y] -= 1
		board[new_x, new_y] += 1
		self.x, self.y = new_x, new_y
		
		# Take key
		if board[new_x, new_y] & 2:
			board[new_x, new_y] -= 2
			reward = 50
			has_key = True
		
		# On door with key?
		if board[new_x, new_y] & 4 and not np.any(board & 2):
			reward = 100
		
		# On death?
		if board[new_x, new_y] & 8:
			reward = -100

		score += reward
		return new_x, new_y, has_key, board, score, reward
	 
	@staticmethod
	def new_game():
		board = np.loadtxt('board.txt', dtype=int).T
		if board.shape != (10,10) or np.sum(board==2) != 1 or np.sum(board==4) != 1:
			raise Exception('board.txt corrupt')

		start_x, start_y = np.where(board == 0)
		i = np.random.randint(len(start_x))
		x, y = start_x[i], start_y[i]
		board[x, y] = 1
		
		score = 0
		has_key = False
		return x, y, has_key, board, score
	


