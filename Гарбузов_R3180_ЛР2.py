import csv
from csv import reader           #импортируем инструмент чтобы читать строки файла
from datetime import datetime    #модуль для работы с текущей датой и временем
import os           #модуль чтобы управлять консолью
import random       #чтобы выбирать случаныйе строки из таблицы

def open_table():   #открываем таблицу и превращаем в удобный список для питон
    try:
        with open ('books.csv', 'r') as csvfile:
            table = list(reader(csvfile, delimiter=';')) #читаем файл и превращаем все в список списков 
        table = table[1:]                                #отрезаем первую строччку с заголовками, чтобы остались только данные
        return table                                     #возвращаем готовую таблицу наружу из ф-ии (чтобы она не пропала после разделения)
    except FileNotFoundError:                            #чтобы программа не вылетела из-за того, что файла нет на компьютере
        print('Файл не найден!')
        return 0                                         #возвращаем 0 как сигнал об ошибке

def length(table):
    count = 0
    for row in table:
        if len(row[1]) > 30:
            count +=1
    print('Количество записей с названием длиннее 30 символов:', count)

def search_name(table):
    searchline = input ('Введите автора: ')
    if searchline in ['0',''] or searchline.isalpha() == False: #если введены не буквы, 0 или пустота то возвращаем 0 (отменяем поиск)
        return 0
    output = open('result.txt', 'w') #создаем файл для записи результатов поиска
    output.write(f'Поиск от: {datetime.today()}\n\n') #записываем текущую дату и время поиска
    print('Автор | Название | Дата | Тип')
    flag = 0  #счетчик, чтобы понять нашли мы что-то или нет
    for row in table:
        if find_string(searchline, row[4]) != -1:  #проверяем есть ли введенное имя автора в колонке автора (если не нашлись то метод возвращает -1)
            if int(row[6][6:10]) > 2017:
                print(f'{row[4]} | {row[1]} | {row[6]} | {row[2]}')
                output.write(f'имя {row[4]} автор {row[1]} дата {row[6]} тип {row[2]}\n')
                flag += 1
    if flag == 0:
        print('Ничего не найдено!')
    else:
        print(f'Найдено позиций: {flag}')
    input('Нажмите Enter') #пауза чтобы пользователь прочитал то что выдала программа и нажал энтер после прочтения
    output.close()

def find_string(searchline, string):
    string = string.lower()   #переводим всю строку в нижний регистр
    index = string.find(searchline.lower())   #ищем индекс (позицию) подстроки поиска, тоже переведенной в нижний регистр
    return index  #возвращаем индекс (если вернет -1 значит текст вообще не найден)

def links(table):
    with open('links.txt', 'w') as file:
        random_rows = random.sample(table, 20)
        for i, row in enumerate(random_rows, 1):   #enumerate дает порядковый номер от 1
            year = row[6][6:10]
            file.write(f"{i}. {row}. {row} - {year}\n")
    print("Файл links.txt со случайными записями создан")


def unique_tags(table):
    tags = []
    for row in table:
        if row[2] not in tags:
            tags.append(row[2])
    print ('Все теги:')
    for tag in tags:
        print(tag) #выводим по очереди каждый уникальный тег из нашего собранного списка

    input('Нажмите Enter')


def top_20_books(table):
    counts = {}
    for row in table:
        counts[row[1]] = counts.get(row[1], 0) + int(row[8])  #добавляем к текущему количеству просмотров книги (row[1] или 0 если не было до этого) новое значение из row[8]
    books = list(counts.items())                       #превращаем словарь в список кортежей (пар), чтобы его можно было отсортировать
    books.sort(key=lambda row: row[1], reverse = True) #сортируем список по значению популярности в обратном порядке (от большего к меньшему)
    print ('Топ 20 популярных книг:')
    for i in range(20):
        row = books[i]
        print (f'{i+1}. {row[0]}')
    input('Нажмите Enter')

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
        case '3':
            top_20_books(open_table())
        case '0':
            links(open_table()) 
            break
        case _:
            print('Нет пункта меню, нажмите Enter')
            input()


open_table()
length(open_table())
