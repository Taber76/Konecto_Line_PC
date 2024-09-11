from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt

from gui.components.keyboard import OnScreenKeyboard


class FooterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Este es el Footer")
        self.label.setStyleSheet(
            "background-color: lightgray; font-size: 14px; padding: 10px;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Botón para mostrar/ocultar el teclado
        # self.toggle_keyboard_button = QPushButton("Mostrar Teclado")
        # self.toggle_keyboard_button.clicked.connect(self.toggle_keyboard)
        # layout.addWidget(self.toggle_keyboard_button)

        # Crear la instancia del teclado pero mantenerlo oculto inicialmente
        # self.keyboard = OnScreenKeyboard()
        # self.keyboard.hide()

    def toggle_keyboard(self):
        if self.keyboard.isVisible():
            self.keyboard.hide()
            self.toggle_keyboard_button.setText("Mostrar Teclado")
        else:
            self.keyboard.show()
            self.toggle_keyboard_button.setText("Ocultar Teclado")
