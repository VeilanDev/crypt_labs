directory = "C:\\Vigileaf\\Vogu\\crypt_labs\\laba6\\"

import struct

ROUNDS = 8
BLOCK_SIZE = 8  # 64 бита
MOD = 2 ** 32

def rotl(x, shift):
    shift = shift % 32
    return ((x << shift) | (x >> (32 - shift))) & (MOD - 1)

def rotr(x, shift):
    shift = shift % 32
    return ((x >> shift) | (x << (32 - shift))) & (MOD - 1)

def bytes_to_words(data):
    if len(data) < BLOCK_SIZE:
        data = data + b'\x00' * (BLOCK_SIZE - len(data))
    return list(struct.unpack('>2I', data[:BLOCK_SIZE]))

def words_to_bytes(words):
    return struct.pack('>2I', *words)

def split_key(key_bytes):
    # Приводим ключ к 8 байтам
    if len(key_bytes) < 8:
        key_bytes = key_bytes + b'\x00' * (8 - len(key_bytes))
    elif len(key_bytes) > 8:
        key_bytes = key_bytes[:8]
    
    K1 = struct.unpack('>I', key_bytes[:4])[0]
    K2 = struct.unpack('>I', key_bytes[4:8])[0]
    return K1, K2

def calculate_V(K1, K2, round_num):
    return (rotl(K1, round_num) + rotr(K2, round_num)) & (MOD - 1)

def F(x, V):
    return (x + V) & (MOD - 1)

def encrypt_block(words, K1, K2):
    L, R = words
    
    for i in range(1, ROUNDS + 1):
        V = calculate_V(K1, K2, i)
        new_L = R
        new_R = L ^ F(R, V)
        L, R = new_L, new_R
    
    return [L, R]

def decrypt_block(words, K1, K2):
    L, R = words
    
    for i in range(ROUNDS, 0, -1):
        V = calculate_V(K1, K2, i)
        new_R = L
        new_L = R ^ F(L, V)
        L, R = new_L, new_R
    
    return [L, R]

def encrypt_text(text, key):
    try:
        key_bytes = key.encode('latin-1')
    except UnicodeEncodeError:
        # Если ключ содержит русские буквы, используем UTF-8 и обрезаем/дополняем
        key_bytes = key.encode('utf-8')[:8]
    
    K1, K2 = split_key(key_bytes)
    data = text.encode('utf-8')
    
    encrypted = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        words = bytes_to_words(block)
        enc_words = encrypt_block(words, K1, K2)
        encrypted.extend(words_to_bytes(enc_words))
    
    return bytes(encrypted)

def decrypt_text(encrypted, key):
    try:
        key_bytes = key.encode('latin-1')
    except UnicodeEncodeError:
        key_bytes = key.encode('utf-8')[:8]
    
    K1, K2 = split_key(key_bytes)
    
    decrypted = bytearray()
    for i in range(0, len(encrypted), BLOCK_SIZE):
        block = encrypted[i:i+BLOCK_SIZE]
        if len(block) < BLOCK_SIZE:
            block = block + b'\x00' * (BLOCK_SIZE - len(block))
        words = bytes_to_words(block)
        dec_words = decrypt_block(words, K1, K2)
        decrypted.extend(words_to_bytes(dec_words))
    
    # Удаляем нулевые байты в конце
    result = decrypted.rstrip(b'\x00')
    
    # Пробуем декодировать
    try:
        return result.decode('utf-8')
    except UnicodeDecodeError:
        return result.decode('utf-8', errors='replace')


def encrypt_mode():
    print("\n" + "-"*40)
    print("Шифрование")
    print("-"*40)
    
    text = input("\nВведите текст для шифрования: ")
    key = input("Введите ключ (8 латинских символов): ")
    
    # Предупреждение о длине ключа
    print(f"\nДлина ключа: {len(key)} символов")
    if len(key) != 8:
        print(f"ВНИМАНИЕ: Ключ должен быть 8 символов! Сейчас {len(key)}")
        print("Программа дополнит ключ нулями или обрежет его.")
    
    # Шифрование
    crypto = encrypt_text(text, key)
    print(f"\nЗашифрованные данные (hex): {crypto.hex().upper()}")
    print(f"Длина зашифрованных данных: {len(crypto)} байт")
    
    # Сохраняем в файлы
    with open(directory + "source_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    with open(directory + "crypto_text.txt", "wb") as f:
        f.write(crypto)
    
    print("\nФайлы сохранены:")
    print("  - source_text.txt (исходный текст)")
    print("  - crypto_text.txt (зашифрованные данные)")
    
    # Демонстрация расшифрования для проверки
    decoded = decrypt_text(crypto, key)
    if text == decoded:
        print("\nПроверка: расшифрование работает корректно!")


def decrypt_mode():
    print("\n" + "-"*40)
    print("Расшифрование")
    print("-"*40)
    
    # Выбор источника зашифрованных данных
    print("\nВыберите источник зашифрованных данных:")
    print("1. Ввести hex-строку")
    print("2. Загрузить из файла crypto_text.txt")
    
    choice = input("\nВаш выбор (1-2): ")
    
    if choice == '1':
        hex_input = input("\nВведите hex-строку: ")
        try:
            encrypted = bytes.fromhex(hex_input)
        except ValueError:
            print("Ошибка: неверный hex-формат!")
            return
    elif choice == '2':
        try:
            with open(directory + "crypto_text.txt", "rb") as f:
                encrypted = f.read()
            print(f"\nЗагружено {len(encrypted)} байт из файла")
        except FileNotFoundError:
            print("Ошибка: файл crypto_text.txt не найден!")
            return
    else:
        print("Неверный выбор!")
        return
    
    key = input("\nВведите ключ (8 латинских символов или цифр): ")
    
    # Предупреждение о длине ключа
    print(f"\nДлина ключа: {len(key)} символов")
    if len(key) != 8:
        print(f"ВНИМАНИЕ: Ключ должен быть 8 символов! Сейчас {len(key)}")
    
    # Расшифрование
    try:
        decoded = decrypt_text(encrypted, key)
        print(f"\nРасшифрованный текст: {decoded}")
        
        # Сохраняем в файл
        with open(directory + "decoded_text.txt", "w", encoding="utf-8") as f:
            f.write(decoded)
        
        print("\nФайл сохранен: decoded_text.txt")
    except Exception as e:
        print(f"\nОшибка расшифрования: {e}")


def main():
    print("="*50)
    print("ВНИМАНИЕ: Для корректной работы используйте")
    print("ключ из 8 ЛАТИНСКИХ букв или цифр (например: password)")
    print("="*50)
    
    while True:
        print("\n" + "-"*40)
        print("ВЫБЕРИТЕ ДЕЙСТВИЕ:")
        print("1. Зашифровать текст")
        print("2. Расшифровать текст")
        print("3. Выйти")
        print("-"*40)
        
        choice = input("\nВаш выбор (1-3): ")
        
        if choice == '1':
            encrypt_mode()
        elif choice == '2':
            decrypt_mode()
        elif choice == '3':
            break
        else:
            print("\nНеверный выбор! Введите 1, 2 или 3.")


if __name__ == "__main__":
    main()