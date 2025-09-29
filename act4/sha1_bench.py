# sha1_bench.py
# Benchmark de SHA-1 "from scratch" con 200,000 strings aleatorios (4-8, a-z,0-9)
# - Tiempo total de hashing
# - Número de colisiones (hash iguales con strings distintos)

import random
import time
from typing import Iterable

# ----------------- SHA-1 (implementación propia, sin hashlib) -----------------

def _rol(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def sha1_bytes(msg: bytes) -> bytes:
    h0, h1, h2, h3, h4 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0

    ml = len(msg) * 8
    msg += b"\x80"
    while (len(msg) % 64) != 56:
        msg += b"\x00"
    msg += ml.to_bytes(8, "big")

    for off in range(0, len(msg), 64):
        chunk = msg[off:off+64]
        w = [int.from_bytes(chunk[i:i+4], "big") for i in range(0, 64, 4)]
        for t in range(16, 80):
            w.append(_rol(w[t-3] ^ w[t-8] ^ w[t-14] ^ w[t-16], 1))

        a, b, c, d, e = h0, h1, h2, h3, h4

        for t in range(80):
            if t <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif t <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif t <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (_rol(a, 5) + f + e + k + w[t]) & 0xFFFFFFFF
            e, d, c, b, a = d, c, _rol(b, 30), a, temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    return b"".join(h.to_bytes(4, "big") for h in (h0, h1, h2, h3, h4))

def sha1_hex(s: str) -> str:
    return sha1_bytes(s.encode("utf-8")).hex()

# ----------------- Generación de strings aleatorios únicos -----------------

def generate_unique_strings(n: int, characters: str = "abcdefghijklmnopqrstuvwxyz0123456789") -> list[str]:
    """
    Genera n cadenas únicas de longitud entre 4 y 8, usando 'characters'.
    """
    seen = set()
    out = []
    random.seed(42)
    while len(out) < n:
        length = random.randint(4, 8)
        s = "".join(random.choice(characters) for _ in range(length))
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

# ----------------- Benchmark -----------------

def benchmark_sha1(strings: Iterable[str]):
    start = time.perf_counter()

    seen_hash_to_str: dict[str, str] = {}
    collisions = 0
    total = 0

    for s in strings:
        total += 1
        h = sha1_hex(s)

        if h in seen_hash_to_str:
            if seen_hash_to_str[h] != s:
                # hash igual pero string diferente -> colisión
                collisions += 1
        else:
            seen_hash_to_str[h] = s

    elapsed = time.perf_counter() - start
    distinct = len(seen_hash_to_str)
    return elapsed, collisions, distinct, total

# ----------------- Main -----------------

if __name__ == "__main__":
    N = 200_000
    print(f"Generando {N} strings aleatorios únicos (a-z0-9, long 4-8)...")
    st = generate_unique_strings(N)

    print("Ejecutando benchmark SHA-1 (implementación propia)...")
    t, col, distinct, total = benchmark_sha1(st)

    print("\n===== Resultados =====")
    print(f"Total de strings:        {total:,}")
    print(f"Strings distintos:       {distinct:,}")
    print(f"Colisiones SHA-1:        {col:,}")
    print(f"Tiempo total hashing:    {t:.3f} s")
    print(f"Throughput aproximado:   {total / t:,.0f} hashes/seg")
