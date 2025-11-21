import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Arc, PathPatch
from matplotlib.path import Path


def add_body(ax):
    # Cuerpo: elipse grande
    body = Ellipse(
        xy=(0, 0),
        width=6.0,
        height=4.0,
        edgecolor="green",
        facecolor="#a8e6a1",
        linewidth=2,
    )
    ax.add_patch(body)

    # Pecho / barriga: elipse más clara
    belly = Ellipse(
        xy=(0, -0.3),
        width=3.5,
        height=2.5,
        edgecolor="none",
        facecolor="#f7f3c2",
        linewidth=1,
    )
    ax.add_patch(belly)


def add_head(ax):
    # Cabeza: elipse
    head = Ellipse(
        xy=(0, 1.8),
        width=3.5,
        height=2.0,
        edgecolor="green",
        facecolor="#a8e6a1",
        linewidth=2,
    )
    ax.add_patch(head)

    # Ojos: elipses
    eye_left = Ellipse(
        xy=(-1.1, 2.4),
        width=0.7,
        height=0.9,
        edgecolor="green",
        facecolor="white",
        linewidth=2,
    )
    eye_right = Ellipse(
        xy=(1.1, 2.4),
        width=0.7,
        height=0.9,
        edgecolor="green",
        facecolor="white",
        linewidth=2,
    )
    ax.add_patch(eye_left)
    ax.add_patch(eye_right)

    # Pupilas: elipses pequeñas
    pupil_left = Ellipse(
        xy=(-1.1, 2.4),
        width=0.25,
        height=0.4,
        edgecolor="black",
        facecolor="black",
    )
    pupil_right = Ellipse(
        xy=(1.1, 2.4),
        width=0.25,
        height=0.4,
        edgecolor="black",
        facecolor="black",
    )
    ax.add_patch(pupil_left)
    ax.add_patch(pupil_right)

    # Mejillas: arcos suaves
    cheek_left = Arc(
        xy=(-0.9, 1.7),
        width=1.3,
        height=0.7,
        angle=0,
        theta1=200,
        theta2=260,
        edgecolor="pink",
        linewidth=2,
    )
    cheek_right = Arc(
        xy=(0.9, 1.7),
        width=1.3,
        height=0.7,
        angle=0,
        theta1=-80,
        theta2=-20,
        edgecolor="pink",
        linewidth=2,
    )
    ax.add_patch(cheek_left)
    ax.add_patch(cheek_right)

    # Boca: curva de Bézier cúbica
    verts = [
        (-1.0, 1.6),   # P0
        (-0.4, 1.3),   # P1
        (0.4, 1.3),    # P2
        (1.0, 1.6),    # P3
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]
    mouth_path = Path(verts, codes)
    mouth_patch = PathPatch(
        mouth_path,
        edgecolor="black",
        facecolor="none",
        linewidth=2,
    )
    ax.add_patch(mouth_patch)


def add_front_legs(ax):
    # Piernas delanteras: curvas de Bézier para dar sensación de flexión

    # Pierna delantera izquierda
    verts_left = [
        (-1.5, 0.8),   # hombro
        (-2.3, 0.0),   # control
        (-2.0, -1.0),  # control
        (-1.4, -1.2),  # muñeca
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]
    leg_left_path = Path(verts_left, codes)
    leg_left_patch = PathPatch(
        leg_left_path,
        edgecolor="green",
        facecolor="none",
        linewidth=3,
    )
    ax.add_patch(leg_left_patch)

    # Pierna delantera derecha (simétrica)
    verts_right = [
        (1.5, 0.8),
        (2.3, 0.0),
        (2.0, -1.0),
        (1.4, -1.2),
    ]
    leg_right_path = Path(verts_right, codes)
    leg_right_patch = PathPatch(
        leg_right_path,
        edgecolor="green",
        facecolor="none",
        linewidth=3,
    )
    ax.add_patch(leg_right_patch)

    # Dedos delanteros: líneas simples
    # Izquierda
    fingers_left = [
        [(-1.4, -1.2), (-1.1, -1.5)],
        [(-1.4, -1.2), (-1.6, -1.5)],
        [(-1.4, -1.2), (-1.3, -1.6)],
    ]
    for (x0, y0), (x1, y1) in fingers_left:
        ax.plot([x0, x1], [y0, y1], color="green", linewidth=2)

    # Derecha
    fingers_right = [
        [(1.4, -1.2), (1.1, -1.5)],
        [(1.4, -1.2), (1.6, -1.5)],
        [(1.4, -1.2), (1.3, -1.6)],
    ]
    for (x0, y0), (x1, y1) in fingers_right:
        ax.plot([x0, x1], [y0, y1], color="green", linewidth=2)


def add_back_legs(ax):
    # Piernas traseras: combinamos un arco y una curva Bézier

    # Muslo izquierdo: arco
    thigh_left = Arc(
        xy=(-2.0, -0.4),
        width=2.4,
        height=2.0,
        angle=0,
        theta1=-120,
        theta2=10,
        edgecolor="green",
        linewidth=3,
    )
    ax.add_patch(thigh_left)

    # Pantorrilla izquierda: Bézier
    verts_left = [
        (-2.1, -1.5),  # unión con el muslo
        (-3.0, -2.0),  # control
        (-2.4, -2.6),  # control
        (-1.6, -2.4),  # tobillo
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]
    calf_left_path = Path(verts_left, codes)
    calf_left_patch = PathPatch(
        calf_left_path,
        edgecolor="green",
        facecolor="none",
        linewidth=3,
    )
    ax.add_patch(calf_left_patch)

    # Dedos traseros izquierdos: líneas
    toes_left = [
        [(-1.6, -2.4), (-1.2, -2.8)],
        [(-1.6, -2.4), (-1.8, -2.9)],
        [(-1.6, -2.4), (-1.4, -3.0)],
    ]
    for (x0, y0), (x1, y1) in toes_left:
        ax.plot([x0, x1], [y0, y1], color="green", linewidth=2)

    # Muslo derecho: arco
    thigh_right = Arc(
        xy=(2.0, -0.4),
        width=2.4,
        height=2.0,
        angle=0,
        theta1=170,
        theta2=300,
        edgecolor="green",
        linewidth=3,
    )
    ax.add_patch(thigh_right)

    # Pantorrilla derecha: Bézier
    verts_right = [
        (2.1, -1.5),
        (3.0, -2.0),
        (2.4, -2.6),
        (1.6, -2.4),
    ]
    calf_right_path = Path(verts_right, codes)
    calf_right_patch = PathPatch(
        calf_right_path,
        edgecolor="green",
        facecolor="none",
        linewidth=3,
    )
    ax.add_patch(calf_right_patch)

    # Dedos traseros derechos: líneas
    toes_right = [
        [(1.6, -2.4), (1.2, -2.8)],
        [(1.6, -2.4), (1.8, -2.9)],
        [(1.6, -2.4), (1.4, -3.0)],
    ]
    for (x0, y0), (x1, y1) in toes_right:
        ax.plot([x0, x1], [y0, y1], color="green", linewidth=2)


def draw_frog():
    fig, ax = plt.subplots(figsize=(6, 6))

    add_body(ax)
    add_head(ax)
    add_front_legs(ax)
    add_back_legs(ax)

    # Ajuste de la vista
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.axis("off")

    plt.title("Rana con líneas, elipses, arcos y curvas de Bézier")
    plt.show()


if __name__ == "__main__":
    draw_frog()
