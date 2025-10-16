from queue import Queue
from buildGraph import WeightedGraph

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
    
    def bfs(graph: WeightedGraph, v0, vg):
        """
        This method finds a path in a graph from vertices v0 to vg using the
        breadth-first search algorithm.
        param graph: The graph to traverse.
        param v0: The initial vertex.
        param vg: The goal vertex.
        return: A dictionary with the path from v0 to vg and its total cost,
                or None if there is no path.
        """

        # Check graph and vertices
        if v0 not in graph.vertices():
            print("Warning: Vertex", v0, "is not in Graph")
        if vg not in graph.vertices():
            print("Warning: Vertex", vg, "is not in Graph")

        frontier = Queue()
        frontier.put(TreeNode(None, v0, 0))

        explored_set = {}

        while True:
            if frontier.empty():
                return None
            
            node = frontier.get()

            if node.v == vg:
                return {"Path": node.path(), "Cost": node.c}
            
            if node.v not in explored_set:
                adjacent_vertices = graph.adjacent_vertices(node.v)
                for vertex in adjacent_vertices:
                    neighbor = vertex[0]
                    weight = vertex[1]

                    frontier.put(TreeNode(node, neighbor, node.c + weight))
                
                explored_set[node.v] = 1