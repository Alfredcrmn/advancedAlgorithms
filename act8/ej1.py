# ejercicio1_affine.py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # necesario para la proyección 3d


class AffineTransformation:
    """
    Clase para manejar transformaciones afines en 3D usando matrices 4x4.

    Convención:
    - Vectores columna homogéneos: [x, y, z, 1]^T
    - p' = T @ p
    - La matriz self.matrix empieza como identidad y se va componiendo como:
      self.matrix = A @ self.matrix
    """

    def __init__(self):
        # Matriz identidad 4x4
        self.matrix = np.eye(4, dtype=float)

    # -----------------------
    # Métodos de transformación
    # -----------------------
    def add_scale(self, sx, sy=None, sz=None):
        """
        Agrega un escalado a la transformación.
        Si sy o sz son None, se reutiliza sx como escala uniforme.
        """
        if sy is None:
            sy = sx
        if sz is None:
            sz = sx

        S = np.array([
            [sx, 0.0, 0.0, 0.0],
            [0.0, sy, 0.0, 0.0],
            [0.0, 0.0, sz, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)

        self.matrix = S @ self.matrix
        return self

    def add_translation(self, tx, ty, tz):
        """
        Agrega una traslación a la transformación.
        """
        T = np.array([
            [1.0, 0.0, 0.0, tx],
            [0.0, 1.0, 0.0, ty],
            [0.0, 0.0, 1.0, tz],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)

        self.matrix = T @ self.matrix
        return self

    def add_rotation_x(self, angle):
        """
        Agrega una rotación alrededor del eje X.
        ángulo en radianes.
        """
        c = float(np.cos(angle))
        s = float(np.sin(angle))

        R = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, c,   -s,  0.0],
            [0.0, s,    c,  0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)

        self.matrix = R @ self.matrix
        return self

    def add_rotation_y(self, angle):
        """
        Agrega una rotación alrededor del eje Y.
        ángulo en radianes.
        """
        c = float(np.cos(angle))
        s = float(np.sin(angle))

        R = np.array([
            [c,   0.0, s,   0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-s,  0.0, c,   0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)

        self.matrix = R @ self.matrix
        return self

    def add_rotation_z(self, angle):
        """
        Agrega una rotación alrededor del eje Z.
        ángulo en radianes.
        """
        c = float(np.cos(angle))
        s = float(np.sin(angle))

        R = np.array([
            [c,   -s,  0.0, 0.0],
            [s,    c,  0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)

        self.matrix = R @ self.matrix
        return self

    def add_rotation_axis(self, axis, angle):
        """
        Agrega una rotación alrededor de un vector unitario dado.
        - axis: iterable de longitud 3 (ux, uy, uz)
        - angle: ángulo en radianes

        Se usa la fórmula de Rodrigues para construir la matriz 3x3 y se
        incrusta en una matriz 4x4.
        """
        axis = np.asarray(axis, dtype=float)
        norm = np.linalg.norm(axis)
        if norm == 0.0:
            raise ValueError("El vector de eje no puede tener norma cero.")

        ux, uy, uz = axis / norm

        c = float(np.cos(angle))
        s = float(np.sin(angle))
        one_c = 1.0 - c

        # Matriz 3x3 de rotación usando fórmula de Rodrigues
        R3 = np.array([
            [c + ux*ux*one_c,      ux*uy*one_c - uz*s, ux*uz*one_c + uy*s],
            [uy*ux*one_c + uz*s,   c + uy*uy*one_c,    uy*uz*one_c - ux*s],
            [uz*ux*one_c - uy*s,   uz*uy*one_c + ux*s, c + uz*uz*one_c   ]
        ], dtype=float)

        R = np.eye(4, dtype=float)
        R[:3, :3] = R3

        self.matrix = R @ self.matrix
        return self

    def add_shear(self, sh_xy=0.0, sh_xz=0.0,
                  sh_yx=0.0, sh_yz=0.0,
                  sh_zx=0.0, sh_zy=0.0):
        """
        Agrega un cizallamiento general en 3D.

        Interpretación con vectores columna:
        x' = x + sh_xy * y + sh_xz * z
        y' = sh_yx * x + y + sh_yz * z
        z' = sh_zx * x + sh_zy * y + z
        """
        Sh = np.array([
            [1.0,   sh_xy, sh_xz, 0.0],
            [sh_yx, 1.0,   sh_yz, 0.0],
            [sh_zx, sh_zy, 1.0,   0.0],
            [0.0,   0.0,   0.0,   1.0]
        ], dtype=float)

        self.matrix = Sh @ self.matrix
        return self

    # -----------------------
    # Aplicación de la transformación
    # -----------------------
    def transform_points(self, points):
        """
        Dada una lista/array de puntos Nx3, devuelve los puntos transformados.
        """
        pts = np.asarray(points, dtype=float)
        if pts.ndim != 2 or pts.shape[1] != 3:
            raise ValueError("Los puntos deben tener forma (N, 3).")

        n = pts.shape[0]
        ones = np.ones((n, 1), dtype=float)
        hom = np.hstack([pts, ones])           # Nx4
        # Convertimos a forma 4xN para aplicar T @ p
        hom_t = hom.T                          # 4xN
        transformed_hom_t = self.matrix @ hom_t  # 4xN
        transformed_hom = transformed_hom_t.T    # Nx4

        return transformed_hom[:, :3]

    def inverse_transform_points(self, points):
        """
        Aplica la transformación inversa a una lista de puntos Nx3.
        """
        inv = self.get_inverse_matrix()
        pts = np.asarray(points, dtype=float)
        if pts.ndim != 2 or pts.shape[1] != 3:
            raise ValueError("Los puntos deben tener forma (N, 3).")

        n = pts.shape[0]
        ones = np.ones((n, 1), dtype=float)
        hom = np.hstack([pts, ones])       # Nx4
        hom_t = hom.T                      # 4xN
        orig_hom_t = inv @ hom_t           # 4xN
        orig_hom = orig_hom_t.T            # Nx4

        return orig_hom[:, :3]

    # -----------------------
    # Acceso a matrices
    # -----------------------
    def get_matrix(self):
        """
        Devuelve una copia de la matriz de transformación 4x4 actual.
        """
        return self.matrix.copy()

    def get_inverse_matrix(self):
        """
        Devuelve la matriz inversa 4x4 de la transformación actual.
        """
        return np.linalg.inv(self.matrix)


# ---------------------------------
# Pruebas numéricas (con asserts)
# ---------------------------------
def run_numeric_tests():
    rng = np.random.default_rng(42)
    print("Ejecutando pruebas numéricas...")

    # 1. Identidad
    t = AffineTransformation()
    pts = rng.uniform(-10, 10, size=(10, 3))
    transformed = t.transform_points(pts)
    assert np.allclose(transformed, pts), "Fallo en la prueba de identidad."

    # 2. Solo traslación
    tx, ty, tz = 1.5, -2.0, 0.7
    t = AffineTransformation().add_translation(tx, ty, tz)
    transformed = t.transform_points(pts)
    expected = pts + np.array([tx, ty, tz])
    assert np.allclose(transformed, expected), "Fallo en la prueba de traslación."

    # 3. Solo escalado
    sx, sy, sz = 2.0, 0.5, -1.0
    t = AffineTransformation().add_scale(sx, sy, sz)
    transformed = t.transform_points(pts)
    expected = pts * np.array([sx, sy, sz])
    assert np.allclose(transformed, expected), "Fallo en la prueba de escalado."

    # 4. Rotación simple alrededor de Z (90 grados)
    angle = np.pi / 2.0
    t = AffineTransformation().add_rotation_z(angle)
    p = np.array([[1.0, 0.0, 0.0]])
    p_rot = t.transform_points(p)[0]
    expected = np.array([0.0, 1.0, 0.0])
    assert np.allclose(p_rot, expected, atol=1e-7), "Fallo en la rotación alrededor de Z."

    # 5. Composición + inversa con muchos puntos
    t = AffineTransformation()
    t.add_scale(1.2, 0.7, 1.5)
    t.add_rotation_x(0.3)
    t.add_rotation_y(-0.4)
    t.add_rotation_z(0.8)
    t.add_shear(sh_xy=0.3, sh_yz=-0.2)
    t.add_translation(3.0, -1.0, 2.0)

    pts_many = rng.uniform(-5, 5, size=(200, 3))
    transformed_many = t.transform_points(pts_many)
    recovered_many = t.inverse_transform_points(transformed_many)

    assert np.allclose(recovered_many, pts_many, atol=1e-7), \
        "Fallo en prueba de ida y vuelta (transformación + inversa)."

    print("Todas las pruebas numéricas pasaron correctamente.")


# ---------------------------------
# Prueba visual con matplotlib
# ---------------------------------
def visualize_random_points():
    rng = np.random.default_rng(0)
    # Al menos 100 puntos, usamos 200 para que se note más
    pts = rng.uniform(-1.0, 1.0, size=(200, 3))

    # Definimos una transformación combinada para que sea visible
    t = AffineTransformation()
    t.add_scale(1.2, 0.5, 1.8)
    # Rotación de 30 grados alrededor del eje (1, 1, 0)
    t.add_rotation_axis([1.0, 1.0, 0.0], np.deg2rad(30.0))
    # Algo de cizallamiento
    t.add_shear(sh_xy=0.4, sh_zx=-0.3)
    # Y una traslación
    t.add_translation(2.0, -1.0, 3.0)

    pts_transformed = t.transform_points(pts)

    fig = plt.figure(figsize=(10, 5))

    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.scatter(pts[:, 0], pts[:, 1], pts[:, 2], s=10)
    ax1.set_title("Puntos originales")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_zlabel("Z")

    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.scatter(pts_transformed[:, 0], pts_transformed[:, 1], pts_transformed[:, 2], s=10)
    ax2.set_title("Puntos transformados")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.set_zlabel("Z")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_numeric_tests()
    visualize_random_points()
