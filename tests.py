import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd

from search_alg import *



def base_case(maze):
    """
    Genera coordenadas del caso base
    """
    start = np.where(maze == 3)
    target = np.where(maze == 2)
    start = (start[0][0], start[1][0])
    target = (target[0][0], target[1][0])
    return start, target 

def random_case(maze):
    """
    Genera coordenadas de inicio aleatorias
    """
    start = np.where(maze != 1)
    target = np.where(maze == 2)
    idx = np.random.randint(0, len(start[0]))
    start = (start[0][idx], start[1][idx])
    target = (target[0][0], target[1][0])
    return start, target


def test_case(maze, start, target, algorithm, heur, visual=False):
    """
    Evalua una ejecución de cualquier algoritmo
    """
    t = time.time()
    cost, visited, bfactor, path, actions = search(maze, start, target, get_neighbors, algorithm, heur=heur)
    t = time.time() - t

    # Genera una visualización
    if visual:
        maze = maze * 2
        for i,j in visited:
            maze[i,j] = 1
        for i,j in path:
            maze[i, j] = 3
        plt.imshow(maze, cmap="Blues")
        plt.title(f"Largo del camino: {cost}\nNodos visitados: {len(visited)}\nTiempo: {t:.4f}s\nBranching factor: {bfactor:.4f}")
        plt.axis("off")
        plt.tight_layout()
        plt.show()


    return {"cost": cost, "nvisited": len(visited), "time": t, "bfactor": bfactor}


if __name__ == "__main__":
    # Evaluación de los casos base
    base_df = {"lab": [], "algorithm": [], "cost": [], "nvisited": [], "time": [], "bfactor": [], "heur": []}
    for k in range(1, 4):
        maze = np.loadtxt(f"mazes/Laberinto{k}.txt", delimiter=",") 
        start, target = base_case(maze)
        for algorithm, heur in [("DFS", "-"), ("BFS", "-"), ("A*", "manhatan"), ("A*", "euclidean"), ("GBFS", "manhatan"), ("GBFS", "euclidean")]:
            if heur == "manhatan":
                heurf = manhatan
            elif heur == "euclidean":
                heurf = euclidean
            else:
                heurf = lambda x, y:0
            data = test_case(maze, start, target, algorithm, heurf)
            base_df["lab"].append(k)
            base_df["cost"].append(data["cost"])
            base_df["nvisited"].append(data["nvisited"])
            base_df["time"].append(data["time"])
            base_df["bfactor"].append(data["bfactor"])
            base_df["heur"].append(heur)
            base_df["algorithm"].append(algorithm)

    base_df = pd.DataFrame(base_df)
    base_df.to_csv("base_test.csv", index=False)


    # Evaluación de casos aleatorios, con 5 iteraciones
    random_df = {"lab": [], "algorithm": [], "cost": [], "nvisited": [], "time": [], "bfactor": [], "heur": []}
    for k in range(1, 4):
        maze = np.loadtxt(f"mazes/Laberinto{k}.txt", delimiter=",") 
        for _ in range(10):
            start, target = random_case(maze)
            for algorithm, heur in [("DFS", "-"), ("BFS", "-"), ("A*", "manhatan"), ("A*", "euclidean"), ("GBFS", "manhatan"), ("GBFS", "euclidean")]:
                if heur == "manhatan":
                    heurf = manhatan
                elif heur == "euclidean":
                    heurf = euclidean
                else:
                    heurf = lambda x, y:0
                data = test_case(maze, start, target, algorithm, heurf)
                random_df["lab"].append(k)
                random_df["cost"].append(data["cost"])
                random_df["nvisited"].append(data["nvisited"])
                random_df["time"].append(data["time"])
                random_df["bfactor"].append(data["bfactor"])
                random_df["heur"].append(heur)
                random_df["algorithm"].append(algorithm)

    random_df = pd.DataFrame(random_df)
    random_df.to_csv("random_test.csv", index=False)




