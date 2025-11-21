import random
from typing import List, Optional, Tuple


class RangeTree1D:
    """
    Estructura de datos Range Tree unidimensional.

    Implementada como un árbol binario de búsqueda balanceado (BST)
    construido a partir de la lista de valores ordenados.

    - Cada nodo almacena:
        - value: valor de la coordenada 1D
        - left, right: subárboles izquierdo y derecho

    - Operaciones principales:
        - build: construir el árbol a partir de una lista de valores
        - query_range: regresar todos los valores en [a, b]
    """

    class Node:
        __slots__ = ("value", "left", "right")

        def __init__(self, value: float):
            self.value: float = value
            self.left: Optional["RangeTree1D.Node"] = None
            self.right: Optional["RangeTree1D.Node"] = None

    def __init__(self, values: List[float]):
        # Ordenamos los valores y construimos un BST balanceado
        sorted_values = sorted(values)
        self.root = self._build_balanced(sorted_values, 0, len(sorted_values) - 1)

    def _build_balanced(
        self, arr: List[float], lo: int, hi: int
    ) -> Optional["RangeTree1D.Node"]:
        """
        Construye recursivamente un BST balanceado
        tomando el elemento medio como raíz.
        """
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = self.Node(arr[mid])
        node.left = self._build_balanced(arr, lo, mid - 1)
        node.right = self._build_balanced(arr, mid + 1, hi)
        return node

    # -------------------------------------------------
    # Consulta de rango
    # -------------------------------------------------
    def query_range(self, a: float, b: float) -> List[float]:
        """
        Regresa todos los valores x tales que a <= x <= b.
        Complejidad típica: O(log n + k) donde k es el número de
        resultados reportados, porque se podan subárboles completos
        que están fuera del rango.
        """
        result: List[float] = []
        self._query_range_recursive(self.root, a, b, result)
        return result

    def _query_range_recursive(
        self, node: Optional["RangeTree1D.Node"], a: float, b: float, result: List[float]
    ) -> None:
        if node is None:
            return

        # Si el valor del nodo está dentro del rango, se agrega
        # y se exploran ambos lados, ya que puede haber más valores
        # en [a, b] tanto a la izquierda como a la derecha.
        if a <= node.value <= b:
            result.append(node.value)
            self._query_range_recursive(node.left, a, b, result)
            self._query_range_recursive(node.right, a, b, result)
        # Si el valor es menor que a, todo lo que está a la izquierda
        # también será <= node.value, por tanto < a, y se puede podar.
        elif node.value < a:
            self._query_range_recursive(node.right, a, b, result)
        # Si el valor es mayor que b, todo lo que está a la derecha
        # será >= node.value, por tanto > b, y se puede podar.
        else:  # node.value > b
            self._query_range_recursive(node.left, a, b, result)


# -------------------------------------------------
# Prueba con 2000 valores aleatorios en [-10, 10]
# -------------------------------------------------
def main():
    rng = random.Random(42)  # semilla fija para reproducibilidad

    # 1. Generar 2000 valores aleatorios uniformes en [-10, 10]
    n = 2000
    values = [rng.uniform(-10.0, 10.0) for _ in range(n)]

    print(f"Se generaron {len(values)} valores aleatorios en [-10, 10].")

    # 2. Construir Range Tree unidimensional
    tree = RangeTree1D(values)

    # 3. Rangos a consultar
    ranges: List[Tuple[float, float]] = [
        (-1.0, -0.5),
        (2.0, 4.0),
        (-5.0, -4.0),
        (-10.0, -9.3),
        (9.0, 9.5),
    ]

    # 4. Ejecutar consultas
    for a, b in ranges:
        res = tree.query_range(a, b)
        res_sorted = sorted(res)
        print(f"\nRango [{a}, {b}]:")
        print(f"  Número de valores encontrados: {len(res_sorted)}")
        # Mostrar algunos valores como ejemplo (hasta 10)
        preview = res_sorted[:10]
        print(f"  Primeros valores ordenados (hasta 10): {preview}")

    # (Opcional) Validación por comparación con búsqueda lineal
    print("\nValidando con búsqueda lineal...")
    all_ok = True
    for a, b in ranges:
        expected = sorted([x for x in values if a <= x <= b])
        got = sorted(tree.query_range(a, b))
        ok = expected == got
        print(f"  Rango [{a}, {b}] -> {'OK' if ok else 'ERROR'}")
        if not ok:
            all_ok = False

    if all_ok:
        print("Todas las consultas coinciden con la búsqueda lineal.")
    else:
        print("Hubo discrepancias con la búsqueda lineal.")


if __name__ == "__main__":
    main()
