import time, heapq

def mochila_dc(valores, pesos, capacidad):
    n = len(valores)
    def f(i, cap):
        if i == 0 or cap == 0:
            return 0
        if pesos[i-1] > cap:
            return f(i-1, cap)
        a = f(i-1, cap)
        b = valores[i-1] + f(i-1, cap - pesos[i-1])
        return a if a >= b else b
    return f(n, capacidad)

def mochila_dp(valores, pesos, capacidad):
    n = len(valores)
    dp = [0]*(capacidad+1)
    for i in range(n):
        p = pesos[i]
        v = valores[i]
        for cap in range(capacidad, p-1, -1):
            s = dp[cap]
            c = dp[cap-p] + v
            dp[cap] = c if c > s else s
    return dp[capacidad]

def mochila_bt(valores, pesos, capacidad):
    n = len(valores)
    mejor_valor = 0
    mejor_sel = []
    sel = []
    def f(i, v, w):
        nonlocal mejor_valor, mejor_sel
        if w > capacidad: # Si el peso acumulado excede la capacidad, se detiene y la rama no es válida
            return
        if i == n:
            if v > mejor_valor:
                mejor_valor = v # Se compara el valor acumulado con el mejor encontrado hasta ahora
                mejor_sel = sel[:]
            return # Se termina la rama
        sel.append(i)
        f(i+1, v + valores[i], w + pesos[i]) # Se añade el valor y el peso de i
        sel.pop()
        f(i+1, v, w) # No se añade valor ni peso
    f(0, 0, 0)
    return mejor_valor, mejor_sel

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


def cota_superior(valores, pesos, capacidad, indice, valor_actual, peso_actual):
    if peso_actual >= capacidad:
        return valor_actual # Si ya o queda capacidad, lo mejor es el valor actual

    n = len(valores) 
    valor_estimado = valor_actual
    capacidad_restante = capacidad - peso_actual
    j = indice

    while j < n and pesos[j] <= capacidad_restante: # Agrega objetos a la mochila siempre y cuando quepan
        capacidad_restante -= pesos[j]
        valor_estimado += valores[j]
        j += 1

    if j < n: # Si aún hay espacio y quedan objetos, añade una fracción del siguiente objeto
        valor_estimado += valores[j] * capacidad_restante / pesos[j]

    return valor_estimado


def mochila_bnb(valores, pesos, capacidad):
    n = len(valores)
    orden = sorted(range(n), key=lambda i: valores[i]/pesos[i], reverse=True) # Ordena índices por densidad valor - peso descendiente
    val_ = [valores[i] for i in orden]
    pes_ = [pesos[i] for i in orden]

    mejor_valor = 0
    mejor_camino = []
    frontera = []
    bound0 = cota_superior(val_, pes_, capacidad, 0, 0, 0) # Calcula la cota desde el estado inicial
    heapq.heappush(frontera, (-bound0, 0, 0, 0, [])) # Heap de mínimos, por lo que se pushea -bound para simular máximos

    while frontera: # Extrae el nodo con mejor bound
        neg_bound, valor, peso, idx, camino = heapq.heappop(frontera)
        bound = -neg_bound
        if bound <= mejor_valor: # Si la mejor promesa de este nodo no supera lo ya logrado, se descarta
            continue
        if idx == n:
            if valor > mejor_valor: # Si el valor es mejor que el actual, actualiza la solución
                mejor_valor = valor
                mejor_camino = camino
            continue
        if peso + pes_[idx] <= capacidad: # Solo se incluye si no se rebasa la capacidad
            v2 = valor + val_[idx] 
            w2 = peso + pes_[idx] # Se cambian los valores si se toman los objetos
            if v2 > mejor_valor:
                mejor_valor = v2
                mejor_camino = camino + [idx]
            b2 = cota_superior(val_, pes_, capacidad, idx+1, v2, w2)
            if b2 > mejor_valor:
                heapq.heappush(frontera, (-b2, v2, w2, idx+1, camino + [idx]))
        b3 = cota_superior(val_, pes_, capacidad, idx+1, valor, peso)
        if b3 > mejor_valor: # Si la cota puede ser mejor, se agrega, sino, poda
            heapq.heappush(frontera, (-b3, valor, peso, idx+1, camino))

    return mejor_valor, [orden[i] for i in mejor_camino]



valores = [30, 37, 44, 51, 58, 65, 72, 79, 86, 93, 100, 107, 114, 121, 128, 135, 142, 149, 36, 43, 50, 57, 64, 71, 78, 85, 92, 99, 106, 113]
pesos   = [5, 10, 15, 20, 25, 30, 35, 5, 10, 15, 20, 25, 30, 35, 5, 10, 15, 20, 25, 30, 35, 5, 10, 15, 20, 25, 30, 35, 5, 10]
capacidad = 60

print("=== Prueba fija ===")
print("Capacidad:", capacidad)

t0 = time.perf_counter()
val_dc = mochila_dc(valores, pesos, capacidad)
t1 = time.perf_counter()
print("DC → valor:", val_dc, "tiempo_ms:", f"{(t1-t0)*1000:.3f}")

t2 = time.perf_counter()
val_dp = mochila_dp(valores, pesos, capacidad)
t3 = time.perf_counter()
print("DP → valor:", val_dp, "tiempo_ms:", f"{(t3-t2)*1000:.3f}")
print("Coinciden DC/DP:", "sí" if val_dc == val_dp else "no")

t4 = time.perf_counter()
val_bt, sel_bt = mochila_bt(valores, pesos, capacidad)
t5 = time.perf_counter()
peso_bt = sum(pesos[i] for i in sel_bt)
print("BT sin poda → valor:", val_bt, "tiempo_ms:", f"{(t5-t4)*1000:.3f}")
print("  selección:", sel_bt if sel_bt else "ninguno")
print("  peso total:", peso_bt)
print("Coinciden BT/DP:", "sí" if val_bt == val_dp else "no")

t6 = time.perf_counter()
val_btp, sel_btp = mochila_bt_poda(valores, pesos, capacidad)
t7 = time.perf_counter()
peso_btp = sum(pesos[i] for i in sel_btp)
print("BT con poda → valor:", val_btp, "tiempo_ms:", f"{(t7-t6)*1000:.3f}")
print("  selección:", sel_btp if sel_btp else "ninguno")
print("  peso total:", peso_btp)
print("Coinciden BT+poda/DP:", "sí" if val_btp == val_dp else "no")

t8 = time.perf_counter()
val_bnb, sel_bnb = mochila_bnb(valores, pesos, capacidad)
t9 = time.perf_counter()
peso_bnb = sum(pesos[i] for i in sel_bnb)
print("B&B → valor:", val_bnb, "tiempo_ms:", f"{(t9-t8)*1000:.3f}")
print("  selección:", sel_bnb if sel_bnb else "ninguno")
print("  peso total:", peso_bnb)
print("Coinciden B&B/DP:", "sí" if val_bnb == val_dp else "no")
print()
