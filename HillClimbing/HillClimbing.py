import math

class Problem:
    def __init__(self, initial, goal):
        self.initial = initial  
        self.goal = goal       
    
    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        return self.goal == state
    
    def action_cost(self, state1, action, state2):
        return 1
   
    def h(self, state):
        return 0

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def path(self):
        lista_path = []
        node = self
        while node:
            lista_path.append(node.state)
            node = node.parent
        return lista_path[::-1]

    def expand(self, problem):
        lista = []
        for action in problem.actions(self.state):
            lista.append(self.child_node(problem, action))
        return lista

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        step_cost = problem.action_cost(self.state, action, next_state)
        return Node(next_state, self, action, self.path_cost + step_cost)

coords_metro = {
    'Cuatro Caminos': (19.4593, -99.2158),
    'Tacubaya': (19.4032, -99.1871),
    'Balderas': (19.4273, -99.1491),
    'Salto del Agua': (19.4269, -99.1422),
    'Pino Suarez': (19.4257, -99.1330),
    'Pantitlan': (19.4157, -99.0722),
    'Bellas Artes': (19.4362, -99.1419),
    'Hidalgo': (19.4371, -99.1471),
    'Guerrero': (19.4448, -99.1456),
    'Chabacano': (19.4084, -99.1356),
    'Taxqueña': (19.3458, -99.1428),
    'Politécnico': (19.5008, -99.1493),
    'La Raza': (19.4702, -99.1367),
    'Centro Medico': (19.4068, -99.1556),
    'Zapata': (19.3709, -99.1587),
    'Instituto del Petroleo': (19.4901, -99.1469),
    'Consulado': (19.4580, -99.1139),
    'Oceania': (19.4452, -99.0871),
    'Garibaldi': (19.4444, -99.1388),
    'Morelos': (19.4388, -99.1192),
    'San Lazaro': (19.4303, -99.1147),
    'Jamaica': (19.4087, -99.1223),
    'Ermita': (19.3619, -99.1429),
    'Atlalilco': (19.3564, -99.1014),
    'Mixcoac': (19.3758, -99.1875)
}

class GraphProblem(Problem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph
    
    def actions(self, state):
        return list(self.graph[state].keys())

    def result(self, state, action):
        return action

    def action_cost(self, state1, action, state2):
        return self.graph[state1][state2]

    def h(self, state):
        lat1, lon1 = coords_metro[state]
        lat2, lon2 = coords_metro[self.goal]
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111


def hill_climbing(problem):
    current = Node(problem.initial)
    
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
            
        #busca el vecino con la menor h(n)
        neighbor = min(neighbors, key=lambda node: problem.h(node.state))
        
        #sino mejora la h(n) del nodo actual, nos detendremos
        if problem.h(neighbor.state) >= problem.h(current.state):
            break
            
        #si mejora, avanzamos
        current = neighbor
    
        if problem.is_goal(current.state):
            break
            
    return current


metro_cdmx = {
    'Cuatro Caminos': {'Tacubaya': 1},
    'Tacubaya': {'Cuatro Caminos': 1, 'Balderas': 1, 'Mixcoac': 1, 'Pantitlan': 1},
    'Balderas': {'Tacubaya': 1, 'Salto del Agua': 1, 'Hidalgo': 1, 'Centro Medico': 1},
    'Salto del Agua': {'Balderas': 1, 'Pino Suarez': 1, 'Chabacano': 1, 'Bellas Artes': 1},
    'Pino Suarez': {'Salto del Agua': 1, 'Pantitlan': 1, 'Bellas Artes': 1, 'Chabacano': 1},
    'Pantitlan': {'Tacubaya': 1, 'Pino Suarez': 1, 'Oceania': 1, 'Jamaica': 1},
    'Bellas Artes': {'Chabacano': 1, 'Hidalgo': 1, 'Salto del Agua': 1, 'Pino Suarez': 1, 'Garibaldi': 1},
    'Hidalgo': {'Bellas Artes': 1, 'La Raza': 1, 'Balderas': 1, 'Guerrero': 1},
    'Chabacano': {'Taxqueña': 1, 'Pino Suarez': 1, 'Bellas Artes': 1, 'Salto del Agua': 1, 'Jamaica': 1, 'Centro Medico': 1},
    'Taxqueña': {'Chabacano': 1, 'Ermita': 1},
    'Politécnico': {'La Raza': 1, 'Instituto del Petroleo': 1},
    'La Raza': {'Politécnico': 1, 'Hidalgo': 1, 'Consulado': 1, 'Instituto del Petroleo': 1, 'Guerrero': 1},
    'Guerrero': {'Hidalgo': 1, 'La Raza': 1, 'Garibaldi': 1},
    'Centro Medico': {'Balderas': 1, 'Zapata': 1, 'Chabacano': 1, 'Tacubaya': 1},
    'Zapata': {'Centro Medico': 1, 'Ermita': 1, 'Mixcoac': 1},
    'Instituto del Petroleo': {'Politécnico': 1, 'La Raza': 1, 'Oceania': 1},
    'Consulado': {'La Raza': 1, 'Oceania': 1, 'Morelos': 1, 'Jamaica': 1},
    'Oceania': {'Instituto del Petroleo': 1, 'Pantitlan': 1, 'Consulado': 1, 'San Lazaro': 1},
    'Garibaldi': {'Bellas Artes': 1, 'Guerrero': 1, 'Morelos': 1},
    'Morelos': {'Garibaldi': 1, 'Consulado': 1, 'San Lazaro': 1},
    'San Lazaro': {'Morelos': 1, 'Oceania': 1, 'Pino Suarez': 1},
    'Jamaica': {'Chabacano': 1, 'Pantitlan': 1, 'Consulado': 1},
    'Ermita': {'Zapata': 1, 'Taxqueña': 1, 'Atlalilco': 1},
    'Atlalilco': {'Ermita': 1, 'Chabacano': 1},
    'Mixcoac': {'Tacubaya': 1, 'Zapata': 1}
}

casos = [
    ("Cuatro Caminos", "Pantitlan"),
    ("Politécnico", "Taxqueña"),
    ("Zapata", "Oceania")
]

for inicio, meta in casos:
    problem = GraphProblem(inicio, meta, metro_cdmx)
    node = hill_climbing(problem)
    
    print("=" * 60)
    print(f"Búsqueda Hill Climbing ({inicio} -> {meta}):")
    print(f"Camino recorrido: {' -> '.join(node.path())}")
    print(f"Estación final alcanzada: {node.state}")
    print(f"¿Alcanzó la meta?: {problem.is_goal(node.state)}")