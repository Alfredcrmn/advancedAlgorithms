#------------------------------------------------------------------------------------------------------------------
#   Problema del Triángulo Mágico (Orden 3)
#------------------------------------------------------------------------------------------------------------------

from simpleai.search import SearchProblem, depth_first

#------------------------------------------------------------------------------------------------------------------
#   Definición del Problema
#------------------------------------------------------------------------------------------------------------------

class MagicTriangle(SearchProblem):
    """ 
    Clase que define el problema del triángulo mágico de orden 3 (6 posiciones).
    
    El estado se representa mediante una tupla de 6 elementos (x0, x1, x2, x3, x4, x5).
    Los ceros representan posiciones vacías.
    
    Mapeo de índices en el triángulo:
          [0]
         /   \
       [5]   [1]
       /       \
     [4]--[3]--[2]
    
    Lados:
    - Lado A: 0, 1, 2
    - Lado B: 2, 3, 4
    - Lado C: 4, 5, 0
    """

    def __init__(self):
        """ Constructor. Inicializa el problema con el tablero vacío (todos ceros). """
        # Estado inicial: vector de 6 posiciones vacías
        SearchProblem.__init__(self, (0, 0, 0, 0, 0, 0))

    def actions(self, state):
        """ 
        Devuelve las acciones disponibles.
        Para evitar combinaciones redundantes, la estrategia es llenar siempre
        la primera posición vacía disponible (el primer 0 que encuentre).
        """
        available_actions = []
        
        # Determinar qué números ya han sido usados
        used_numbers = set(state)
        # El dominio disponible son los números del 1 al 6 que NO están en el estado
        domain = [n for n in range(1, 7) if n not in used_numbers]

        # Encontrar el índice de la primera posición vacía (0)
        try:
            first_empty_index = state.index(0)
        except ValueError:
            return [] # No hay acciones si el tablero está lleno

        # Generar una acción por cada número disponible para esa posición
        for number in domain:
            # La acción se define como una tupla: (número, índice)
            available_actions.append((number, first_empty_index))

        return available_actions

    def result(self, state, action):
        """ 
        Retorna el nuevo estado después de aplicar la acción.
        action: (valor_a_colocar, indice_donde_colocar)
        """
        value, index = action
        
        # Convertimos la tupla a lista para modificarla
        new_state = list(state)
        new_state[index] = value
        
        # Retornamos como tupla (inmutable) para simpleai
        return tuple(new_state)

    def is_goal(self, state):
        """ 
        Evalúa si el estado es una solución válida (Objetivo).
        """
        # 1. Criterio de Completitud: Si hay algún 0, no hemos terminado.
        if 0 in state:
            return False

        # 2. Criterio de Suma Mágica
        # Definición de los lados según los índices del vector
        side_a = state[0] + state[1] + state[2]
        side_b = state[2] + state[3] + state[4]
        side_c = state[4] + state[5] + state[0]

        # El objetivo es verdadero si los tres lados suman lo mismo
        return side_a == side_b == side_c

#------------------------------------------------------------------------------------------------------------------
#   Programa Principal
#------------------------------------------------------------------------------------------------------------------

# Resolver el problema
# Usamos depth_first porque sabemos que la solución está a una profundidad fija (6 movimientos)
result = depth_first(MagicTriangle())

# Imprimir resultados
if result:
    print("¡Solución encontrada!")
    print("-" * 30)
    for i, (action, state) in enumerate(result.path()):
        if action is None:
            print('Configuración Inicial:', state)
        else:
            val, idx = action
            print(f'Paso {i}: Colocar el número {val} en la posición {idx}')
            print(f'Estado actual: {state}')
    
    print("-" * 30)
    final_state = result.state
    s1 = final_state[0] + final_state[1] + final_state[2]
    s2 = final_state[2] + final_state[3] + final_state[4]
    s3 = final_state[4] + final_state[5] + final_state[0]
    print(f"Verificación de sumas: Lado A={s1}, Lado B={s2}, Lado C={s3}")
else:
    print("No se encontró solución.")

#------------------------------------------------------------------------------------------------------------------
#   Fin del archivo
#------------------------------------------------------------------------------------------------------------------