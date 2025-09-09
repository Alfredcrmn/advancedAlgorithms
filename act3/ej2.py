import random, time

def mochila_bt(valores, pesos, capacidad):
    n = len(valores)
    mejor_valor = 0
    mejor_sel = []
    sel = []
    def f(i, v, w):
        nonlocal mejor_valor, mejor_sel
        if w > capacidad:
            return
        if i == n:
            if v > mejor_valor:
                mejor_valor = v
                mejor_sel = sel[:]
            return
        sel.append(i)
        f(i+1, v + valores[i], w + pesos[i])
        sel.pop()
        f(i+1, v, w)
    f(0, 0, 0)
    return mejor_valor, mejor_sel

random.seed(123)

for n in range(5, 51, 8):
    valores = [random.randint(1, 20) for _ in range(n)]
    pesos = [random.randint(1, 10) for _ in range(n)]
    capacidad = random.randint(10, 50)

    t0 = time.perf_counter()
    val_bt, sel_bt = mochila_bt(valores, pesos, capacidad)
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
