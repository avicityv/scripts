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
        self.table = "customers"  # Начальная таблица
        self.tables = {
            "customers": ["customer_id", "name", "email", "phone", "address"],
            "employees": ["employee_id", "name", "position", "hire_date", "salary"],
            "suppliers": ["supplier_id", "name", "contact_name", "phone", "address"],
            "categories": ["category_id", "name"],
            "products": ["product_id", "name", "description", "price", "stock_quantity", "category_id"],
            "orders": ["order_id", "customer_id", "order_date", "total_amount"],
            "order_items": ["order_item_id", "order_id", "product_id", "quantity", "price"],
            "payments": ["payment_id", "order_id", "payment_date", "amount", "payment_method"]
        }

        # Параметры подключения
        self.db_name = "trading_firm"
        self.db_user = "postgres"
        self.db_password = "postgres"
        self.db_host = "127.0.0.1"  # Базовое значение IP-адреса

        self.form1 = Form('Выбор таблицы', '600x600+400+200')
        self.create_table_selector()
        self.entries = []  # Инициализация self.entries перед вызовом load_data
        self.load_data()
        self.create_entries()
        self.form1.root.mainloop()

    def create_table_selector(self):
        self.table_var = StringVar(self.form1.root)
        self.table_var.set(self.table)
        self.table_menu = OptionMenu(self.form1.root, self.table_var, *self.tables.keys(), command=self.change_table)
        self.table_menu.pack()

    def create_entries(self):
        # Очистка предыдущих записей
        for entry in self.entries:
            entry.lab_1.pack_forget()
            entry.ent_1.pack_forget()
        self.entries.clear()
        
        for column_name in self.tables[self.table]:
            entry = Entry_1(self.form1, column_name + ":", "")
            self.entries.append(entry)
        
        self.but_1 = Button_1(self.form1, "Следующая запись", 50, 2, self.next_record)
        self.but_2 = Button_1(self.form1, "Предыдущая запись", 50, 2, self.previous_record)
        self.but_3 = Button_1(self.form1, "Добавить запись", 50, 2, self.add_record)
        self.but_4 = Button_1(self.form1, "Удалить запись", 50, 2, self.delete_record)

    def load_data(self):
        conn = psycopg2.connect(database=self.db_name, user=self.db_user, password=self.db_password, host=self.db_host, port="5432")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {self.table};')
        self.rows = cur.fetchall()
        conn.close()
        if not self.rows:
            self.rows = [[None] * len(self.tables[self.table])]

        self.n = 0
        self.update_entries()

    def update_entries(self):
        for i, entry in enumerate(self.entries):
            entry.set_1(self.rows[self.n][i])

    def next_record(self):
        if self.n < len(self.rows) - 1:
            self.n += 1
            self.update_entries()

    def previous_record(self):
        if self.n > 0:
            self.n -= 1
            self.update_entries()

    def add_record(self):
        new_data = tuple(entry.get() for entry in self.entries)
        
        conn = psycopg2.connect(database=self.db_name, user=self.db_user, password=self.db_password, host=self.db_host, port="5432")
        cur = conn.cursor()
        cur.execute(f'INSERT INTO {self.table} VALUES (DEFAULT, {", ".join(["%s"] * len(new_data))});', new_data)
        conn.commit()
        cur.close()
        conn.close()
        self.load_data()

    def delete_record(self):
        id_to_delete = self.entries[0].get()
        
        conn = psycopg2.connect(database=self.db_name, user=self.db_user, password=self.db_password, host=self.db_host, port="5432")
        cur = conn.cursor()
        cur.execute(f'DELETE FROM {self.table} WHERE {self.tables[self.table][0]}=%s;', (id_to_delete,))
        conn.commit()
        cur.close()
        conn.close()
        
        self.load_data()

    def change_table(self, selected_table):
        self.table = selected_table
        self.load_data()
        self.create_entries()

# Установка IP-адреса базы данных
db_host = "127.0.0.1"  # Базовый IP-адрес
scene = Scene_1()
