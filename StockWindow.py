# StockWindow.py
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datebase import ProductOnWarehouse, Warehouse, Connect
from styles import TABLE_WIDGET_STYLE
import numpy as np

class StockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Connect.create_connection()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        # Создание canvas для matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.load_pie_chart_data()
        self.setStyleSheet(TABLE_WIDGET_STYLE)

    def load_pie_chart_data(self):
        # Получение данных из ProductOnWarehouse
        stocks = self.session.query(ProductOnWarehouse).all()
        
        # Агрегация количества продукции по складам
        warehouse_totals = {}
        for stock in stocks:
            warehouse_id = stock.id_склада
            warehouse = self.session.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
            warehouse_name = warehouse.Название if warehouse else f"Склад {warehouse_id}"
            warehouse_totals[warehouse_name] = warehouse_totals.get(warehouse_name, 0) + stock.Количество

        # Подготовка данных для круговой диаграммы
        warehouses = list(warehouse_totals.keys())
        quantities = list(warehouse_totals.values())

        # Очистка предыдущего графика
        self.figure.clear()

        # Создание круговой диаграммы
        ax = self.figure.add_subplot(111)
        ax.pie(quantities, labels=warehouses, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Устанавливаем равные пропорции для круга
        ax.set_title('Распределение продукции по складам')

        # Обновление canvas
        self.canvas.draw()