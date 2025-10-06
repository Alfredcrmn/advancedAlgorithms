#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Longest Common Substring (LCSubstr)
Detecta los dos primeros archivos .txt en la carpeta ./books/
y aplica la DP completa (n x m) sin optimización de memoria.
"""

import os
import time
from array import array

def load_text(path: str, limit: int | None) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    if limit is not None and limit > 0:
        return text[:limit]
    return text

def human_bytes(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    x = float(n)
    while x >= 1024 and i < len(units) - 1:
        x /= 1024.0
        i += 1
    return f"{x:.2f} {units[i]}"

def longest_common_substring(s1: str, s2: str) -> tuple[int, str, int, int]:
    """Devuelve (maxlen, substring, end_i, end_j)."""
    n, m = len(s1), len(s2)
    if n == 0 or m == 0:
        return 0, "", -1, -1

    lc: list[array] = [array("I", [0]) * m for _ in range(n)]
    maxlen = 0
    end_i = end_j = -1

    for i in range(n):
        si = s1[i]
        row = lc[i]
        if i == 0:
            for j in range(m):
                row[j] = 1 if si == s2[j] else 0
                if row[j] > maxlen:
                    maxlen, end_i, end_j = row[j], i, j
        else:
            prev = lc[i - 1]
            for j in range(m):
                if si == s2[j]:
                    row[j] = prev[j - 1] + 1 if j > 0 else 1
                    if row[j] > maxlen:
                        maxlen, end_i, end_j = row[j], i, j
                else:
                    row[j] = 0

    substr = s1[end_i - maxlen + 1 : end_i + 1] if maxlen > 0 else ""
    return maxlen, substr, end_i, end_j

def main():
    books_dir = os.path.join(os.getcwd(), "books")
    limit = 50000

    if not os.path.isdir(books_dir):
        print(f"No existe la carpeta 'books' en {os.getcwd()}")
        return

    txt_files = sorted(
        [os.path.join(books_dir, f) for f in os.listdir(books_dir) if f.lower().endswith(".txt")]
    )

    if len(txt_files) < 2:
        print("Debes tener al menos dos archivos .txt en la carpeta 'books/'.")
        return

    book1, book2 = txt_files[:2]

    print("=== Longest Common Substring (DP completa) ===")
    print(f"Archivo 1: {book1}")
    print(f"Archivo 2: {book2}")
    print(f"Límite por archivo: {limit} caracteres\n")

    t0 = time.time()
    s1 = load_text(book1, limit)
    s2 = load_text(book2, limit)
    load_time = time.time() - t0

    n, m = len(s1), len(s2)
    approx_mem = n * m * 4
    print(f"Tamaño procesado: |S1| = {n:,}  |S2| = {m:,}")
    print(f"Memoria aprox. para DP: {human_bytes(approx_mem)}\n")

    t1 = time.time()
    maxlen, substr, end_i, end_j = longest_common_substring(s1, s2)
    dp_time = time.time() - t1

    if maxlen > 0:
        start_i = end_i - maxlen + 1
        start_j = end_j - maxlen + 1
    else:
        start_i = start_j = -1

    print(">>> RESULTADOS")
    print(f"Longitud del substring común: {maxlen}")
    print(f"Substring común: {repr(substr)}")
    print(f"Posición en S1: inicio {start_i}, fin {end_i}")
    print(f"Posición en S2: inicio {start_j}, fin {end_j}\n")

    print(">>> Tiempos")
    print(f"Carga/recorte: {load_time:.3f} s")
    print(f"DP (LCSubstr): {dp_time:.3f} s")

if __name__ == "__main__":
    main()
