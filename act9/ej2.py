import random
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


Point = Tuple[float, float]


class KDNode:
    """
    Nodo de un Kd Tree 2D.
    - point: tupla (x, y)
    - axis: 0 para dividir por x, 1 para dividir por y
    - left, right: subárboles
    """

    __slots__ = ("point", "axis", "left", "right")

    def __init__(self, point: Point, axis: int):
        self.point: Point = point
        self.axis: int = axis
        self.left: Optional["KDNode"] = None
        self.right: Optional["KDNode"] = None


class KDTree2D:
    """
    Kd Tree 2D para búsquedas de rango.
    """

    def __init__(self, points: List[Point]):
        # Construimos el árbol a partir de los puntos
        pts_copy = list(points)
        self.root = self._build(pts_copy, depth=0)

    def _build(self, points: List[Point], depth: int) -> Optional[KDNode]:
        if not points:
            return None

        k = 2  # dimensión
        axis = depth % k

        # Ordenar los puntos según el eje actual y escoger la mediana
        points.sort(key=lambda p: p[axis])
        mid = len(points) // 2
        node = KDNode(points[mid], axis)

        node.left = self._build(points[:mid], depth + 1)
        node.right = self._build(points[mid + 1 :], depth + 1)
        return node

    # -----------------------------
    # Búsqueda de rango
    # -----------------------------
    def range_search(
        self,
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
    ) -> List[Point]:
        result: List[Point] = []
        self._range_search_recursive(self.root, xmin, xmax, ymin, ymax, result)
        return result

    def _range_search_recursive(
        self,
        node: Optional[KDNode],
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
        result: List[Point],
    ) -> None:
        if node is None:
            return

        x, y = node.point

        # Si el punto del nodo está dentro del rectángulo, lo agregamos
        if xmin <= x <= xmax and ymin <= y <= ymax:
            result.append(node.point)

        axis = node.axis
        coord = x if axis == 0 else y

        # Dependiendo del eje, decidimos qué subárboles explorar
        if axis == 0:
            # División vertical por x
            if xmin <= coord:
                self._range_search_recursive(
                    node.left, xmin, xmax, ymin, ymax, result
                )
            if coord <= xmax:
                self._range_search_recursive(
                    node.right, xmin, xmax, ymin, ymax, result
                )
        else:
            # División horizontal por y
            if ymin <= coord:
                self._range_search_recursive(
                    node.left, xmin, xmax, ymin, ymax, result
                )
            if coord <= ymax:
                self._range_search_recursive(
                    node.right, xmin, xmax, ymin, ymax, result
                )


# --------------------------------------
# Generación de datos y pruebas
# --------------------------------------
def generate_random_points(n: int, low: float = -10.0, high: float = 10.0):
    rng = random.Random(123)
    return [(rng.uniform(low, high), rng.uniform(low, high)) for _ in range(n)]


def plot_all(points: List[Point]):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(xs, ys, s=20, color="black")
    ax.set_title("Puntos aleatorios (200)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", alpha=0.3)
    plt.show()


def plot_ranges(points: List[Point], ranges: List[Tuple[float, float, float, float]], tree: KDTree2D):
    """
    Crea un grid de subplots, uno por rango, mostrando:
    - todos los puntos en gris
    - los puntos dentro del rango resaltados en rojo
    - el rectángulo del rango
    """
    num_ranges = len(ranges)
    cols = 3
    rows = (num_ranges + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    axes = axes.flatten()

    all_x = [p[0] for p in points]
    all_y = [p[1] for p in points]
    xmin_global = min(all_x) - 1
    xmax_global = max(all_x) + 1
    ymin_global = min(all_y) - 1
    ymax_global = max(all_y) + 1

    for idx, (xmin, xmax, ymin, ymax) in enumerate(ranges):
        ax = axes[idx]

        # Puntos dentro del rango
        inside = tree.range_search(xmin, xmax, ymin, ymax)

        ax.scatter(all_x, all_y, s=15, color="lightgray", label="Todos los puntos")
        if inside:
            xs_in = [p[0] for p in inside]
            ys_in = [p[1] for p in inside]
            ax.scatter(xs_in, ys_in, s=25, color="red", label="En el rango")

        # Dibujar el rectángulo del rango
        rect = Rectangle(
            (xmin, ymin),
            xmax - xmin,
            ymax - ymin,
            fill=False,
            edgecolor="blue",
            linewidth=2,
        )
        ax.add_patch(rect)

        ax.set_title(f"Rango x∈[{xmin}, {xmax}], y∈[{ymin}, {ymax}]\nPuntos: {len(inside)}")
        ax.set_xlim(xmin_global, xmax_global)
        ax.set_ylim(ymin_global, ymax_global)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linestyle="--", alpha=0.3)

    # Si hay subplots de sobra, los apagamos
    for j in range(num_ranges, rows * cols):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


def main():
    # 1) Generar 200 puntos en el plano, x,y ∈ [-10, 10]
    points = generate_random_points(200, -10.0, 10.0)
    print(f"Se generaron {len(points)} puntos en [-10,10] x [-10,10].")

    # 2) Construir Kd Tree
    tree = KDTree2D(points)

    # 3) Graficar todos los puntos
    plot_all(points)

    # 4) Rangos a consultar
    ranges = [
        (-1.0, 1.0, -2.0, 2.0),
        (-2.0, 1.0, 3.0, 5.0),
        (-7.0, 0.0, -6.0, 4.0),
        (-2.0, 2.0, -3.0, 3.0),
        (-7.0, 5.0, -3.0, 1.0),
    ]

    # 5) Ejecutar consultas e imprimir resumen
    for (xmin, xmax, ymin, ymax) in ranges:
        inside = tree.range_search(xmin, xmax, ymin, ymax)
        print(f"\nRango x ∈ [{xmin}, {xmax}], y ∈ [{ymin}, {ymax}]:")
        print(f"  Puntos encontrados: {len(inside)}")
        preview = inside[:10]
        print(f"  Algunos puntos (hasta 10): {preview}")

    # 6) Graficar resultados por rango
    plot_ranges(points, ranges, tree)


if __name__ == "__main__":
    main()
