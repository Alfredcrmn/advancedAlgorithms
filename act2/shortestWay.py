import random, math
import matplotlib.pyplot as plt

def distancia(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def longitud_trazo(puntos, orden):
    s = 0.0
    for k in range(len(orden)-1):
        s += distancia(puntos[orden[k]], puntos[orden[k+1]])
    return s

def min_trazo(puntos, iter_max=50000, semilla=42):
    random.seed(semilla)
    n = len(puntos)
    orden = list(range(n))
    L = longitud_trazo(puntos, orden)
    for _ in range(iter_max):
        i = random.randrange(n)
        j = random.randrange(n)
        if i == j:
            continue
        if i > j:
            i, j = j, i
        orden[i], orden[j] = orden[j], orden[i]
        L2 = longitud_trazo(puntos, orden)
        if L2 >= L:
            orden[i], orden[j] = orden[j], orden[i]
        else:
            L = L2
    return orden, L

def graficar(puntos, orden, titulo):
    xs = [puntos[i][0] for i in orden]
    ys = [puntos[i][1] for i in orden]
    plt.plot(xs, ys, marker='o')
    plt.title(titulo)
    plt.axis('equal')

puntos = [
    (20,20),(20,40),(20,160),(30,120),(40,140),(40,150),(50,20),
    (60,40),(60,80),(60,200),(70,200),(80,150),(90,170),(90,170),
    (100,50),(100,40),(100,130),(100,150),(110,10),(110,70),
    (120,80),(130,70),(130,170),(140,140),(140,180),(150,50),
    (160,20),(170,100),(180,70),(180,200),(200,30),(200,70),(200,100)
]

orden_inicial = list(range(len(puntos)))
L_ini = longitud_trazo(puntos, orden_inicial)
orden_final, L_fin = min_trazo(puntos, iter_max=80000, semilla=7)

plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
graficar(puntos, orden_inicial, f"Original: Inicial  L={L_ini:.1f}")
plt.subplot(1,2,2)
graficar(puntos, orden_final, f"Original: Greedy (2-swap)  L={L_fin:.1f}")
plt.tight_layout()
plt.show()

random.seed(123)
p50 = [(random.randint(0,300), random.randint(0,300)) for _ in range(50)]
orden_inicial2 = list(range(len(p50)))
L_ini2 = longitud_trazo(p50, orden_inicial2)
orden_final2, L_fin2 = min_trazo(p50, iter_max=120000, semilla=9)

plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
graficar(p50, orden_inicial2, f"Nuevos (50 pts): Inicial  L={L_ini2:.1f}")
plt.subplot(1,2,2)
graficar(p50, orden_final2, f"Nuevos (50 pts): Greedy (2-swap)  L={L_fin2:.1f}")
plt.tight_layout()
plt.show()
