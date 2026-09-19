from collections import deque
import math
import heapq

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


class GraphProblem(Problem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph
    
    def actions(self, state):
        lista = []
        for key in self.graph[state].keys():
            lista.append(key)
        return lista

    def result(self, state, action):
        return action

    def action_cost(self, state1, action, state2):
        return self.graph[state1][state2]

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

def depth_first_graph_search(problem):
    start_node = Node(problem.initial)
    if problem.is_goal(start_node.state):
        return start_node
    frontier = [start_node]
    explored = set()

    while frontier:
        node = frontier.pop()
        explored.add(node.state)

        if problem.is_goal(node.state):
            return node

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
    return None

def breadth_first_graph_search(problem):
    start_node = Node(problem.initial)
    if problem.is_goal(start_node.state):
        return start_node
    frontier = deque([start_node])
    explored = set()

    while frontier:
        node = frontier.popleft()
        explored.add(node.state)

        if problem.is_goal(node.state):
            return node

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
    return None

class GraphAStartProblem(Problem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph
    
    def actions(self, state):
        lista = []
        for key in self.graph[state].keys():
            lista.append(key)
        return lista

    # Función de transición
    def result(self, state, action):
        return action

    def action_cost(self, state1, action, state2):
        return self.graph[state1][state2]

    # distancia aproximada en km entre la estación actual y la meta
    def h(self, state):
        lat1, lon1 = coords_metro[state]
        lat2, lon2 = coords_metro[self.goal]
        # distancia en grados multiplicada por el factor de km aprox 111 km por grado
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111

def a_star_graph_search(problem):
    start_node = Node(problem.initial)
    if problem.is_goal(start_node.state):
        return start_node
    
    #se agrega id(node) para evitar errores de comparación
    frontier = [(problem.h(start_node.state), id(start_node), start_node)]
    explored = set()

    while frontier:
        priority, _, node = heapq.heappop(frontier)
        
        if problem.is_goal(node.state):
            return node

        if node.state not in explored:
            explored.add(node.state)

            for child in node.expand(problem):
                if child.state not in explored:
                    f_cost = child.path_cost + problem.h(child.state)
                    heapq.heappush(frontier, (f_cost, id(child), child))
    return None

metro_cdmx = {
    # linea 1
    'Cuatro Caminos': {'Tacubaya': 1},
    'Tacubaya': {'Cuatro Caminos': 1, 'Balderas': 1, 'Mixcoac': 1, 'Pantitlan': 1},
    'Balderas': {'Tacubaya': 1, 'Salto del Agua': 1, 'Hidalgo': 1, 'Centro Medico': 1},
    'Salto del Agua': {'Balderas': 1, 'Pino Suarez': 1, 'Chabacano': 1, 'Bellas Artes': 1},
    'Pino Suarez': {'Salto del Agua': 1, 'Pantitlan': 1, 'Bellas Artes': 1, 'Chabacano': 1},
    'Pantitlan': {'Tacubaya': 1, 'Pino Suarez': 1, 'Oceania': 1, 'Jamaica': 1},

    # linea 2
    'Bellas Artes': {'Chabacano': 1, 'Hidalgo': 1, 'Salto del Agua': 1, 'Pino Suarez': 1, 'Garibaldi': 1},
    'Hidalgo': {'Bellas Artes': 1, 'La Raza': 1, 'Balderas': 1, 'Guerrero': 1},
    'Chabacano': {'Taxqueña': 1, 'Pino Suarez': 1, 'Bellas Artes': 1, 'Salto del Agua': 1, 'Jamaica': 1, 'Centro Medico': 1},
    'Taxqueña': {'Chabacano': 1, 'Ermita': 1},

    # linea 3
    'Politécnico': {'La Raza': 1, 'Instituto del Petroleo': 1},
    'La Raza': {'Politécnico': 1, 'Hidalgo': 1, 'Consulado': 1, 'Instituto del Petroleo': 1, 'Guerrero': 1},
    'Guerrero': {'Hidalgo': 1, 'La Raza': 1, 'Garibaldi': 1},
    'Centro Medico': {'Balderas': 1, 'Zapata': 1, 'Chabacano': 1, 'Tacubaya': 1},
    'Zapata': {'Centro Medico': 1, 'Ermita': 1, 'Mixcoac': 1},

    # linea 5
    'Instituto del Petroleo': {'Politécnico': 1, 'La Raza': 1, 'Oceania': 1},
    'Consulado': {'La Raza': 1, 'Oceania': 1, 'Morelos': 1, 'Jamaica': 1},
    'Oceania': {'Instituto del Petroleo': 1, 'Pantitlan': 1, 'Consulado': 1, 'San Lazaro': 1},

    #otras conecciones
    'Garibaldi': {'Bellas Artes': 1, 'Guerrero': 1, 'Morelos': 1},
    'Morelos': {'Garibaldi': 1, 'Consulado': 1, 'San Lazaro': 1},
    'San Lazaro': {'Morelos': 1, 'Oceania': 1, 'Pino Suarez': 1},
    'Jamaica': {'Chabacano': 1, 'Pantitlan': 1, 'Consulado': 1},
    'Ermita': {'Zapata': 1, 'Taxqueña': 1, 'Atlalilco': 1},
    'Atlalilco': {'Ermita': 1, 'Chabacano': 1},
    'Mixcoac': {'Tacubaya': 1, 'Zapata': 1}
}

#coordenadas geograficas de las estacuines usadas para calcular la distancia en línea recta entre ellas
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

casos_prueba = [
    ("Cuatro Caminos", "Pantitlan"),
    ("Politécnico", "Taxqueña"),
    ("Zapata", "Oceania")
]

for origen, destino in casos_prueba:
    print("=" * 60)
    print(f"Ruta: {origen} -> {destino}")
    
    prob = GraphProblem(origen, destino, metro_cdmx)
    
    # busqueda en BFS
    nodo_bfs = breadth_first_graph_search(prob)
    path_bfs = nodo_bfs.path() if nodo_bfs else "No encontrada"
    costo_bfs = nodo_bfs.path_cost if nodo_bfs else "-"
    
    # busqueda en DFS
    nodo_dfs = depth_first_graph_search(prob)
    path_dfs = nodo_dfs.path() if nodo_dfs else "No encontrada"
    costo_dfs = nodo_dfs.path_cost if nodo_dfs else "-"

    #busqueda A*
    for inicio, meta in casos_prueba:
      problem = GraphAStartProblem(inicio, meta, metro_cdmx)
      node = a_star_graph_search(problem)
    
    print("=" * 60)
    print(f"Ruta A* ({inicio} -> {meta}):")
    print(f"  Camino: {' -> '.join(node.path())}")
    print(f"  Costo Total (Estaciones): {node.path_cost}")

    print("Búsqueda en Anchura")
    print(f"  Ruta: {' -> '.join(path_bfs)}")
    print(f"  Costo (Estaciones): {costo_bfs}")
    
    print("Búsqueda en Profundidad")
    print(f"  Ruta: {' -> '.join(path_dfs)}")
    print(f"  Costo (Estaciones): {costo_dfs}")
    print()