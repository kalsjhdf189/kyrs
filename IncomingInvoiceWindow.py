# IncomingInvoiceWindow.py
from PySide6.QtWidgets import (
    QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QPushButton, 
    QHBoxLayout, QDialog, QFormLayout, QComboBox, QLineEdit, QDateTimeEdit, QMessageBox, QSizePolicy, QHeaderView
)
from PySide6.QtCore import QDateTime
from datebase import IncomingInvoice, Product, Warehouse, ProductOnWarehouse, Connect
from styles import TABLE_WIDGET_STYLE, DIALOG_STYLE
from sqlalchemy import and_

class AddIncomingInvoiceDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Добавить поступление товара")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.product_combo = QComboBox()
        products = self.session.query(Product).all()
        for product in products:
            self.product_combo.addItem(product.Наименование, product.id)
        layout.addRow("Продукция:", self.product_combo)

        self.warehouse_combo = QComboBox()
        warehouses = self.session.query(Warehouse).all()
        for warehouse in warehouses:
            self.warehouse_combo.addItem(warehouse.Название, warehouse.id)
        layout.addRow("Склад:", self.warehouse_combo)

        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        self.date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        layout.addRow("Дата поступления:", self.date_edit)

        self.quantity_edit = QLineEdit()
        self.quantity_edit.setPlaceholderText("Введите количество")
        layout.addRow("Количество товара:", self.quantity_edit)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_invoice)
        layout.addWidget(self.save_btn)

        self.setStyleSheet(DIALOG_STYLE)

    def save_invoice(self):
        product_id = self.product_combo.currentData()
        warehouse_id = self.warehouse_combo.currentData()
        date = self.date_edit.dateTime().toPython()
        try:
            quantity = int(self.quantity_edit.text())
            if quantity <= 0:
                raise ValueError("Количество должно быть положительным")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректное количество: {str(e)}")
            return

        new_invoice = IncomingInvoice(
            id_продукция=product_id,
            id_склад=warehouse_id,
            Дата_поступления=date,
            Кол_во_товара=quantity
        )
        self.session.add(new_invoice)

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

class IncomingInvoiceWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Connect.create_connection()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("+")
        self.add_btn.clicked.connect(self.add_invoice)
        self.btn_layout.addWidget(self.add_btn)

        self.layout.addLayout(self.btn_layout)

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Добавлено
        self.layout.addWidget(self.table)

        self.load_table_data()
        self.setStyleSheet(TABLE_WIDGET_STYLE)

    def load_table_data(self):
        invoices = self.session.query(IncomingInvoice).all()

        columns = [
            "ID", "Продукция", "Склад", "Дата поступления", "Количество товара"
        ]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(invoices))

        for row, invoice in enumerate(invoices):
            self.table.setItem(row, 0, QTableWidgetItem(str(invoice.id)))
            self.table.setItem(row, 1, QTableWidgetItem(invoice.продукция.Наименование if invoice.продукция else "Не указан"))
            self.table.setItem(row, 2, QTableWidgetItem(invoice.склад.Название if invoice.склад else "Не указан"))
            self.table.setItem(row, 3, QTableWidgetItem(str(invoice.Дата_поступления)))
            self.table.setItem(row, 4, QTableWidgetItem(str(invoice.Кол_во_товара)))

    def add_invoice(self):
        dialog = AddIncomingInvoiceDialog(self.session, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_table_data()