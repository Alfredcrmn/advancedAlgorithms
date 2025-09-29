# sha1_from_scratch_demo.py
# Implementación pura de SHA-1 (FIPS 180-4) + demo visual en consola
# No usa hashlib.

from typing import Iterable

# ----------------- SHA-1 puro -----------------

def _rol(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def sha1_bytes(msg: bytes) -> bytes:
    # Constantes iniciales (h0..h4)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Preprocesamiento: padding
    ml = len(msg) * 8  # longitud en bits
    msg += b"\x80"
    # Relleno con ceros hasta que len ≡ 56 (mod 64)
    while (len(msg) % 64) != 56:
        msg += b"\x00"
    # Añadir longitud original (64 bits big-endian)
    msg += ml.to_bytes(8, "big")

    # Procesar en bloques de 512 bits (64 bytes)
    for chunk_start in range(0, len(msg), 64):
        chunk = msg[chunk_start:chunk_start + 64]
        # Romper en 16 palabras de 32 bits big-endian
        w = [int.from_bytes(chunk[i:i+4], "big") for i in range(0, 64, 4)]
        # Extender a 80 palabras
        for t in range(16, 80):
            w.append(_rol(w[t-3] ^ w[t-8] ^ w[t-14] ^ w[t-16], 1))

        a, b, c, d, e = h0, h1, h2, h3, h4

        for t in range(80):
            if 0 <= t <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= t <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= t <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:  # 60..79
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (_rol(a, 5) + f + e + k + w[t]) & 0xFFFFFFFF
            e = d
            d = c
            c = _rol(b, 30)
            b = a
            a = temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    return b"".join(h.to_bytes(4, "big") for h in (h0, h1, h2, h3, h4))

def sha1_hex(s: str) -> str:
    return sha1_bytes(s.encode("utf-8")).hex()

# ----------------- Utilidades demo -----------------

def hamming_bits(a: bytes, b: bytes) -> int:
    n = min(len(a), len(b))
    diff = 0
    for i in range(n):
        diff += (a[i] ^ b[i]).bit_count()
    if len(a) != len(b):
        rest = a[n:] + b[n:]
        diff += sum(x.bit_count() for x in rest)
    return diff

def bar(percent: float, width: int = 40) -> str:
    fill = int(percent * width + 0.5)
    return "[" + "#" * fill + "-" * (width - fill) + "]"

def print_table(rows: Iterable[tuple[str, str]]):
    print(f"{'Cadena':<28} {'SHA-1 (hex)':<40}")
    print("-" * 70)
    for s, h in rows:
        print(f"{s:<28} {h:<40}")

# ----------------- Pruebas de corrección -----------------

def selftest():
    # Vectores conocidos
    vectors = [
        ("", "da39a3ee5e6b4b0d3255bfef95601890afd80709"),
        ("abc", "a9993e364706816aba3e25717850c26c9cd0d89d"),
        ("The quick brown fox jumps over the lazy dog",
         "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12"),
        ("The quick brown fox jumps over the lazy dog.",
         "408d94384216f890ff7a0c3528e8bed1e0b01621"),
    ]
    for s, expected in vectors:
        got = sha1_hex(s)
        assert got == expected, f"Fallo en vector: {s!r}\nEsperado: {expected}\nObt:      {got}"
    print("Self-test OK (vectores conocidos).")

# ----------------- Demo visual -----------------

def demo():
    # 1) Tabla de ejemplos (sensibilidad a espacios/mayúsculas)
    ejemplos = [
        "hola",
        "Hola",
        "hola ",
        "hola  ",
        "hola_mundo",
        "hola-mundo",
        "bananana",
        "ana",
        "ana ",
    ]
    print("\nTabla de hashes SHA-1 (implementación propia)")
    print_table((s, sha1_hex(s)) for s in ejemplos)

    # 2) Efecto avalancha: cambiar 1 carácter
    base, mut = "bananana", "bananaoa"   # cambia una letra
    h1, h2 = sha1_bytes(base.encode()), sha1_bytes(mut.encode())
    bits_total = 160
    bits_diff = hamming_bits(h1, h2)
    pct = bits_diff / bits_total

    print("\nEfecto avalancha (1 cambio ⇒ muchos bits distintos)")
    print(f"A: {base!r}\n  SHA1(A): {h1.hex()}")
    print(f"B: {mut!r}\n  SHA1(B): {h2.hex()}")
    print(f"Bits distintos: {bits_diff}/{bits_total}  {bar(pct)}  {pct*100:.1f}%")

    # 3) Comparar cadenas muy parecidas
    pares = [
        ("password", "password1"),
        ("The quick brown fox", "The quick brown fix"),
        ("abc", "abd"),
    ]
    print("\nComparación de pares parecidos")
    for a, b in pares:
        ha, hb = sha1_bytes(a.encode()), sha1_bytes(b.encode())
        diff = hamming_bits(ha, hb)
        p = diff / bits_total
        print(f"- {a!r}  vs  {b!r}")
        print(f"  {ha.hex()}  vs  {hb.hex()}")
        print(f"  Bits distintos: {diff}/{bits_total}  {bar(p)}  {p*100:.1f}%")

if __name__ == "__main__":
    selftest()
    demo()
