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

text = str(input("Введите текст: "))
code = int(input("Вветите сдвиг: "))
text = text.strip()

cryptText = ""
act = int(action)
if act == 1:
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
elif act == 2:
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
print(text)
text = cryptText
print(text)