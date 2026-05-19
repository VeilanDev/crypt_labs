import random as r

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

p = int(input("\n\nВведите простое число\np : "))

while not is_prime(p):
    print("Ошибка: число должно быть простым!")
    p = int(input("Введите простое число\np : "))

g = r.randint(2, p - 2)
print("g : ", g)

a = r.randint(1, p - 2)
b = r.randint(1, p - 2)
print("\na : ", a, "\nb : ", b)

# Функции шифрования/дешифрования
def encrypt(key, message):
    result = ""
    for i in range(len(message)):
        result = result + chr(ord(message[i]) ^ (key % 256))
    return result

def decrypt(key, message):
    return encrypt(key, message)

# Функции для аутентификации
def EA(message):
    return "EA{" + message + "}"

def DA(message):
    return message.replace("EA{", "").replace("}", "")

def EB(message):
    return "EB{" + message + "}"

def DB(message):
    return message.replace("EB{", "").replace("}", "")

# 1. Абонент A посылает абоненту B сообщение g^a mod p
ga = pow(g, a, p)
print("\nA->B : ", ga)

# 2. Абонент B:
# - вычисляет общий ключ
kb = pow(ga, b, p)
print("\nB вычислил ключ k : ", kb)

# - создает подпись
gb = pow(g, b, p)
signature_B = str(ga) + "," + str(gb)
signed_B = DB(signature_B)
print("B создал подпись : ", signed_B)

# - шифрует подпись
encrypted_B = encrypt(kb, signed_B)
print("B зашифровал подпись : ", encrypted_B)

# - отправляет абоненту A сообщение
print("\nB->A : ", gb, ", ", encrypted_B)

# 3. Абонент A:
# - вычисляет общий ключ
ka = pow(gb, a, p)
print("\nA вычислил ключ k : ", ka)

# - создает подпись
signature_A = str(ga) + "," + str(gb)
signed_A = DA(signature_A)
print("A создал подпись : ", signed_A)

# - шифрует подпись
encrypted_A = encrypt(ka, signed_A)
print("A зашифровал подпись : ", encrypted_A)

# - проверяет подпись B (расшифровываем и сравниваем с signature_B)
decrypted_B = decrypt(ka, encrypted_B)
print("A расшифровал подпись B : ", decrypted_B)

# - отправляет абоненту B сообщение
print("\nA->B : ", encrypted_A)

# 4. Абонент B проверяет подпись A
decrypted_A = decrypt(kb, encrypted_A)
print("\nB расшифровал подпись A : ", decrypted_A)

# Результат
print("\nРезультат аутентификации:")
print("Ожидаемая подпись B: ", signature_B)
print("Полученная подпись B: ", decrypted_B)
print("Ожидаемая подпись A: ", signature_A)
print("Полученная подпись A: ", decrypted_A)

if decrypted_B == signature_B:
    print("Подпись B верна")
else:
    print("Подпись B не верна")

if decrypted_A == signature_A:
    print("Подпись A верна")
else:
    print("Подпись A не верна")

if decrypted_B == signature_B and decrypted_A == signature_A:
    print("\nВзаимная аутентификация успешно завершена!")
    print("Общий ключ k : ", ka)
else:
    print("\nОшибка аутентификации!")