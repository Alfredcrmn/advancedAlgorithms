from buildGraph import WeightedGraph
from bfs import bfs
from dfs import dfs
from ucs import uniform_cost
from dijkstra import dijkstra
from floyd import floyd_warshall_distance
import numpy as np

# --------------------------------------------------------------------
# Construcción del grafo (no dirigido)
# --------------------------------------------------------------------
graph = WeightedGraph(directed=False)

# Vértices
for v in [
    'goxmont','zrusall','niaphia','adaset','ertonwell','strento','duron',
    'lagos','oriaron','blebus','ylane','goding','ontdale','togend'
]:
    graph.add_vertex(v)

# Aristas (km)
graph.add_edge('goxmont',  'niaphia',  212)
graph.add_edge('niaphia',  'lagos',    300)
graph.add_edge('niaphia',  'ertonwell', 56)
graph.add_edge('lagos',    'duron',    119)
graph.add_edge('duron',    'ertonwell',121)
graph.add_edge('ertonwell','adaset',   130)
graph.add_edge('goxmont',  'adaset',   103)
graph.add_edge('goxmont',  'zrusall',  112)
graph.add_edge('adaset',   'zrusall',  15)
graph.add_edge('zrusall',  'strento',  121)
graph.add_edge('strento',  'oriaron',  221)
graph.add_edge('oriaron',  'blebus',   291)
graph.add_edge('blebus',   'duron',    160)
graph.add_edge('strento',  'ylane',    99)
graph.add_edge('ylane',    'oriaron',  117)
graph.add_edge('ylane',    'goding',   88)
graph.add_edge('goding',   'ontdale',  98)
graph.add_edge('oriaron',  'ontdale',  219)
graph.add_edge('ontdale',  'blebus',   165)
graph.add_edge('blebus',   'togend',   121)
graph.add_edge('ontdale',  'togend',   210)

# --------------------------------------------------------------------
# Utilidad: imprimir lista de adyacencia directamente desde el grafo
# --------------------------------------------------------------------
def print_adjacency_from_graph(g: WeightedGraph):
    print("\n----- Adjacency List -----")
    # Ordenamos por nombre para que sea estable y legible
    for v in sorted(g.vertices()):
        neighs = g.adjacent_vertices(v)  # lista de (vecino, peso)
        items = "  ".join(f"({u}, {w})" for (u, w) in neighs)
        print(f"{v}: {items}")

print_adjacency_from_graph(graph)
print("\n")

# --------------------------------------------------------------------
# Búsquedas entre pares de ciudades
# --------------------------------------------------------------------
def run_all_searches(g: WeightedGraph, start: str, goal: str, title: str):
    print("======================================================================")
    print(title)
    # BFS
    r = bfs(g, start, goal)
    if r is not None:
        print("BFS Path found:", r["Path"])
        print("BFS Total cost:", r["Cost"], "\n")
    else:
        print("No path found between", start, "and", goal)

    # DFS
    r = dfs(g, start, goal)
    if r is not None:
        print("DFS Path found:", r["Path"])
        print("DFS Total cost:", r["Cost"], "\n")
    else:
        print("No path found between", start, "and", goal)

    # UCS
    r = uniform_cost(g, start, goal)
    if r is not None:
        print("UCS Path found:", r["Path"])
        print("UCS Total cost:", r["Cost"], "\n")
    else:
        print("No path found between", start, "and", goal)

# Goding → Niaphia
run_all_searches(graph, 'goding', 'niaphia',
                 "----- Path search from Goding to Niaphia -----")

# Zrusall → Togend
run_all_searches(graph, 'zrusall', 'togend',
                 "----- Path search from Zrusall to Togend -----")

# Blebus → Ylane
run_all_searches(graph, 'blebus', 'ylane',
                 "----- Path search from Blebus to Ylane -----")

# Goxmont → Ontdale
run_all_searches(graph, 'goxmont', 'ontdale',
                 "----- Path search from Goxmont to Ontdale -----")

print("====================================================================== \n\n")

# --------------------------------------------------------------------
# Dijkstra desde Goding (SSSP)
# --------------------------------------------------------------------
print("----- Dijkstra Algorithm from Goding -----")
source = 'goding'
dj = dijkstra(graph, source)
dist = dj["Distances"]
parent = dj["Parents"]

print(f"\nCaminos óptimos desde {source} a cada nodo:")
for target in sorted(graph.vertices()):
    if dist.get(target, float("inf")) == float("inf"):
        print(f"  {source:10s} -> {target:10s} : INALCANZABLE")
        continue
    # reconstrucción del camino
    path = []
    cur = target
    while cur is not None:
        path.insert(0, cur)
        cur = parent[cur]
    if not path or path[0] != source:
        print(f"  {source:10s} -> {target:10s} : INALCANZABLE")
    else:
        print(f"  {source:10s} -> {target:10s} : {' -> '.join(path)}  |  Costo = {dist[target]}", "\n")

print("====================================================================== \n\n")

# --------------------------------------------------------------------
# Floyd–Warshall (APSP) con matriz creada desde el grafo
# --------------------------------------------------------------------
print("----- Floyd-Warshall Algorithm from Goding -----")

# Fijamos un orden estable de nodos (para que la matriz sea legible)
nodes = [
    'goxmont','zrusall','niaphia','adaset','ertonwell','strento','duron',
    'lagos','oriaron','blebus','ylane','goding','ontdale','togend'
]
idx = {v: i for i, v in enumerate(nodes)}

# Matriz de adyacencia (0 = sin arista; diagonal 0)
n = len(nodes)
adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
for (u, v, w) in graph.edges():  # devuelve cada arista una sola vez en no dirigidos
    i, j = idx[u], idx[v]
    adj_matrix[i][j] = w
    adj_matrix[j][i] = w  # simétrico

dist_matrix = floyd_warshall_distance(adj_matrix)
print("\n----- Floyd–Warshall (Minimum Distances Matrix) -----")
print(np.round(dist_matrix, 1))
