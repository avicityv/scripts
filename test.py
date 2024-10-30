from tkinter import *
import psycopg2

class Form:
    def __init__(self, form_name, geom):
        self.root = Tk()
        self.root.title(form_name)
        self.root.geometry(geom)
        self.width = 50

class Entry_1:
    def __init__(self, form, label, data):
        self.lab_1 = Label(form.root, text=label)
        self.ent_1 = Entry(form.root, width=form.width + 16)
        self.lab_1.pack()
        self.ent_1.pack()
        self.ent_1.insert(0, data)
    
    def set_1(self, text):
        self.ent_1.delete(0, END)
        self.ent_1.insert(0, text)
    
    def get(self):
        return self.ent_1.get()

class Button_1:
    def __init__(self, form, text_b, width_b, height_b, command_b):
        self.b1 = Button(form.root, text=text_b, width=width_b, height=height_b)
        self.b1.config(command=command_b)
        self.b1.pack()

class Scene_1:
    def __init__(self):
        self.n = 0
        self.selected_table = 'поставщики'  # Начальная таблица
        self.setup_ui()
        self.load_data()
        self.update_entries()

    def setup_ui(self):
        self.form1 = Form('Форма для работы с таблицами', '500x500+400+200')
        
        # Выбор таблицы
        self.table_select = Entry_1(self.form1, 'Выберите таблицу:', self.selected_table)
        self.switch_table_button = Button_1(self.form1, "Переключить таблицу", 50, 2, self.switch_table)
        
        # Поля для данных (инициализация пустыми значениями)
        self.entries = [Entry_1(self.form1, f'Поле {i+1}:', '') for i in range(6)]
        
        # Кнопки для управления записями
        self.but_1 = Button_1(self.form1, "Следующая запись", 50, 2, self.next_record)
        self.but_2 = Button_1(self.form1, "Предыдущая запись", 50, 2, self.previous_record)
        self.but_3 = Button_1(self.form1, "Добавить запись", 50, 2, self.add_record)
        self.but_4 = Button_1(self.form1, "Удалить запись", 50, 2, self.delete_record)

        self.form1.root.mainloop()

    def load_data(self):
        # Загрузка данных из выбранной таблицы
        conn = psycopg2.connect(database="torg_firm", user="postgres", password="postgres", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM "{self.selected_table}";')
        self.rows = cur.fetchall()
        conn.close()
        if not self.rows:
            self.rows = [[0] * len(self.entries)]
        
        self.n = 0  # Сброс индекса для первой записи

    def switch_table(self):
        # Переключение таблицы
        self.selected_table = self.table_select.get()
        self.load_data()
        self.update_entries()

    def next_record(self):
        if self.n < len(self.rows) - 1:
            self.n += 1
            self.update_entries()

    def previous_record(self):
        if self.n > 0:
            self.n -= 1
            self.update_entries()

    def update_entries(self):
        # Обновление полей данных на основе текущей записи
        for i, entry in enumerate(self.entries):
            if i < len(self.rows[self.n]):
                entry.set_1(self.rows[self.n][i])
            else:
                entry.set_1('')  # Пустое поле, если данных меньше

    def add_record(self):
        # Добавление новой записи в текущую таблицу
        new_data = tuple(entry.get() for entry in self.entries)
        
        conn = psycopg2.connect(database="trading_firm", user="postgres", password="1", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        placeholders = ', '.join(['%s'] * len(new_data))
        cur.execute(f'INSERT INTO "{self.selected_table}" VALUES ({placeholders});', new_data)
        conn.commit()
        cur.close()
        conn.close()
        self.load_data()  # Обновление данных
        self.update_entries()

    def delete_record(self):
        # Удаление текущей записи из таблицы
        id_to_delete = self.entries[0].get()  # Предполагаем, что первый entry — это ID
        
         conn = psycopg2.connect(database="trading_firm", user="postgres", password="1", host="127.0.0.1", port="5432")
        cur = conn.cursor()
        cur.execute(f'DELETE FROM "{self.selected_table}" WHERE id=%s;', (id_to_delete,))
        conn.commit()
        cur.close()
        conn.close()
        
        self.load_data()  # Обновление данных
        self.update_entries()

scene = Scene_1()
