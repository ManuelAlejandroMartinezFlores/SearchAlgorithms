from queues import factory_queue, Node 
from math import sqrt

def search(maze, start, target, get_neighbors, algorithm, heur=None, cost=lambda x,y: 1):
    """
    Ejecuta el algoritmo de búsqueda
    """
    queue = factory_queue(algorithm)
    queue.add(Node(start))
    visited = set()
    expanded = set()
    ngenerated = 0

    while not queue.empty():
        current = queue.pop()
        if current.id == target: 
            break
        if current.id in visited:
            continue
        # Expande los nodos vecinos
        for n, action in get_neighbors(maze, current.id):
            if n in visited: 
                continue
            node = Node(n)
            node.parent = current 
            node.action = action
            if algorithm == "GBFS" or algorithm == "A*":
                node.heur = heur(n, target)
            node.cost = current.cost + cost(current.id, n)
            queue.add(node)
            expanded.add(n)
        # Agrega a la fila de visitados
        visited.add(current.id)

    # Regenera el camino y las acciones
    path = [current.id]
    actions = [current.action]
    final_cost = current.cost
    while current.parent != None:
        current = current.parent 
        path.append(current.id)
        actions.append(current.action)
    # Calculo del branching factor
    bfactor = calculate_branching_factor(len(visited), len(path))
    return final_cost, visited, bfactor, path[::-1], actions[::-1]


def get_neighbors(maze, loc):
    """
    Genera vecinos con prioridad U, R, D, L
    """
    i, j = loc 
    H, W = maze.shape 
    neighbors = []
    if maze[i-1, j] != 1:
        neighbors.append(((i-1, j), "U"))
    if maze[i, j+1] != 1:
        neighbors.append(((i, j+1), "R"))
    if maze[i+1, j] != 1:
        neighbors.append(((i+1, j), "D"))
    if maze[i, j-1] != 1:
        neighbors.append(((i, j-1), "L"))
    return neighbors

def manhatan(loc1, loc2):
    """
    Distancia L1
    """
    i, j = loc1 
    x, y = loc2
    return abs(i - x) + abs(j - y)

def euclidean(loc1, loc2):
    """
    Distancia L2
    """
    i, j = loc1 
    x, y = loc2
    return sqrt((i - x)**2 + abs(j - y)**2)


def calculate_branching_factor(total_nodes, depth):
    """
    N = 1 + ... + b^d
    """
    
    def f(b):
        sum = 0
        for i in range(depth + 1):
            sum += b ** i
        return sum - total_nodes
    

    left, right = 1.0, 1.1
    while right - left > 0.0001:
        mid = (left + right) / 2
        if f(mid) < 0:
            left = mid
        else:
            right = mid
            
    return left