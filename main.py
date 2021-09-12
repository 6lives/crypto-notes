from bs4 import BeautifulSoup
import requests, fake_useragent
import time
from pyfiglet import Figlet
import os, sys
import json


class Main_loop():

    def menu(self):
        #название проги
        text = Figlet(font='slant')
        print(text.renderText('Crypto-Notes'))
        #заголовок
        print('Название монеты  ', 'Количество  ' , ' Цена  ', ' Профит ','\n\n')
        check = os.path.isfile('db.json')
        no = 0
        if check:
            with open('db.json') as file:
                some = json.load(file)
            for id, items in some.items():
                    print(no+1,')', items['name'], items['count'] ,items['price'], '(ваш профит):', (float(items['act_price']) - float(items['price'])) * float(items['count']) ,'$')
                    no +=1

        print(f'\n\n 1) Добавить заметку \n', '2) Выход \n')
        user_imp = input('Ввод: ')
        if user_imp == '1':
            os.system('cls')
            self.add_new()
        elif user_imp == '2':
            sys.exit()

    def add_new(self):
        #счетчик для добавления айди
        self.id_no = 0
        check = os.path.isfile('db.json')
        if check:
            with open('db.json') as file:
                some = json.load(file)
            for keys in some:
                self.id_no +=1

        #дозапись данных в json
        #title = input('заголовок: ')
        name = input('Название: ')
        count = input('Сколько штук: ')
        price = float(input('Цена: '))
        act_price = self.parser(name)
        new_pin = {'name':name, 'price':price,'count': count, 'act_price': act_price}
        if check:
            some.update({f'id{self.id_no + 1}' : new_pin})
        with open('db.json', 'w') as file:
            if check:
                json.dump(some, file, indent=4, ensure_ascii=False)
            else:
                x = {'id1': new_pin}
                json.dump(x, file, indent=4, ensure_ascii=False)
        os.system('cls')
        self.menu()

    def parser(self, name):
        #сетап для захвата страницы
        url = name
        UsAg = fake_useragent.UserAgent()
        user = UsAg.random
        self.header = {'User-Agent': str(user)}
        self.ipSite = f'https://coinmarketcap.com/currencies/{url}/'
        #перехватываем страницу и начинаем поиск числа на ней
        adress = requests.get(self.ipSite, headers=self.header)
        soup = BeautifulSoup(adress.text, "lxml")
        try:
            price = soup.find(class_= 'priceValue').text
        except Exception:
            print('ошибка в наименовании валюты')
        #так как цифра достается в виде строки с доп символами, конвертируем ее в нужный вид
        price = price.replace('$','')
        price = price.replace(',','')
        act_price = float(price)
        act_price = "{:.4f}".format(act_price)
        return act_price

if __name__ == '__main__':
    x = Main_loop()
    x.menu()
    #x.add_new()
