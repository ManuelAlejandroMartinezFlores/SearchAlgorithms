import numpy as np

from tests import base_case, random_case, test_case
from search_alg import manhatan, euclidean

PATH = "mazes/Laberinto1.txt"
ALGO = "A*"
HEUR = "euclidean"


if HEUR == "manhatan":
    heurf = manhatan
elif HEUR == "euclidean":
    heurf = euclidean
else:
    heurf = lambda x, y:0

maze = np.loadtxt(PATH, delimiter=",")
start, target = base_case(maze)
test_case(maze, start, target, ALGO, heurf, True)