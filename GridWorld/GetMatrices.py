import pandas  as pd




def EmptyStateMatrix(initial_value: int = 0) -> list:
	board = pd.read_csv('board.txt',sep = ' ',header = None)
	shp = board.shape
	b = [[[{t: initial_value for t in ['left', 'right', 'up', 'down']} for _ in [0, 1]] for _ in range(shp[1])] for _ in range(
		shp[0])]

	#for x in range(shp[0]) for y in range(

		#	shp[1]) for has_key in [0, 1]]
	return b

if __name__ == '__main__':
	print(EmptyStateMatrix())