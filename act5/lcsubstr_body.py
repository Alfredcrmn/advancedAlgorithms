#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LCSubstr (DP completa) entre dos .txt detectados automáticamente en ./books,
eliminando el boilerplate de Project Gutenberg
"""

import os
import time
from array import array

def load_text(path: str, limit: int | None) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    if limit is not None and limit > 0:
        text = text[:limit]
    return text

def strip_gutenberg_boilerplate(text: str) -> tuple[str, dict]:
    """
    Intenta remover encabezado y pie típicos de Project Gutenberg.
    Devuelve (body, info) donde 'info' resume lo detectado para imprimir un reporte.

    Estrategia:
      - Buscar marcadores "*** START OF ..." y "*** END OF ..." (variantes comunes).
      - Si no aparecen, intenta heurísticas suaves: cortar bloques de licencia largos con "Project Gutenberg".
      - Si nada aplica, devuelve el texto original.
    """
    upper = text.upper()

    start_markers = [
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "***START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THE PROJECT GUTENBERG EBOOK:",
        "*** START OF THE PROJECT GUTENBERG",
    ]
    end_markers = [
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "***END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THE PROJECT GUTENBERG",
    ]

    lo = None
    for s in start_markers:
        k = upper.find(s)
        if k != -1:
            # Salta al final de línea donde está el marcador
            nl = text.find("\n", k)
            lo = (nl + 1) if nl != -1 else (k + len(s))
            break

    hi = None
    for e in end_markers:
        k = upper.find(e)
        if k != -1:
            # Corta desde el inicio de línea donde empieza el marcador
            prev_nl = text.rfind("\n", 0, k)
            hi = prev_nl if prev_nl != -1 else k
            break

    used_markers = (lo is not None) or (hi is not None)
    n = len(text)

    if lo is None:
        lo = 0
    if hi is None:
        hi = n

    # Heurística adicional: si no hubo marcadores pero hay un bloque de licencia largo al inicio
    # con "Project Gutenberg", intenta recortar hasta la primera línea en blanco tras ese bloque.
    used_heuristic = False
    if not used_markers:
        first_pg = upper.find("PROJECT GUTENBERG")
        if 0 <= first_pg <= 5000:  # típico: aparece muy al inicio
            # Busca un doble salto de línea (fin de bloque) después de esa mención
            blk_end = text.find("\n\n", first_pg)
            if blk_end != -1 and blk_end < n * 0.2:  # que no se coma demasiado
                lo = blk_end + 2
                used_heuristic = True

        # Pie: a veces hay notas de licencia largas al final
        last_pg = upper.rfind("PROJECT GUTENBERG")
        if last_pg != -1 and last_pg >= n - 5000:
            # Corta desde una línea antes de esa aparición
            prev_nl = text.rfind("\n", 0, last_pg)
            if prev_nl != -1 and prev_nl > lo:
                hi = prev_nl

    body = text[lo:hi].strip()
    if not body:
        body = text  # fallback seguro

    info = {
        "original_len": n,
        "body_len": len(body),
        "used_markers": used_markers,
        "used_heuristic": used_heuristic,
        "lo": lo,
        "hi": hi,
    }
    return body, info

def human_bytes(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    x = float(n)
    while x >= 1024 and i < len(units) - 1:
        x /= 1024.0
        i += 1
    return f"{x:.2f} {units[i]}"

def longest_common_substring(s1: str, s2: str) -> tuple[int, str, int, int]:
    """
    DP completa para LCSubstr.
    Retorna: (maxlen, substring, end_idx_s1, end_idx_s2) con índices sobre s1/s2 tras strip.
    """
    n, m = len(s1), len(s2)
    if n == 0 or m == 0:
        return 0, "", -1, -1

    lc: list[array] = [array("I", [0]) * m for _ in range(n)]
    maxlen = 0
    end_i = -1
    end_j = -1

    for i in range(n):
        si = s1[i]
        row = lc[i]
        if i == 0:
            for j in range(m):
                row[j] = 1 if si == s2[j] else 0
                if row[j] > maxlen:
                    maxlen = row[j]
                    end_i, end_j = i, j
        else:
            prev = lc[i - 1]
            for j in range(m):
                if si == s2[j]:
                    row[j] = prev[j - 1] + 1 if j > 0 else 1
                    if row[j] > maxlen:
                        maxlen = row[j]
                        end_i, end_j = i, j
                else:
                    row[j] = 0

    substr = s1[end_i - maxlen + 1 : end_i + 1] if maxlen > 0 else ""
    return maxlen, substr, end_i, end_j

def visualize_one_line(sample: str, max_chars: int = 200) -> str:
    """Representación amigable para captura: reemplaza saltos de línea por símbolos y recorta."""
    s = sample.replace("\r\n", "\n").replace("\r", "\n")
    s = s.replace("\n", "⏎")
    if len(s) > max_chars:
        s = s[:max_chars] + "…"
    return s

def main():
    books_dir = os.path.join(os.getcwd(), "books")
    limit = 50000  # igual que el script original, para comparar

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

    print("=== LCSubstr sobre el CUERPO del libro (boilerplate removido) ===")
    print(f"Archivo 1: {book1}")
    print(f"Archivo 2: {book2}")
    print(f"Límite por archivo: {limit} caracteres\n")

    t0 = time.time()
    raw1 = load_text(book1, limit)
    raw2 = load_text(book2, limit)

    body1, info1 = strip_gutenberg_boilerplate(raw1)
    body2, info2 = strip_gutenberg_boilerplate(raw2)
    load_time = time.time() - t0

    print(">>> Resumen de limpieza")
    print(f"S1 original: {info1['original_len']:,} chars  ->  cuerpo: {info1['body_len']:,} chars "
          f"(markers={info1['used_markers']}, heuristic={info1['used_heuristic']})")
    print(f"S2 original: {info2['original_len']:,} chars  ->  cuerpo: {info2['body_len']:,} chars "
          f"(markers={info2['used_markers']}, heuristic={info2['used_heuristic']})\n")

    n, m = len(body1), len(body2)
    approx_mem = n * m * 4
    print(f"Tamaño procesado tras strip: |S1| = {n:,}  |S2| = {m:,}")
    print(f"Memoria aprox. para DP: {human_bytes(approx_mem)}\n")

    t1 = time.time()
    maxlen, substr, end_i, end_j = longest_common_substring(body1, body2)
    dp_time = time.time() - t1

    if maxlen > 0:
        start_i = end_i - maxlen + 1
        start_j = end_j - maxlen + 1
    else:
        start_i = start_j = -1

    print(">>> RESULTADOS (sobre el cuerpo, sin boilerplate)")
    print(f"Longitud del substring común: {maxlen}")
    print(f"Substring común (vista 1 línea): {visualize_one_line(substr, 200)}")
    print(f"Posición en S1 (post-strip): inicio {start_i}, fin {end_i}")
    print(f"Posición en S2 (post-strip): inicio {start_j}, fin {end_j}\n")

    print(">>> Tiempos")
    print(f"Carga/strip: {load_time:.3f} s")
    print(f"DP (LCSubstr): {dp_time:.3f} s")

if __name__ == "__main__":
    main()
