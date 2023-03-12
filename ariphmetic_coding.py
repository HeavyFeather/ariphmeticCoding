import pickle
import struct
from collections import Counter

def keyFunc(item): # Ключ для сортировки списка перед созданием словаря
   return item[1]

def get_key(freq_table, value):
    for k, v in freq_table.items():
        if v == value:
            return k

def next_value(freq_table, value):
    for k, v in freq_table.items():
        if value < v:
            return v

def create_table(word):
    tmp_arr = [] # список для подсчёта частоты символов
    for char, count in Counter(word).items(): 
        tmp_arr.append((char, count))
    
    tmp_arr.sort(key = keyFunc, reverse = True)
    
    freq_table = {char: count / len(word) for char, count in tmp_arr} # Таблица с частотой
    
    i = 0
     
    for char in freq_table: # Приводим заначения таблицы к диапазону
        i += freq_table[char]
        freq_table[char] = i
    freq_table["Lenght"] = len(word) # Добавли значение длины исходного слова для декодировки
    print("[+] Table created")
    return freq_table

def alg_encoding(): # Функция для кодирования
    fileName = input("Enter name of file you want to encode: ")
    fpIn = open(fileName, "r")

    word = fpIn.read()

    freq_table = create_table(word)

    coded_message = ''
    left, right = 0, 10000 
    count = 0
    for sym in word:
        left = left + (right - left) * freq_table[sym]
        right = left + (right - left) * next_value(freq_table, freq_table[sym]) -1
        count += 1

        if count == freq_table["Lenght"]:
            coded_message += str(int(left))
        elif (right - left) < 1000:
            coded_message += str(int(left / 1000)) 
            left = int(left) % 1000 * 10
            right = int(right) % 1000 * 10 + 9
    

    code = "{0:b}".format(int(coded_message))

    pack = b'' 

    for i in range(0, len(code), 8):
        pack += struct.pack('B', int(code[i: i + 8], 2))

    with open(fileName + ".encoded", 'wb') as f: # Дампаем словарь с кодами символов, затем записываем код
        pickle.dump(freq_table, f)
        f.write(pack)

    print(f"[+] Encoding complete\nCreated file: {fileName}.encoded")
    print(coded_message) 
    fpIn.close()

def alg_decoding():
    filenameIn = input("Enter name of file you want to decode: ")
     
    with open(filenameIn, 'rb') as f: # Берём дамп словаря с кодировкой и само сообщение
        freq_table = pickle.load(f)
        unpack = f.read()

    code_unpack = ''

    for i in unpack:
        code_unpack += '{0:08b}'.format(i)

    fileName = filenameIn.replace(".encoded", "")
    fpOut = open(fileName, 'w')
     
    code = int(code_unpack, 2)

    left, right = 0, 10000

    for value in code:
        




    #fpOut.write("")
    print(f"[+] Decoding of {fileName}.encoded complited!!!") 
    fpOut.close()

def main():
    i = input("Enter 1 to encrypt, or 2 to decrypt: ")
    if (int(i) == 1):
        alg_encoding()
    elif (int(i) == 2):
        alg_decoding()

if __name__ == "__main__":
    main()
