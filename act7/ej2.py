from collections import deque

# =========================
# Definición del grafo
# =========================

nodes = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']

# (u, v, capacity)
edges = [
    ('H', 'I', 23),
    ('H', 'G', 61),
    ('H', 'B', 85),
      
    ('B', 'H', 72),

    ('I', 'G', 82),
    ('I', 'J', 60),

    ('J', 'G', 42),
    ('J', 'N', 90),

    ('G', 'K', 76),
    ('G', 'F', 25),
    
    ('F', 'G', 24),
    ('F', 'E', 47),

    ('A', 'F', 37),
    ('F', 'A', 43),

    ('A', 'B', 70),
    ('A', 'C', 80),

    ('K', 'E', 66),
    ('K', 'N', 34),
    ('N', 'K', 55),
    ('K', 'M', 42),
    ('K', 'L', 50),

    ('M', 'N', 75),

    ('E', 'C', 44),
    ('E', 'D', 69),
    ('E', 'L', 71),

    ('C', 'D', 54),

    ('D', 'L', 82),

    ('L', 'M', 66),
]



# =========================
# Implementación de Dinic
# =========================

class Dinic:
    def __init__(self, nodes):
        self.nodes = nodes
        self.n = len(nodes)
        self.id = {v: i for i, v in enumerate(nodes)}
        self.adj = [[] for _ in range(self.n)] 

    def add_edge(self, u, v, cap):
        ui = self.id[u]
        vi = self.id[v]
        self.adj[ui].append([vi, cap, len(self.adj[vi])])
        self.adj[vi].append([ui, 0, len(self.adj[ui]) - 1])

    def _bfs_levels(self, s, t):
        level = [-1] * self.n
        dq = deque()
        level[s] = 0
        dq.append(s)
        while dq:
            v = dq.popleft()
            for to, cap, _ in self.adj[v]:
                if cap > 0 and level[to] < 0:
                    level[to] = level[v] + 1
                    dq.append(to)
        return level

    def _dfs_flow(self, v, t, f, level, it):
        if v == t:
            return f
        for i in range(it[v], len(self.adj[v])):
            it[v] = i
            to, cap, rev = self.adj[v][i]
            if cap > 0 and level[v] < level[to]:
                pushed = self._dfs_flow(to, t, min(f, cap), level, it)
                if pushed > 0:
                    self.adj[v][i][1] -= pushed
                    self.adj[to][rev][1] += pushed
                    return pushed
        return 0

    def max_flow(self, s_label, t_label):
        s = self.id[s_label]
        t = self.id[t_label]
        flow = 0
        INF = 10**18

        while True:
            level = self._bfs_levels(s, t)
            if level[t] < 0:
                break

            it = [0] * self.n
            while True:
                pushed = self._dfs_flow(s, t, INF, level, it)
                if pushed == 0:
                    break
                flow += pushed

        return flow


# =========================
# Construir grafo base
# =========================

def build_dinic():
    d = Dinic(nodes)
    for u, v, c in edges:
        d.add_edge(u, v, c)
    return d


# =========================
# Cálculos pedidos
# =========================

# 1) Flujo máximo de A a N
dinic_AN = build_dinic()
maxflow_A_N = dinic_AN.max_flow('A', 'N')
print("Flujo máximo de A a N:", maxflow_A_N)

# 2) Otras tres parejas de vértices
pairs = [
    ('H', 'L'),
    ('G', 'N'),
    ('J', 'D'),
]

for s, t in pairs:
    d = build_dinic()
    f = d.max_flow(s, t)
    print(f"Flujo máximo de {s} a {t}: {f}")
