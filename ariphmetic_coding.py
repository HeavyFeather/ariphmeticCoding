import random
import pickle
import os
from collections import Counter

def keyFunc(item): # Ключ для сортировки списка перед созданием словаря
   return item[1]

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
    print(freq_table)
    return freq_table

def alg_encoding(): # Функция для кодирования
    fileName = input("Enter name of file you want to encode: ")
    fileNameOut = fileName + ".encoded"
    fpIn = open(fileName, "r")
    fpOut = open(fileNameOut, "w")

    word = fpIn.read()

    freq_table = create_table(word)

    with open(fileName + ".pickle", 'wb') as f: # Дампаем словарь c диапазонами и длинной
        pickle.dump(freq_table, f)

    left, right = 0, 1
    isFirstValuePassed = False # Эти переменные - небольшой костыль для нормальной работы со словарями (из-за особенности взятия по ключу)
    prevSym = ""
    for sym in word:
        if isFirstValuePassed == False:
            prevSym = sym
            isFirstValuePassed = True
            continue

        left, right = (left + (right - left) * freq_table[prevSym],
                        left + (right - left) * freq_table[sym])
        prevSym = sym
        
    code = random.uniform(left, right)
    
    code = str(code)

    fpOut.write(code) # Запись сообщения в файл
    
    print("[+] Encoding complete\nCreated file: " + fileNameOut + "\nCreated code file: " + fileName + ".pickle")

    fpIn.close()
    fpOut.close()

def alg_decoding():
    filenameIn = input("Enter name of file you want to decode without '.encoded': ")
    fpIn = open(filenameIn + ".encoded", "r")
    fpOut = open(filenameIn, "w")

    code = fpIn.read()
    code = float(code)
    word = ''
    left, right = 0, 1

    with open(filenameIn + '.pickle', 'rb') as f: # Берём дамп словаря с диапазонами и длинной
        freq_table_decode = pickle.load(f)

    lenght = freq_table_decode["Lenght"]

    lenght = int(lenght)
    
    isFirstValuePassed = False # Эти переменные - небольшой костыль для нормальной работы со словарями (из-за особенности взятия по ключу)
    prevSym = ""

    for i in range(lenght):
        for leter in freq_table_decode.values():
            if isFirstValuePassed == False:
                prevSym = sym
                isFirstValuePassed = True
                continue

            interval = (left + (right - left) * freq_table_decode[prevSym], 
                        left + (right - left) * freq_table_decode[sym])
            prevSym = sym
 
            if interval[0] <= code < interval[1]:
                word += freq_table_decode[prevSym]
                code = (code - interval[0]) / (interval[1] - interval[0])
                break

    print("[+] Decoding of " + filenameIn + ".encoded complited!!!") 
    os.remove(filenameIn + '.pickle') # Удаляем словарь с кодировкой за безнабностью
    print("Decoder file: " + filenameIn + ".pickle removed")
    fpIn.close()
    fpOut.close()
    os.remove(filenameIn + '.encoded') # Удалем закодированный файл
    print("Encoded file: " + filenameIn + ".encoded removed")

def main():
    i = input("Enter 1 to encrypt, or 2 to decrypt: ")
    if (int(i) == 1):
        alg_encoding()
    elif (int(i) == 2):
        alg_decoding()

if __name__ == "__main__":
    main()
