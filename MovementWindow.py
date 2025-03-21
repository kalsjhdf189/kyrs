# MovementWindow.py
from PySide6.QtWidgets import (
    QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QPushButton, 
    QHBoxLayout, QDialog, QFormLayout, QComboBox, QMessageBox, QSizePolicy, QHeaderView, QLineEdit, QDateTimeEdit, QMessageBox
)
from PySide6.QtCore import QDateTime, Qt
from datebase import Employee, Product, ProductMovement, ProductOnWarehouse, Warehouse, Connect
from styles import TABLE_WIDGET_STYLE, DIALOG_STYLE
from sqlalchemy import and_

class EditMovementDialog(QDialog):
    def __init__(self, session, movement, parent=None):
        super().__init__(parent)
        self.session = session
        self.movement = movement
        self.setWindowTitle("Редактировать перемещение")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["В пути", "Доставлено", "Отменено"])
        self.status_combo.setCurrentText(self.movement.Статус or "В пути")
        layout.addRow("Статус:", self.status_combo)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_changes)
        layout.addWidget(self.save_btn)

        self.setStyleSheet(DIALOG_STYLE)

    def save_changes(self):
        new_status = self.status_combo.currentText()
        old_status = self.movement.Статус

        if new_status != old_status:
            self.movement.Статус = new_status
            if new_status == "Доставлено" and old_status != "Доставлено":
                product_id = self.movement.id_продукции
                to_warehouse_id = self.movement.id_склад_куда
                quantity = self.movement.Количество

                to_stock = self.session.query(ProductOnWarehouse).filter(
                    and_(
                        ProductOnWarehouse.id_продукции == product_id,
                        ProductOnWarehouse.id_склада == to_warehouse_id
                    )
                ).first()
                if to_stock:
                    to_stock.Количество += quantity
                else:
                    new_stock = ProductOnWarehouse(
                        id_продукции=product_id,
                        id_склада=to_warehouse_id,
                        Количество=quantity
                    )
                    self.session.add(new_stock)

            self.session.commit()
            QMessageBox.information(self, "Успех", "Статус перемещения успешно обновлён!")
        else:
            QMessageBox.information(self, "Информация", "Статус не изменился.")
        self.accept()

class AddMovementDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Добавить перемещение")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.product_combo = QComboBox()
        products = self.session.query(Product).all()
        for product in products:
            self.product_combo.addItem(product.Наименование, product.id)
        layout.addRow("Продукция:", self.product_combo)

        self.from_warehouse_combo = QComboBox()
        warehouses = self.session.query(Warehouse).all()
        for warehouse in warehouses:
            self.from_warehouse_combo.addItem(warehouse.Название, warehouse.id)
        layout.addRow("Склад откуда:", self.from_warehouse_combo)

        self.to_warehouse_combo = QComboBox()
        for warehouse in warehouses:
            self.to_warehouse_combo.addItem(warehouse.Название, warehouse.id)
        layout.addRow("Склад куда:", self.to_warehouse_combo)

        self.quantity_edit = QLineEdit()
        self.quantity_edit.setPlaceholderText("Введите количество")
        layout.addRow("Количество:", self.quantity_edit)

        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        self.date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        layout.addRow("Дата перемещения:", self.date_edit)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["В пути", "Доставлено", "Отменено"])
        layout.addRow("Статус:", self.status_combo)

        self.employee_combo = QComboBox()
        employees = self.session.query(Employee).all()
        for emp in employees:
            self.employee_combo.addItem(f"{emp.Фамилия} {emp.Имя[0]}. {emp.Отчество[0]}.", emp.id)
        layout.addRow("Сотрудник:", self.employee_combo)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_movement)
        layout.addWidget(self.save_btn)

        self.setStyleSheet(DIALOG_STYLE)

    def save_movement(self):
        product_id = self.product_combo.currentData()
        from_warehouse_id = self.from_warehouse_combo.currentData()
        to_warehouse_id = self.to_warehouse_combo.currentData()

        if from_warehouse_id == to_warehouse_id:
            QMessageBox.warning(self, "Ошибка", "Склад 'откуда' и склад 'куда' не могут быть одинаковыми!")
            return

        try:
            quantity = int(self.quantity_edit.text())
            if quantity <= 0:
                raise ValueError("Количество должно быть положительным")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректное количество: {str(e)}")
            return

        stock = self.session.query(ProductOnWarehouse).filter(
            ProductOnWarehouse.id_продукции == product_id,
            ProductOnWarehouse.id_склада == from_warehouse_id
        ).first()

        if not stock or stock.Количество < quantity:
            QMessageBox.warning(self, "Ошибка", "Недостаточно продукции на складе 'откуда'!")
            return

        new_movement = ProductMovement(
            id_продукции=product_id,
            id_склад_откуда=from_warehouse_id,
            id_склад_куда=to_warehouse_id,
            Количество=quantity,
            Дата_перемещения=self.date_edit.dateTime().toPython(),
            Статус=self.status_combo.currentText(),
            id_сотрудник=self.employee_combo.currentData()
        )
        self.session.add(new_movement)

        stock.Количество -= quantity
        if stock.Количество == 0:
            self.session.delete(stock)

        if self.status_combo.currentText() == "Доставлено":
            to_stock = self.session.query(ProductOnWarehouse).filter(
                ProductOnWarehouse.id_продукции == product_id,
                ProductOnWarehouse.id_склада == to_warehouse_id
            ).first()
            if to_stock:
                to_stock.Количество += quantity
            else:
                new_stock = ProductOnWarehouse(
                    id_продукции=product_id,
                    id_склада=to_warehouse_id,
                    Количество=quantity
                )
                self.session.add(new_stock)

        self.session.commit()
        QMessageBox.information(self, "Успех", "Перемещение успешно добавлено!")
        self.accept()

class MovementWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Connect.create_connection()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("+")
        self.add_btn.clicked.connect(self.add_movement)
        self.btn_layout.addWidget(self.add_btn)

        self.layout.addLayout(self.btn_layout)

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.doubleClicked.connect(self.edit_movement)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.table)

        self.load_table_data()
        self.setStyleSheet(TABLE_WIDGET_STYLE)

    def load_table_data(self):
        movements = self.session.query(ProductMovement).all()

        columns = [
            "Продукция", "Склад откуда", "Склад куда", "Количество", 
            "Дата перемещения", "Статус", "Сотрудник"
        ]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(movements))

        for row, movement in enumerate(movements):
            item0 = QTableWidgetItem(movement.продукция.Наименование if movement.продукция else "Не указан")
            item0.setData(Qt.UserRole, movement)  # Сохраняем объект movement
            self.table.setItem(row, 0, item0)

            self.table.setItem(row, 1, QTableWidgetItem(movement.склад_откуда.Название if movement.склад_откуда else "Не указан"))
            self.table.setItem(row, 2, QTableWidgetItem(movement.склад_куда.Название if movement.склад_куда else "Не указан"))
            self.table.setItem(row, 3, QTableWidgetItem(str(movement.Количество)))
            self.table.setItem(row, 4, QTableWidgetItem(str(movement.Дата_перемещения)))
            self.table.setItem(row, 5, QTableWidgetItem(movement.Статус or "Не указан"))
            employee_name = (f"{movement.сотрудник.Фамилия} {movement.сотрудник.Имя[0]}. {movement.сотрудник.Отчество[0]}."
                            if movement.сотрудник else "Не указан")
            self.table.setItem(row, 6, QTableWidgetItem(employee_name))

    def add_movement(self):
        dialog = AddMovementDialog(self.session, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_table_data()

    def edit_movement(self):
        selected = self.table.currentRow()
        if selected >= 0:
            movement = self.table.item(selected, 0).data(Qt.UserRole)  # Извлекаем movement из данных ячейки
            if movement:
                dialog = EditMovementDialog(self.session, movement, self)
                if dialog.exec() == QDialog.Accepted:
                    self.load_table_data()
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите перемещение для редактирования")