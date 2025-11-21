import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----------------------------
# Datos del problema
# ----------------------------
POINTS = [
    (-19, -17), (-15, 3), (-12, 11), (-8, -5), (-7, 14),
    (-3, -9), (-1, 0), (2, 18), (4, -13), (6, 7),
    (9, -16), (11, 5), (13, -2), (16, 12), (18, -7),
    (-20, 6), (-14, -18), (-9, 9), (-4, -12), (-2, 15),
    (1, -14), (3, 10), (7, -8), (12, 19), (17, -4),
]


# ----------------------------
# Utilidades geométricas
# ----------------------------
def cross(o, a, b):
    """
    Producto cruz de OA x OB (con puntos en 2D).
    > 0: giro a la izquierda
    < 0: giro a la derecha
    = 0: colineales
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def distance_sq(a, b):
    """Distancia al cuadrado entre dos puntos."""
    return (a[0] - b[0])**2 + (a[1] - b[1])**2


# ----------------------------
# Graham scan con captura de estados
# ----------------------------
def graham_scan_with_steps(points):
    """
    Implementación de Graham scan que devuelve:
    - hull_final: lista de puntos del casco convexo
    - steps: lista de estados intermedios de la pila (stack)
      para animar la construcción del casco.
    Cada 'estado' es una copia de la pila en ese momento.
    """
    pts = points[:]
    if len(pts) < 3:
        return pts, [pts]

    # 1. Encontrar el punto con menor y (y si hay empate, menor x)
    pivot = min(pts, key=lambda p: (p[1], p[0]))

    # 2. Ordenar el resto por ángulo polar respecto al pivote
    def polar_angle(p):
        return math.atan2(p[1] - pivot[1], p[0] - pivot[0])

    def sort_key(p):
        return (polar_angle(p), distance_sq(pivot, p))

    pts.remove(pivot)
    pts.sort(key=sort_key)

    # Lista ordenada: pivot seguido de los ordenados
    sorted_points = [pivot] + pts

    # 3. Recorrido con stack
    stack = []
    steps = []  # estados intermedios de la pila

    for p in sorted_points:
        stack.append(p)
        # Mientras haya al menos 3 puntos y el giro no sea a la izquierda, sacamos el del medio
        while len(stack) >= 3 and cross(stack[-3], stack[-2], stack[-1]) <= 0:
            # Si el giro es cero o a la derecha, eliminar el punto del medio
            middle = stack[-2]
            stack.pop(-2)

        # Guardar una copia del estado actual de la pila
        steps.append(stack[:])

    hull = stack
    return hull, steps


# ----------------------------
# Funciones de dibujo
# ----------------------------
def setup_axes(ax, points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    margin = 3

    ax.set_xlim(min(xs) - margin, max(xs) + margin)
    ax.set_ylim(min(ys) - margin, max(ys) + margin)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")


def draw_all_points(ax, points, pivot=None):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.scatter(xs, ys, color="black", s=40, label="Puntos")

    if pivot is not None:
        ax.scatter([pivot[0]], [pivot[1]], color="red", s=60, label="Pivote")


def draw_hull(ax, stack, is_final=False):
    if len(stack) <= 1:
        return

    # Dibujar líneas entre los puntos de la pila
    for i in range(len(stack) - 1):
        x0, y0 = stack[i]
        x1, y1 = stack[i + 1]
        ax.plot([x0, x1], [y0, y1],
                color="blue" if not is_final else "green",
                linewidth=2)

    # Si es el casco final, cerramos el polígono
    if is_final and len(stack) >= 3:
        x0, y0 = stack[-1]
        x1, y1 = stack[0]
        ax.plot([x0, x1], [y0, y1], color="green", linewidth=2)


# ----------------------------
# Animación
# ----------------------------
def animate_graham_scan(points):
    # Calcular casco convexo y pasos intermedios
    hull, steps = graham_scan_with_steps(points)
    pivot = min(points, key=lambda p: (p[1], p[0]))

    fig, ax = plt.subplots(figsize=(6, 6))
    setup_axes(ax, points)

    # Para la leyenda, la dibujamos solo una vez
    draw_all_points(ax, points, pivot=pivot)
    ax.legend(loc="upper left")

    # Esta función se llamará en cada frame de la animación
    def update(frame_index):
        ax.clear()
        setup_axes(ax, points)
        draw_all_points(ax, points, pivot=pivot)

        # Si es el último frame, mostramos el casco final
        if frame_index >= len(steps):
            draw_hull(ax, hull, is_final=True)
            ax.set_title("Casco convexo final (Graham scan)")
        else:
            current_stack = steps[frame_index]
            draw_hull(ax, current_stack, is_final=False)
            ax.set_title(f"Paso {frame_index + 1} de {len(steps)}")

    ani = FuncAnimation(
        fig,
        update,
        frames=len(steps) + 2,  # algunos frames extra para ver el casco final
        interval=800,
        repeat=False
    )

    plt.show()

    # También regresamos el casco por si quieres imprimirlo
    return hull


# ----------------------------
# Programa principal
# ----------------------------
if __name__ == "__main__":
    hull = animate_graham_scan(POINTS)
    print("Casco convexo (en orden):")
    for p in hull:
        print(p)
