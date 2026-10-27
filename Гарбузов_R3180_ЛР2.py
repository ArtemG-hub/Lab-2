import csv
from csv import reader
from datetime import datetime
import os
import random

def open_table():
    try:
        with open ('books.csv', 'r') as csvfile:
            table = list(reader(csvfile, delimiter=';'))
        table = table[1:]
        return table
    except FileNotFoundError:
        print('Файл не найден!')
        return 0

def length():
    count = 0
    with open ('books.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if len(row['Название']) > 30:
                count +=1
    print('Количество записей с названием длиннее 30 символов:', count)

def search_name(table):
    searchline = input ('Введите автора: ')
    if searchline in ['0',''] or searchline.isalpha() == False:
        return 0
    output = open('result.txt', 'w')
    output.write(f'Поиск от: {datetime.today()}\n\n')
    print('Автор | Название | Дата | Тип')
    flag = 0
    for row in table:
        if find_string(searchline, row[4]) != -1:
            if int(row[6][6:10]) > 2017:
                print(f'{row[4]} | {row[1]} | {row[6]} | {row[2]}')
                output.write(f'имя {row[4]} автор {row[1]} дата {row[6]} тип {row[2]}\n')
                flag += 1
    if flag == 0:
        print('Ничего не найдено!')
    else:
        print(f'Найдено позиций: {flag}')
    input('Нажмите Enter')
    output.close()

def find_string(searchline, string):
    string = string.lower()
    index = string.find(searchline.lower())
    return index

def links(table):
    with open('links.txt', 'w') as file:
        random_rows = random.sample(table, 20)
        for i, row in enumerate(random_rows, 1):
            year = row[6:10]
            file.write(f"{i}. {row}. {row} - {year}\n")
    print("Файл links.txt со случайными записями создан")


def unique_tags(table):
    tags = []
    for row in table:
        if row[2] not in tags:
            tags.append(row[2])
    print ('Все теги:')
    for tag in tags:
        print(tag)


def top_20_books(table):
    counts = {}
    for row in table[1:]:
        counts[row[1]] = counts.get(row[1], 0) + int(row[8])
    books = list(counts.items())
    books.sort(key=lambda row: row[1], reverse = True)
    print ('Топ 20 популярных книг:')
    for i in range(20):
        row = books[i]
        print (f'{i+1}. {row[0]}')

while True:
    os.system('cls')
    if open_table() == 0:
        break
    print('Меню:\n1 - Поиск по автору\n2 - Вывести все теги без повторений\n3 - Вывести 20 самых популярных книг\n0 - Выход')
    menu = input('Выберите пункт меню: ')
    match menu:
        case '1':
            search_name(open_table())
        case '2':
            unique_tags(open_table())
            input()
        case '3':
            top_20_books(open_table())
            input()
        case '0':
            links(open_table()) 
            break
        case _:
            print('Нет пункта меню, нажмите Enter')
            input()


open_table()
length()
