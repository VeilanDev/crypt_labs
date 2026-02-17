alph = "abcdefghigklmnopqrstuvwxyz"
ALPH = "ABCDEFGHIGKLMNOPQRSTUVWXYZ"

print("\nШифр Вижинера\n1.Зашифровать текст\n2.Расшифровать текст\n")
while 1:
    action = str(input("Выберите действие(1, 2): "))
    if action >= "0" and action <= "9" and action != "":
        if int(action) == 1:
            print("Зашифровать")
            break
        elif int(action) == 2:
            print("Расшифровать")
            break

text = str(input("Введите текст: "))
code = str(input("Вветите кодовое слово: "))
text = text.strip()
code = code.strip()

i = 0
codeLen = len(code)
while len(code) < len(text):
    code += code[i]
    #print(i, " ", code[i], " : ")
    if i < codeLen - 1:
        i += 1
    else:
        i = 0
print(text)
print(code)

cryptText = ""
act = int(action)
if act == 1:
    for i in range(len(text)):
        if text[i].islower():
            sim = abs(ord(text[i]) + alph.find(code[i], 0, len(alph) - 1))
            if sim > ord(alph[len(alph) - 1]):
                sim = ord(alph[abs(sim - ord(alph[len(alph) - 1])) - 1])
            #print(text[i], "(", ord(text[i]) , ")", code[i], "(", alph.find(code[i], 0, len(alph) - 1) , ")" , " -> ", chr(sim),"(", sim ,")")
            cryptText = cryptText + chr(sim)
        elif text[i].isupper():
            sim = abs(ord(text[i]) + ALPH.find(code[i], 0, len(ALPH) - 1))
            if sim > ord(ALPH[len(ALPH) - 1]):
                sim = ord(ALPH[abs(sim - ord(ALPH[len(ALPH) - 1])) - 1])
            #print(text[i], "(", ord(text[i]) , ")", code[i], "(", ALPH.find(code[i], 0, len(ALPH) - 1) , ")" , " -> ", chr(sim),"(", sim ,")")
            cryptText = cryptText + chr(sim)
elif act == 2:
    pass
print(text)
text = cryptText
print(text)