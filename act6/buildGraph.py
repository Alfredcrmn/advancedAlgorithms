class WeightedGraph:

    _directed = True                # Directed or not
    _adjacency_list = {}            # Adjacency list

    def __init__(self, directed: bool = False):

        self._directed = directed
        self._adjacency_list = {}

    def clear(self):                # Clears the graph
        self._adjacency_list = {}

    def number_of_vertices(self):   # Returns the number of vertices of the graph
        return len(self._adjacency_list)
    
    def vertices(self):             # Returns the list of vertices

        v = []

        for vi in self._adjacency_list:
            v.append(vi)
        return v
    
    def edges(self):                # Returns the list of edges
        e = []
        if self._directed:
            for v in self._adjacency_list:
                for edge in self._adjacency_list[v]:
                    e.append((v, edge[0], edge[1]))
        else:
                for v in self._adjacency_list:
                    for edge in self._adjacency_list[v]:
                        if (edge[0], v, edge[1]) not in e:
                            e.append((v, edge[0], edge[1]))
        return e
    
    def add_vertex(self, v):        # Add vertex to the graph
        if v in self._adjacency_list:
            print("Warning: Vertex ", v, " already exists.")
        else:
            self._adjacency_list[v] = []

    def remove_vertex(self, v):     # Remove vertex from the graph
        if not v in self._adjacency_list:
            print("Warning: Vertex ", v, " is not in graph.")
        else:

            self._adjacency_list.remove(v)

            for vertex in self._adjacency_list:
                for edge in self._adjacency_list[vertex]:
                    if edge[0] == v:
                        self._adjacency_list[vertex].remove(edge)
    
    def add_edge(self, v1, v2, e = 0):

        '''
        Add edge to the graph. The edge is defined by two vertices, v1 and v2,
        and the weight e of the edge.
        param v1: the start vertex of the new edge.
        param v2: The end vertex of the new edge.
        param e: The weight of the new edge.
        '''
        if v1 not in self._adjacency_list:
            # The start vertex does not exist.
            print("Warning: Vertex ", v1, " does not exist.")
        elif v2 not in self._adjacency_list:
            # The end vertex does not exist.
            print("Warning: Vertex ", v2, " does not exist.")
        elif not self._directed and v1 == v2:
            # The graph is undirected, so it is not allowed to have autocycles.
            print("Warning: An undirected graph cannot have autocycles.")
        elif (v2, e) in self._adjacency_list[v1]:
            # The edge is already in graph.
            print("Warning: The edge (", v1, "," ,v2, ",", e, ") already exists.")
        else:
            self._adjacency_list[v1].append((v2, e))
            if not self._directed:
                self._adjacency_list[v2].append((v1, e))

    def remove_edge(self, v1, v2, e):
        """
        Remove edge from the graph.
        param v1: The start vertex of the edge to be removed.
        param v2: The end vertex of the edge to be removed.
        param e: The weight of the edge to be removed.
        """
        if v1 not in self._adjacency_list:
            print("Warning: Vertex ", v1, " does not exist.")
        elif v2 not in self._adjacency_list:
            print("Warning: Vertex ", v2, " does not exist.")
        else:
            for edge in self._adjacency_list[v1]:
                if edge == (v2, e):
                    self._adjacency_list[v1].remove(edge)
            if not self._directed:
                for edge in self._adjacency_list[v2]:
                    if edge == (v1, e):
                        self._adjacency_list[v2].remove(edge)
    
    def adjacent_vertices(self, v):
        """
        Adjacent vertices of a vertex.
        param v: The vertex whose adjacent vertices are to be returned.
        return: The list of adjacent vertices of v.
        """
        if v not in self._adjacency_list:
            print("Warning: Vertex ", v, " does not exist.")
            return []
        else:
            return self._adjacency_list[v]
    

    def is_adjacent(self, v1, v2) -> bool:
        if v1 not in self._adjacency_list:
            print("Warning: Vertex ", v1, " does not exist.")
            return False
        elif v2 not in self._adjacency_list:
            print("Warning: Vertex ", v2, " does not exist.")
            return False
        else:
            for edge in self._adjacency_list[v1]:
                if edge[0] == v2:
                    return True
                return False
    
    def print_graph(self):
        for vertex in self._adjacency_list:
            for edges in self._adjacency_list[vertex]:
                print(vertex, " -> ", edges[0], " edge weight: ", edges[1])