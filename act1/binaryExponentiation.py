from math import pow

def binaryExp(a, b):
    if b == 0:
        return 1
    
    power = binaryExp(a,  b//2)
    result = power * power

    if b % 2 == 1:
        result *= a
    
    return result

print(binaryExp(8,10))

print(pow(8,10))