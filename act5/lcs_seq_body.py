#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LCS con DP completa y reconstrucción, eliminando el boilerplate de Gutenberg.
- Detecta los dos primeros .txt en ./books
- Recorta a 'limit' chars
- Aplica strip de encabezado/pie con marcadores comunes
- Construye tabla (n+1)x(m+1) con array('H')
- Backtracking para recuperar UNA subsecuencia óptima
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

def strip_gutenberg_boilerplate(text: str) -> tuple[str, dict]:
    upper = text.upper()
    starts = [
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "***START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THE PROJECT GUTENBERG EBOOK:",
        "*** START OF THE PROJECT GUTENBERG",
    ]
    ends = [
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "***END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THE PROJECT GUTENBERG",
    ]
    lo = None
    for s in starts:
        k = upper.find(s)
        if k != -1:
            nl = text.find("\n", k)
            lo = (nl + 1) if nl != -1 else (k + len(s))
            break
    hi = None
    for e in ends:
        k = upper.find(e)
        if k != -1:
            prev_nl = text.rfind("\n", 0, k)
            hi = prev_nl if prev_nl != -1 else k
            break
    used_markers = (lo is not None) or (hi is not None)
    n = len(text)
    if lo is None:
        lo = 0
    if hi is None:
        hi = n

    used_heuristic = False
    if not used_markers:
        first_pg = upper.find("PROJECT GUTENBERG")
        if 0 <= first_pg <= 5000:
            blk_end = text.find("\n\n", first_pg)
            if blk_end != -1 and blk_end < n * 0.2:
                lo = blk_end + 2
                used_heuristic = True
        last_pg = upper.rfind("PROJECT GUTENBERG")
        if last_pg != -1 and last_pg >= n - 5000:
            prev_nl = text.rfind("\n", 0, last_pg)
            if prev_nl != -1 and prev_nl > lo:
                hi = prev_nl

    body = text[lo:hi].strip()
    if not body:
        body = text
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

def visualize_one_line(sample: str, head: int = 150, tail: int = 150) -> str:
    s = sample.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "⏎")
    if len(s) <= head + tail:
        return s
    return s[:head] + " … " + s[-tail:]

def lcs_full_dp(s1: str, s2: str):
    n, m = len(s1), len(s2)
    dp = [array('H', [0]) * (m + 1)]
    for i in range(1, n + 1):
        ai = s1[i - 1]
        prev = dp[i - 1]
        cur = array('H', [0]) * (m + 1)
        for j in range(1, m + 1):
            bj = s2[j - 1]
            if ai == bj:
                cur[j] = prev[j - 1] + 1
            else:
                up = prev[j]
                left = cur[j - 1]
                cur[j] = up if up >= left else left
        dp.append(cur)
    return dp, n, m

def lcs_backtrack(dp, s1: str, s2: str) -> str:
    i, j = len(s1), len(s2)
    out = []
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            out.append(s1[i - 1]); i -= 1; j -= 1
        else:
            if dp[i - 1][j] >= dp[i][j - 1]:
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
    print("=== LCS sobre el CUERPO del libro (boilerplate removido) ===")
    print(f"Archivo 1: {b1}")
    print(f"Archivo 2: {b2}")
    print(f"Límite por archivo: {limit} caracteres\n")

    t0 = time.time()
    raw1 = load_text(b1, limit)
    raw2 = load_text(b2, limit)
    body1, info1 = strip_gutenberg_boilerplate(raw1)
    body2, info2 = strip_gutenberg_boilerplate(raw2)
    load_t = time.time() - t0

    print(">>> Resumen de limpieza")
    print(f"S1 original: {info1['original_len']:,} -> cuerpo: {info1['body_len']:,} "
          f"(markers={info1['used_markers']}, heuristic={info1['used_heuristic']})")
    print(f"S2 original: {info2['original_len']:,} -> cuerpo: {info2['body_len']:,} "
          f"(markers={info2['used_markers']}, heuristic={info2['used_heuristic']})\n")

    n, m = len(body1), len(body2)
    approx_mem = (n + 1) * (m + 1) * 2
    print(f"Tamaño procesado tras strip: |S1| = {n:,}  |S2| = {m:,}")
    print(f"Memoria aprox. para DP: {human_bytes(approx_mem)}\n")

    t1 = time.time()
    dp, _, _ = lcs_full_dp(body1, body2)
    dp_build_t = time.time() - t1

    t2 = time.time()
    lcs_str = lcs_backtrack(dp, body1, body2)
    back_t = time.time() - t2

    print(">>> RESULTADOS (sobre el cuerpo, sin boilerplate)")
    print(f"Longitud de la LCS: {len(lcs_str):,}")
    print(f"LCS (vista abreviada): {visualize_one_line(lcs_str)}\n")

    print(">>> Tiempos")
    print(f"Carga/strip: {load_t:.3f} s")
    print(f"DP (tabla):  {dp_build_t:.3f} s")
    print(f"Backtrack:   {back_t:.3f} s")

if __name__ == "__main__":
    main()
