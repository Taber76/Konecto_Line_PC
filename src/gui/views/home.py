from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTableView, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem

from db.batches.dao import get_all
from config.config import load_styles
style = load_styles()


class Home_View(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.items = get_all()
        self.init_ui()

    def init_ui(self):
        # Widgets -------------------------
        # title
        self.title = QLabel("Batches")
        self.title.setStyleSheet(
            f"font-size: {int(style['header']['font-size']*1.5)}px;"
        )
        self.title.setAlignment(Qt.AlignCenter)

        # table
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            ["Code", "Product ID", "Product", "Date", "Total Produced", "Total Defects", "Batch ID"])
        self.populate_table(self.items)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.clicked.connect(self.row_clicked)

        self.table_view.setColumnWidth(0, 125)
        self.table_view.hideColumn(1)
        self.table_view.setColumnWidth(2, 290)
        self.table_view.setColumnWidth(3, 190)
        self.table_view.setColumnWidth(4, 180)
        self.table_view.setColumnWidth(5, 180)
        self.table_view.hideColumn(6)
       # N self.table_view.resizeColumnsToContents()
        self.table_view.setStyleSheet("""
            QTableView {
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                font-size: 14px;
                color: #333;
            }
            QTableView::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #e1e1e1;
                padding: 5px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
        """)

        # Layouts -------------------------
        # vertical layout
        lay_vertical_layout = QVBoxLayout()
        lay_vertical_layout.setAlignment(Qt.AlignCenter)
        lay_vertical_layout.addWidget(self.title)
        lay_vertical_layout.addWidget(self.table_view)

        # main horizontal layout
        lay_horizontal_layout = QHBoxLayout()
        lay_horizontal_layout.setAlignment(Qt.AlignCenter)
        lay_horizontal_layout.addLayout(lay_vertical_layout)
        self.setLayout(lay_horizontal_layout)
        self.setStyleSheet(
            f"font-family: {style['body']['font']};"
            f"font-size: {int(style['body']['font-size']*1)}px;"
            f"font-weight: {style['body']['font-weight']};"
            f"color: {style['body']['text_color']};"
        )

    def populate_table(self, items):
        for item in items:
            row = [
                QStandardItem(str(item.code)),
                QStandardItem(str(item.product_id)),
                QStandardItem(str(item.product_name)),
                QStandardItem(str(item.updated_at)),
                QStandardItem(str(item.total_produced)),
                QStandardItem(str(item.total_defects)),
                QStandardItem(str(item.id)),
            ]
            self.model.appendRow(row)

    def row_clicked(self, index):
        row_data = [self.model.item(index.row(), col).text()
                    for col in range(self.model.columnCount())]
        self.main_window.product = row_data[2]
        self.main_window.batch = f" / Batch: {row_data[0]}"
        self.main_window.batch_id = row_data[6]

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle(f"Loading")  # {row_data[2]}")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.show()
        self.main_window.change_view("session")
        self.dialog.close()
