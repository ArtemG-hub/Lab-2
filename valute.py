import xml.dom.minidom as minidom

xml_file = open('currency.xml', 'r')
xml_data = xml_file.read()          #считываем содержимое в виде одной длинной строки

dom = minidom.parseString(xml_data) #превращаем текстовую строку в древовидную структуру (DOM-дерево) с которой Python умеет работать
dom.normalize()                     #нормализуем дерево: объединяем соседние текстовые узлы и удаляем пустые (очищаем структуру)

elements = dom.getElementsByTagName('Valute') #ищем в дереве абсолютно все теги с именем Valute и сохраняем этот список в elements
currency_dict = {}

for node in elements:                         #для конкретной валюты из всего списка запускаем цикл (и так по всем валютам)
    for child in node.childNodes:             #для конкретной валюты перебираем все ее внутренности
        if child.nodeType == 1:               #проверяем, что перед нами полноценный тег (с помощью цифры 1) а не пробел или перенос строки
            if child.tagName == 'Name':       #если тег name то...
                if child.firstChild.nodeType == 3:   #если тег содержит текст (проверяем с помощью кода 3) 
                    title = child.firstChild.data    #то записываем текст в title
            if child.tagName == 'CharCode':          #аналогично
                if child.firstChild.nodeType == 3:
                    code = child.firstChild.data
    currency_dict[title] = code   #кладём в наш словарь готовую пару — название валюты и её код. title: code

print(currency_dict)

xml_file.close()   #закрываем файл чтобы он не висел в памяти компьютера
