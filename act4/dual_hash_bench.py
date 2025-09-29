# dual_hash_bench.py
# Genera 200,000 cadenas (4-8, a-z), calcula:
#  - SHA-1 (implementación propia, sin hashlib)
#  - PRHF (polynomial rolling hash) como hash complementario
# Mide tiempos y cuenta colisiones individuales y conjuntas.

import random
import time
from typing import Iterable

# ---------- SHA-1 from scratch ----------
def _rol(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def sha1_bytes(msg: bytes) -> bytes:
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

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

# ---------- Polynomial Rolling Hash (PRHF) ----------
# Referencia: p cercano al tamaño del alfabeto; m grande para baja colisión:contentReference[oaicite:4]{index=4}
def prhf(s: str, p: int = 53, m: int = 1_000_000_007) -> int:
    # map a->1, b->2, ..., z->26 (asumimos 'a'-'z')
    h = 0
    pwr = 1
    for ch in s:
        code = (ord(ch) - ord('a') + 1)  # 1..26
        h = (h + code * pwr) % m
        pwr = (pwr * p) % m
    return h

# ---------- Random strings ----------
def generate_random_strings(n: int, characters: str = "abcdefghijklmnopqrstuvwxyz") -> list[str]:
    random.seed(42)  # reproducible (opcional)
    out = []
    for _ in range(n):
        length = random.randint(4, 8)
        s = "".join(random.choice(characters) for _ in range(length))
        out.append(s)
    return out

# ---------- Benchmarks ----------
def bench_single_hash(strings: Iterable[str], hfunc):
    start = time.perf_counter()
    seen = {}
    collisions = 0
    duplicates = 0
    total = 0
    for s in strings:
        total += 1
        h = hfunc(s)
        if h in seen:
            if seen[h] == s:
                duplicates += 1
            else:
                collisions += 1
        else:
            seen[h] = s
    elapsed = time.perf_counter() - start
    return elapsed, collisions, duplicates, len(seen), total

def bench_dual_hash(strings: Iterable[str], h1, h2):
    start = time.perf_counter()
    seen_pair = {}
    joint_collisions = 0
    duplicates = 0
    total = 0
    for s in strings:
        total += 1
        a = h1(s)
        b = h2(s)
        key = (a, b)
        if key in seen_pair:
            if seen_pair[key] == s:
                duplicates += 1
            else:
                joint_collisions += 1
        else:
            seen_pair[key] = s
    elapsed = time.perf_counter() - start
    return elapsed, joint_collisions, duplicates, len(seen_pair), total

if __name__ == "__main__":
    N = 200_000
    print(f"Generando {N} strings aleatorios (a-z, long 4-8)...")
    data = generate_random_strings(N)

    print("\n--- Hash individual ---")
    t_sha1, col_sha1, dup_sha1, distinct_sha1, total = bench_single_hash(data, sha1_hex)
    print(f"SHA-1 propio -> t={t_sha1:.3f}s  colisiones={col_sha1:,}  duplicados={dup_sha1:,}  distintos={distinct_sha1:,}")

    t_prhf, col_prhf, dup_prhf, distinct_prhf, _ = bench_single_hash(data, lambda s: prhf(s))
    print(f"PRHF(p=53,m=1e9+7) -> t={t_prhf:.3f}s  colisiones={col_prhf:,}  duplicados={dup_prhf:,}  distintos={distinct_prhf:,}")

    print("\n--- Hash conjunto (doble) ---")
    t_both, joint_col, joint_dup, joint_distinct, _ = bench_dual_hash(data, sha1_hex, lambda s: prhf(s))
    print(f"(SHA-1, PRHF) -> t={t_both:.3f}s  colisiones_conjuntas={joint_col:,}  duplicados={joint_dup:,}  distintos={joint_distinct:,}")
