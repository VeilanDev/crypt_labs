directory = "C:\\Vigileaf\\Vogu\\crypt_labs\\laba4\\"

alph_ru = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPH_RU = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

forward = [1, 4, 2, 3, 0, 5]

backward = [0] * len(forward)
for i, p in enumerate(forward):
    backward[p] = i

def encrypt_permutation(text, perm):
    """Шифрование методом перестановки"""
    result = ""
    # Разбиваем текст на блоки по 6 символов
    for i in range(0, len(text), 6):
        block = text[i:i+6]
        # Если блок меньше 6 символов, дополняем пробелами
        if len(block) < 6:
            block = block + " " * (6 - len(block))
        
        # Создаем блок для зашифрованного текста
        encrypted_block = [''] * 6
        # Для каждой позиции в исходном блоке
        for old_pos in range(6):
            new_pos = perm[old_pos]
            encrypted_block[new_pos] = block[old_pos]
        
        result += ''.join(encrypted_block)
    return result

def decrypt_permutation(text, back_perm):
    """Расшифрование методом перестановки"""
    result = ""
    # Разбиваем на блоки по 6 символов
    for i in range(0, len(text), 6):
        block = text[i:i+6]
        if len(block) < 6:
            block = block + " " * (6 - len(block))
        
        # Создаем блок для расшифрованного текста
        decrypted_block = [''] * 6
        # Для каждой позиции в зашифрованном блоке
        for new_pos in range(6):
            old_pos = back_perm[new_pos]
            decrypted_block[old_pos] = block[new_pos]
        
        result += ''.join(decrypted_block)
    return result.rstrip()  # убираем лишние пробелы в конце

def main():
    while True:
        print("\nВыберите действие:")
        print("1. Зашифровать текст")
        print("2. Расшифровать текст")
        print("3. Выйти")
        
        choice = input("\nВаш выбор: ")
        
        if choice == '1':
            text = input("\nВведите текст для шифрования: ")
            encrypted = encrypt_permutation(text, forward)
            print(f"\nЗашифрованный текст: {encrypted}")
            
            # Сохраняем в файл
            with open(directory + "source_text.txt", "w", encoding="utf-8") as f:
                f.write(text)
            with open(directory + "crypto_text.txt", "w", encoding="utf-8") as f:
                f.write(encrypted)
            print("\nФайлы сохранены: source_text.txt, crypto_text.txt")
            
        elif choice == '2':
            text = input("\nВведите текст для расшифрования: ")
            decrypted = decrypt_permutation(text, backward)
            print(f"\nРасшифрованный текст: {decrypted}")
            
            # Сохраняем в файл
            with open(directory + "decoded_text.txt", "w", encoding="utf-8") as f:
                f.write(decrypted)
            print("\nФайл сохранен: decoded_text.txt")
            
        elif choice == '3':
            break
        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()