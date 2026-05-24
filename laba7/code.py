directory = "C:\\Vigileaf\\Vogu\\crypt_labs\\laba7\\"

import math

p = 211
q = 317

n = p * q
phi = (p - 1) * (q - 1)

e = 2
while math.gcd(e, phi) != 1:
    e += 1

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

d = mod_inverse(e, phi)

def are_coprime(a, b):
    return math.gcd(a, b) == 1

def str_to_int(text):
    result = 0
    for char in text:
        result = result * 256 + ord(char)
    return result

def int_to_str(num):
    chars = []
    while num > 0:
        chars.append(chr(num % 256))
        num //= 256
    return ''.join(reversed(chars))

def powmod(a, b, m):
    result = 1
    a = a % m
    while b > 0:
        if b & 1:
            result = (result * a) % m
        a = (a * a) % m
        b >>= 1
    return result

def encrypt_char(m, e, n):
    return powmod(m, e, n)

def decrypt_char(c, d, n):
    return powmod(c, d, n)

def encrypt_text(text, e, n):
    block_size = len(str(n)) // 3  # Примерный размер блока
    
    # Преобразуем текст в байты
    data = text.encode('utf-8')
    
    encrypted = []
    i = 0
    while i < len(data):
        # Берем блок байт
        block = data[i:i+block_size]
        # Преобразуем блок в число
        m = 0
        for byte in block:
            m = (m << 8) | byte
        # Шифруем блок
        c = encrypt_char(m, e, n)
        encrypted.append(c)
        i += block_size
    
    return encrypted

def decrypt_text(encrypted, d, n):
    decrypted_bytes = bytearray()
    
    for c in encrypted:
        # Расшифровываем блок
        m = decrypt_char(c, d, n)
        # Преобразуем число обратно в байты
        block = []
        while m > 0:
            block.insert(0, m & 0xFF)
            m >>= 8
        decrypted_bytes.extend(block)
    
    return decrypted_bytes.decode('utf-8', errors='replace')

def encrypt_mode():
    print("\n" + "-"*40)
    print("Шифрование RSA")
    print("-"*40)
    
    text = input("\nВведите текст для шифрования: ")
    
    # Показываем параметры
    print(f"\nПараметры RSA (Вариант 2):")
    print(f"  p = {p}")
    print(f"  q = {q}")
    print(f"  n = p*q = {n}")
    print(f"  φ(n) = {phi}")
    print(f"  e = {e} (минимальное, взаимно простое с φ(n))")
    print(f"  d = {d}")
    print(f"\nПроверка: e*d mod φ(n) = {(e * d) % phi}")
    
    # Шифрование
    encrypted = encrypt_text(text, e, n)
    
    print(f"\nЗашифрованные данные (блоки):")
    for i, block in enumerate(encrypted):
        print(f"  Блок {i+1}: {block}")
    
    # Сохраняем в файлы
    with open(directory + "source_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    with open(directory + "crypto_text(blocks).txt", "w", encoding="utf-8") as f:
        f.write(','.join(str(block) for block in encrypted))

    with open(directory + "public_key.txt", "w", encoding="utf-8") as f:
        f.write(f"e={e}\nn={n}")
    with open(directory + "private_key.txt", "w", encoding="utf-8") as f:
        f.write(f"d={d}\nn={n}\np={p}\nq={q}")
    
    print("\nФайлы сохранены:")
    print("  - source_text.txt (исходный текст)")
    print("  - crypto_text.txt (зашифрованные данные)")
    print("  - crypto_text(blocks).txt (зашифрованные данные в виде блоков)")
    print("  - public_key.txt (открытый ключ e,n)")
    print("  - private_key.txt (закрытый ключ d,n,p,q)")
    
    # Демонстрация расшифрования для проверки
    decoded = decrypt_text(encrypted, d, n)
    if text == decoded:
        print("\nПроверка: расшифрование работает корректно!")

def decrypt_mode():
    print("\n" + "-"*40)
    print("Расшифрование RSA")
    print("-"*40)
    
    # Выбор источника зашифрованных данных
    print("\nВыберите источник зашифрованных данных:")
    print("1. Ввести строку блоков (числа через запятую)")
    print("2. Загрузить из файла crypto_text(blocks).txt")
    
    choice = input("\nВаш выбор (1-2): ")
    
    encrypted = []
    
    if choice == '1':
        input_str = input("\nВведите числа через запятую (например: 11487,63690,...): ")
        try:
            encrypted = [int(x.strip()) for x in input_str.split(',')]
            print(f"\nЗагружено {len(encrypted)} блоков")
        except ValueError:
            print("Ошибка: неверный формат! Введите числа через запятую.")
            return
    elif choice == '2':
        try:
            with open(directory + "crypto_text(blocks).txt", "r", encoding="utf-8") as f:
                content = f.read().strip()
            # Пробуем прочитать как числа через запятую
            if ',' in content:
                encrypted = [int(x) for x in content.split(',')]
            
            print(f"\nЗагружено {len(encrypted)} блоков из файла")
        except FileNotFoundError:
            print("Ошибка: файл crypto_text(blocks).txt не найден!")
            return
    else:
        print("Неверный выбор!")
        return
    
    # Загружаем закрытый ключ или вводим вручную
    print("\nВыберите источник закрытого ключа:")
    print("1. Загрузить из файла private_key.txt")
    print("2. Ввести вручную")
    
    key_choice = input("\nВаш выбор (1-2): ")
    
    if key_choice == '1':
        try:
            with open(directory + "private_key.txt", "r", encoding="utf-8") as f:
                content = f.read()
            # Парсим файл
            for line in content.split('\n'):
                if line.startswith('d='):
                    d_val = int(line.split('=')[1])
                elif line.startswith('n='):
                    n_val = int(line.split('=')[1])
            print(f"\nЗагружен ключ: d={d_val}, n={n_val}")
        except:
            print("Ошибка: не удалось загрузить ключ!")
            return
    else:
        try:
            d_val = int(input("\nВведите d (закрытая экспонента): "))
            n_val = int(input("Введите n: "))
        except ValueError:
            print("Ошибка ввода!")
            return
    
    # Расшифрование
    try:
        decoded = decrypt_text(encrypted, d_val, n_val)
        print(f"\nРасшифрованный текст: {decoded}")
        
        # Сохраняем в файл
        with open(directory + "decoded_text.txt", "w", encoding="utf-8") as f:
            f.write(decoded)
        
        print("\nФайл сохранен: decoded_text.txt")
    except Exception as e:
        print(f"\nОшибка расшифрования: {e}")

def main():
    print("="*50)
    print("RSA (Вариант 2)")
    print(f"p = {p}, q = {q}")
    print("="*50)
    
    while True:
        print("\n" + "-"*40)
        print("ВЫБЕРИТЕ ДЕЙСТВИЕ:")
        print("1. Зашифровать текст")
        print("2. Расшифровать текст")
        print("3. Показать ключи")
        print("4. Выйти")
        print("-"*40)
        
        choice = input("\nВаш выбор (1-4): ")
        
        if choice == '1':
            encrypt_mode()
        elif choice == '2':
            decrypt_mode()
        elif choice == '3':
            print("\n" + "="*40)
            print("КЛЮЧИ RSA (Вариант 2)")
            print("="*40)
            print(f"\nОткрытый ключ (public key):")
            print(f"  e = {e}")
            print(f"  n = {n}")
            print(f"\nЗакрытый ключ (private key):")
            print(f"  d = {d}")
            print(f"  n = {n}")
            print(f"  p = {p}")
            print(f"  q = {q}")
            print(f"\nПроверка: e*d = {(e * d) % phi} mod φ(n)")
        elif choice == '4':
            break
        else:
            print("\nНеверный выбор! Введите 1, 2, 3 или 4.")

if __name__ == "__main__":
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)
    main()