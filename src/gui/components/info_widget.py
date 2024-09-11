from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

from config.config import load_config
config = load_config()


class InfoWidget(QWidget):
    def __init__(self, label_text, value_text, height, size):
        super().__init__()
        self.init_ui(label_text, value_text, height, size)

    def init_ui(self, label_text, value_text, height, size):
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(config['style']['label'][size])

        self.value = QLabel(value_text)
        self.value.setAlignment(Qt.AlignCenter)
        self.value.setStyleSheet(config['style']['label'][size])

        frame = QVBoxLayout()
        frame.addWidget(label)
        frame.addWidget(self.value)
        self.setLayout(frame)
        self.setFixedHeight(height)

    def update_value(self, new_value):
        self.value.setText(new_value)
