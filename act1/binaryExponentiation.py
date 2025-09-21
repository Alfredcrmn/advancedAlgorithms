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

for i in range(20):
    a = random.randint(1, 10)
    b = random.randint(1, 20)
    custom = binaryExp(a, b)
    builtin = pow(a, b)
    
    print(f"Test {i+1}:\n"
          f"{a}^{b}\n"
          f"binaryExp={custom}\n"
          f"pow={builtin}\n"
          f"OK? {custom == builtin}\n")