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
from GetMatrices import EmptyStateMatrix
import collections
import time

# Initialize the environment



def run_game(
	env = None,
	runai = True,
	render = True,
	slow = False,
	done = False,
	exit_program = False,
	action_taken = False,
	gamma = 0.9,
	index = 0,
	res = None):
	
	if env is None:
		env = GridWorld(pygame_on = render)
		env.reset()
	
	start_time = time.time()
	
	if res is None:
		res = [None]
	next_state = env.get_state()
	# Game clock
	if env.pygame_on:
		clock = env.pygame.time.Clock()
	
	
	# INSERT YOUR CODE HERE (1/2)
	# Define data structure for q-table and define the discount factor
	state_value = EmptyStateMatrix(0)
	state_value_dd = collections.defaultdict(lambda: {'left': 0, 'right': 0, 'up': 0, 'down': 0})
	
	deaths = 0
	wins = 0
	moves = 0
	
	#default dict
	def_dict = True
	#def_dict = False
	# END OF YOUR CODE (1/2)
	
	while not exit_program:
		
		if render:
			env.render()
		
		# Slow down rendering to 5 fps
		if slow and runai:
			clock.tick(5)
			pass
		
		# Automatic reset environment in AI mode
		if done and runai:
			env.reset()
			next_state = x, y, has_key = env.get_state()
			done = False
			continue
		
		# Process game events
		if env.pygame_on:
			for event in env.pygame.event.get():
				if event.type == env.pygame.QUIT:
					exit_program = True
				if event.type == env.pygame.KEYDOWN:
					if event.key in [env.pygame.K_ESCAPE, env.pygame.K_q]:
						exit_program = True
					if event.key == env.pygame.K_UP:
						action, action_taken = 'up', True
					if event.key == env.pygame.K_DOWN:
						action, action_taken = 'down', True
					if event.key == env.pygame.K_RIGHT:
						action, action_taken = 'right', True
					if event.key == env.pygame.K_LEFT:
						action, action_taken = 'left', True
					if event.key ==env. pygame.K_r:
						env.reset()
					if event.key == env.pygame.K_d:
						render = not render
					if event.key == env.pygame.K_s:
						slow = not slow
					if event.key == env.pygame.K_a:
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
			if not def_dict:
				action = max(state_value[x][y][has_key].items(), key = lambda item: item[1])[0]
				
				#Step
				(x1, y1, has_key1), reward, done = env.step(action)
				
				#Update the state value
				state_value[x][y][has_key][action] = reward + gamma * max(state_value[x1][y1][has_key1].values())
				
				#Update the state to the new state
				x, y, has_key = x1, y1, has_key1
			else:
				
				cur_state = next_state
				
				action = max(state_value_dd[cur_state].items(), key = lambda item: item[1])[0]
				
				#Step
				next_state, reward, done = env.step(action)
				
				#Update the state value
				state_value_dd[cur_state][action] = reward + gamma * max(state_value_dd[next_state].values())
			
			x, y, has_key = next_state
			deaths += 1 if env.game_over(x, y, has_key, env.board) and not env.won(x, y, has_key, env.board) else 0
			wins += 1 if env.won(x, y, has_key, env.board) else 0
			moves += 1
			if wins == 1000 or deaths == 1000 or moves == 200000:
				time_elapsed = time.time() - start_time
				res[index] = deaths, moves, wins, gamma, time_elapsed
				print(f"thread {index} finished in {time_elapsed:.2f} seconds")
				return deaths, moves, wins
			
		# END OF YOUR CODE (2/2)
		
		# Human controller
		else:
			if action_taken:
				(x, y, has_key), reward, done = env.step(action)
				action_taken = False

if __name__ == '__main__':
	#Run the game
	run_game(render = True)

