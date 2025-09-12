import random, time

def mochila_dc(valores, pesos, capacidad):
    n = len(valores)
    def f(i, cap): # Sin objetos o peso disponible, el mejor valor es 0
        if i == 0 or cap == 0:
            return 0
        if pesos[i-1] > cap: # Si el peso del objeto actual no cabe, no se toma
            return f(i-1, cap)
        a = f(i-1, cap) # No tomar el objeto
        b = valores[i-1] + f(i-1, cap - pesos[i-1]) # Tomarlo y sumar su valor
        return a if a >= b else b # devuelve el máximo de las decisiones
    return f(n, capacidad)

def mochila_dp(valores, pesos, capacidad):
    n = len(valores)
    dp = [0]*(capacidad+1)
    for i in range(n): # Se extra el peso y valor de cada objeto
        p = pesos[i]
        v = valores[i]
        for cap in range(capacidad, p-1, -1): # Recorre las capacidades de mayor a menor
            s = dp[cap] # Valor si no se toma el objeto
            c = dp[cap-p] + v # Valor si se toma el objeto
            dp[cap] = c if c > s else s
    return dp[capacidad]

random.seed(123)
limite_dc = 40

for n in range(5, 101, 5):
    valores = [random.randint(1, 20) for _ in range(n)]
    pesos = [random.randint(1, 10) for _ in range(n)]
    capacidad = random.randint(10, 50)

    print("Objetos:", n)
    print("Valores:", valores)
    print("Pesos:", pesos)
    print("Capacidad:", capacidad)

    if n <= limite_dc:
        t0 = time.perf_counter()
        val_dc = mochila_dc(valores, pesos, capacidad)
        t1 = time.perf_counter()
        print("DC → valor:", val_dc, "tiempo_ms:", f"{(t1-t0)*1000:.3f}")
    else:
        val_dc = None
        print("DC → omitido por tamaño")

    t2 = time.perf_counter()
    val_dp = mochila_dp(valores, pesos, capacidad)
    t3 = time.perf_counter()
    print("DP → valor:", val_dp, "tiempo_ms:", f"{(t3-t2)*1000:.3f}")

    if val_dc is not None:
        print("Coinciden:", "sí" if val_dc == val_dp else "no")
    print()
