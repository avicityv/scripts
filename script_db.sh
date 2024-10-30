export PGPASSWORD='postgres';
psql -U postgres -c "-- Создание базы данных
CREATE DATABASE torg_firm;

-- Подключение к базе данных
\c torg_firm;

-- Таблица для клиентов
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT
);

-- Таблица для товаров
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    category_id INT REFERENCES categories(category_id)
);

-- Таблица для категорий
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Таблица для заказов
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(10, 2) NOT NULL
);

-- Таблица для товаров в заказах (связующая таблица)
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);

-- Таблица для поставщиков
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT
);

-- Таблица для платежей
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount NUMERIC(10, 2) NOT NULL,
    payment_method VARCHAR(50)
);

-- Таблица для сотрудников
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100),
    hire_date DATE,
    salary NUMERIC(10, 2)
);
-- Заполнение таблицы customers
INSERT INTO customers (name, email, phone, address) VALUES
('Иван Иванов', 'ivan@example.com', '1234567890', 'г. Москва, ул. Пушкина, д. 1'),
('Светлана Петрова', 'svetlana@example.com', '0987654321', 'г. Санкт-Петербург, ул. Ленина, д. 2'),
('Алексей Смирнов', 'alexey@example.com', '1122334455', 'г. Казань, ул. Горького, д. 3'),
('Мария Кузнецова', 'maria@example.com', '5566778899', 'г. Новосибирск, ул. Чкалова, д. 4'),
('Дмитрий Васильев', 'dmitry@example.com', '2233445566', 'г. Екатеринбург, ул. Лермонтова, д. 5');

-- Заполнение таблицы categories
INSERT INTO categories (name) VALUES
('Электроника'),
('Одежда'),
('Книги'),
('Косметика'),
('Спорт');

-- Заполнение таблицы products
INSERT INTO products (name, description, price, stock_quantity, category_id) VALUES
('Смартфон', 'Современный смартфон с 128 ГБ памяти', 29999.99, 50, 1),
('Куртка', 'Тёплая зимняя куртка', 4999.99, 30, 2),
('Роман', 'Интересный роман для чтения', 399.99, 100, 3),
('Помада', 'Нежная губная помада', 199.99, 200, 4),
('Футбольный мяч', 'Мяч для игры в футбол', 1499.99, 20, 5);

-- Заполнение таблицы orders
INSERT INTO orders (customer_id, total_amount) VALUES
(1, 34999.98),
(2, 5199.98),
(3, 399.99),
(4, 199.99),
(5, 1499.99);

-- Заполнение таблицы order_items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 29999.99),
(1, 4, 2, 199.99),
(2, 2, 1, 4999.99),
(3, 3, 1, 399.99),
(5, 5, 1, 1499.99);

-- Заполнение таблицы suppliers
INSERT INTO suppliers (name, contact_name, phone, address) VALUES
('ТехноМаг', 'Андрей Андреев', '1112223334', 'г. Москва, ул. Технологическая, д. 10'),
('ОдеждаПро', 'Елена Еленова', '4445556667', 'г. Санкт-Петербург, ул. Модная, д. 11'),
('Книжный мир', 'Сергей Сергеев', '7778889990', 'г. Казань, ул. Литературная, д. 12'),
('Косметика Плюс', 'Анна Антонова', '0001112223', 'г. Новосибирск, ул. Красоты, д. 13'),
('СпортГид', 'Игорь Игорев', '3334445556', 'г. Екатеринбург, ул. Спортивная, д. 14');

-- Заполнение таблицы payments
INSERT INTO payments (order_id, amount, payment_method) VALUES
(1, 34999.98, 'Кредитная карта'),
(2, 5199.98, 'Наличные'),
(3, 399.99, 'Кредитная карта'),
(4, 199.99, 'Электронный кошелёк'),
(5, 1499.99, 'Наличные');

-- Заполнение таблицы employees
INSERT INTO employees (name, position, hire_date, salary) VALUES
('Ольга Романова', 'Менеджер по продажам', '2023-01-15', 60000.00),
('Виктор Николаев', 'Секретарь', '2022-05-20', 40000.00),
('Анна Мартынова', 'Бухгалтер', '2021-08-30', 50000.00),
('Максим Сидоров', 'Логист', '2020-11-05', 55000.00),
('Екатерина Тихонова', 'Маркетолог', '2019-03-10', 65000.00);
"
psql -U postgres -d mydatabase -c "\d"
