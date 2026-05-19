import os

ALPH = "ABCDEFGHIGKLMNOPQRSTUVWXYZ"

vigenere = [['#'] + ['|'] + [i for i in ALPH]]
vigenere.append(['-'] +  ['+'] +['-' for i in range(len(ALPH))])

for i in range(len(ALPH)):
    string = [ALPH[i]] + ['|'] + list(ALPH[i:] + ALPH[:i])
    vigenere.append(string)

#print(vigenere)

directory = "C:\\Vigileaf\\Vogu\\crypt_labs\\laba1\\"
filename = "vigenere_table.txt"

tempFilename = filename + ".tmp"
try:
    with open(directory + tempFilename, "w", encoding='utf-8') as writefile:
        for vig_str in vigenere:
            string = ""
            for word in vig_str:
                string += word + " "
            writefile.write(string.strip() + "\n")
    
    os.remove(directory + filename)
    os.rename(directory + tempFilename, directory + filename)
        
except FileNotFoundError:
    os.rename(directory + tempFilename, directory + filename)
except Exception as e:
    print(f"Произошла ошибка: {e}")