import numpy as np
import pandas  as pd




def EmptyStateMatrix() -> list:
	board = pd.read_csv('board.txt',sep = ' ',header = None)
	shp = board.shape
	b = [{'x':x, 'y': y, 'has_key': has_key, **{t: 0 for t in ['left', 'right', 'up', 'down']} } for x in range(shp[0]) for y in range(shp[1]) for has_key in [0, 1]]
	return b

if __name__ == '__main__':
	print(EmptyStateMatrix())