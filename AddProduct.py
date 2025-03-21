# AddProduct.py
from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QComboBox, QMessageBox, QMessageBox
from datebase import Product, ProductType
from styles import DIALOG_STYLE  # Импорт стилей

class AddProductDialog(QDialog):
    def __init__(self, session, parent=None, product=None):
        super().__init__(parent)
        self.session = session
        self.product = product
        self.setWindowTitle("Редактировать продукцию" if product else "Добавить продукцию")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.type_combo = QComboBox()
        types = self.session.query(ProductType).all()
        for t in types:
            self.type_combo.addItem(t.Наименование, t.id)
        if self.product:
            self.type_combo.setCurrentIndex(self.type_combo.findData(self.product.id_тип))
        layout.addRow("Тип:", self.type_combo)

        self.name_edit = QLineEdit(self.product.Наименование if self.product else "")
        layout.addRow("Наименование:", self.name_edit)

        self.description_edit = QLineEdit(self.product.Описание if self.product else "")
        layout.addRow("Описание:", self.description_edit)

        self.min_cost_edit = QLineEdit(str(self.product.Мин_стоимость) if self.product else "")
        layout.addRow("Мин. стоимость:", self.min_cost_edit)

        self.package_size_edit = QLineEdit(self.product.Размер_упаковки if self.product else "")
        layout.addRow("Размер упаковки:", self.package_size_edit)

        self.weight_no_package_edit = QLineEdit(str(self.product.Вес_без_упаковки) if self.product else "")
        layout.addRow("Вес без упаковки:", self.weight_no_package_edit)

        self.weight_with_package_edit = QLineEdit(str(self.product.Вес_с_упаковкой) if self.product else "")
        layout.addRow("Вес с упаковкой:", self.weight_with_package_edit)

        self.quality_cert_edit = QLineEdit(self.product.Сертификат_качества if self.product else "")
        layout.addRow("Сертификат качества:", self.quality_cert_edit)

        self.cost_price_edit = QLineEdit(str(self.product.Себестоимость) if self.product else "")
        layout.addRow("Себестоимость:", self.cost_price_edit)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_product)
        layout.addWidget(self.save_btn)

        self.setStyleSheet(DIALOG_STYLE)

    def save_product(self):
        try:
            name = self.name_edit.text().strip()
            if not name:
                raise ValueError("Наименование не может быть пустым")

            min_cost = float(self.min_cost_edit.text()) if self.min_cost_edit.text().strip() else None
            weight_no_package = float(self.weight_no_package_edit.text()) if self.weight_no_package_edit.text().strip() else None
            weight_with_package = float(self.weight_with_package_edit.text()) if self.weight_with_package_edit.text().strip() else None
            cost_price = float(self.cost_price_edit.text()) if self.cost_price_edit.text().strip() else None

            if self.product:
                self.product.id_тип = self.type_combo.currentData()
                self.product.Наименование = name
                self.product.Описание = self.description_edit.text().strip() or None
                self.product.Мин_стоимость = min_cost
                self.product.Размер_упаковки = self.package_size_edit.text().strip() or None
                self.product.Вес_без_упаковки = weight_no_package
                self.product.Вес_с_упаковкой = weight_with_package
                self.product.Сертификат_качества = self.quality_cert_edit.text().strip() or None
                self.product.Себестоимость = cost_price
                self.session.commit()
                QMessageBox.information(self, "Успех", "Продукт успешно обновлён!")
            else:
                new_product = Product(
                    id_тип=self.type_combo.currentData(),
                    Наименование=name,
                    Описание=self.description_edit.text().strip() or None,
                    Мин_стоимость=min_cost,
                    Размер_упаковки=self.package_size_edit.text().strip() or None,
                    Вес_без_упаковки=weight_no_package,
                    Вес_с_упаковкой=weight_with_package,
                    Сертификат_качества=self.quality_cert_edit.text().strip() or None,
                    Себестоимость=cost_price
                )
                self.session.add(new_product)
                self.session.commit()
                QMessageBox.information(self, "Успех", "Продукт успешно добавлен!")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить продукт: {str(e)}")
            self.session.rollback()