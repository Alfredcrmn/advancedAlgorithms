# run_manacher_books.py
# Ejecuta Manacher sobre todos los .txt en ./books,
# limpia encabezados/pies de Gutenberg, filtra para palíndromos “reales”,
# mide tiempo y muestra resultados con palíndromo y contexto.

import re
import time
import unicodedata
from pathlib import Path
from typing import Tuple, List
from manacher import manacher_longest_palindrome

BOOKS_DIR = Path(__file__).parent / "books"

HEADER_RE = re.compile(r"\*\*\*\s*START OF.*?\*\*\*", re.IGNORECASE | re.DOTALL)
FOOTER_RE = re.compile(r"\*\*\*\s*END OF.*", re.IGNORECASE | re.DOTALL)


def strip_gutenberg_boilerplate(text: str) -> str:
    start_cut = HEADER_RE.search(text)
    if start_cut:
        text = text[start_cut.end():]
    end_cut = FOOTER_RE.search(text)
    if end_cut:
        text = text[:end_cut.start()]
    return text


def normalize_basic(text: str) -> str:
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strip_accents(s: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(ch)
    )


def build_filtered(text: str) -> Tuple[str, List[int]]:
    clean_chars = []
    map_idx = []
    t = strip_accents(text).lower()
    for i, ch in enumerate(t):
        if ch.isalnum():
            clean_chars.append(ch)
            map_idx.append(i)
    return "".join(clean_chars), map_idx


def analyze_book(path: Path, min_len: int = 7):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    base = strip_gutenberg_boilerplate(raw)
    base = normalize_basic(base)

    clean, map_idx = build_filtered(base)

    t0 = time.perf_counter()
    pal_clean, start_clean, length = manacher_longest_palindrome(clean)
    t1 = time.perf_counter()

    if length < min_len:
        print("=" * 80)
        print(f"Book: {path.name}")
        print(f"No se encontró palíndromo (limpio) con longitud >= {min_len}")
        print(f"Tiempo: {(t1 - t0)*1000:.2f} ms\n")
        return

    start_orig = map_idx[start_clean]
    end_orig = map_idx[start_clean + length - 1] + 1

    palindrome = base[start_orig:end_orig]
    left_ctx = max(0, start_orig - 60)
    right_ctx = min(len(base), end_orig + 60)
    context = base[left_ctx:start_orig] + "[" + palindrome + "]" + base[end_orig:right_ctx]

    print("=" * 80)
    print(f"Book: {path.name}")
    print(f"Length (clean): {len(clean):,} chars")
    print(f"Longest palindrome length (clean): {length:,}")
    print(f"Time: {(t1 - t0)*1000:.2f} ms")
    print(f"Start index (original): {start_orig:,}  |  End index (original): {end_orig:,}")
    print("Palindrome:")
    print(palindrome)
    print("Context  (≈120 chars and palindrome inside []):")
    print(context)
    print()


def main():
    txts = sorted(BOOKS_DIR.glob("*.txt"))
    if not txts:
        print("No se encontraron .txt en ./books")
        return
    for p in txts:
        analyze_book(p)


if __name__ == "__main__":
    main()
