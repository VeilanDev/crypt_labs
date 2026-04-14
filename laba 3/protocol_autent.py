import random as r

p = int(input("\n\nВведите простое число\np : "))
g = r.randint(-10000, p - 1)
print("g : ", g)

a = r.randint(1, p - 1)
b = r.randint(1, p - 1)
print("\na : ", a, "\nb : ", b)

B = (g**a) % p
kb = (g**a)**b % p
