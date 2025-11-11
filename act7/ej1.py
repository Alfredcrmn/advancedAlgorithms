import tsp

# ============================================================
# Construcción del grafo
# ============================================================
def build_graph() -> tsp.WeightedGraph:
    g = tsp.WeightedGraph(directed=False)
    labels = list("ABCDEFGHIJKLMNOPQRST")
    for v in labels:
        g.add_vertex(v)
    edges = [
        ('A','B',  7),  ('B','C',14), ('C','D', 9), ('D','E',11), ('E','F', 8),
        ('F','G',10),  ('G','H',13), ('H','I', 6), ('I','J',15), ('J','K',12),
        ('K','L', 9),  ('L','M',16), ('M','N', 5), ('N','O',14), ('O','P',10),
        ('P','Q',13),  ('Q','R',  7), ('R','S',  9), ('S','T', 8), ('T','A',11),
        ('A','G',20), ('C','I',22), ('E','K',25), ('G','M',18), ('I','O',23),
        ('K','Q',27), ('M','S',16), ('O','A',30),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g

# ============================================================
# Utilidades
# ============================================================
def print_adjacency_list(g: tsp.WeightedGraph) -> None:
    """Imprime la lista de adyacencia ordenada por nombre de vértice."""
    print("\n----- Adjacency List -----")
    for v in sorted(g.vertices()):
        items = "  ".join(f"({u}, {w})" for (u, w) in g.adjacent_vertices(v))
        print(f"{v}: {items}")
    print()

def show_result(tag: str, res):
    if res is None:
        print(f"{tag}: no encontró ciclo Hamiltoniano.")
        return
    cost = res["Cost"]
    path_vertices = " -> ".join(v for (v, _) in res["Path"])
    print(f"{tag} -> Costo:", cost)
    print(f"{tag} -> Path :", path_vertices)

# ============================================================
# Ejecución
# ============================================================

g = build_graph()
tsp.gr = g

print_adjacency_list(g)

start = "A"
print("-----Uniform cost search-----")
res_ucs = tsp.tsp_ucs(g, start)
show_result("UCS", res_ucs)

print("-----Branch and bound-----")
res_bnb = tsp.tsp_bb(g, start)
show_result("BnB", res_bnb)