from pathlib import Path
from typing import List
import unicodedata
import sys

# Config
BOOK_PATH = Path(__file__).parent / "books" / "mobyDick.txt"
PATTERNS = [
    "whale", "ahab", "ishmael", "queequeg", "pequod",
    "harpoon", "mast", "voyage", "leviathan", "ocean"
]
WHOLE_WORDS_ONLY = True   # True: solo palabras completas, False: subcadenas
CTX_RADIUS = 35           # caracteres alrededor de la coincidencia
MAX_CONTEXTS = 5          # cuántos contextos mostrar por patrón
MAX_POS_PRINT = 10        # cuántas posiciones mostrar en el resumen


# Utils
def normalize_lower_ascii(s: str) -> str:
    #Minúsculas y sin acentos para comparación consistente.
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")


def is_word_char(ch: str) -> bool:
    return ch.isalnum() or ch == "_"


def filter_whole_word_matches(text: str, m: int, matches: List[int]) -> List[int]:
    #Conserva matches delimitados por no-palabra
    out = []
    n = len(text)
    for p in matches:
        left_ok = (p == 0) or (not is_word_char(text[p - 1]))
        right_ok = (p + m == n) or (not is_word_char(text[p + m]))
        if left_ok and right_ok:
            out.append(p)
    return out


def contexts(text: str, pos_list: List[int], m: int,
             radius: int = 30, max_ctx: int = 5) -> List[tuple[int, str]]:
    #Extrae ventanas de contexto alrededor de coincidencias.
    out = []
    for p in pos_list[:max_ctx]:
        a = max(0, p - radius)
        b = min(len(text), p + m + radius)
        frag = text[a:b].replace("\n", " ")
        out.append((p, frag))
    return out


def pretty_positions(pos_list: List[int], max_to_show: int = 10) -> str:
    if not pos_list:
        return "[]"
    show = pos_list[:max_to_show]
    s = "[" + ", ".join(str(x) for x in show)
    if len(pos_list) > max_to_show:
        s += ", …"
    s += "]"
    return s


# Función Z - O(n)
def z_function(s: str) -> List[int]:

    n = len(s)
    z = [0] * n
    l = 0
    r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l = i
            r = i + z[i]
    return z


# Z-based search
def find_with_z(pattern: str, text: str) -> List[int]:
    if not pattern:
        return []
    s = pattern + text
    m = len(pattern)
    z = z_function(s)
    return [i - m for i in range(m, len(s)) if z[i] >= m]


# Main
def run() -> None:
    try:
        raw = BOOK_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo: {BOOK_PATH}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error leyendo {BOOK_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

    text = normalize_lower_ascii(raw)

    print("=== Búsqueda con Función Z ===")
    print(f"Archivo: {BOOK_PATH}")
    print(f"Patrones ({len(PATTERNS)}): {PATTERNS}")
    print(f"Modo: {'palabras completas' if WHOLE_WORDS_ONLY else 'subcadenas'}\n")

    for pat in PATTERNS:
        p = normalize_lower_ascii(pat)
        pos = find_with_z(p, text)
        if WHOLE_WORDS_ONLY:
            pos = filter_whole_word_matches(text, len(p), pos)

        print(f"Patrón: '{pat}'  |  largo={len(p)}")
        print(f"Total de ocurrencias: {len(pos)}")
        print(f"Primeras posiciones: {pretty_positions(pos, MAX_POS_PRINT)}")

        for p0, frag in contexts(text, pos, len(p), radius=CTX_RADIUS, max_ctx=MAX_CONTEXTS):
            print(f"  - pos={p0}: …{frag}…")
        print("-" * 72)


if __name__ == "__main__":
    run()