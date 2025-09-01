regions = ["Mark","Steve","Julia","Allan","Michelle","Amanda","Joanne","Derek","Brian","Kelly","Chris"] # Regiones en orden
indices = {name:i for i, name in enumerate(regions)} # Le da un índice a los nombres
n = len(regions)

# Restricciones:
restrictions = {
    "Mark":     ["Steve","Julia"],
    "Steve":    ["Mark","Allan","Michelle","Amanda","Julia"],
    "Julia":    ["Mark","Steve","Amanda","Derek","Brian"],
    "Allan":    ["Steve","Michelle"],
    "Michelle": ["Steve","Amanda","Allan","Joanne"],
    "Amanda":   ["Steve","Michelle","Julia","Joanne","Derek"],
    "Joanne":   ["Michelle","Amanda","Derek","Chris"],
    "Derek":    ["Amanda","Julia","Joanne","Brian","Kelly","Chris"],
    "Brian":    ["Julia","Derek","Kelly"],
    "Kelly":    ["Derek","Brian","Chris"],
    "Chris":    ["Derek","Joanne","Kelly"],
}

# Crea una matriz n x n llena de 0s
graph = [[0]*n for i in range(n)] 
for u, nbrs in restrictions.items():
    for v in nbrs:
        graph[indices[u]][indices[v]] = 1 # Si uno es vecino del otro
        graph[indices[v]][indices[u]] = 1 # Se considera en ambos


colors = ["Rojo","Verde","Azul","Gris"] # Colores en orden a ser llamados

def valid_coloring(neighbours, colored, color) -> bool:
    return not any(nei == 1 and colored[i] == color # Hay algún vecino que tenga el mismo color?
                   for i, nei in enumerate(neighbours)) # Si existe algún conflicto, devuelve True, y not lo pasa a False porque no es válido

def util_color_all(graph, m, colored, index, solutions):
    if index == len(graph):
        solutions.append(colored.copy()) # Todos están coloreados y guarda una copia
        return
    for c in range(m):
        if valid_coloring(graph[index], colored, c):
            colored[index] = c
            util_color_all(graph, m, colored, index+1, solutions)
            colored[index] = -1

def color_all(graph, m=4):
    colored = [-1]*len(graph)
    sols = []
    util_color_all(graph, m, colored, 0, sols)
    return sols


solutions = color_all(graph, m=4)
print("Total de soluciones válidas:", len(solutions))


K = min(5, len(solutions))
for s in solutions[:K]:
    parsedSolution = {regions[i]: colors[c] for i, c in enumerate(s)}
    print(parsedSolution)
