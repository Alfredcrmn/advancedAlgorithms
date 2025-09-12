import random, time, heapq

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

random.seed(123)

for n in [10, 20, 50, 100, 150]:
    valores = [random.randint(1, 20) for _ in range(n)]
    pesos = [random.randint(1, 10) for _ in range(n)]
    capacidad = random.randint(10, 60)

    t0 = time.perf_counter()
    val, sel = mochila_bnb(valores, pesos, capacidad)
    t1 = time.perf_counter()

    peso_total = sum(pesos[i] for i in sel)

    print("Objetos:", n)
    print("Valores:", valores)
    print("Pesos:", pesos)
    print("Capacidad:", capacidad)
    print("B&B → valor:", val)
    print("  Selección:", sel if sel else "ninguno")
    print("  Peso total:", peso_total)
    print("  Tiempo:", f"{(t1-t0)*1000:.3f} ms")
    print()
