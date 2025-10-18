from queue import PriorityQueue
from buildGraph import WeightedGraph

def dijkstra(graph: WeightedGraph, source):
    """
    Computes single-source shortest paths (SSSP) from 'source' to all vertices.
    Assumes non-negative edge weights.
    Returns:
      {
        "Distances": {v: dist_from_source},
        "Parents":   {v: parent_of_v}
      }
    """
    if source not in graph.vertices():
        print("Warning: Vertex", source, "is not in Graph")

    dist = {}
    parent = {}
    for v in graph.vertices():
        dist[v] = float("inf")
        parent[v] = None
    dist[source] = 0.0

    pq = PriorityQueue()
    tie = 0
    pq.put((0.0, tie, source))

    while True:
        if pq.empty():
            break

        cur_cost, _, u = pq.get()

        if cur_cost > dist[u]:
            continue

        for v, w in graph.adjacent_vertices(u):
            new_cost = dist[u] + w
            if new_cost < dist[v]:
                dist[v] = new_cost
                parent[v] = u
                tie += 1
                pq.put((new_cost, tie, v))

    return {"Distances": dist, "Parents": parent}
