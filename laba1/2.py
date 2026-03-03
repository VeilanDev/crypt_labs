import os

directory = "C:\\Vigileaf\\Vogu\\crypt_labs\\laba1\\"

alph = "abcdefghigklmnopqrstuvwxyz"
ALPH = "ABCDEFGHIGKLMNOPQRSTUVWXYZ"

print("\nШифр Цезаря\n1.Зашифровать текст\n2.Расшифровать текст\n")
while 1:
    action = str(input("Выберите действие(1, 2): "))
    if action >= "0" and action <= "9" and action != "":
        if int(action) == 1:
            print("Зашифровать")
            break
        elif int(action) == 2:
            print("Расшифровать")
            break
act = int(action)

fileName = str(input("\nВведите название текстового файла из этой директории (./laba1/)\n(напиример text.txt): "))
pFile = directory + fileName
if (os.path.exists(pFile)):
    pass
else:
    print("файл не найден (некоректне имя файла или файла не существует)")
    exit()

code = int(input("Вветите сдвиг: "))

# print(file)
# text = file.read()

def crypt(text):
    cryptText = ""
    for i in range(len(text)):
        if text[i].islower():
            sim = abs(ord(text[i]) + code)
            if sim > ord(alph[len(alph) - 1]):
                sim = ord(alph[abs(sim - ord(alph[len(alph) - 1])) - 1])
            #print(text[i], "(", ord(text[i]) , ")" , " -> ", chr(sim),"(", sim ,")")
            cryptText = cryptText + chr(sim)
        elif text[i].isupper():
            sim = abs(ord(text[i]) + code)
            if sim > ord(ALPH[len(ALPH) - 1]):
                sim = ord(ALPH[abs(sim - ord(ALPH[len(ALPH) - 1])) - 1])
            #print(text[i], "(", ord(text[i]) , ")" , " -> ", chr(sim),"(", sim ,")")
            cryptText = cryptText + chr(sim)
        else:
            sim = ord(text[i]) + code
            #print(text[i], " (", ord(text[i]), ")", "->", chr(sim), " (", sim, ")")
            cryptText = cryptText + chr(sim)
    return cryptText

def encrypt(text):
    cryptText = ""
    for i in range(len(text)):
        if text[i].islower():
            sim = abs(ord(text[i]) - code)
            if sim < ord(alph[0]):
                sim = ord(alph[-abs(sim - ord(alph[0]))])
            #print(text[i], "(", ord(text[i]) , ")" , " -> ", chr(sim),"(", sim ,")")
            cryptText = cryptText + chr(sim)
        elif text[i].isupper():
            sim = abs(ord(text[i]) - code)
            if sim < ord(ALPH[0]):
                sim = ord(ALPH[-abs(sim - ord(ALPH[0]))])
            #print(text[i], "(", ord(text[i]) , ")" , " -> ", chr(sim),"(", sim ,")")
            cryptText = cryptText + chr(sim)
        else:
            sim = ord(text[i]) - code
            #print(text[i], " (", ord(text[i]), ")", "->", chr(sim), " (", sim, ")")
            cryptText = cryptText + chr(sim)
    return cryptText

def open_file(filename):
    tempFilename = filename + ".tmp"
    with open(directory + filename, "r") as readFile, open(directory + tempFilename, "w") as writefile:
        for lineNum, line in enumerate(readFile, 1):
            originLine = line.rstrip("\n")
            if act == 1:
                cryptLine = crypt(originLine)
            elif act == 2:
                cryptLine = encrypt(originLine)
            else:
                return "Ошибка выбора режима"
            writefile.write(cryptLine + "\n")
    os.remove(directory + filename)
    os.rename(directory + tempFilename, directory + filename)
    print("Файл успешно зашифрован/расшифрован")

open_file(fileName)
