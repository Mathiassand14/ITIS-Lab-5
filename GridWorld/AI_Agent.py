from AI_GridWorld import run_game
from GridWorld import GridWorld
from threading import Thread

while True:
	threads = []
	amount = 201
	res = [None] * int(amount)
	
	for j in range(int(amount)):
		threads.append(Thread(target = run_game,
		                      args = (GridWorld(), True, False, False, False,
		                              False,
		                              False,
		                              float(j/100.), int(j),
		                              res)))
		threads[j].start()
	
	for thread in threads:
		thread.join()
	
	for j in res:
		print(f"Deaths {j[0]}, Moves {j[1]}, Wins {j[2]}, Gamma {j[3]}, Time {j[4]}")
	
	
	# with open('results.csv', 'a') as f:
	# 	for j in res:
	# 		f.write(f"{j[0]},{j[1]},{j[2]},{j[3]},{j[4]}\n")
	
	
	with open('results.csv', 'r') as f:
		lines = f.readlines()
		print(f"{len(lines) / 201}")