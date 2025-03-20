CREATE TABLE юридический_адрес (
    id SERIAL PRIMARY KEY,
    Индекс INT,
    Регион VARCHAR(50),
    Город VARCHAR(50),
    Улица VARCHAR(50),
    Дом INT
);

CREATE TABLE тип_склада (
    id SERIAL PRIMARY KEY,
    Наименование VARCHAR(50)
);

CREATE TABLE склад (
    id SERIAL PRIMARY KEY,
    Название VARCHAR(50),
    id_тип INT REFERENCES тип_склада(id),
    Описание VARCHAR(255),
    id_юр_адрес INT REFERENCES юридический_адрес(id)
);

CREATE TABLE тип_продукции (
    id SERIAL PRIMARY KEY,
    Наименование VARCHAR(50)
);

CREATE TABLE продукция (
    id SERIAL PRIMARY KEY,
    id_тип INT REFERENCES тип_продукции(id),
    Наименование VARCHAR(50),
    Описание VARCHAR(255),
    Мин_стоимость FLOAT,
    Размер_упаковки VARCHAR(50),
    Вес_без_упаковки INT,
    Вес_с_упаковкой INT,
    Сертификат_качества VARCHAR(255),
    Себестоимость FLOAT
);

CREATE TABLE паспорт (
    id SERIAL PRIMARY KEY,
    Серия INT,
    Номер INT,
    Кем_выдан VARCHAR(255),
    Дата_выдачи DATE
);

CREATE TABLE банковские_реквизиты (
    id SERIAL PRIMARY KEY,
    Название_организации VARCHAR(255),
    Название_банка VARCHAR(255),
    ИНН VARCHAR(10),
    БИК VARCHAR(9),
    Корреспондентский_счет VARCHAR(255)
);

CREATE TABLE должность (
    id SERIAL PRIMARY KEY,
    Наименование VARCHAR(50)
);

CREATE TABLE сотрудник (
    id SERIAL PRIMARY KEY,
    Фамилия VARCHAR(50),
    Имя VARCHAR(50),
    Отчество VARCHAR(50),
    Дата_рождения DATE,
    id_паспорт INT REFERENCES паспорт(id),
    id_банк_реквизиты INT REFERENCES банковские_реквизиты(id),
    id_должность INT REFERENCES должность(id),
    Логин VARCHAR(50),
    Пароль VARCHAR(255)
);

CREATE TABLE поступление_товара (
    id SERIAL PRIMARY KEY,
    id_продукция INT REFERENCES продукция(id),
    id_склад INT REFERENCES склад(id),
    Дата_поступления TIMESTAMP,
    Кол_во_товара INT
);

CREATE TABLE перемещение_продукции (
    id SERIAL PRIMARY KEY,
    id_продукции INT REFERENCES продукция(id),
    id_склад_откуда INT REFERENCES склад(id),
    id_склад_куда INT REFERENCES склад(id),
    Количество INT,
    Дата_перемещения TIMESTAMP,
    Статус VARCHAR(50),
    id_сотрудник INT REFERENCES сотрудник(id)
);

CREATE TABLE продукция_на_складе (
    id SERIAL PRIMARY KEY,
    id_склада INT REFERENCES склад(id),
    id_продукции INT REFERENCES продукция(id),
    Количество INT
);

CREATE TABLE тип_партнера (
    id SERIAL PRIMARY KEY,
    Наименование VARCHAR(50)
);

CREATE TABLE партнер (
    id SERIAL PRIMARY KEY,
    id_юр_адрес INT REFERENCES юридический_адрес(id),
    Наименование VARCHAR(255),
    ИНН VARCHAR(20),
    ФИО_директора VARCHAR(255),
    id_тип INT REFERENCES тип_партнера(id),
    Телефон VARCHAR(11),
    Email VARCHAR(255),
    Места_продаж VARCHAR(255)
);

CREATE TABLE заказ (
    id SERIAL PRIMARY KEY,
    Дата_создания DATE,
    Статус VARCHAR(50),
    id_сотрудник INT REFERENCES сотрудник(id),
    id_партнер INT REFERENCES партнер(id),
    Предоплата FLOAT,
    Согласована BOOLEAN
);

CREATE TABLE заказ_продукции (
    id SERIAL PRIMARY KEY,
    id_заказа INT REFERENCES заказ(id),
    id_продукции INT REFERENCES продукция(id),
    Количество INT,
    Стоимость FLOAT
);