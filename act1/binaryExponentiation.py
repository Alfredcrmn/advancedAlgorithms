import random
from math import pow

def binaryExp(a, b):
    if b == 0:
        return 1
    
    power = binaryExp(a, b // 2)
    result = power * power

    if b % 2 == 1:
        result *= a
    
    return result

# === Casos de prueba aleatorios ===
for i in range(10):  # Genera 10 casos
    a = random.randint(1, 10)
    b = random.randint(1, 20)
    custom = binaryExp(a, b)
    builtin = pow(a, b)  # mantiene float
    
    print(f"Test {i+1}:\n"
          f"{a}^{b}\n"
          f"binaryExp={custom:.3f}\n"
          f"pow={builtin:.3f}\n"
          f"OK? {round(custom,3) == round(builtin,3)}\n")