from queue import PriorityQueue
from buildGraph import WeightedGraph

class TreeNode:
    """
    Node for search trees.
    - parent: reference to parent node
    - v: current graph vertex
    - c: accumulated path cost (g-cost)
    """
    def __init__(self, parent, v, c):
        self.parent = parent
        self.v = v
        self.c = c

    def path(self):
        node = self
        path = []
        while node is not None:
            path.insert(0, node.v)
            node = node.parent
        return path
    
def uniform_cost(graph: WeightedGraph, v0, vg):
    """
    Finds a minimum-cost path from v0 to vg using Uniform Cost Search.
    Returns: {"Path": [...], "Cost": total_cost} or None if no path exists.
    Notes:
      - Assumes non-negative edge weights.
      - Expands nodes in order of increasing accumulated cost (g).
    """
    # Sanity checks (mismo estilo que tu código)
    if v0 not in graph.vertices():
        print("Warning: Vertex", v0, "is not in Graph")
    if vg not in graph.vertices():
        print("Warning: Vertex", vg, "is not in Graph")

    frontier = PriorityQueue()
    tie = 0
    frontier.put((0, tie, TreeNode(None, v0, 0)))

    best_cost = {v0: 0}

    while True:
        if frontier.empty():
            return None
        
        cost, _, node = frontier.get()

        if best_cost.get(node.v, float("inf")) < cost:
            continue

        if node.v == vg:
            return {"Path": node.path(), "Cost": node.c}
        
        for neighbor, w in graph.adjacent_vertices(node.v):
            new_cost = node.c + w

            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                tie += 1
                frontier.put((new_cost, tie, TreeNode(node, neighbor, new_cost)))