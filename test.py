import tkinter as tk
import psycopg2

class EntryField:
    """Поле ввода с меткой для отображения данных из базы данных."""
    def __init__(self, form, label_text, width=50):
        self.label = tk.Label(form, text=label_text)
        self.entry = tk.Entry(form, width=width)
        self.label.pack()
        self.entry.pack()

    def set_value(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

    def get_value(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, tk.END)


class DatabaseApp:
    def __init__(self):
        # Настройка основного окна
        self.root = tk.Tk()
        self.root.title("Database GUI")
        self.root.geometry("600x600")

        # Подключение к базе данных
        self.db_config = {
            "database": "trading_firm",
            "user": "postgres",
            "password": "postgres",
            "host": "127.0.0.1",
            "port": "5432"
        }

        # Данные о таблицах
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

        # Переменные для хранения текущего состояния
        self.current_table = "customers"
        self.current_row_index = 0
        self.rows = []

        # Интерфейс
        self.create_widgets()
        self.load_table_data()

        self.root.mainloop()

    def create_widgets(self):
        """Создание интерфейса"""
        # Меню для выбора таблицы
        self.table_var = tk.StringVar(self.root)
        self.table_var.set(self.current_table)
        self.table_menu = tk.OptionMenu(self.root, self.table_var, *self.tables.keys(), command=self.on_table_change)
        self.table_menu.pack()

        # Поля ввода
        self.entry_fields = []
        self.update_entry_fields()

        # Кнопки управления
        self.btn_next = tk.Button(self.root, text="Следующая запись", command=self.next_record)
        self.btn_next.pack()

        self.btn_prev = tk.Button(self.root, text="Предыдущая запись", command=self.previous_record)
        self.btn_prev.pack()

        self.btn_add = tk.Button(self.root, text="Добавить запись", command=self.add_record)
        self.btn_add.pack()

        self.btn_delete = tk.Button(self.root, text="Удалить запись", command=self.delete_record)
        self.btn_delete.pack()

    def update_entry_fields(self):
        """Обновление полей ввода при смене таблицы"""
        # Очистка старых полей
        for field in self.entry_fields:
            field.label.destroy()
            field.entry.destroy()
        self.entry_fields = []

        # Создание новых полей ввода на основе выбранной таблицы
        for column in self.tables[self.current_table]:
            entry_field = EntryField(self.root, column + ":")
            self.entry_fields.append(entry_field)

    def on_table_change(self, selected_table):
        """Смена таблицы и обновление данных"""
        self.current_table = selected_table
        self.current_row_index = 0
        self.update_entry_fields()
        self.load_table_data()

    def load_table_data(self):
        """Загрузка данных из выбранной таблицы"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.current_table}")
            self.rows = cursor.fetchall()
            conn.close()
            self.current_row_index = 0
            self.update_entry_values()
        except Exception as e:
            print("Ошибка при загрузке данных:", e)

    def update_entry_values(self):
        """Обновление значений в полях ввода на основе текущей записи"""
        if self.rows:
            current_row = self.rows[self.current_row_index]
            for entry_field, value in zip(self.entry_fields, current_row):
                entry_field.set_value(value)
        else:
            # Очистка полей, если данных нет
            for entry_field in self.entry_fields:
                entry_field.clear()

    def next_record(self):
        """Переход к следующей записи"""
        if self.rows and self.current_row_index < len(self.rows) - 1:
            self.current_row_index += 1
            self.update_entry_values()

    def previous_record(self):
        """Переход к предыдущей записи"""
        if self.rows and self.current_row_index > 0:
            self.current_row_index -= 1
            self.update_entry_values()

    def add_record(self):
        """Добавление новой записи в таблицу"""
        new_data = [entry_field.get_value() for entry_field in self.entry_fields]
        placeholders = ', '.join(['%s'] * len(new_data))
        query = f"INSERT INTO {self.current_table} VALUES (DEFAULT, {placeholders})"

        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute(query, new_data)
            conn.commit()
            conn.close()
            self.load_table_data()  # Перезагрузка данных после добавления
        except Exception as e:
            print("Ошибка при добавлении записи:", e)

    def delete_record(self):
        """Удаление текущей записи из таблицы"""
        if not self.rows:
            return  # Нет данных для удаления

        record_id = self.rows[self.current_row_index][0]
        primary_column = self.tables[self.current_table][0]
        query = f"DELETE FROM {self.current_table} WHERE {primary_column} = %s"

        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute(query, (record_id,))
            conn.commit()
            conn.close()
            self.load_table_data()  # Перезагрузка данных после удаления
        except Exception as e:
            print("Ошибка при удалении записи:", e)

