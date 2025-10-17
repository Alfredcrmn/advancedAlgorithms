from buildGraph import WeightedGraph
from bfs import bfs

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

start = 'goding'
goal = 'niaphia'

resultBfs = bfs(graph, start, goal)

if resultBfs is not None:
    print("BFS Path found:", resultBfs["Path"])
    print("BFS Total cost:", resultBfs["Cost"])

else:
    print("No path found between", start, "and", goal)