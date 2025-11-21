import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay, ConvexHull

# -----------------------------
# Puntos del problema
# -----------------------------
points = np.array([
    (9, 7),
    (1, 3),
    (7, 2),
    (1, 9),
    (5, 4),
], dtype=float)


# -----------------------------
# Cálculos geométricos
# -----------------------------
# Casco convexo
hull = ConvexHull(points)

# Triangulación de Delaunay
tri = Delaunay(points)

# Diagrama de Voronoi
vor = Voronoi(points)


# -----------------------------
# Utilidad: círculo circunscrito
# -----------------------------
def circumcircle(p1, p2, p3):
    """
    Regresa (centro_x, centro_y, radio) del círculo circunscrito
    de un triángulo definido por p1, p2, p3 (puntos 2D).

    Fórmula: resolver intersección de bisectrices perpendiculares.
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    # Matriz y vector del sistema lineal
    A = np.array([
        [2 * (x2 - x1), 2 * (y2 - y1)],
        [2 * (x3 - x1), 2 * (y3 - y1)]
    ], dtype=float)

    b = np.array([
        x2**2 + y2**2 - x1**2 - y1**2,
        x3**2 + y3**2 - x1**2 - y1**2
    ], dtype=float)

    # Resolver A * [cx, cy]^T = b
    cx, cy = np.linalg.solve(A, b)

    # Radio: distancia del centro a cualquiera de los vértices
    r = np.sqrt((cx - x1)**2 + (cy - y1)**2)

    return cx, cy, r


# -----------------------------
# Figura y subplots (4 gráficas)
# -----------------------------
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
ax_hull, ax_tri, ax_vor, ax_circ = axes.flat


# -----------------------------
# 1) Casco convexo
# -----------------------------
ax_hull.set_title("Casco convexo")
ax_hull.set_aspect("equal", adjustable="box")
ax_hull.grid(True, linestyle="--", alpha=0.3)

# Dibujar todos los puntos
ax_hull.scatter(points[:, 0], points[:, 1], color="black", zorder=3)

# Dibujar el casco (aristas)
for simplex in hull.simplices:
    x0, y0 = points[simplex[0]]
    x1, y1 = points[simplex[1]]
    ax_hull.plot([x0, x1], [y0, y1], color="green", linewidth=2)

for i, (x, y) in enumerate(points):
    ax_hull.text(x + 0.1, y + 0.1, f"P{i}", fontsize=8)

ax_hull.set_xlabel("X")
ax_hull.set_ylabel("Y")


# -----------------------------
# 2) Triangulación de Delaunay
# -----------------------------
ax_tri.set_title("Triangulación de Delaunay")
ax_tri.set_aspect("equal", adjustable="box")
ax_tri.grid(True, linestyle="--", alpha=0.3)

ax_tri.scatter(points[:, 0], points[:, 1], color="black", zorder=3)

for simplex in tri.simplices:
    cycle = np.append(simplex, simplex[0])  # cerrar triángulo
    ax_tri.plot(points[cycle, 0], points[cycle, 1],
                color="blue", linewidth=2)

for i, (x, y) in enumerate(points):
    ax_tri.text(x + 0.1, y + 0.1, f"P{i}", fontsize=8)

ax_tri.set_xlabel("X")
ax_tri.set_ylabel("Y")


# -----------------------------
# 3) Diagrama de Voronoi
# -----------------------------
ax_vor.set_title("Diagrama de Voronoi")
ax_vor.set_aspect("equal", adjustable="box")
ax_vor.grid(True, linestyle="--", alpha=0.3)

voronoi_plot_2d(
    vor,
    ax=ax_vor,
    show_vertices=True,
    line_colors="tab:blue",
    line_width=2,
    line_alpha=0.8,
    point_size=20,
)

for i, (x, y) in enumerate(points):
    ax_vor.text(x + 0.1, y + 0.1, f"P{i}", fontsize=8, color="black")

ax_vor.set_xlabel("X")
ax_vor.set_ylabel("Y")


# -----------------------------
# 4) Círculos de la triangulación de Delaunay
# -----------------------------
ax_circ.set_title("Círculos circunscritos (Delaunay)")
ax_circ.set_aspect("equal", adjustable="box")
ax_circ.grid(True, linestyle="--", alpha=0.3)

# Dibujar puntos
ax_circ.scatter(points[:, 0], points[:, 1], color="black", zorder=3)

# Dibujar triángulos y sus círculos
for simplex in tri.simplices:
    # Vértices del triángulo
    p1 = points[simplex[0]]
    p2 = points[simplex[1]]
    p3 = points[simplex[2]]

    # Triángulo
    cycle = np.append(simplex, simplex[0])
    ax_circ.plot(points[cycle, 0], points[cycle, 1],
                 color="blue", linewidth=1.5)

    # Círculo circunscrito
    cx, cy, r = circumcircle(p1, p2, p3)
    circ = Circle((cx, cy), r, fill=False,
                  edgecolor="red", linestyle="--", linewidth=1.5, alpha=0.9)
    ax_circ.add_patch(circ)

for i, (x, y) in enumerate(points):
    ax_circ.text(x + 0.1, y + 0.1, f"P{i}", fontsize=8)

ax_circ.set_xlabel("X")
ax_circ.set_ylabel("Y")

plt.tight_layout()
plt.show()


# -----------------------------
# Información útil en consola
# -----------------------------
print("Puntos (índice -> coordenadas):")
for i, p in enumerate(points):
    print(f"P{i}: {tuple(p)}")

print("\nCasco convexo (índices en el orden de las aristas):")
print(hull.simplices)

print("\nTriángulos de Delaunay (índices de cada triángulo):")
print(tri.simplices)

print("\nRegiones de Voronoi (ridge_points = pares que comparten arista de Voronoi):")
print(vor.ridge_points)
