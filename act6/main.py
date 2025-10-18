from buildGraph import WeightedGraph
from bfs import bfs
from dfs import dfs
from ucs import uniform_cost
from dijkstra import dijkstra

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
