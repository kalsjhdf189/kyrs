# OrderWindow.py
from PySide6.QtWidgets import (
    QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QPushButton, QHBoxLayout, 
    QDialog, QFormLayout, QComboBox, QLineEdit, QCheckBox, QDateTimeEdit, QMessageBox, QSizePolicy, QHeaderView, QLabel, QMessageBox
)
from PySide6.QtCore import QDateTime
from datebase import ProductOnWarehouse, OrderProduct, Product, Order, Employee, Partner, Connect
from styles import TABLE_WIDGET_STYLE, DIALOG_STYLE
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class OrderProductsDialog(QDialog):
    def __init__(self, session, order, parent=None):
        super().__init__(parent)
        self.session = session
        self.order = order
        self.setWindowTitle(f"Продукция заказа #{order.id}")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Информация о заказе
        info_label = QLabel(f"ID заказа: {self.order.id}\nДата создания: {self.order.Дата_создания}")
        layout.addWidget(info_label)

        # Таблица продукции
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить продукцию")
        self.add_btn.clicked.connect(self.add_order_product)
        self.close_btn = QPushButton("Закрыть")
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)

        self.load_table_data()

        self.setStyleSheet(DIALOG_STYLE)

    def load_table_data(self):
        order_products = self.session.query(OrderProduct).filter(OrderProduct.id_заказа == self.order.id).all()

        columns = ["ID продукции", "Количество"]  # Возвращаем "ID продукции"
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(order_products))

        for row, order_product in enumerate(order_products):
            self.table.setItem(row, 0, QTableWidgetItem(str(order_product.id_продукции)))
            self.table.setItem(row, 1, QTableWidgetItem(str(order_product.Количество)))

    def add_order_product(self):
        dialog = AddOrderProductDialog(self.session, self.order, self)
        if dialog.exec() == QDialog.Accepted:
            self.load_table_data()

    def load_table_data(self):
        order_products = self.session.query(OrderProduct).filter(OrderProduct.id_заказа == self.order.id).all()

        columns = ["ID продукции", "Наименование", "Количество"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(order_products))

        for row, order_product in enumerate(order_products):
            product = self.session.query(Product).filter(Product.id == order_product.id_продукции).first()
            self.table.setItem(row, 0, QTableWidgetItem(str(order_product.id_продукции)))
            self.table.setItem(row, 1, QTableWidgetItem(product.Наименование if product else "Не указан"))
            self.table.setItem(row, 2, QTableWidgetItem(str(order_product.Количество)))

            
class AddOrderProductDialog(QDialog):
    def __init__(self, session, order, parent=None):
        super().__init__(parent)
        self.session = session
        self.order = order
        self.setWindowTitle("Добавить продукцию к заказу")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Выбор продукции
        self.product_combo = QComboBox()
        products = self.session.query(Product).all()
        for product in products:
            self.product_combo.addItem(product.Наименование, product.id)
        layout.addRow("Продукция:", self.product_combo)

        # Ввод количества
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setPlaceholderText("Введите количество")
        layout.addRow("Количество:", self.quantity_edit)

        # Кнопка сохранения
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_order_product)
        layout.addWidget(self.save_btn)

        self.setStyleSheet(DIALOG_STYLE)

    def save_order_product(self):
        product_id = self.product_combo.currentData()
        try:
            quantity = int(self.quantity_edit.text())
            if quantity <= 0:
                raise ValueError("Количество должно быть положительным")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректное количество: {str(e)}")
            return

        # Проверка, существует ли уже запись для данной продукции в заказе
        existing_product = self.session.query(OrderProduct).filter(
            OrderProduct.id_заказа == self.order.id,
            OrderProduct.id_продукции == product_id
        ).first()

        if existing_product:
            existing_product.Количество += quantity
        else:
            new_order_product = OrderProduct(
                id_заказа=self.order.id,
                id_продукции=product_id,
                Количество=quantity
            )
            self.session.add(new_order_product)

        self.session.commit()
        self.accept()

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

        self.view_products_btn = QPushButton("Просмотреть продукцию")
        self.view_products_btn.clicked.connect(self.view_order_products)
        layout.addWidget(self.view_products_btn)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_order)
        layout.addWidget(self.save_btn)

        self.setStyleSheet(DIALOG_STYLE)

    def view_order_products(self):
        dialog = OrderProductsDialog(self.session, self.order, self)
        dialog.exec()

    def save_order(self):
        try:
            prepayment = float(self.prepayment_edit.text()) if self.prepayment_edit.text() else 0.0
            if prepayment < 0:
                raise ValueError("Предоплата не может быть отрицательной")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректная предоплата: {str(e)}")
            return

        new_status = self.status_combo.currentText()
        old_status = self.order.Статус

        self.order.id_сотрудник = self.employee_combo.currentData()
        self.order.id_партнер = self.partner_combo.currentData()
        self.order.Дата_создания = self.date_edit.dateTime().toPython()
        self.order.Статус = new_status
        self.order.Предоплата = prepayment
        self.order.Согласована = self.approved_check.isChecked()

        # Если статус изменился на "Выполнен"
        if new_status == "Выполнен" and old_status != "Выполнен":
            order_products = self.session.query(OrderProduct).filter(OrderProduct.id_заказа == self.order.id).all()
            for order_product in order_products:
                product_id = order_product.id_продукции
                quantity = order_product.Количество

                # Находим запись в ProductOnWarehouse (предполагаем, что склад один или берём первый доступный)
                stock = self.session.query(ProductOnWarehouse).filter(
                    ProductOnWarehouse.id_продукции == product_id
                ).first()

                if stock:
                    if stock.Количество >= quantity:
                        stock.Количество -= quantity
                        if stock.Количество == 0:
                            self.session.delete(stock)
                    else:
                        QMessageBox.warning(self, "Ошибка", f"Недостаточно продукции {product_id} на складе!")
                        self.session.rollback()
                        return
                else:
                    QMessageBox.warning(self, "Ошибка", f"Продукция {product_id} не найдена на складе!")
                    self.session.rollback()
                    return

        self.session.commit()
        self.accept()

class OrderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Connect.create_connection()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.btnLayout = QHBoxLayout()

        self.addBtn = QPushButton("+")
        self.addBtn.clicked.connect(self.add_order)
        self.deleteBtn = QPushButton("-")
        self.deleteBtn.clicked.connect(self.delete_order)
        self.report_btn = QPushButton("Отчёт")
        self.report_btn.clicked.connect(self.select_order_for_report)

        self.btnLayout.addWidget(self.addBtn)
        self.btnLayout.addWidget(self.deleteBtn)
        self.btnLayout.addWidget(self.report_btn)  # Добавляем кнопку "Отчёт" в btnLayout
        self.btnLayout.addStretch()  # Добавляем растяжку для выравнивания

        self.layout.addLayout(self.btnLayout)
        
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.doubleClicked.connect(self.edit_order)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.table)

        self.load_table_data()
        self.setStyleSheet(TABLE_WIDGET_STYLE)

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
            QMessageBox.information(self, "Успех", "Заказ успешно добавлен!")
    
    def edit_order(self):
        selected = self.table.currentRow()
        if selected >= 0:
            order_id = int(self.table.item(selected, 0).text())
            order = self.session.query(Order).filter(Order.id == order_id).first()
            if order:
                dialog = EditOrderDialog(self.session, order, self)
                if dialog.exec() == QDialog.Accepted:
                    self.load_table_data()
                    QMessageBox.information(self, "Успех", "Заказ успешно отредактирован!")
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
                    QMessageBox.information(self, "Успех", "Заказ успешно удалён!")
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите заказ для удаления")
            
    def select_order_for_report(self):
        # Диалог для выбора заказа
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбор заказа для отчёта")
        layout = QVBoxLayout(dialog)

        combo = QComboBox()
        orders = self.session.query(Order).all()
        for order in orders:
            combo.addItem(f"Заказ #{order.id} от {order.Дата_создания}", order.id)

        ok_btn = QPushButton("Сформировать отчёт")
        ok_btn.clicked.connect(lambda: self.generate_order_report(combo.currentData(), dialog))
        layout.addWidget(combo)
        layout.addWidget(ok_btn)

        dialog.exec()
    
    def generate_order_report(self, order_id, dialog):
        dialog.accept()

        pdfmetrics.registerFont(TTFont('SegoeUIRegular', 'C:/Windows/Fonts/SegoeUI.ttf'))
        order = self.session.query(Order).filter(Order.id == order_id).first()
        if not order:
            QMessageBox.warning(self, "Ошибка", "Заказ не найден!")
            return

        order_products = self.session.query(OrderProduct).filter(OrderProduct.id_заказа == order_id).all()
        if not order_products:
            QMessageBox.warning(self, "Предупреждение", "В заказе нет продукции для отчёта!")
            return

        pdf_file = f"order_report_{order_id}.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        style = styles['Normal']
        style.fontName = 'SegoeUIRegular'
        style.fontSize = 12

        elements.append(Paragraph(f"Заказ #{order.id}", style))
        elements.append(Paragraph(f"Дата создания: {order.Дата_создания}", style))
        elements.append(Paragraph("<br/>", style))

        data = [["Продукция", "Количество"]]
        for op in order_products:
            product = self.session.query(Product).filter(Product.id == op.id_продукции).first()
            product_name = product.Наименование if product else "Не указан"
            data.append([product_name, op.Количество])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'SegoeUIRegular'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)
        QMessageBox.information(self, "Успех", f"Отчёт по заказу #{order_id} успешно сохранён как {pdf_file}!")