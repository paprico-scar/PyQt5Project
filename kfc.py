import sqlite3
import sys
import datetime as dt
from PyQt5 import uic
from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog


class Menu(QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        self.dict_order = {}
        self.initUI()
        self.con = sqlite3.connect("KFCmenu.db")
        self.q = 0  # Нумерация id в таблице tb_order от 1 и т.д
        cur = self.con.cursor()
        # Удаление старой таблицы
        cur.execute("""DROP TABLE IF EXISTS tb_order""")
        self.con.commit()

    def add_in_basket(self, product):
        cur = self.con.cursor()
        # Создание таблицы, если ее нет!!!
        cur.execute("""CREATE TABLE IF NOT EXISTS tb_order(
        id INTEGER,
        name TEXT,
        price INT,
        k INT,
        price_k INT
        )
        """)
        self.con.commit()
        # Узнаем цену товара и сохраняем в переменной price
        cur.execute("""SELECT price FROM tb_menu WHERE dish_name = '{}'""".format(product))
        price = cur.fetchall()[0][0]
        # Если product выбирают два или более раз, то мы меняем информацию о кол-ве и цены на кол-во в tb_order
        if product in self.dict_order:
            self.dict_order[product] += 1
            cur.execute("""UPDATE tb_order SET k='{}' WHERE name='{}'""".format(self.dict_order[product], product))
            self.con.commit()
            cur.execute("""UPDATE tb_order
            SET price_k='{}' WHERE name='{}'""".format(self.dict_order[product] * price, product))
            self.con.commit()
        # Если product выьираю впервыен , то мы добовляем этот product в tb_order
        else:
            self.q += 1
            add_list = [self.q, product, price, 1, price]
            cur.execute("INSERT INTO tb_order VALUES(?,?,?,?,?);", add_list)
            self.con.commit()
            self.dict_order[product] = 1
        # При измениении или добавении в таблице товаров в korzina меняется информация о заказе
        self.korzina.clear()
        self.korzina.addItem('Название товара:    Кол-во:    Цена:')
        add_listwidget = cur.execute('''SELECT name, k, price_k FROM tb_order''').fetchall()
        for i in add_listwidget:
            convent_into_str = [str(j) for j in i]
            self.korzina.addItem('     '.join(convent_into_str))

    def initUI(self):
        # Загрузка в проект внешнегшо вида программы
        uic.loadUi('primer.ui', self)
        # Подключение всех кнопок к функции add_in_basket с определенным значением
        self.baskdobra8ostr.clicked.connect(partial(self.add_in_basket, 'Баскет Добра 8 ножек острый'))
        self.baskdobra8orig.clicked.connect(partial(self.add_in_basket, 'Баскет Добра 8 ножек оригинальный'))
        self.baskdobraL.clicked.connect(partial(self.add_in_basket, 'Баскет Добра L'))
        self.baskdobraM.clicked.connect(partial(self.add_in_basket, 'Баскет Добра M'))
        self.baskdobraS.clicked.connect(partial(self.add_in_basket, 'Баскет Добра S'))
        self.baskdyetorig.clicked.connect(partial(self.add_in_basket, 'Баскет Дуэт оригинальный'))
        self.baskdyetostr.clicked.connect(partial(self.add_in_basket, 'Баскет Дуэт острый'))
        self.baskostrkrlL.clicked.connect(partial(self.add_in_basket, 'Баскет L с острыми крылышками'))
        self.baskostrkrlM.clicked.connect(partial(self.add_in_basket, 'Баскет M с острыми крылышками'))
        self.baskostrkrlS.clicked.connect(partial(self.add_in_basket, 'Баскет S с острыми крылышками'))
        self.dombaskorig.clicked.connect(partial(self.add_in_basket, 'Домашний Баскет оригинальный'))
        self.dombaskostr.clicked.connect(partial(self.add_in_basket, 'Домашний Баскет острый'))
        self.chefbur.clicked.connect(partial(self.add_in_basket, 'Шефбургер'))
        self.chefburdeluks.clicked.connect(partial(self.add_in_basket, 'Шефбургер Де Люкс'))
        self.chefburdeluksostr.clicked.connect(partial(self.add_in_basket, 'Шефбургер Де Люкс острый'))
        self.chefburjun.clicked.connect(partial(self.add_in_basket, 'Шефбургер Джуниор'))
        self.chefburostr.clicked.connect(partial(self.add_in_basket, 'Шефбургер острый'))
        self.cheesburgdeluks.clicked.connect(partial(self.add_in_basket, 'Чизбургер Де Люкс'))
        self.boxorig.clicked.connect(partial(self.add_in_basket, 'Боксмастер оригинальный'))
        self.boxostr.clicked.connect(partial(self.add_in_basket, 'Боксмастер острый'))
        self.tvistorig.clicked.connect(partial(self.add_in_basket, 'Твистер оригинальный'))
        self.tvistostr.clicked.connect(partial(self.add_in_basket, 'Твистер острый'))
        self.tvistdeluksorig.clicked.connect(partial(self.add_in_basket, 'Твистер Де Люкс оригинальный'))
        self.tivstdeluksostr.clicked.connect(partial(self.add_in_basket, 'Твистер Де Люкс острый'))
        self.ketchup.clicked.connect(partial(self.add_in_basket, 'Кетчуп Томатный'))
        self.sousbbq.clicked.connect(partial(self.add_in_basket, 'Соус Барбекю'))
        self.souschees.clicked.connect(partial(self.add_in_basket, 'Соус Сырный'))
        self.sousgarlic.clicked.connect(partial(self.add_in_basket, 'Соус Чесночный'))
        self.sousteriyaki.clicked.connect(partial(self.add_in_basket, 'Соус Терияки'))
        self.pepsi.clicked.connect(partial(self.add_in_basket, 'Pepsi'))
        self.mirinda.clicked.connect(partial(self.add_in_basket, 'Mirinda'))
        self.up.clicked.connect(partial(self.add_in_basket, '7up'))
        self.lipton.clicked.connect(partial(self.add_in_basket, 'Чай Lipton Лимон'))
        self.icebanana.clicked.connect(partial(self.add_in_basket, 'Мороженое банановое'))
        self.icekaramel.clicked.connect(partial(self.add_in_basket, 'Мороженое карамельное'))
        self.icechokolate.clicked.connect(partial(self.add_in_basket, 'Мороженое шеколадное'))
        self.iceklubnika.clicked.connect(partial(self.add_in_basket, 'Мороженое клубничное'))
        self.icerojok.clicked.connect(partial(self.add_in_basket, 'Мороженое "Рожок"'))
        # Подключение кнопок clear и end к фунуциям delete_all_from_basket и end
        self.clear.clicked.connect(self.delete_all_from_basket)
        self.all_end.clicked.connect(self.end)

    def delete_all_from_basket(self):
        # Очищаем все из dict_order, korzina, output_line и удаляем таблицу tb_order
        self.korzina.clear()
        self.dict_order = {}
        cur = self.con.cursor()
        cur.execute("""DROP TABLE IF EXISTS tb_order""")
        self.con.commit()
        self.output_line.setText('')

    def end(self):
        # Проверка на исключения если пользователь ничего не выберет и завершит заказ
        try:
            # Спрашиваем имя пользователя для того, чтобы добавть имя в чек
            name, ok_pressed = QInputDialog.getText(self, "Введите имя", "Как вас зовут?")
            if ok_pressed:
                # Узнаем цену за заказ и сохраняеим в переменной result
                cur = self.con.cursor()
                cur.execute("""SELECT SUM(price_k) FROM tb_order""")
                result = cur.fetchone()
                # Выводим результат в output_line
                self.output_line.setText(str(result[0]) + ' рублей')
                # Узнаем последний id в таблице tb_checks
                cur = self.con.cursor()
                new_id = cur.execute("""SELECT MAX(id) FROM tb_checks""").fetchone()
                # Узнаем дату в которую был сделан заказ
                data = str(dt.datetime.now().date())
                # Создаем название чека(файла)
                file_name = data + '-' + str(new_id[0] + 1)
                # Создаем список для того чтобы добавть название файла в таблицу tb_checks и список для добаления в файл
                # информации о заказе
                add_in_tb_checks = [new_id[0] + 1, file_name]
                add_in_file = cur.execute("""SELECT name, k, price_k FROM tb_order""").fetchall()
                # Создаем txt файл в котором будет чек
                f = open('checks/{}.txt'.format(file_name), 'w')
                # Небольшое оформление чека
                f.write('-' * 35 + '\n')
                f.write('Чек: №{}\n'.format(file_name))
                f.write('Имя покупателя: {}\n'.format(name))
                f.write('Дата покупи: {}'.format(data) + '\n')
                f.write('Место: Вариативное меню KFC v2.0\n')
                f.write('Название товара:    Кол-во:    Цена:\n')
                # Добавление в чек информации из списка add_in_file
                for i in add_in_file:
                    for j in i:
                        f.write(str(j) + '\t')
                    f.write('\n')
                # Опять небольшое оформление чека
                f.write('-' * 35 + '\n')
                f.write('ИТОГ:                         ={}'.format(str(result[0])) + '\n')
                f.write('-' * 35 + '\n')
                f.write('Продавец: Cотников Ярослав)' + '\n')
                f.write('Спасибо за покупку <3')
                f.close()
                # Добаление названия файла в таблицу tb_checks
                cur.execute("INSERT INTO tb_checks VALUES(?,?);", add_in_tb_checks)
                self.con.commit()  # сохраняем результат
        except Exception:
            # Если происходит ошибка в output_line ничего не выводится
            self.output_line.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())
