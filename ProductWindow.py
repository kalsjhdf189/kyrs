# ProductWindow.py
from PySide6.QtWidgets import (
    QWidget, QTableWidget, QVBoxLayout, QPushButton, QHBoxLayout, 
    QTableWidgetItem, QDialog, QLineEdit, QLabel, QComboBox, QMessageBox, QSizePolicy, QHeaderView
)
from PySide6.QtCore import Qt
from datebase import Product, ProductType, ProductOnWarehouse, Connect
from AddProduct import AddProductDialog
from styles import TABLE_WIDGET_STYLE
from sqlalchemy import func

class ProductWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Connect.create_connection()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.btnLayout = QHBoxLayout()
        self.filterLayout = QHBoxLayout()

        self.addBtn = QPushButton("+")
        self.addBtn.clicked.connect(self.add_product)
        self.editBtn = QPushButton("Редактировать")
        self.editBtn.clicked.connect(self.edit_product)
        self.deleteBtn = QPushButton("-")
        self.deleteBtn.clicked.connect(self.delete_product)

        self.searchLabel = QLabel("Поиск:")
        self.searchEdit = QLineEdit()
        self.searchEdit.textChanged.connect(self.search_products)

        self.typeLabel = QLabel("Тип продукции:")
        self.typeCombo = QComboBox()
        self.load_product_types()
        self.typeCombo.currentIndexChanged.connect(self.filter_by_type)

        self.btnLayout.addWidget(self.addBtn)
        self.btnLayout.addWidget(self.editBtn)
        self.btnLayout.addWidget(self.deleteBtn)
        
        self.filterLayout.addWidget(self.searchLabel)
        self.filterLayout.addWidget(self.searchEdit)
        self.filterLayout.addWidget(self.typeLabel)
        self.filterLayout.addWidget(self.typeCombo)

        self.layout.addLayout(self.btnLayout)
        self.layout.addLayout(self.filterLayout)
        
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.load_table_data()
        self.setStyleSheet(TABLE_WIDGET_STYLE)

    def load_product_types(self):
        self.typeCombo.clear()
        self.typeCombo.addItem("Все типы", None)
        types = self.session.query(ProductType).all()
        for type_ in types:
            self.typeCombo.addItem(type_.Наименование, type_.id)

    def load_table_data(self, search_query=None, type_id=None):
        query = self.session.query(Product)
        
        if search_query:
            query = query.filter(
                (Product.Наименование.ilike(f"%{search_query}%")) |
                (Product.Описание.ilike(f"%{search_query}%"))
            )
        
        if type_id:
            query = query.filter(Product.id_тип == type_id)

        products = query.all()

        stock_query = (
            self.session.query(ProductOnWarehouse.id_продукции, func.sum(ProductOnWarehouse.Количество).label("total_stock"))
            .group_by(ProductOnWarehouse.id_продукции)
            .all()
        )
        stock_dict = {item.id_продукции: item.total_stock for item in stock_query}

        columns = [
            "ID", "Тип", "Наименование", "Описание", "Мин. стоимость",
            "Размер упаковки", "Вес без упаковки", "Вес с упаковкой",
            "Сертификат качества", "Себестоимость", "Количество на складе"
        ]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product.id)))
            self.table.setItem(row, 1, QTableWidgetItem(product.тип.Наименование if product.тип else "Не указан"))
            self.table.setItem(row, 2, QTableWidgetItem(product.Наименование or ""))
            self.table.setItem(row, 3, QTableWidgetItem(product.Описание or ""))
            self.table.setItem(row, 4, QTableWidgetItem(str(product.Мин_стоимость or "")))
            self.table.setItem(row, 5, QTableWidgetItem(product.Размер_упаковки or ""))
            self.table.setItem(row, 6, QTableWidgetItem(str(product.Вес_без_упаковки or "")))
            self.table.setItem(row, 7, QTableWidgetItem(str(product.Вес_с_упаковкой or "")))
            self.table.setItem(row, 8, QTableWidgetItem(product.Сертификат_качества or ""))
            self.table.setItem(row, 9, QTableWidgetItem(str(product.Себестоимость or "")))
            total_stock = stock_dict.get(product.id, 0)
            self.table.setItem(row, 10, QTableWidgetItem(str(total_stock)))

    def search_products(self):
        search_query = self.searchEdit.text().strip()
        type_id = self.typeCombo.currentData()
        self.load_table_data(search_query if search_query else None, type_id)

    def filter_by_type(self):
        search_query = self.searchEdit.text().strip()
        type_id = self.typeCombo.currentData()
        self.load_table_data(search_query if search_query else None, type_id)

    def add_product(self):
        dialog = AddProductDialog(self.session, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_table_data(search_query=self.searchEdit.text().strip(), type_id=self.typeCombo.currentData())

    def edit_product(self):
        selected = self.table.currentRow()
        if selected >= 0:
            product_id = int(self.table.item(selected, 0).text())
            product = self.session.query(Product).filter(Product.id == product_id).first()
            if product:
                dialog = AddProductDialog(self.session, self, product)
                if dialog.exec() == QDialog.Accepted:
                    self.load_table_data(search_query=self.searchEdit.text().strip(), type_id=self.typeCombo.currentData())
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите продукт для редактирования")

    def delete_product(self):
        selected = self.table.currentRow()
        if selected >= 0:
            product_id = int(self.table.item(selected, 0).text())
            product = self.session.query(Product).filter(Product.id == product_id).first()
            if product:
                self.session.delete(product)
                self.session.commit()
                self.load_table_data(search_query=self.searchEdit.text().strip(), type_id=self.typeCombo.currentData())