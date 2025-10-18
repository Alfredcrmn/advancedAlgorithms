from queue import PriorityQueue
from buildGraph import WeightedGraph

def _reconstruct_path(parent, start, goal):
    path = []
    cur = goal

    while cur is not None:
        path.insert(0, cur)
        cur = parent.get(cur, None)

    if len(path) == 0 or path[0] != start:
        return None 
    return path

def dijkstra(graph: WeightedGraph, v0, vg):
    """
    Finds a minimum-cost path from v0 to vg using Dijkstra.
    Returns: {"Path": [...], "Cost": total_cost} or None if no path exists.
    Assumes non-negative edge weights.
    """
    # Verificaciones básicas (mismo estilo que el resto de tu código)
    if v0 not in graph.vertices():
        print("Warning: Vertex", v0, "is not in Graph")
    if vg not in graph.vertices():
        print("Warning: Vertex", vg, "is not in Graph")

    dist = {}
    parent = {}

    for v in graph.vertices():
        dist[v] = float("inf")
        parent[v] = None
    dist[v0] = 0.0

    pq = PriorityQueue
    tie = 0
    pq.put((0.0, tie, v0))

    visited = {}

    while True:
        if pq.empty():
            return None
        
        cur_cost, _, u = pq.get()

        if cur_cost > dist[u]:
            continue

        if u not in visited:
            visited[u] = 1

        if u == vg:
            path = _reconstruct_path(parent, v0, vg)
            return {"Path": path, "Cost": dist[vg]}
        
        for v, w in graph.adjacent_vertices(u):
            new_cost = dist[u] + w
            if new_cost < dist[v]:
                dist[v] = new_cost
                parent[v] = u
                tie += 1
                pq.put((new_cost, tie, v))
