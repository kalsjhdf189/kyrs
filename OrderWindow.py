# OrderWindow.py
from PySide6.QtWidgets import (
    QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QPushButton, QHBoxLayout, 
    QDialog, QFormLayout, QComboBox, QLineEdit, QCheckBox, QDateTimeEdit, QMessageBox, QSizePolicy, QHeaderView
)
from PySide6.QtCore import QDateTime
from datebase import Order, Employee, Partner, Connect
from styles import TABLE_WIDGET_STYLE, DIALOG_STYLE  # Используем TABLE_WIDGET_STYLE как в ProductWindow

class AddOrderDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Добавить заказ")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.employee_combo = QComboBox()
        employees = self.session.query(Employee).all()
        for emp in employees:
            self.employee_combo.addItem(f"{emp.Фамилия} {emp.Имя[0]}. {emp.Отчество[0]}.", emp.id)
        layout.addRow("Сотрудник:", self.employee_combo)

        self.partner_combo = QComboBox()
        partners = self.session.query(Partner).all()
        for partner in partners:
            self.partner_combo.addItem(partner.Наименование, partner.id)
        layout.addRow("Партнёр:", self.partner_combo)

        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        self.date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        layout.addRow("Дата создания:", self.date_edit)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Новый", "В обработке", "Выполнен", "Отменён"])
        layout.addRow("Статус:", self.status_combo)

        self.prepayment_edit = QLineEdit()
        self.prepayment_edit.setPlaceholderText("Введите сумму предоплаты")
        layout.addRow("Предоплата:", self.prepayment_edit)

        self.approved_check = QCheckBox()
        layout.addRow("Согласована:", self.approved_check)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_order)
        layout.addWidget(self.save_btn)

        self.setStyleSheet(DIALOG_STYLE)

    def save_order(self):
        try:
            prepayment = float(self.prepayment_edit.text()) if self.prepayment_edit.text() else 0.0
            if prepayment < 0:
                raise ValueError("Предоплата не может быть отрицательной")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректная предоплата: {str(e)}")
            return

        new_order = Order(
            id_сотрудник=self.employee_combo.currentData(),
            id_партнер=self.partner_combo.currentData(),
            Дата_создания=self.date_edit.dateTime().toPython(),
            Статус=self.status_combo.currentText(),
            Предоплата=prepayment,
            Согласована=self.approved_check.isChecked()
        )
        self.session.add(new_order)
        self.session.commit()
        self.accept()

class EditOrderDialog(QDialog):
    def __init__(self, session, order, parent=None):
        super().__init__(parent)
        self.session = session
        self.order = order
        self.setWindowTitle("Редактировать заказ")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.employee_combo = QComboBox()
        employees = self.session.query(Employee).all()
        for emp in employees:
            self.employee_combo.addItem(f"{emp.Фамилия} {emp.Имя[0]}. {emp.Отчество[0]}.", emp.id)
        self.employee_combo.setCurrentIndex(self.employee_combo.findData(self.order.id_сотрудник))
        layout.addRow("Сотрудник:", self.employee_combo)

        self.partner_combo = QComboBox()
        partners = self.session.query(Partner).all()
        for partner in partners:
            self.partner_combo.addItem(partner.Наименование, partner.id)
        self.partner_combo.setCurrentIndex(self.partner_combo.findData(self.order.id_партнер))
        layout.addRow("Партнёр:", self.partner_combo)

        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.fromString(str(self.order.Дата_создания), "yyyy-MM-dd HH:mm:ss"))
        self.date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        layout.addRow("Дата создания:", self.date_edit)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Новый", "В обработке", "Выполнен", "Отменён"])
        self.status_combo.setCurrentText(self.order.Статус)
        layout.addRow("Статус:", self.status_combo)

        self.prepayment_edit = QLineEdit()
        self.prepayment_edit.setText(str(self.order.Предоплата if self.order.Предоплата is not None else "0.0"))
        layout.addRow("Предоплата:", self.prepayment_edit)

        self.approved_check = QCheckBox()
        self.approved_check.setChecked(self.order.Согласована)
        layout.addRow("Согласована:", self.approved_check)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_order)
        layout.addWidget(self.save_btn)

        self.setStyleSheet(DIALOG_STYLE)

    def save_order(self):
        try:
            prepayment = float(self.prepayment_edit.text()) if self.prepayment_edit.text() else 0.0
            if prepayment < 0:
                raise ValueError("Предоплата не может быть отрицательной")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректная предоплата: {str(e)}")
            return

        self.order.id_сотрудник = self.employee_combo.currentData()
        self.order.id_партнер = self.partner_combo.currentData()
        self.order.Дата_создания = self.date_edit.dateTime().toPython()
        self.order.Статус = self.status_combo.currentText()
        self.order.Предоплата = prepayment
        self.order.Согласована = self.approved_check.isChecked()

        self.session.commit()
        self.accept()

class OrderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Connect.create_connection()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.btnLayout = QHBoxLayout()  # Аналогично ProductWindow

        # Кнопки как в ProductWindow
        self.addBtn = QPushButton("+")
        self.addBtn.clicked.connect(self.add_order)
        self.editBtn = QPushButton("Редактировать")
        self.editBtn.clicked.connect(self.edit_order)
        self.deleteBtn = QPushButton("-")
        self.deleteBtn.clicked.connect(self.delete_order)

        self.btnLayout.addWidget(self.addBtn)
        self.btnLayout.addWidget(self.editBtn)
        self.btnLayout.addWidget(self.deleteBtn)

        self.layout.addLayout(self.btnLayout)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.load_table_data()
        self.setStyleSheet(TABLE_WIDGET_STYLE)  # Используем тот же стиль, что и в ProductWindow

    def load_table_data(self):
        orders = self.session.query(Order).all()

        columns = [
            "ID", "Дата создания", "Статус", "Сотрудник", "Партнёр", "Предоплата", "Согласована"
        ]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(orders))

        for row, order in enumerate(orders):
            self.table.setItem(row, 0, QTableWidgetItem(str(order.id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(order.Дата_создания)))
            self.table.setItem(row, 2, QTableWidgetItem(order.Статус or "Не указан"))
            employee_name = (f"{order.сотрудник.Фамилия} {order.сотрудник.Имя[0]}. {order.сотрудник.Отчество[0]}."
                             if order.сотрудник else "Не указан")
            self.table.setItem(row, 3, QTableWidgetItem(employee_name))
            self.table.setItem(row, 4, QTableWidgetItem(order.партнер.Наименование if order.партнер else "Не указан"))
            self.table.setItem(row, 5, QTableWidgetItem(str(order.Предоплата) if order.Предоплата is not None else "0.0"))
            self.table.setItem(row, 6, QTableWidgetItem("Да" if order.Согласована else "Нет"))

    def add_order(self):
        dialog = AddOrderDialog(self.session, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_table_data()

    def edit_order(self):
        selected = self.table.currentRow()
        if selected >= 0:
            order_id = int(self.table.item(selected, 0).text())
            order = self.session.query(Order).filter(Order.id == order_id).first()
            if order:
                dialog = EditOrderDialog(self.session, order, self)
                if dialog.exec() == QDialog.Accepted:
                    self.load_table_data()
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите заказ для редактирования")

    def delete_order(self):
        selected = self.table.currentRow()
        if selected >= 0:
            order_id = int(self.table.item(selected, 0).text())
            order = self.session.query(Order).filter(Order.id == order_id).first()
            if order:
                reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить этот заказ?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.session.delete(order)
                    self.session.commit()
                    self.load_table_data()
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите заказ для удаления")