-- 1. юридический_адрес
INSERT INTO юридический_адрес (Индекс, Регион, Город, Улица, Дом) VALUES
(101000, 'Москва', 'Москва', 'Ленинградский проспект', 15),
(630099, 'Новосибирская область', 'Новосибирск', 'Советская', 23),
(344000, 'Ростовская область', 'Ростов-на-Дону', 'Буденновский проспект', 42),
(620000, 'Свердловская область', 'Екатеринбург', 'Малышева', 71),
(443000, 'Самарская область', 'Самара', 'Московское шоссе', 17);

-- 2. тип_склада
INSERT INTO тип_склада (Наименование) VALUES
('Холодильный'),
('Сухой'),
('Оптовый'),
('Розничный'),
('Транзитный');

-- 3. склад
INSERT INTO склад (Название, id_тип, Описание, id_юр_адрес) VALUES
('Склад Москва-1', 1, 'Холодильный склад для скоропортящихся товаров', 1),
('Склад НСК-Центр', 2, 'Сухой склад для длительного хранения', 2),
('Склад Ростов-Опт', 3, 'Оптовый склад для крупных партий', 3),
('Склад ЕКБ-Розница', 4, 'Склад для розничной торговли', 4),
('Склад Самара-Т', 5, 'Транзитный склад для перегрузки', 5);

-- 4. тип_продукции
INSERT INTO тип_продукции (Наименование) VALUES
('Молочная продукция'),
('Мясные изделия'),
('Бакалея'),
('Напитки'),
('Кондитерские изделия');

-- 5. продукция
INSERT INTO продукция (id_тип, Наименование, Описание, Мин_стоимость, Размер_упаковки, Вес_без_упаковки, Вес_с_упаковкой, Сертификат_качества, Себестоимость) VALUES
(1, 'Молоко 3.2%', 'Пастеризованное молоко', 45.50, '1л', 950, 1000, 'ГОСТ 31450-2013', 30.00),
(2, 'Колбаса Сервелат', 'Колбаса варено-копченая', 350.00, '400г', 380, 400, 'ГОСТ 31785-2012', 280.00),
(3, 'Рис длиннозерный', 'Рис белый шлифованный', 80.00, '1кг', 980, 1000, 'ГОСТ 6292-93', 60.00),
(4, 'Сок яблочный', 'Сок натуральный осветленный', 90.00, '1л', 950, 1000, 'ГОСТ 32101-2013', 65.00),
(5, 'Шоколад молочный', 'Шоколад с орехами', 120.00, '100г', 95, 100, 'ГОСТ 31721-2012', 90.00);

-- 6. паспорт
INSERT INTO паспорт (Серия, Номер, Кем_выдан, Дата_выдачи) VALUES
(4510, 123456, 'Отделением УФМС по г. Москва', '2015-06-15'),
(4512, 654321, 'ОВД г. Новосибирск', '2016-08-20'),
(4515, 789123, 'УМВД по Ростовской области', '2017-03-10'),
(4518, 456789, 'Отделом МВД по г. Екатеринбург', '2018-11-25'),
(4520, 321987, 'УФМС г. Самара', '2019-05-30');

-- 7. банковские_реквизиты
INSERT INTO банковские_реквизиты (Название_организации, Название_банка, ИНН, БИК, Корреспондентский_счет) VALUES
('ООО "ТоргПром"', 'Сбербанк', '7701234567', '044525225', '30101810400000000225'),
('ООО "СибирьТорг"', 'ВТБ', '5401234567', '045209777', '30101810900000000777'),
('ООО "ЮгСнаб"', 'Альфа-Банк', '6161234567', '046015602', '30101810600000000602'),
('ООО "УралТрейд"', 'Тинькофф', '6671234567', '044583974', '30101810145250000974'),
('ООО "ВолгаЭкспорт"', 'Росбанк', '6311234567', '044030861', '30101810000000000861');

-- 8. должность
INSERT INTO должность (Наименование) VALUES
('Менеджер'),
('Кладовщик'),
('Бухгалтер'),
('Водитель'),
('Директор');

-- 9. сотрудник
INSERT INTO сотрудник (Фамилия, Имя, Отчество, Дата_рождения, id_паспорт, id_банк_реквизиты, id_должность, Логин, Пароль) VALUES
('Иванов', 'Петр', 'Сергеевич', '1985-03-15', 1, 1, 1, 'ivanov_p', 'pass123'),
('Петрова', 'Анна', 'Викторовна', '1990-07-22', 2, 2, 2, 'petrova_a', 'secure456'),
('Сидоров', 'Алексей', 'Иванович', '1988-11-10', 3, 3, 3, 'sidorov_a', 'qwerty789'),
('Кузнецова', 'Елена', 'Дмитриевна', '1992-05-05', 4, 4, 4, 'kuznetsova_e', 'driver101'),
('Морозов', 'Дмитрий', 'Александрович', '1980-09-30', 5, 5, 5, 'morozov_d', 'admin2020');

-- 10. поступление_товара
INSERT INTO поступление_товара (id_продукция, id_склад, Дата_поступления, Кол_во_товара) VALUES
(1, 1, '2025-03-01 10:30:00', 1000),
(2, 2, '2025-03-02 14:15:00', 500),
(3, 3, '2025-03-03 09:45:00', 2000),
(4, 4, '2025-03-04 16:20:00', 800),
(5, 5, '2025-03-05 11:10:00', 1500);

-- 11. перемещение_продукции
INSERT INTO перемещение_продукции (id_продукции, id_склад_откуда, id_склад_куда, Количество, Дата_перемещения, Статус, id_сотрудник) VALUES
(1, 1, 2, 200, '2025-03-10 13:00:00', 'Выполнено', 1),
(2, 2, 3, 100, '2025-03-11 15:30:00', 'В процессе', 2),
(3, 3, 4, 500, '2025-03-12 09:15:00', 'Выполнено', 3),
(4, 4, 5, 300, '2025-03-13 14:45:00', 'Запланировано', 4),
(5, 5, 1, 400, '2025-03-14 10:20:00', 'Выполнено', 5);

-- 12. продукция_на_складе
INSERT INTO продукция_на_складе (id_склада, id_продукции, Количество) VALUES
(1, 1, 800),
(2, 2, 400),
(3, 3, 1500),
(4, 4, 500),
(5, 5, 1100);

-- 13. тип_партнера
INSERT INTO тип_партнера (Наименование) VALUES
('Поставщик'),
('Дистрибьютор'),
('Розничная сеть'),
('Оптовик'),
('Производитель');

-- 14. партнер
INSERT INTO партнер (id_юр_адрес, Наименование, ИНН, ФИО_директора, id_тип, Телефон, Email, Места_продаж) VALUES
(1, 'ООО "МолокоПром"', '7723456789', 'Смирнов Иван Петрович', 1, '89161234567', 'milk@prom.ru', 'Москва'),
(2, 'ООО "СибирьСнаб"', '5402345678', 'Ковалев Олег Викторович', 2, '89139876543', 'snab@sib.ru', 'Новосибирск'),
(3, 'ООО "ЮгТорг"', '6163456789', 'Лебедева Анна Сергеевна', 3, '89184567890', 'torg@yug.ru', 'Ростов-на-Дону'),
(4, 'ООО "УралПоставка"', '6672345678', 'Зайцев Павел Игоревич', 4, '89123456789', 'postavka@ural.ru', 'Екатеринбург'),
(5, 'ООО "ВолгаПродукт"', '6313456789', 'Михайлов Сергей Александрович', 5, '89176543210', 'product@volga.ru', 'Самара');

-- 15. заказ
INSERT INTO заказ (Дата_создания, Статус, id_сотрудник, id_партнер, Предоплата, Согласована) VALUES
('2025-03-15', 'Новый', 1, 1, 5000.00, FALSE),
('2025-03-16', 'Согласован', 2, 2, 10000.00, TRUE),
('2025-03-17', 'В обработке', 3, 3, 7500.00, FALSE),
('2025-03-18', 'Выполнен', 4, 4, 15000.00, TRUE),
('2025-03-19', 'Отменен', 5, 5, 0.00, FALSE);

-- 16. заказ_продукции
INSERT INTO заказ_продукции (id_заказа, id_продукции, Количество, Стоимость) VALUES
(1, 1, 100, 4550.00),
(2, 2, 50, 17500.00),
(3, 3, 200, 16000.00),
(4, 4, 150, 13500.00),
(5, 5, 80, 9600.00);