import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay, ConvexHull

# -----------------------------
# 1. Datos
# -----------------------------
# A = (1,1), B = (5,2), C = (2,5), D = (4,4), E = (3,1)
points = np.array([
    [1, 1],  # A
    [5, 2],  # B
    [2, 5],  # C
    [4, 4],  # D
    [3, 1],  # E
])
labels = ["A", "B", "C", "D", "E"]

# -----------------------------
# 2. Estructuras geométricas
# -----------------------------
vor = Voronoi(points)
delaunay = Delaunay(points)
hull = ConvexHull(points)

# -----------------------------
# 3. Gráfica
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 6))

# Puntos
ax.scatter(points[:, 0], points[:, 1], color="orange", zorder=5)
for (x, y), label in zip(points, labels):
    ax.text(x + 0.05, y + 0.05, label, fontsize=10)

# Delaunay (triangulación) – amarillo
for simplex in delaunay.simplices:
    poly = points[simplex]
    ax.plot(
        np.append(poly[:, 0], poly[0, 0]),
        np.append(poly[:, 1], poly[0, 1]),
        linestyle="-",
        color="gold",
        linewidth=1.5,
        label="Delaunay" if "Delaunay" not in ax.get_legend_handles_labels()[1] else ""
    )

# Casco convexo – negro más grueso
for i, j in hull.simplices:
    ax.plot(
        [points[i, 0], points[j, 0]],
        [points[i, 1], points[j, 1]],
        color="black",
        linewidth=2.5,
        label="Casco convexo" if "Casco convexo" not in ax.get_legend_handles_labels()[1] else ""
    )

# Voronoi – aristas y vértices
voronoi_plot_2d(
    vor,
    ax=ax,
    show_vertices=True,
    show_points=False,
    line_colors="tab:blue",
    line_width=1.5,
    point_size=20,
)

# -----------------------------
# 4. Estética
# -----------------------------
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Voronoi, Delaunay y casco convexo")
ax.grid(True, linestyle="--", alpha=0.3)
ax.legend(loc="upper left")

plt.tight_layout()
plt.show()