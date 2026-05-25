directory = "C:\\Vigileaf\\Vogu\\crypt_labs\\laba8\\"

import random
import math

# Параметры системы (ГОСТ Р34.10-94)
p = 787     # простое число
q = 131      # простой делитель
a = 10         # a^q mod p = 1

# Ключи
x = random.randint(1, q - 1)      # секретный ключ
y = pow(a, x, p)                  # открытый ключ

print("=" * 60)
print("Хэш: умножение кодов символов mod 65536")
print("=" * 60)
print(f"p={p}, q={q}, a={a}")
print(f"Секретный ключ x={x}")
print(f"Открытый ключ y={y}")


def hash_function(text):
    """Хэш-функция: умножение кодов символов по модулю 65536"""
    MOD = 65536
    result = 1
    for char in text:
        result = (result * ord(char)) % MOD
        if result == 0:
            result = 1
    return result


def extended_gcd(a, b):
    """Расширенный алгоритм Евклида"""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


def mod_inverse(a, m):
    """Обратное число по модулю m"""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m


def generate_signature(message, x, q, a, p):
    """Создание ЭЦП с проверкой"""
    print("\n" + "-" * 40)
    print("ГЕНЕРАЦИЯ ПОДПИСИ")
    print("-" * 40)
    
    h = hash_function(message) % q
    if h == 0:
        h = 1
    
    print(f"Хэш сообщения H(M) = {hash_function(message)}")
    print(f"h = H(M) mod q = {h}")
    
    if math.gcd(h, q) != 1:
        print(f"Предупреждение: h и q не взаимно просты! НОД={math.gcd(h, q)}")
        h = h + 1
        while math.gcd(h, q) != 1:
            h = (h + 1) % q
            if h == 0:
                h = 1
        print(f"Исправленное h = {h}")
    
    max_attempts = 100
    attempts = 0
    
    while attempts < max_attempts:
        attempts += 1
        k = random.randint(1, q - 1)
        print(f"\nПопытка {attempts}: k = {k}")
        
        r = pow(a, k, p)
        r1 = r % q
        print(f"r = {r}, r1 = {r1}")
        
        if r1 == 0:
            print("r1 = 0, выбираем другое k")
            continue
        
        s = (x * r1 + k * h) % q
        print(f"s = ({x}*{r1} + {k}*{h}) mod {q} = {s}")
        
        if s == 0:
            print("s = 0, выбираем другое k")
            continue
        
        # Проверяем созданную подпись сразу
        if verify_signature(message, r1, s, y, q, a, p, verbose=False):
            print(f"\n✓ ПОДПИСЬ: (r1, s) = ({r1}, {s})")
            return r1, s, h, k
        else:
            print("Подпись не прошла проверку, пробуем другое k")
            continue
    
    raise Exception("Не удалось создать корректную подпись")

def verify_signature(message, r1, s, y, q, a, p, verbose=True):
    """Проверка ЭЦП"""
    if verbose:
        print("\n" + "-" * 40)
        print("ПРОВЕРКА ПОДПИСИ")
        print("-" * 40)
    
    if not (0 < r1 < q and 0 < s < q):
        if verbose:
            print(f"Ошибка: условия не выполнены (r1={r1}, s={s})")
        return False
    
    h = hash_function(message) % q
    if h == 0:
        h = 1
    
    if verbose:
        print(f"Хэш сообщения H(M) = {hash_function(message)}")
        print(f"h = H(M) mod q = {h}")
    
    w = mod_inverse(h, q)
    if w is None:
        if verbose:
            print("Ошибка: нет обратного элемента для h")
        return False
    
    if verbose:
        print(f"w = h^(-1) mod q = {w}")
    
    u1 = (s * w) % q
    u2 = ((q - r1) * w) % q
    
    if verbose:
        print(f"u1 = s * w mod q = {u1}")
        print(f"u2 = (q - r1) * w mod q = {u2}")
    
    a_u1 = pow(a, u1, p)
    y_u2 = pow(y, u2, p)
    v = (a_u1 * y_u2) % p
    v = v % q
    
    if verbose:
        print(f"a^u1 mod p = {a_u1}")
        print(f"y^u2 mod p = {y_u2}")
        print(f"v = (a^u1 * y^u2 mod p) mod q = {v}")
    
    if v == r1:
        if verbose:
            print("\n✓ ПОДПИСЬ ВЕРНА")
        return True
    else:
        if verbose:
            print("\n✗ ПОДПИСЬ НЕВЕРНА")
        return False


while True:
    print("\n" + "-" * 40)
    print("1. Подписать сообщение")
    print("2. Проверить подпись")
    print("3. Выйти")
    
    choice = input("\nВаш выбор: ")
    
    if choice == '1':
        message = input("Введите сообщение: ")
        
        r, s, h, k = generate_signature(message, x, q, a, p)
        
        print(f"\nПодпись: r={r}, s={s}")
        
        with open(directory + "message.txt", "w", encoding="utf-8") as f:
            f.write(message)
        with open(directory + "signature.txt", "w") as f:
            f.write(f"{r},{s}")
        
        print("Файлы сохранены: message.txt, signature.txt")
        
        if verify_signature(message, r, s, y, q, a, p):
            print("\n✓ ВСЕ ХОРОШО: Подпись прошла проверку!")
        else:
            print("\n✗ КРИТИЧЕСКАЯ ОШИБКА: Подпись не прошла проверку!")
            
    elif choice == '2':
        print("\n1. Ввести вручную")
        print("2. Загрузить из файла message.txt")
        
        sub = input("Выбор: ")
        
        if sub == '1':
            message = input("Сообщение: ")
            r = int(input("r: "))
            s = int(input("s: "))
        else:
            try:
                with open(directory + "message.txt", "r", encoding="utf-8") as f:
                    message = f.read()
                with open(directory + "signature.txt", "r") as f:
                    r, s = map(int, f.read().split(','))
                print(f"Сообщение: {message}")
                print(f"Подпись: r={r}, s={s}")
            except Exception as e:
                print(f"Ошибка загрузки файлов: {e}")
                continue
        
        verify_signature(message, r, s, y, q, a, p)
            
    elif choice == '3':
        break
    else:
        print("Неверный выбор!")