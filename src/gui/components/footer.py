from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt


class FooterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Configurar el contenido del footer
        self.label = QLabel("Este es el Footer")
        self.label.setStyleSheet(
            "background-color: lightgray; font-size: 14px; padding: 10px;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
