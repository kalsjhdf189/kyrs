# main.py
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QHeaderView
)
from ProductWindow import ProductWidget
from MovementWindow import MovementWidget
from IncomingInvoiceWindow import IncomingInvoiceWidget
from OrderWindow import OrderWidget
from styles import MAIN_WINDOW_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление складом")
        self.setGeometry(200, 200, 900, 600)
        self.product_widget = None
        self.movement_widget = None
        self.invoice_widget = None
        self.order_widget = None
        self.setup_ui()

    def setup_ui(self):
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        
        self.show_products_btn = QPushButton("Продукция")
        self.show_products_btn.clicked.connect(self.toggle_product_table)
        
        self.show_movements_btn = QPushButton("Перемещения")
        self.show_movements_btn.clicked.connect(self.toggle_movement_table)
        
        self.show_invoices_btn = QPushButton("Поступления")
        self.show_invoices_btn.clicked.connect(self.toggle_invoice_table)
        
        self.show_orders_btn = QPushButton("Заказы")
        self.show_orders_btn.clicked.connect(self.toggle_order_table)
        
        self.button_layout.addWidget(self.show_products_btn)
        self.button_layout.addWidget(self.show_movements_btn)
        self.button_layout.addWidget(self.show_invoices_btn)
        self.button_layout.addWidget(self.show_orders_btn)
        self.button_layout.addStretch()
        
        self.main_layout.addLayout(self.button_layout)
        
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.main_layout.addWidget(self.content_area)
        
        self.setCentralWidget(self.main_widget)
        self.setStyleSheet(MAIN_WINDOW_STYLE)

    def toggle_product_table(self):
        if self.product_widget is None:
            if self.movement_widget is not None:
                self.content_layout.removeWidget(self.movement_widget)
                self.movement_widget.deleteLater()
                self.movement_widget = None
                self.show_movements_btn.setText("Перемещения")
            if self.invoice_widget is not None:
                self.content_layout.removeWidget(self.invoice_widget)
                self.invoice_widget.deleteLater()
                self.invoice_widget = None
                self.show_invoices_btn.setText("Поступления")
            if self.order_widget is not None:
                self.content_layout.removeWidget(self.order_widget)
                self.order_widget.deleteLater()
                self.order_widget = None
                self.show_orders_btn.setText("Заказы")
            
            self.product_widget = ProductWidget(self)
            self.content_layout.addWidget(self.product_widget)
            self.show_products_btn.setText("Скрыть продукцию")
        else:
            self.content_layout.removeWidget(self.product_widget)
            self.product_widget.deleteLater()
            self.product_widget = None
            self.show_products_btn.setText("Продукция")

    def toggle_movement_table(self):
        if self.movement_widget is None:
            if self.product_widget is not None:
                self.content_layout.removeWidget(self.product_widget)
                self.product_widget.deleteLater()
                self.product_widget = None
                self.show_products_btn.setText("Продукция")
            if self.invoice_widget is not None:
                self.content_layout.removeWidget(self.invoice_widget)
                self.invoice_widget.deleteLater()
                self.invoice_widget = None
                self.show_invoices_btn.setText("Поступления")
            if self.order_widget is not None:
                self.content_layout.removeWidget(self.order_widget)
                self.order_widget.deleteLater()
                self.order_widget = None
                self.show_orders_btn.setText("Заказы")
            
            self.movement_widget = MovementWidget(self)
            self.content_layout.addWidget(self.movement_widget)
            self.show_movements_btn.setText("Скрыть перемещения")
        else:
            self.content_layout.removeWidget(self.movement_widget)
            self.movement_widget.deleteLater()
            self.movement_widget = None
            self.show_movements_btn.setText("Перемещения")

    def toggle_invoice_table(self):
        if self.invoice_widget is None:
            if self.product_widget is not None:
                self.content_layout.removeWidget(self.product_widget)
                self.product_widget.deleteLater()
                self.product_widget = None
                self.show_products_btn.setText("Продукция")
            if self.movement_widget is not None:
                self.content_layout.removeWidget(self.movement_widget)
                self.movement_widget.deleteLater()
                self.movement_widget = None
                self.show_movements_btn.setText("Перемещения")
            if self.order_widget is not None:
                self.content_layout.removeWidget(self.order_widget)
                self.order_widget.deleteLater()
                self.order_widget = None
                self.show_orders_btn.setText("Заказы")
            
            self.invoice_widget = IncomingInvoiceWidget(self)
            self.content_layout.addWidget(self.invoice_widget)
            self.show_invoices_btn.setText("Скрыть поступления")
        else:
            self.content_layout.removeWidget(self.invoice_widget)
            self.invoice_widget.deleteLater()
            self.invoice_widget = None
            self.show_invoices_btn.setText("Поступления")

    def toggle_order_table(self):
        if self.order_widget is None:
            if self.product_widget is not None:
                self.content_layout.removeWidget(self.product_widget)
                self.product_widget.deleteLater()
                self.product_widget = None
                self.show_products_btn.setText("Продукция")
            if self.movement_widget is not None:
                self.content_layout.removeWidget(self.movement_widget)
                self.movement_widget.deleteLater()
                self.movement_widget = None
                self.show_movements_btn.setText("Перемещения")
            if self.invoice_widget is not None:
                self.content_layout.removeWidget(self.invoice_widget)
                self.invoice_widget.deleteLater()
                self.invoice_widget = None
                self.show_invoices_btn.setText("Поступления")
            
            self.order_widget = OrderWidget(self)
            self.content_layout.addWidget(self.order_widget)
            self.show_orders_btn.setText("Скрыть заказы")
        else:
            self.content_layout.removeWidget(self.order_widget)
            self.order_widget.deleteLater()
            self.order_widget = None
            self.show_orders_btn.setText("Заказы")