directory = "C:\\Vigileaf\\Vogu\\crypt_labs\\laba5\\"

A = 5
C = 3
T0 = 7
b = 6
M = 2 ** b

alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

def char_to_code(c):
    c = c.lower()
    if c in alph:
        return alph.index(c) + 1
    return ord(c) % M

def code_to_char(code):
    if 1 <= code <= 33:
        return alph[code - 1]
    return chr(code)

def text_to_binary(text):
    res = ""
    for c in text:
        code = char_to_code(c)
        res += format(code, '0' + str(b) + 'b')
    return res

def binary_to_text(binary):
    res = ""
    for i in range(0, len(binary), b):
        if i + b <= len(binary):
            code = int(binary[i:i+b], 2)
            res += code_to_char(code)
    return res

def generate_gamma(seed, count):
    gamma = []
    curr = seed
    for _ in range(count):
        curr = (A * curr + C) % M
        gamma.append(curr)
    return gamma

def xor_encrypt(text, gamma):
    # Получаем двоичные строки
    text_bin = text_to_binary(text)
    
    # Создаём гамму нужной длины
    gamma_bin = ""
    for g in gamma:
        gamma_bin += format(g, '0' + str(b) + 'b')
    
    # Повторяем гамму если нужно
    if len(gamma_bin) < len(text_bin):
        gamma_bin = gamma_bin * (len(text_bin) // len(gamma_bin) + 1)
    gamma_bin = gamma_bin[:len(text_bin)]
    
    # XOR
    result_bin = ""
    for i in range(len(text_bin)):
        result_bin += str(int(text_bin[i]) ^ int(gamma_bin[i]))
    
    return binary_to_text(result_bin)

def process_text(text, mode):
    # Генерация гаммы
    gamma = generate_gamma(T0, len(text))
    
    if mode == "encrypt":
        print("\nГамма шифра:")
        for i, g in enumerate(gamma):
            print(f"  T{i+1} = {g:2d} ({format(g, '0'+str(b)+'b')})")
    
    # Выполняем преобразование
    result = xor_encrypt(text, gamma)
    return result, gamma


print("="*50)
while True:
    print("\n" + "-"*40)
    print("Выберите действие:")
    print("1. Зашифровать текст")
    print("2. Расшифровать текст")
    print("3. Выйти")
    
    choice = input("\nВаш выбор (1-3): ")
    
    if choice == '1':
        # Режим шифрования
        text = input("\nВведите текст для шифрования: ")
        print(f"\nИсходный текст: {text}")
        
        # Шифрование
        crypto, gamma = process_text(text, "encrypt")
        print(f"\nЗашифрованный текст: {crypto}")
        
        #расшифрование
        decoded = xor_encrypt(crypto, gamma)

        # Запись в файлы
        with open(directory + "source_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        with open(directory + "crypto_text.txt", "w", encoding="utf-8") as f:
            f.write(crypto)
        with open(directory + "decoded_text.txt", "w", encoding="utf-8") as f:
            f.write(decoded)

        print("\n✓ Файлы сохранены:")
        print("  - source_text.txt (исходный текст)")
        print("  - crypto_text.txt (зашифрованный текст)")
        print("  - decoded_text.txt (расшифрованный текст)")

    elif choice == '2':
        # Режим расшифрования
        text = input("\nВведите текст для расшифрования: ")
        print(f"\nЗашифрованный текст: {text}")
        
        # Расшифрование
        decoded, gamma = process_text(text, "decrypt")
        print(f"\nРасшифрованный текст: {decoded}")
        
        # Запись в файл
        with open(directory + "decoded_text.txt", "w", encoding="utf-8") as f:
            f.write(decoded)
        
        print("\nФайл сохранен:")
        print("  - decoded_text.txt (расшифрованный текст)")
        
    elif choice == '3':
        break
    
    else:
        print("\n✗ Неверный выбор! Введите 1, 2 или 3.")