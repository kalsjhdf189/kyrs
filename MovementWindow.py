# MovementWindow.py
from PySide6.QtWidgets import (
    QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QPushButton, 
    QHBoxLayout, QDialog, QFormLayout, QComboBox, QMessageBox, QSizePolicy, QHeaderView
)
from datebase import ProductMovement, ProductOnWarehouse, Warehouse, Connect
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
        if new_status != self.movement.Статус:
            self.movement.Статус = new_status
            if new_status == "Доставлено":
                product_id = self.movement.id_продукции
                warehouse_id = self.movement.id_склад_куда
                quantity = self.movement.Количество

                stock = self.session.query(ProductOnWarehouse).filter(
                    and_(
                        ProductOnWarehouse.id_продукции == product_id,
                        ProductOnWarehouse.id_склада == warehouse_id
                    )
                ).first()

                if stock:
                    stock.Количество += quantity
                else:
                    new_stock = ProductOnWarehouse(
                        id_продукции=product_id,
                        id_склада=warehouse_id,
                        Количество=quantity
                    )
                    self.session.add(new_stock)

            self.session.commit()
        self.accept()

class MovementWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Connect.create_connection()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.btn_layout = QHBoxLayout()

        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self.edit_movement)
        self.btn_layout.addWidget(self.edit_btn)

        self.layout.addLayout(self.btn_layout)

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.load_table_data()
        self.setStyleSheet(TABLE_WIDGET_STYLE)

    def load_table_data(self):
        movements = self.session.query(ProductMovement).all()

        columns = [
            "ID", "Продукция", "Склад откуда", "Склад куда", "Количество", 
            "Дата перемещения", "Статус", "Сотрудник"
        ]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(movements))

        for row, movement in enumerate(movements):
            self.table.setItem(row, 0, QTableWidgetItem(str(movement.id)))
            self.table.setItem(row, 1, QTableWidgetItem(movement.продукция.Наименование if movement.продукция else "Не указан"))
            self.table.setItem(row, 2, QTableWidgetItem(movement.склад_откуда.Название if movement.склад_откуда else "Не указан"))
            self.table.setItem(row, 3, QTableWidgetItem(movement.склад_куда.Название if movement.склад_куда else "Не указан"))
            self.table.setItem(row, 4, QTableWidgetItem(str(movement.Количество)))
            self.table.setItem(row, 5, QTableWidgetItem(str(movement.Дата_перемещения)))
            self.table.setItem(row, 6, QTableWidgetItem(movement.Статус or "Не указан"))
            employee_name = (f"{movement.сотрудник.Фамилия} {movement.сотрудник.Имя[0]}. {movement.сотрудник.Отчество[0]}."
                             if movement.сотрудник else "Не указан")
            self.table.setItem(row, 7, QTableWidgetItem(employee_name))

    def edit_movement(self):
        selected = self.table.currentRow()
        if selected >= 0:
            movement_id = int(self.table.item(selected, 0).text())
            movement = self.session.query(ProductMovement).filter(ProductMovement.id == movement_id).first()
            if movement:
                dialog = EditMovementDialog(self.session, movement, self)
                if dialog.exec() == QDialog.Accepted:
                    self.load_table_data()
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите перемещение для редактирования")