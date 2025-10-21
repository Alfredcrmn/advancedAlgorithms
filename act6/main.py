from buildGraph import WeightedGraph
from bfs import bfs
from dfs import dfs
from ucs import uniform_cost
from dijkstra import dijkstra
from floyd import floyd_warshall_distance
import numpy as np

graph = WeightedGraph(directed = False)

# Vértices
graph.add_vertex('goxmont')
graph.add_vertex('zrusall')
graph.add_vertex('niaphia')
graph.add_vertex('adaset')
graph.add_vertex('ertonwell')
graph.add_vertex('strento')
graph.add_vertex('duron')
graph.add_vertex('lagos')
graph.add_vertex('oriaron')
graph.add_vertex('blebus')
graph.add_vertex('ylane')
graph.add_vertex('goding')
graph.add_vertex('ontdale')
graph.add_vertex('togend')

# Aristas
graph.add_edge('goxmont', 'niaphia', 212)
graph.add_edge('niaphia', 'lagos', 300)
graph.add_edge('niaphia', 'ertonwell', 56)
graph.add_edge('lagos', 'duron', 119)
graph.add_edge('duron', 'ertonwell', 121)
graph.add_edge('ertonwell', 'adaset', 130)
graph.add_edge('goxmont', 'adaset', 103)
graph.add_edge('goxmont', 'zrusall', 112)
graph.add_edge('adaset', 'zrusall', 15)
graph.add_edge('zrusall', 'strento', 121)
graph.add_edge('strento', 'oriaron', 221)
graph.add_edge('oriaron', 'blebus', 291)
graph.add_edge('blebus', 'duron', 160)
graph.add_edge('strento', 'ylane', 99)
graph.add_edge('ylane', 'oriaron', 117)
graph.add_edge('ylane', 'goding', 88)
graph.add_edge('goding', 'ontdale', 98)
graph.add_edge('oriaron', 'ontdale', 219)
graph.add_edge('ontdale', 'blebus', 165)
graph.add_edge('blebus', 'togend', 121)
graph.add_edge('ontdale', 'togend', 210)

def print_adjacency_list(adjacency_list):
    print("\n----- Adjacency List -----")
    for vertex, neighbors in adjacency_list.items():
        
        print(f"{vertex}: ", end="")
        for neighbor, weight in neighbors:
            print(f"({neighbor}, {weight})", end="  ")
        print()

adjacency_list = {
    'goxmont': [('niaphia', 212), ('zrusall', 112), ('adaset', 103)],
    'zrusall': [('goxmont', 112), ('adaset', 15), ('strento', 121)],
    'niaphia': [('goxmont', 212), ('lagos', 300), ('ertonwell', 56)],
    'adaset': [('goxmont', 103), ('zrusall', 15), ('ertonwell', 130)],
    'ertonwell': [('niaphia', 56), ('lagos', 119), ('duron', 121), ('adaset', 130)],
    'strento': [('zrusall', 121), ('oriaron', 221), ('ylane', 99)],
    'duron': [('lagos', 119), ('ertonwell', 121), ('blebus', 160)],
    'lagos': [('niaphia', 300), ('duron', 119)],
    'oriaron': [('strento', 221), ('blebus', 291), ('ylane', 117), ('ontdale', 219)],
    'blebus': [('oriaron', 291), ('duron', 160), ('ontdale', 165), ('togend', 121)],
    'ylane': [('strento', 99), ('oriaron', 117), ('goding', 88)],
    'goding': [('ylane', 88), ('ontdale', 98)],
    'ontdale': [('goding', 98), ('oriaron', 219), ('blebus', 165), ('togend', 210)],
    'togend': [('blebus', 121), ('ontdale', 210)]
}
print_adjacency_list(adjacency_list)
print("\n")

# Search from Goding to Niaphia
print("======================================================================")
print("----- Path search from Goding to Niaphia -----")

start = 'goding'
goal = 'niaphia'


# BFS Search
resultBfs = bfs(graph, start, goal)

if resultBfs is not None:
    print("BFS Path found:", resultBfs["Path"])
    print("BFS Total cost:", resultBfs["Cost"], "\n")

else:
    print("No path found between", start, "and", goal)


# DFS Search
resultDfs = dfs(graph, start, goal)

if resultDfs is not None:
    print("DFS Path found:", resultDfs["Path"])
    print("DFS Total cost:", resultDfs["Cost"], "\n")
else:
    print("No path found between", start, "and", goal)


# UCS Search
resultUcs = uniform_cost(graph, start, goal)

if resultUcs is not None:
    print("UCS Path found:", resultUcs["Path"])
    print("UCS Total cost:", resultUcs["Cost"], "\n")
else:
    print("No path found between", start, "and", goal)

print("======================================================================")



# Search from Zrusall to Togend
print("----- Path search from Zrusall to Togend -----")
start = 'zrusall'
goal = 'togend'


# BFS Search
resultBfs = bfs(graph, start, goal)

if resultBfs is not None:
    print("BFS Path found:", resultBfs["Path"])
    print("BFS Total cost:", resultBfs["Cost"], "\n")

else:
    print("No path found between", start, "and", goal)


# DFS Search
resultDfs = dfs(graph, start, goal)

if resultDfs is not None:
    print("DFS Path found:", resultDfs["Path"])
    print("DFS Total cost:", resultDfs["Cost"], "\n")
else:
    print("No path found between", start, "and", goal)


# UCS Search
resultUcs = uniform_cost(graph, start, goal)

if resultUcs is not None:
    print("UCS Path found:", resultUcs["Path"])
    print("UCS Total cost:", resultUcs["Cost"], "\n")
else:
    print("No path found between", start, "and", goal)

print("======================================================================")



# Search from Blebus to Ylane
print("----- Path search from Bleblus to Ylane -----")

start = 'blebus'
goal = 'ylane'


# BFS Search
resultBfs = bfs(graph, start, goal)

if resultBfs is not None:
    print("BFS Path found:", resultBfs["Path"])
    print("BFS Total cost:", resultBfs["Cost"], "\n")

else:
    print("No path found between", start, "and", goal)


# DFS Search
resultDfs = dfs(graph, start, goal)

if resultDfs is not None:
    print("DFS Path found:", resultDfs["Path"])
    print("DFS Total cost:", resultDfs["Cost"], "\n")
else:
    print("No path found between", start, "and", goal)


# UCS Search
resultUcs = uniform_cost(graph, start, goal)

if resultUcs is not None:
    print("UCS Path found:", resultUcs["Path"])
    print("UCS Total cost:", resultUcs["Cost"], "\n")
else:
    print("No path found between", start, "and", goal)

print("======================================================================")



# Search from goxmont to ontdale
print("----- Path search from Goxmont to Ontdale -----")

start = 'goxmont'
goal = 'ontdale'


# BFS Search
resultBfs = bfs(graph, start, goal)

if resultBfs is not None:
    print("BFS Path found:", resultBfs["Path"])
    print("BFS Total cost:", resultBfs["Cost"], "\n")

else:
    print("No path found between", start, "and", goal)


# DFS Search
resultDfs = dfs(graph, start, goal)

if resultDfs is not None:
    print("DFS Path found:", resultDfs["Path"])
    print("DFS Total cost:", resultDfs["Cost"], "\n")
else:
    print("No path found between", start, "and", goal)


# UCS Search
resultUcs = uniform_cost(graph, start, goal)

if resultUcs is not None:
    print("UCS Path found:", resultUcs["Path"])
    print("UCS Total cost:", resultUcs["Cost"], "\n")
else:
    print("No path found between", start, "and", goal)

print("====================================================================== \n\n")





# Dijkstra Algorithm from Goding
print("----- Dijkstra Algorithm from Goding -----")

source = 'goding'
result = dijkstra(graph, source)

dist = result["Distances"]
parent = result["Parents"]

print(f"\nCaminos óptimos desde {source} a cada nodo:")
for target in graph.vertices():
    # Reconstruir el camino source -> target
    path = []
    cur = target
    # Si el nodo es inalcanzable, su distancia será inf y parent[cur] será None (excepto el propio source)
    if dist.get(target, float("inf")) == float("inf"):
        print(f"  {source:10s} -> {target:10s} : INALCANZABLE")
        continue

    while cur is not None:
        path.insert(0, cur)
        cur = parent[cur]

    # Validar que el camino realmente inicia en 'source'
    if not path or path[0] != source:
        print(f"  {source:10s} -> {target:10s} : INALCANZABLE")
    else:
        print(f"  {source:10s} -> {target:10s} : {' -> '.join(path)}  |  Costo = {dist[target]}", "\n")




print("====================================================================== \n\n")
print("----- Floyd-Warshall Algorithm from Goding -----")

adjacency_matrix = [
# goxmont zrusall niaphia adaset  ertonwell strento duron  lagos  oriaron blebus ylane goding ontdale togend
[     0,     112,    212,    103,      0,       0,     0,     0,     0,     0,    0,     0,      0,     0], # goxmont
[   112,       0,      0,     15,      0,     121,     0,     0,     0,     0,    0,     0,      0,     0], # zrusall
[   212,       0,      0,      0,     56,       0,     0,   300,     0,     0,    0,     0,      0,     0], # niaphia
[   103,      15,      0,      0,    130,       0,     0,     0,     0,     0,    0,     0,      0,     0], # adaset
[     0,       0,     56,    130,      0,       0,   121,     0,     0,     0,    0,     0,      0,     0], # ertonwell
[     0,     121,      0,      0,      0,       0,     0,     0,   221,     0,   99,     0,      0,     0], # strento
[     0,       0,      0,      0,    121,       0,     0,   119,     0,   160,    0,     0,      0,     0], # duron
[     0,       0,    300,      0,      0,       0,   119,     0,     0,     0,    0,     0,      0,     0], # lagos
[     0,       0,      0,      0,      0,     221,     0,     0,     0,   291,  117,     0,    219,     0], # oriaron
[     0,       0,      0,      0,      0,       0,   160,     0,   291,     0,    0,     0,    165,   121], # blebus
[     0,       0,      0,      0,      0,      99,     0,     0,   117,     0,    0,    88,      0,     0], # ylane
[     0,       0,      0,      0,      0,       0,     0,     0,     0,     0,   88,     0,     98,     0], # goding
[     0,       0,      0,      0,      0,       0,     0,     0,   219,   165,    0,    98,      0,   210], # ontdale
[     0,       0,      0,      0,      0,       0,     0,     0,     0,   121,    0,     0,    210,     0]  # togend
]

# Como el grafo es no dirigido, hacemos simétrica la matriz
adjacency_matrix = np.maximum(adjacency_matrix, np.transpose(adjacency_matrix))


dist_matrix = floyd_warshall_distance(adjacency_matrix)

print("\n----- Floyd–Warshall (Minimum Distances Matrix) -----")
print(np.round(dist_matrix, 1))