import random, time

def mochila_bt_poda(valores, pesos, capacidad):
    n = len(valores)
    indices = list(range(n)) # Crea los índices
    razones = [valores[i]/pesos[i] for i in range(n)] # Calcula el valor - peso de cada objeto
    indices.sort(key=lambda i: razones[i], reverse=True) # Los ordena de mayor a menor
    valores = [valores[i] for i in indices]
    pesos = [pesos[i] for i in indices]

    mejor_valor = 0
    mejor_sel = []
    sel = []

    def calcular_cota(i, v, w):
        if w >= capacidad:
            return 0
        c = v
        cap_rest = capacidad - w
        while i < n and pesos[i] <= cap_rest:
            cap_rest -= pesos[i]
            c += valores[i]
            i += 1
        if i < n:
            c += valores[i] * cap_rest / pesos[i]
        return c

    def f(i, v, w):
        nonlocal mejor_valor, mejor_sel
        if w > capacidad: # Si supera la capacidad se detiene esta rama
            return
        if i == n:
            if v > mejor_valor: # Si el valor v supera el mejor encontrado, actualiza mejor solución
                mejor_valor = v
                mejor_sel = sel[:]
            return
        if calcular_cota(i, v, w) <= mejor_valor: # Si ni el mejor caso teórico puede superar mejor_valor, se termina aquí
            return
        sel.append(i)
        f(i+1, v + valores[i], w + pesos[i])
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
