#------------------------------------------------------------------------------------------------------------------
#   Problema de las 3 Jarras (Water Pouring Puzzle)
#------------------------------------------------------------------------------------------------------------------

from simpleai.search import SearchProblem, breadth_first

#------------------------------------------------------------------------------------------------------------------
#   Definición del Problema
#------------------------------------------------------------------------------------------------------------------

class JarrasProblem(SearchProblem):
    """
    Clase que define el problema de las 3 jarras.
    Estado: Tupla (j8, j5, j3) representando los litros actuales en cada jarra.
    Capacidades: 8L, 5L, 3L.
    """

    def __init__(self):
        # Definimos las capacidades como atributo de la clase para usarlas luego
        self.capacities = (8, 5, 3) 
        # Estado inicial: (8, 0, 0) -> Jarra de 8L llena, las otras vacías
        SearchProblem.__init__(self, (8, 0, 0))

    def actions(self, state):
        """
        Genera las acciones válidas.
        Una acción se representa como una tupla (origen, destino) indicando los índices de las jarras.
        Índices: 0=8L, 1=5L, 2=3L
        """
        available_actions = []
        
        # Todas las combinaciones posibles de verter de una jarra a otra
        # (Origen, Destino)
        permutations = [
            (0, 1), (0, 2), # De 8L a 5L o 3L
            (1, 0), (1, 2), # De 5L a 8L o 3L
            (2, 0), (2, 1)  # De 3L a 8L o 5L
        ]

        for src, dst in permutations:
            # Condición 1: La jarra de origen debe tener algo de líquido
            has_water = state[src] > 0
            # Condición 2: La jarra de destino debe tener espacio (no estar llena)
            has_space = state[dst] < self.capacities[dst]
            
            if has_water and has_space:
                available_actions.append((src, dst))

        return available_actions

    def result(self, state, action):
        """
        Aplica la acción de verter agua y devuelve el nuevo estado.
        action: tupla (src_idx, dst_idx)
        """
        src, dst = action
        
        # Convertimos a lista para modificar
        new_state = list(state)
        
        src_amount = new_state[src]
        dst_amount = new_state[dst]
        dst_capacity = self.capacities[dst]
        
        # Lógica de vertido:
        # Se vierte lo que hay en origen, O lo que cabe en destino (lo que sea menor)
        transfer_amount = min(src_amount, dst_capacity - dst_amount)
        
        new_state[src] -= transfer_amount
        new_state[dst] += transfer_amount
        
        return tuple(new_state)

    def is_goal(self, state):
        """
        El objetivo es tener 4 litros en la jarra de 8L y 4 litros en la de 5L.
        Estado objetivo: (4, 4, 0)
        """
        return state == (4, 4, 0)

#------------------------------------------------------------------------------------------------------------------
#   Programa Principal
#------------------------------------------------------------------------------------------------------------------

# Mapeo de índices a nombres para imprimir bonito
jar_names = {0: "8L", 1: "5L", 2: "3L"}

# Resolver el problema usando Búsqueda en Anchura (Breadth First)
# Esto garantiza encontrar la solución más corta (menos pasos)
result = breadth_first(JarrasProblem(), graph_search=True)

if result:
    print(f"¡Objetivo alcanzado en {len(result.path()) - 1} pasos!")
    print("-" * 40)
    
    for i, (action, state) in enumerate(result.path()):
        if action is None:
            print(f"Inicio: \t\t{state}")
        else:
            src, dst = action
            print(f"Paso {i}: Verter {jar_names[src]} -> {jar_names[dst]} \t{state}")
            
    print("-" * 40)
else:
    print("No se encontró solución.")