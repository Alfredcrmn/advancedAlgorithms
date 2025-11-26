#------------------------------------------------------------------------------------------------------------------
#   Problema de Misioneros y Caníbales
#------------------------------------------------------------------------------------------------------------------

from simpleai.search import SearchProblem, breadth_first

class MisionerosYCanibales(SearchProblem):
    """
    Representación del estado: (M_izq, C_izq, M_der, C_der, Bote)
    - M_izq, C_izq: Número de misioneros y caníbales en la orilla izquierda.
    - M_der, C_der: Número de misioneros y caníbales en la orilla derecha.
    - Bote: 'L' (Left/Izquierda) o 'R' (Right/Derecha).
    """

    def __init__(self):
        # Estado Inicial: 3 Misioneros y 3 Caníbales a la izquierda ('L')
        # (3, 3, 0, 0, 'L')
        SearchProblem.__init__(self, (3, 3, 0, 0, 'L'))

    def actions(self, state):
        """
        Genera las acciones válidas desde el estado actual.
        Una acción es una tupla (m, c) que indica cuántos misioneros (m) 
        y cuántos caníbales (c) se suben al bote.
        """
        available_actions = []
        
        # Posibles movimientos teóricos (misioneros, canibales)
        # El bote lleva máximo 2 personas, mínimo 1.
        moves = [
            (1, 0), # 1 Misionero
            (2, 0), # 2 Misioneros
            (0, 1), # 1 Caníbal
            (0, 2), # 2 Caníbales
            (1, 1)  # 1 Misionero y 1 Caníbal
        ]

        m_l, c_l, m_r, c_r, boat = state

        # Determinar dirección y recursos disponibles
        if boat == 'L':
            # Si el bote está en la izquierda, necesitamos gente en la izquierda
            for m, c in moves:
                if m_l >= m and c_l >= c: # ¿Hay suficientes personas?
                    if self.is_safe(m_l - m, c_l - c, m_r + m, c_r + c):
                        available_actions.append((m, c))
        else:
            # Si el bote está en la derecha, necesitamos gente en la derecha
            for m, c in moves:
                if m_r >= m and c_r >= c: # ¿Hay suficientes personas?
                    if self.is_safe(m_l + m, c_l + c, m_r - m, c_r - c):
                        available_actions.append((m, c))

        return available_actions

    def is_safe(self, ml, cl, mr, cr):
        """
        Verifica si el estado propuesto es seguro.
        Regla: Caníbales no pueden superar Misioneros en ninguna orilla
        (a menos que haya 0 misioneros en esa orilla).
        """
        # Chequeo orilla izquierda
        if ml > 0 and cl > ml:
            return False
        # Chequeo orilla derecha
        if mr > 0 and cr > mr:
            return False
        return True

    def result(self, state, action):
        """
        Aplica la acción y devuelve el nuevo estado.
        action: (m, c) cantidad de personas a mover.
        """
        m_move, c_move = action
        m_l, c_l, m_r, c_r, boat = state

        if boat == 'L':
            # De Izquierda a Derecha
            return (m_l - m_move, c_l - c_move, m_r + m_move, c_r + c_move, 'R')
        else:
            # De Derecha a Izquierda
            return (m_l + m_move, c_l + c_move, m_r - m_move, c_r - c_move, 'L')

    def is_goal(self, state):
        """
        Objetivo: Todos (3M, 3C) en la derecha.
        """
        return state == (0, 0, 3, 3, 'R')

#------------------------------------------------------------------------------------------------------------------
#   Ejecución
#------------------------------------------------------------------------------------------------------------------

# Usamos Breadth First (Anchura) para encontrar la solución óptima (menos pasos)
result = breadth_first(MisionerosYCanibales(), graph_search=True)

if result:
    print(f"¡Solución encontrada en {len(result.path()) - 1} viajes!")
    print("-" * 50)
    for i, (action, state) in enumerate(result.path()):
        if action is None:
            print(f"Inicio: \t{state}")
        else:
            m, c = action
            people = f"{m} Misionero(s) y {c} Caníbal(es)"
            direction = "->" if state[4] == 'R' else "<-"
            print(f"Viaje {i}: {direction} Mover {people}. \tEstado: {state}")
    print("-" * 50)
else:
    print("No hay solución.")