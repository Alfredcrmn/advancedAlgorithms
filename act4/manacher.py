# manacher.py
# Implementación fiel a las láminas del algoritmo de Manacher.
# Retorna el palíndromo más largo y metadatos útiles.

from typing import Tuple

def _build_T(S: str) -> str:
    # Agrega '^' al inicio, '$' al final y '|' entre caracteres
    # Nota: No insertamos '|' al inicio para mantener índices como en las láminas
    return "^" + "|".join(S) + "|$"

def manacher_longest_palindrome(S: str) -> Tuple[str, int, int]:
    """
    Entrada:  S (string)
    Salida:   (palindromo_mas_largo, start_en_S, length)

    Implementación basada en las diapositivas:
      - Construye T con '^', '|', '$'
      - Arreglo L (radios)
      - Recorre i, calcula m = 2c - i, inicializa L[i]
        con min(r - i, L[m]) si i < r; si no, 0.
      - Expande mientras T[i + L[i] + 1] == T[i - L[i] - 1]
      - Si i + L[i] > r, actualiza c = i y r = i + L[i]
      - Al final, hallar imax = argmax L[i], lmax = L[imax]
        y start = (imax - lmax)//2, devolver S[start:start+lmax]
    """
    if not S:
        return "", 0, 0

    T = _build_T(S)
    N = len(T)
    L = [0] * N

    c = 0   # centro del palíndromo más a la derecha
    r = 0   # límite derecho

    for i in range(1, N - 1):
        m = 2 * c - i  # posición espejo

        # Inicializa L[i]
        if i < r:
            # ojo: r - i puede ser negativo; min lo maneja
            L[i] = min(r - i, L[m])
        else:
            L[i] = 0

        # Expande alrededor de i
        while i + L[i] + 1 < N and i - L[i] - 1 >= 0 and T[i + L[i] + 1] == T[i - L[i] - 1]:
            L[i] += 1

        # Actualiza centro si rebasamos el límite
        if i + L[i] > r:
            c = i
            r = i + L[i]

    # Encuentra máximo
    imax = max(range(1, N - 1), key=lambda k: L[k])
    lmax = L[imax]
    start = (imax - lmax) // 2  # división entera, como en las láminas

    return S[start:start + lmax], start, lmax
