from pathlib import Path
from typing import List, Tuple
import unicodedata
import sys

# Config
BOOK_PATH = Path(__file__).parent / "books" / "mobyDick.txt"
PATTERNS = [
    "whale", "ahab", "ishmael", "queequeg", "pequod",
    "harpoon", "mast", "voyage", "leviathan", "ocean"
]
WHOLE_WORDS_ONLY = True   # True: solo palabras completas, False: subcadenas
CTX_RADIUS = 35
MAX_CONTEXTS = 5
MAX_POS_PRINT = 10


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
             radius: int = 30, max_ctx: int = 5) -> List[Tuple[int, str]]:
    #Extrae ventanas de contexto alrededor de coincidencias
    out: List[Tuple[int, str]] = []
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


# longest prefix-suffix)
def kmp_lps(pattern: str) -> List[int]:
    m = len(pattern)
    lps = [0] * m
    j = 0  # longitud actual del prefijo-sufijo más largo
    i = 1
    while i < m:
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
            i += 1
        elif j > 0:
            j = lps[j - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


# KMP Search
def find_with_kmp(pattern: str, text: str) -> List[int]:

    if not pattern:
        return []

    lps = kmp_lps(pattern)
    m = len(pattern)
    n = len(text)
    matches: List[int] = []

    i = 0  # índice en text
    j = 0  # índice en pattern
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]          
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1

    return matches


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

    print("=== Búsqueda con KMP ===")
    print(f"Archivo: {BOOK_PATH}")
    print(f"Patrones ({len(PATTERNS)}): {PATTERNS}")
    print(f"Modo: {'palabras completas' if WHOLE_WORDS_ONLY else 'subcadenas'}\n")

    for pat in PATTERNS:
        p = normalize_lower_ascii(pat)
        pos = find_with_kmp(p, text)
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