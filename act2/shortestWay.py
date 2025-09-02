import matplotlib.pyplot as plt
import numpy as np
import random



num_points = 50
points = [(random.randint(0, 200), random.randint(0, 200)) for _ in range(num_points)]
print("Lista de 50 puntos aleatorios:")
print(points)


def distance(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) # Fórmula de Pitágoras entre p1 y p2

def nearest_neighbor(points):
    # Inicialización
    unvisited = points.copy()  # Copia de todos los puntos, inicialmente todos sin visitar
    path = []  # Lista donde se guardará el recorrido
    total_distance = 0  # Acumulador de la distancia recorrida
    current_point = unvisited.pop(0)  # Se inicia desde el primer punto de la lista
    path.append(current_point)  # Se agrega el primer punto al recorrido

    # Mientras queden puntos sin visitar
    while unvisited:
        # Buscar el punto más cercano al actual
        nearest_point = min(unvisited, key=lambda p: distance(current_point, p))
        unvisited.remove(nearest_point)  # Eliminarlo de la lista de no visitados
        path.append(nearest_point)  # Agregarlo al recorrido
        total_distance += distance(current_point, nearest_point)  # Sumar la distancia recorrida
        current_point = nearest_point  # Actualizar el punto actual

    # Regresar al punto inicial para cerrar el ciclo
    total_distance += distance(current_point, path[0])

    return path, total_distance # Regresa el recorrido completo y la distancia total

path, total_distance = nearest_neighbor(points)

# Graficar un recorrido
def plot_path(path, title):
    x, y = zip(*path)  # Separar coordenadas X y Y
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b')  # Dibujar el trazo entre puntos
    plt.scatter(x, y, color='r')
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

plot_path(path, "Recorrido Inicial (Algoritmo Avaro)")

print(f"Distancia total recorrida: {total_distance}")