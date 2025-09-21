import random, time

def mochila_bt_poda(valores, pesos, capacidad):
    n = len(valores)
    indices = list(range(n))
    razones = [valores[i]/pesos[i] for i in range(n)]
    indices.sort(key=lambda i: razones[i], reverse=True)
    val = [valores[i] for i in indices]
    pes = [pesos[i] for i in indices]

    mejor_valor = 0
    mejor_sel = []
    sel = []

    def cota(i, v, w):
        if w >= capacidad:
            return v
        c = v
        cap = capacidad - w
        j = i
        while j < n and pes[j] <= cap:
            cap -= pes[j]
            c += val[j]
            j += 1
        if j < n:
            c += val[j] * cap / pes[j]
        return c

    def f(i, v, w):
        nonlocal mejor_valor, mejor_sel
        if w > capacidad:
            return
        if w == capacidad or i == n:
            if v > mejor_valor:
                mejor_valor = v
                mejor_sel = sel[:]
            return
        if cota(i, v, w) <= mejor_valor:
            return
        sel.append(i)
        f(i+1, v + val[i], w + pes[i])
        sel.pop()
        f(i+1, v, w)

    f(0, 0, 0)
    return mejor_valor, [indices[i] for i in mejor_sel]


random.seed(123)

for n in [10, 20, 50, 100, 150]: 
    valores = [random.randint(1, 20) for _ in range(n)]
    pesos = [random.randint(1, 10) for _ in range(n)]
    capacidad = random.randint(10, 50)

    t0 = time.perf_counter()
    val_bt, sel_bt = mochila_bt_poda(valores, pesos, capacidad)
    t1 = time.perf_counter()

    peso_total = sum(pesos[i] for i in sel_bt)

    print("Objetos:", n)
    print("Valores:", valores)
    print("Pesos:", pesos)
    print("Capacidad:", capacidad)
    print("BT → valor:", val_bt)
    print("  Selección:", sel_bt if sel_bt else "ninguno")
    print("  Peso total:", peso_total)
    print("  Tiempo:", f"{(t1-t0)*1000:.3f} ms")
    print()
