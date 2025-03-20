# AddProduct.py
from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QComboBox
from datebase import Product, ProductType
from styles import DIALOG_STYLE  # Импорт стилей

class AddProductDialog(QDialog):
    def __init__(self, session, parent=None, product=None):
        super().__init__(parent)
        self.session = session
        self.product = product
        self.setWindowTitle("Добавить продукт" if not product else "Редактировать продукт")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.typeCombo = QComboBox()
        types = self.session.query(ProductType).all()
        for t in types:
            self.typeCombo.addItem(t.Наименование, t.id)

        self.nameEdit = QLineEdit()
        self.descEdit = QLineEdit()
        self.minCostEdit = QLineEdit()
        self.packSizeEdit = QLineEdit()
        self.weightNoPackEdit = QLineEdit()
        self.weightPackEdit = QLineEdit()
        self.certEdit = QLineEdit()
        self.costEdit = QLineEdit()

        if self.product:
            self.typeCombo.setCurrentText(self.product.тип.Наименование)
            self.nameEdit.setText(self.product.Наименование or "")
            self.descEdit.setText(self.product.Описание or "")
            self.minCostEdit.setText(str(self.product.Мин_стоимость or ""))
            self.packSizeEdit.setText(self.product.Размер_упаковки or "")
            self.weightNoPackEdit.setText(str(self.product.Вес_без_упаковки or ""))
            self.weightPackEdit.setText(str(self.product.Вес_с_упаковкой or ""))
            self.certEdit.setText(self.product.Сертификат_качества or "")
            self.costEdit.setText(str(self.product.Себестоимость or ""))

        layout.addRow("Тип продукции:", self.typeCombo)
        layout.addRow("Наименование:", self.nameEdit)
        layout.addRow("Описание:", self.descEdit)
        layout.addRow("Мин. стоимость:", self.minCostEdit)
        layout.addRow("Размер упаковки:", self.packSizeEdit)
        layout.addRow("Вес без упаковки:", self.weightNoPackEdit)
        layout.addRow("Вес с упаковкой:", self.weightPackEdit)
        layout.addRow("Сертификат качества:", self.certEdit)
        layout.addRow("Себестоимость:", self.costEdit)

        self.saveBtn = QPushButton("Сохранить")
        self.saveBtn.clicked.connect(self.save_product)
        layout.addWidget(self.saveBtn)

        self.setStyleSheet(DIALOG_STYLE)  # Применяем стили

    def save_product(self):
        if not self.product:
            self.product = Product()
        self.product.id_тип = self.typeCombo.currentData()
        self.product.Наименование = self.nameEdit.text() or None
        self.product.Описание = self.descEdit.text() or None
        self.product.Мин_стоимость = float(self.minCostEdit.text()) if self.minCostEdit.text() else None
        self.product.Размер_упаковки = self.packSizeEdit.text() or None
        self.product.Вес_без_упаковки = int(self.weightNoPackEdit.text()) if self.weightNoPackEdit.text() else None
        self.product.Вес_с_упаковкой = int(self.weightPackEdit.text()) if self.weightPackEdit.text() else None
        self.product.Сертификат_качества = self.certEdit.text() or None
        self.product.Себестоимость = float(self.costEdit.text()) if self.costEdit.text() else None

        self.session.add(self.product)
        self.session.commit()
        self.accept()