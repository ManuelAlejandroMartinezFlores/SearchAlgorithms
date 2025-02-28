class Node:
    """
    Node para instanciar en el search tree
    """
    def __init__(self, id):
        self.id = id 
        self.parent = None
        self.cost = 0 
        self.heur = 0
        self.action = ""
    def __repr__(self):
        return f"Node: {self.id}"
    

class FIFO:
    """
    First in First Out
    """
    def __init__(self):
        self.data = []

    def empty(self):
        return len(self.data) == 0

    def top(self):
        return self.data[0]

    def pop(self):
        return self.data.pop(0)

    def add(self, item):
        self.data.append(item)

    
class LIFO:
    """
    Last In First Out
    """
    def __init__(self):
        self.data = []

    def empty(self):
        return len(self.data) == 0

    def top(self):
        return self.data[-1]

    def pop(self):
        return self.data.pop(-1)

    def add(self, item):
        self.data.append(item)


class Priority:
    """
    Ordena con prioridad dada por funcion score
    """
    def __init__(self, score):
        self.data = []
        self.score = score

    def empty(self):
        return len(self.data) == 0

    def top(self):
        return self.data[0]

    def pop(self):
        return self.data.pop(0)

    def add(self, item):
        for i in range(len(self.data)):
            if self.score(self.data[i]) > self.score(item):
                self.data.insert(i, item)
                return
        self.data.append(item)


def factory_queue(algorithm):
    """
    Genera queue dependiendo del algoritmo
    """
    if algorithm == "DFS":
        return LIFO()
    if algorithm == "BFS":
        return FIFO()
    if algorithm == "GBFS":
        return Priority(lambda x: x.heur)
    if algorithm == "A*":
        return Priority(lambda x: x.cost + x.heur)
        