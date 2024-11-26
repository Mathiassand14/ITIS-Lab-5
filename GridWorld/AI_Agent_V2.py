from AI_GridWorld import run_game
from GridWorld import GridWorld
import multiprocessing
import time


def main():
	print(multiprocessing.cpu_count())
	while True:
		amount = 201
		res = multiprocessing.Manager().list([None] * amount)
		with multiprocessing.Pool(processes = multiprocessing.cpu_count()) as pool:
			# Use pool.apply_async to start processes
			processes = []
			processes.extend(pool.apply_async(run_game, (
				None,True, False, False, False, False, False, float(j / 100.), int(j), res))
			                 for j in range(amount))
			
			
			pool.close()  # Close the pool to prevent new processes from being submitted
			pool.join()  # Wait for all processes to complete
		
		
		[print(f"Deaths {j[0]}, Moves {j[1]}, Wins {j[2]}, Gamma {j[3]}, Time {j[4]}") for j in res]
		
		with open('results.csv', 'a') as f:
			[f.write(f"{j[0]},{j[1]},{j[2]},{j[3]},{j[4]}\n") if all(val is not None for val in j) else f.write(
				"Timeout\n") for j in res]
		
		with open('results.csv', 'r') as f:
			lines = f.readlines()
			print(f"{(len(lines) - 1) / 201}")


if __name__ == '__main__':
	main()