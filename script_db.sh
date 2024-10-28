export PGPASSWORD='postgres';
psql -U postgres
CREATE DATABASE mydatabase;
\q
psql -U postgres -d mydatabase
CREATE TABLE Товары (
    ID_товара SERIAL PRIMARY KEY,
    Название_товара VARCHAR(255),
    Количество_на_складе INT,
    Ед_измерения VARCHAR(50),
    Цена_за_единицу NUMERIC
);

-- Создаем таблицу для клиентов
CREATE TABLE Клиент (
    ID_клиента SERIAL PRIMARY KEY,
    Фамилия_контактного_лица VARCHAR(255),
    Имя_контактного_лица VARCHAR(255),
    Отчество_контактного_лица VARCHAR(255),
    Телефон_контактного_лица VARCHAR(50),
    Название_клиента VARCHAR(255),
    Страна_клиента VARCHAR(255),
    Город_клиента VARCHAR(255),
    Улица_клиента VARCHAR(255),
    Дом_клиента VARCHAR(50),
    Квартира_офис_клиента VARCHAR(50)
);

-- Создаем таблицу для сотрудников
CREATE TABLE Сотрудник (
    ID_сотрудника SERIAL PRIMARY KEY,
    Фамилия_сотрудника VARCHAR(255),
    Имя_сотрудника VARCHAR(255),
    Отчество_сотрудника VARCHAR(255),
    Паспортные_данные VARCHAR(50),
    Страна_регистрации VARCHAR(255),
    Город_регистрации VARCHAR(255),
    Улица_регистрации VARCHAR(255),
    Дом_регистрации VARCHAR(50),
    Квартира_офис_регистрации VARCHAR(50),
    Телефон VARCHAR(50),
    ID_должности INT
);

-- Создаем таблицу для должностей
CREATE TABLE Должность (
    ID_должности SERIAL PRIMARY KEY,
    Название_должности VARCHAR(255),
    Зарплата NUMERIC
);

-- Создаем таблицу для заказов
CREATE TABLE Заказы (
    №_заказа SERIAL PRIMARY KEY,
    Дата_заказа DATE,
    Дата_доставки DATE,
    Страна_доставки VARCHAR(255),
    Город_доставки VARCHAR(255),
    Улица_доставки VARCHAR(255),
    Дом_доставки VARCHAR(50),
    Квартира_офис_доставки VARCHAR(50),
    ID_клиента INT REFERENCES Клиент(ID_клиента)
);

-- Создаем таблицу для выполнения заказов
CREATE TABLE Исполнение_заказов (
    ID_процесса SERIAL PRIMARY KEY,
    №_заказа INT REFERENCES Заказы(№_заказа),
    ID_сотрудника INT REFERENCES Сотрудник(ID_сотрудника)
);

-- Создаем таблицу для комплектации заказов
CREATE TABLE Комплектация_заказа (
    ID_процесса SERIAL PRIMARY KEY,
    ID_товара INT REFERENCES Товары(ID_товара),
    №_заказа INT REFERENCES Заказы(№_заказа)
);

-- Создаем таблицу для оплаты
CREATE TABLE Оплата (
    №_транзакции SERIAL PRIMARY KEY,
    Дата_оплаты DATE,
    Сумма NUMERIC,
    ID_клиента INT REFERENCES Клиент(ID_клиента)
);
\d