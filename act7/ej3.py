from math import inf

# Nodos del grafo
nodes = [
    "Goxmont", "Zrusall", "Adaset", "Niaphia", "Ertonwell", "Duron",
    "Lagos", "Blebus", "Togend", "Ontdale", "Goding", "Ylane",
    "Strento", "Oriaron"
]

# Aristas (u, v, w) según la imagen
edges = [
    ("Ylane",   "Goding",   88),
    ("Ylane",   "Strento",  99),
    ("Ylane",   "Oriaron", 117),

    ("Zrusall", "Goxmont", 112),
    ("Zrusall", "Adaset",   15),
    ("Zrusall", "Strento", 121),

    ("Goxmont", "Adaset",  103),
    ("Goxmont", "Niaphia", 212),

    ("Adaset",  "Ertonwell",130),

    ("Ertonwell","Niaphia", 56),
    ("Ertonwell","Duron",  121),

    ("Niaphia", "Lagos",   300),

    ("Duron",   "Lagos",   119),
    ("Duron",   "Blebus",  160),

    ("Blebus",  "Togend",  121),
    ("Blebus",  "Ontdale", 165),
    ("Blebus",  "Oriaron", 291),

    ("Ontdale", "Goding",   98),
    ("Ontdale", "Togend",   210),
    ("Ontdale", "Oriaron", 219),

    ("Strento", "Oriaron", 221),
]


# Construimos lista de adyacencia para grafo NO dirigido
adj = {v: [] for v in nodes}
for u, v, w in edges:
    adj[u].append((v, w))
    adj[v].append((u, w))

def prim(start):
    selected = {start}
    remain = set(nodes) - selected
    mst_edges = []
    cost = 0

    while remain:
        mincost = inf
        best_u = None
        next_v = None

        # Buscar la arista más barata que salga del conjunto selected
        for u in selected:
            for v, w in adj[u]:
                if v in remain and w < mincost:
                    mincost = w
                    best_u = u
                    next_v = v

        if next_v is None:
            # No hay manera de alcanzar más nodos: el grafo estaría desconectado
            break

        # Agregamos el vértice y la arista elegida al árbol
        selected.add(next_v)
        remain.remove(next_v)
        mst_edges.append((best_u, next_v, mincost))
        cost += mincost

    return mst_edges, cost

# Disjoint Set Union (Union-Find) sencillo

class DSU:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, v):
        # compresión de camino simple
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])
        return self.parent[v]

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False  # ya estaban en el mismo conjunto
        # unión por rango
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

def kruskal_mst(vertices, edges):
    dsu = DSU(vertices)
    mst_edges = []
    cost = 0

    # Ordenamos todas las aristas por peso ascendente
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if dsu.union(u, v):      # solo se agrega si conecta componentes distintos
            mst_edges.append((u, v, w))
            cost += w

    return mst_edges, cost



# Ejecutamos Prim desde cualquier vértice, por ejemplo "Ylane"
prim_mst, prim_cost = prim("Ylane")

print("MST con Prim:")
for u, v, w in prim_mst:
    print(f"{u} - {v} : {w}")
print("Costo total:", prim_cost)

#Kruskal

kruskal_mst_edges, kruskal_cost = kruskal_mst(nodes, edges)

print("\nMST con Kruskal:")
for u, v, w in kruskal_mst_edges:
    print(f"{u} - {v} : {w}")
print("Costo total:", kruskal_cost)




