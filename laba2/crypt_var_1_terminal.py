import sys

directory = "C:\\Vigileaf\\Vogu\\crypt_labs\\laba2\\"

alph_en = "abcdefghijklmnopqrstuvwxyz"
ALPH_EN = "ABCDEFGHIGKLMNOPQRSTUVWXYZ"
alph_ru = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPH_RU = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

cryptTable = [[' ' for _ in range(8)] for _ in range(4)]

text = str(input("Введите текст: "))
cryptText = ""
cryptWord = str(input("Введите ключ (слово без пробелов, только строчными или заглавными буквами): "))
cryptWord = cryptWord.strip()

def distinct(cryptWord, editCryptWord = ""):
    for i in range(0, len(cryptWord)):
        inWord = False
        for j in range(0, len(editCryptWord)):
            if cryptWord[i] == editCryptWord[j]:
                inWord = True
                break
            if cryptWord[i] == " ":
                print("error: в слове не должно быть пробелов")
                sys.exit(0)
        if inWord == False:
            editCryptWord = editCryptWord + cryptWord[i]
    return editCryptWord

def writeTable(cryptWord):
    cryptWordAlph = distinct(alph_ru, cryptWord)
    for i in range(4):
        for j in range(8):
            cryptTable[i][j] = cryptWordAlph[0].lower()
            cryptWordAlph = cryptWordAlph[1:]

def cryptTextFun(text):
    textDub = text
    cryptTextDub = ""
    while len(textDub) > 0:
        for i in range(4):
            inWord = False
            for j in range(8):
                sim = ""
                if textDub[0] >= "a" and textDub[0] <= "я":
                    if textDub[0] == cryptTable[i][j].lower():
                        if i < 3:
                            sim = cryptTable[i + 1][j].lower()
                        else:
                            sim = cryptTable[0][j].lower()
                        cryptTextDub = cryptTextDub + sim
                        textDub = textDub[1:]
                        inWord = True
                        break
                elif textDub[0] >= "А" and textDub[0] <= "Я":
                    if textDub[0] == cryptTable[i][j].upper():
                        if i < 3:
                            sim = cryptTable[i + 1][j].upper()
                        else:
                            sim = cryptTable[0][j].upper()
                        cryptTextDub = cryptTextDub + sim
                        textDub = textDub[1:]
                        inWord = True
                        break
                else:
                    cryptTextDub = cryptTextDub + textDub[0]
                    textDub = textDub[1:]
                    inWord = True
                    break
            if inWord == True:
                break
    return cryptTextDub

def decryptTextFun(cryptText):
    textDub = cryptText
    decryptTextDub = ""
    while len(textDub) > 0:
        for i in range(4):
            inWord = False
            for j in range(8):
                sim = ""
                if textDub[0] >= "a" and textDub[0] <= "я":
                    if textDub[0] == cryptTable[i][j].lower():
                        if i > 0:
                            sim = cryptTable[i - 1][j].lower()
                        else:
                            sim = cryptTable[3][j].lower()
                        decryptTextDub = decryptTextDub + sim
                        textDub = textDub[1:]
                        inWord = True
                        break
                elif textDub[0] >= "А" and textDub[0] <= "Я":
                    if textDub[0] == cryptTable[i][j].upper():
                        if i > 0:
                            sim = cryptTable[i - 1][j].upper()
                        else:
                            sim = cryptTable[3][j].upper()
                        decryptTextDub = decryptTextDub + sim
                        textDub = textDub[1:]
                        inWord = True
                        break
                else:
                    decryptTextDub = decryptTextDub + textDub[0]
                    textDub = textDub[1:]
                    inWord = True
                    break
            if inWord == True:
                break
    return decryptTextDub

cryptWord = distinct(cryptWord)
# print("После удаления повторов букв: ", cryptWord)
writeTable(cryptWord)

# print(cryptTable)

cryptText = cryptTextFun(text)
# print("Зашифрованный текст: ", cryptText)

decryptText = decryptTextFun(cryptText)

with open(directory + "source_text.txt", "w", encoding="utf-8") as f1:
    f1.write(text)

with open(directory + "crypto_text.txt", "w", encoding="utf-8") as f2:
    f2.write(cryptText)

with open(directory + "decoded_text.txt", "w", encoding="utf-8") as f3:
    f3.write(decryptText)

print("\nФайлы созданы:")
print("1. source_text.txt - исходный текст")
print("2. crypto_text.txt - зашифрованный текст")
print("3. decoded_text.txt - расшифрованный текст")