#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Longest Common Subsequence (LCS) con DP completa y reconstrucción.
- Detecta los dos primeros .txt en ./books (orden alfabético).
- Recorta cada archivo a 'limit' chars (default: 50_000).
- Construye la tabla completa (n+1) x (m+1) con array('H') para ahorrar memoria.
- Luego hace backtracking para reconstruir UNA subsecuencia óptima.
"""

import os
import time
from array import array

def load_text(path: str, limit: int | None) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        t = f.read()
    if limit and limit > 0:
        t = t[:limit]
    return t

def human_bytes(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    x = float(n)
    while x >= 1024 and i < len(units) - 1:
        x /= 1024.0
        i += 1
    return f"{x:.2f} {units[i]}"

def visualize_one_line(sample: str, head: int = 150, tail: int = 150) -> str:
    """Vista abreviada: primeros 'head' y últimos 'tail' chars, con ⏎ en lugar de saltos."""
    s = sample.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "⏎")
    if len(s) <= head + tail:
        return s
    return s[:head] + " … " + s[-tail:]

def lcs_full_dp(s1: str, s2: str):
    """
    Construye tabla DP de LCS con array('H') (0..65535).
    dp[i][j] = longitud de LCS de s1[:i] y s2[:j]
    Retorna (dp, n, m)
    """
    n, m = len(s1), len(s2)
    # Fila 0: todo 0
    dp = [array('H', [0]) * (m + 1)]
    # Construcción fila por fila
    for i in range(1, n + 1):
        ai = s1[i - 1]
        prev = dp[i - 1]
        cur = array('H', [0]) * (m + 1)
        cij = 0  # referencia local para micro-opt
        for j in range(1, m + 1):
            bj = s2[j - 1]
            if ai == bj:
                cij = prev[j - 1] + 1
                cur[j] = cij
            else:
                # max(up, left)
                up = prev[j]
                left = cur[j - 1]
                cur[j] = up if up >= left else left
        dp.append(cur)
    return dp, n, m

def lcs_backtrack(dp, s1: str, s2: str) -> str:
    """Reconstruye UNA LCS a partir de la tabla completa."""
    i, j = len(s1), len(s2)
    out = []
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            out.append(s1[i - 1])
            i -= 1
            j -= 1
        else:
            up = dp[i - 1][j]
            left = dp[i][j - 1]
            if up >= left:
                i -= 1
            else:
                j -= 1
    out.reverse()
    return "".join(out)

def main():
    books_dir = os.path.join(os.getcwd(), "books")
    limit = 50_000

    if not os.path.isdir(books_dir):
        print(f"No existe la carpeta 'books' en {os.getcwd()}")
        return

    txt = sorted([os.path.join(books_dir, f) for f in os.listdir(books_dir)
                  if f.lower().endswith(".txt")])
    if len(txt) < 2:
        print("Debes tener al menos dos archivos .txt en 'books/'.")
        return

    b1, b2 = txt[:2]
    print("=== Longest Common Subsequence (DP completa) ===")
    print(f"Archivo 1: {b1}")
    print(f"Archivo 2: {b2}")
    print(f"Límite por archivo: {limit} caracteres\n")

    t0 = time.time()
    s1 = load_text(b1, limit)
    s2 = load_text(b2, limit)
    load_t = time.time() - t0

    n, m = len(s1), len(s2)
    approx_mem = (n + 1) * (m + 1) * 2  # 'H' = 2 bytes
    print(f"Tamaño procesado: |S1| = {n:,}  |S2| = {m:,}")
    print(f"Memoria aprox. para DP: {human_bytes(approx_mem)}\n")

    t1 = time.time()
    dp, _, _ = lcs_full_dp(s1, s2)
    dp_build_t = time.time() - t1

    t2 = time.time()
    lcs_str = lcs_backtrack(dp, s1, s2)
    back_t = time.time() - t2

    print(">>> RESULTADOS")
    print(f"Longitud de la LCS: {len(lcs_str):,}")
    print(f"LCS (vista abreviada): {visualize_one_line(lcs_str)}\n")

    print(">>> Tiempos")
    print(f"Carga:      {load_t:.3f} s")
    print(f"DP (tabla): {dp_build_t:.3f} s")
    print(f"Backtrack:  {back_t:.3f} s")

if __name__ == "__main__":
    main()
