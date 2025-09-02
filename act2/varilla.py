import math, time

precios = [1,5,8,9,10,17,17,20,24,30]

def precio_directo(l):
    if 1 <= l <= 10:
        return precios[l-1]
    return 0

def cortar_recursivo(n):
    if n == 0:
        return 0
    mejor = -math.inf
    mejor = max(mejor, precio_directo(n))
    for i in range(1, n):
        mejor = max(mejor, precio_directo(i) + cortar_recursivo(n - i))
    return mejor

def cortar_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n == 0:
        memo[0] = 0
        return 0
    mejor = precio_directo(n)
    for i in range(1, n):
        mejor = max(mejor, precio_directo(i) + cortar_memo(n - i, memo))
    memo[n] = mejor
    return mejor

def cortar_tabla(n):
    dp = [0] * (n + 1)
    for k in range(1, n + 1):
        mejor = precio_directo(k)
        for i in range(1, k):
            mejor = max(mejor, precio_directo(i) + dp[k - i])
        dp[k] = mejor
    return dp[n]

def medir(f, *args, rep=1):
    inicio = time.perf_counter()
    r = None
    for _ in range(rep):
        r = f(*args)
    fin = time.perf_counter()
    return r, (fin - inicio) / rep

pruebas = [0, 10, 15, 20, 25]

print("n | recursivo | memo | tabla")
for n in pruebas:
    val1, t1 = medir(cortar_recursivo, n)
    val2, t2 = medir(cortar_memo, n)
    val3, t3 = medir(cortar_tabla, n)
    print(f"{n} | {val1} ({t1:.5f}s) | {val2} ({t2:.5f}s) | {val3} ({t3:.5f}s)")
