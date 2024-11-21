# Grid World: AI-controlled play

# Instructions:
#   Move up, down, left, or right to move the character. The 
#   objective is to find the key and get to the door
#
# Control:
#    arrows  : Merge up, down, left, or right
#    s       : Toggle slow play
#    a       : Toggle AI player
#    d       : Toggle rendering 
#    r       : Restart game
#    q / ESC : Quit

from GridWorld import GridWorld
import numpy as np
import pygame
from collections import defaultdict
from GetMatrices import EmptyStateMatrix
import collections
import random

# Initialize the environment
env = GridWorld()
env.reset()
x, y, has_key = env.get_state()

# Definitions and default settings
actions = ['left', 'right', 'up', 'down']
exit_program = False
action_taken = False
slow = True
runai = True
render = True
done = False

# Game clock
clock = pygame.time.Clock()

# INSERT YOUR CODE HERE (1/2)
# Define data structure for q-table and define the discount factor
state_value = EmptyStateMatrix(0)
# END OF YOUR CODE (1/2)

while not exit_program:

	if render:
		env.render()

	# Slow down rendering to 5 fps
	if slow and runai:
		clock.tick(5)

	# Automatic reset environment in AI mode
	if done and runai:
		env.reset()
		x, y, has_key = env.get_state()
		done = False
		continue

	# Process game events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit_program = True
		if event.type == pygame.KEYDOWN:
			if event.key in [pygame.K_ESCAPE, pygame.K_q]:
				exit_program = True
			if event.key == pygame.K_UP:
				action, action_taken = 'up', True
			if event.key == pygame.K_DOWN:
				action, action_taken = 'down', True
			if event.key == pygame.K_RIGHT:
				action, action_taken = 'right', True
			if event.key == pygame.K_LEFT:
				action, action_taken = 'left', True
			if event.key == pygame.K_r:
				env.reset()
			if event.key == pygame.K_d:
				render = not render
			if event.key == pygame.K_s:
				slow = not slow
			if event.key == pygame.K_a:
				runai = not runai
				clock.tick(5)
			
		

	# AI controller (enable/disable by pressing 'a')
	if runai:
		# INSERT YOUR CODE HERE (2/2)
		#
		# Implement a Grid World AI (q-learning): Control the person by
		# learning the optimal actions through trial and error
		#
		# The state of the environment is available in the variables
		#    x, y     : Coordinates of the person (integers 0-9)
		#    has_key  : Has key or not (boolean)
		#
		# To take an action in the environment, use the call
		#    (x, y, has_key), reward, done = env.step(action)
		#
		#    This gives you an updated state and reward as well as a Boolean
		#    done indicating if the game is finished. When the AI is running,
		#    the game restarts if done=True
		
		#Get the best action
		action = max(state_value[x][y][has_key].items(), key = lambda item: item[1])[0]

		#Step
		(x1, y1, has_key1), reward, done = env.step(action)

		#Update the state value
		state_value[x][y][has_key][action] = reward + 0.9 * max(state_value[x1][y1][has_key1].values())
		
		#Update the state to the new state
		x, y, has_key = x1, y1, has_key1

		
		# END OF YOUR CODE (2/2)

	# Human controller
	else:
		if action_taken:
			(x, y, has_key), reward, done = env.step(action)
			action_taken = False
		
	
env.close()
