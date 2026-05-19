import os

directory = "C:\\Vigileaf\\Vogu\\crypt_labs\\laba1\\"

alph = "abcdefghigklmnopqrstuvwxyz"
ALPH = "ABCDEFGHIGKLMNOPQRSTUVWXYZ"

def process_text(text, code, action):
    """Функция для шифрования/расшифровки текста"""
    # Подгоняем длину кодового слова
    i = 0
    codeLen = len(code)
    while len(code) < len(text):
        code += code[i]
        if i < codeLen - 1:
            i += 1
        else:
            i = 0
    
    cryptText = ""
    if action == 1:  # Шифрование
        for i in range(len(text)):
            if text[i].islower():
                sim = ord(text[i]) + alph.find(code[i].lower(), 0, len(alph) - 1)
                if sim > ord(alph[len(alph) - 1]):
                    sim = sim - len(alph)
                cryptText = cryptText + chr(sim)
            elif text[i].isupper():
                sim = ord(text[i]) + ALPH.find(code[i].upper(), 0, len(ALPH) - 1)
                if sim > ord(ALPH[len(ALPH) - 1]):
                    sim = sim - len(ALPH)
                cryptText = cryptText + chr(sim)
            else:
                cryptText += text[i]  # Сохраняем не-буквы как есть
    else:  # Расшифровка
        for i in range(len(text)):
            if text[i].islower():
                sim = ord(text[i]) - alph.find(code[i].lower(), 0, len(alph) - 1)
                if sim < ord(alph[0]):
                    sim = sim + len(alph)
                cryptText = cryptText + chr(sim)
            elif text[i].isupper():
                sim = ord(text[i]) - ALPH.find(code[i].upper(), 0, len(ALPH) - 1)
                if sim < ord(ALPH[0]):
                    sim = sim + len(ALPH)
                cryptText = cryptText + chr(sim)
            else:
                cryptText += text[i]  # Сохраняем не-буквы как есть
    return cryptText

print("\nШифр Вижинера")
print("1. Зашифровать текст")
print("2. Расшифровать текст")
print("3. Зашифровать файл")
print("4. Расшифровать файл\n")

while True:
    action = input("Выберите действие(1, 2, 3, 4): ")
    if action.isdigit() and action in ["1", "2", "3", "4"]:
        action = int(action)
        break
    print("Ошибка! Введите число от 1 до 4.")

if action in [1, 2]:  # Работа с текстом
    text = input("Введите текст: ")
    code = input("Введите кодовое слово: ")
    text = text.strip()
    code = code.strip()
    
    result = process_text(text, code, action)
    
    if action == 1:
        print("\nЗашифрованный текст:")
    else:
        print("\nРасшифрованный текст:")
    print(result)

else:  # Работа с файлом (3 или 4)
    filename = input("Введите имя файла: ")
    code = input("Введите кодовое слово: ")
    code = code.strip()

    tempFilename = filename + ".tmp"
    try:
        with open(directory + filename, "r", encoding='utf-8') as readFile, \
            open(directory + tempFilename, "w", encoding='utf-8') as writefile:
            
            for lineNum, line in enumerate(readFile, 1):
                originLine = line.rstrip("\n")
                cryptLine = process_text(originLine, code, action - 2)  # action 3 или 4 превращаем в 1 или 2
                writefile.write(cryptLine + "\n")
        
        os.remove(directory + filename)
        os.rename(directory + tempFilename, directory + filename)
        
        if action == 3:
            print("Файл успешно зашифрован")
        else:
            print("Файл успешно расшифрован")
            
    except FileNotFoundError:
        print(f"Ошибка: Файл '{directory + filename}' не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")