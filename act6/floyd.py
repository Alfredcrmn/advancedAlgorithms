import numpy as np

INF = 10**12 

def floyd_warshall_distance(adj_matrix):
    """
    Computes shortest-path distances between all pairs using Floyd–Warshall.
    Input:
      adj_matrix: square matrix (list of lists or np.array) where:
        - adj_matrix[i][i] == 0
        - adj_matrix[i][j] > 0 is the edge weight i->j
        - adj_matrix[i][j] == 0 means NO EDGE (except diagonal)
    Returns:
      dist: np.array with all-pairs shortest distances
    """
    A = np.array(adj_matrix, dtype=float)
    n = A.shape[0]

    for i in range(n):
        A[i, i] = 0.0

    for i in range(n):
        for j in range(n):
            if i != j and A[i, j] == 0:
                A[i, j] = INF

    for k in range(n):
        for i in range(n):
            Aik = A[i, k]
            if Aik == INF:
                continue
            for j in range(n):
                alt = Aik + A[k, j]
                if alt < A[i, j]:
                    A[i, j] = alt

    return A