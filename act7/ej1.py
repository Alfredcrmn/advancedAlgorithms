from queue import PriorityQueue
from buildGraph import WeightedGraph
import math

INF = float("inf")

# ============================================================
# Construcción del grafo
# ============================================================
def build_graph() -> WeightedGraph:
    g = WeightedGraph(directed=False)
    labels = list("ABCDEFGHIJKLMNOPQRST")
    for v in labels:
        g.add_vertex(v)
    edges = [
        ('A','B',  7),  ('B','C',14), ('C','D', 9), ('D','E',11), ('E','F', 8),
        ('F','G',10),  ('G','H',13), ('H','I', 6), ('I','J',15), ('J','K',12),
        ('K','L', 9),  ('L','M',16), ('M','N', 5), ('N','O',14), ('O','P',10),
        ('P','Q',13),  ('Q','R',  7), ('R','S',  9), ('S','T', 8), ('T','A',11),
        ('A','G',20), ('C','I',22), ('E','K',25), ('G','M',18), ('I','O',23),
        ('K','Q',27), ('M','S',16), ('O','A',30),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g

# ============================================================
# Utilidades
# ============================================================
def print_adjacency_list(g: WeightedGraph) -> None:
    """Imprime la lista de adyacencia ordenada por nombre de vértice."""
    print("\n----- Adjacency List -----")
    for v in sorted(g.vertices()):
        items = "  ".join(f"({u}, {w})" for (u, w) in g.adjacent_vertices(v))
        print(f"{v}: {items}")
    print()

def weight_of(graph: WeightedGraph, u, v) -> float:
    """Peso de (u,v) si existe; INF si no existe."""
    for (nbr, w) in graph.adjacent_vertices(u):
        if nbr == v:
            return w
    return INF

def min_edge_to_set(graph: WeightedGraph, u, S) -> float:
    """min_{x∈S} w(u,x); INF si no hay conexión."""
    best = INF
    for (nbr, w) in graph.adjacent_vertices(u):
        if nbr in S and w < best:
            best = w
    return best

# ============================================================
# Búsqueda de Costo Uniforme (UCS)
# ============================================================
class UCSNode:
    def __init__(self, parent, v, c, visited: set):
        self.parent = parent
        self.v = v
        self.c = c
        self.visited = visited

    def path(self):
        node, p = self, []
        while node is not None:
            p.append(node.v)
            node = node.parent
        return list(reversed(p))

def uniform_cost(graph: WeightedGraph):
    """
    Encuentra un ciclo Hamiltoniano de costo mínimo (TSP) con UCS.
    Devuelve: {"path":[v0,...,v0], "Cost": C} o None si no existe ciclo.
    Requisitos: pesos no negativos.
    """
    order = list(graph.vertices())
    if not order:
        return None
    start = order[0]
    n = len(order)

    frontier = PriorityQueue()              # (g, tie, node)
    tie = 0
    root = UCSNode(None, start, 0, {start})
    frontier.put((0, tie, root))

    # Mejor costo conocido para (v, visited) usando tupla ordenada como llave
    best = {(start, tuple(sorted({start}))): 0}

    while not frontier.empty():
        g_cost, _, node = frontier.get()
        state_key = (node.v, tuple(sorted(node.visited)))
        if g_cost > best.get(state_key, INF):
            continue

        # Objetivo: estar de vuelta en start con todos visitados
        if node.v == start and len(node.visited) == n and node.parent is not None:
            return {"Path": node.path(), "Cost": node.c}

        for (nbr, w) in graph.adjacent_vertices(node.v):
            if w < 0:
                continue  # UCS asume pesos no negativos

            if nbr == start:
                # Solo permitir cierre si ya visitamos todos
                if len(node.visited) == n:
                    new_g = node.c + w
                    key = (start, tuple(sorted(node.visited)))
                    if new_g < best.get(key, INF):
                        tie += 1
                        best[key] = new_g
                        frontier.put((new_g, tie, UCSNode(node, start, new_g, set(node.visited))))
                continue

            if nbr in node.visited:
                continue  # no revisitar vértices (salvo el cierre a start)

            new_visited = set(node.visited)
            new_visited.add(nbr)
            new_g = node.c + w
            key = (nbr, tuple(sorted(new_visited)))

            if new_g < best.get(key, INF):
                tie += 1
                best[key] = new_g
                frontier.put((new_g, tie, UCSNode(node, nbr, new_g, new_visited)))

    return None

# ============================================================
# Ramificación y Poda
# ============================================================
class BnBNode:
    def __init__(self, parent, v, g, visited: set, path: list):
        self.parent = parent
        self.v = v
        self.g = g
        self.visited = visited
        self.path = path

def lower_bound(graph: WeightedGraph, start, current, g, visited: set, all_vertices: list) -> float:

    U = set(all_vertices) - set(visited)
    if not U:
        return g + weight_of(graph, current, start)

    c_in  = min_edge_to_set(graph, current, U)  # entrar a U
    c_out = min_edge_to_set(graph, start,   U)  # regresar a start
    if math.isinf(c_in) or math.isinf(c_out):
        return INF  # rama imposible

    return g + c_in + c_out

def branch_and_bound(graph: WeightedGraph):

    order = list(graph.vertices())
    if not order:
        return None
    start = order[0]

    pq = PriorityQueue()
    tie = 0
    root = BnBNode(None, start, 0, {start}, [start])

    LB_root = lower_bound(graph, start, start, 0, root.visited, order)
    pq.put((LB_root, tie, root))

    best_cost, best_path = INF, None

    while not pq.empty():
        lb, _, node = pq.get()
        if lb >= best_cost:
            continue

        if len(node.visited) == len(order):
            back = weight_of(graph, node.v, start)
            if not math.isinf(back):
                total = node.g + back
                if total < best_cost:
                    best_cost = total
                    best_path = node.path + [start]
            continue

        for (nbr, w) in graph.adjacent_vertices(node.v):
            if nbr in node.visited:
                continue
            new_g = node.g + w
            if new_g >= best_cost:
                continue

            new_visited = set(node.visited)
            new_visited.add(nbr)
            child = BnBNode(node, nbr, new_g, new_visited, node.path + [nbr])

            lb_child = lower_bound(graph, start, nbr, new_g, new_visited, order)
            if lb_child < best_cost:
                tie += 1
                pq.put((lb_child, tie, child))

    if best_path is None:
        return None
    return {"Path": best_path, "Cost": best_cost}

# --- EJECUCIÓN ---
g = build_graph()
print_adjacency_list(g)

# UCS
ucs = uniform_cost(g)
if ucs is None:
    print("UCS: no encontró ciclo Hamiltoniano.")
else:
    print("UCS -> Costo:", ucs["Cost"])
    print("UCS -> Path :", " -> ".join(ucs["Path"]))

# BnB
bnb = branch_and_bound(g)
if bnb is None:
    print("BnB: no encontró ciclo Hamiltoniano.")
else:
    print("BnB -> Costo:", bnb["Cost"])
    print("BnB -> Path :", " -> ".join(bnb["Path"]))