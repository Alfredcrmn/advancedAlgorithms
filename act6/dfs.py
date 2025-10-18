from buildGraph import WeightedGraph
from queue import LifoQueue

class TreeNode:
    def __init__(self,parent, v, c):
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
    
def dfs(graph: WeightedGraph, v0, vg):
    """
    Finds a path in a graph from v0 to vg using Depth-First Search (DFS).
    NOTE: DFS does not guarantee minimum cost or minimum number of edges.
    return: {"Path": [...], "Cost": total_cost} or None if no path exists.
    """

    if v0 not in graph.vertices():
        print("Warning: Vertex", v0, "is not in Graph")
    if vg not in graph.vertices():
        print("Warning: Vertex", vg, "is not in Graph")

    
    frontier = LifoQueue()
    frontier.put(TreeNode(None, v0, 0))

    explored_set = {}

    while True:
        if frontier.empty():
            return None
        
        node = frontier.get()

        if node.v == vg:
            return {"Path": node.path(), "Cost": node.c}
        
        if node.v not in explored_set:
            for neighbor, w in graph.adjacent_vertices(node.v):
                frontier.put(TreeNode(node, neighbor, node.c + w))

            explored_set[node.v] = 1