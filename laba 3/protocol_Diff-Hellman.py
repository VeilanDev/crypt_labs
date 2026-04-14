import random as r

p = int(input("\n\nВведите простое число\np : "))
g = r.randint(1, p - 1)
print("g : ", g)

a = r.randint(1, p - 1)
b = r.randint(1, p - 1)
print("\na : ", a, "\nb : ", b)

B = (g**a) % p
A = (g**b) % p
print("\nA->B : ", B, "\nB->A : ", A)

ka = (g**b)**a % p
kb = (g**a)**b % p
print("\nka : ", ka, "\nkb : ", kb)