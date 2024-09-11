from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit


class OnScreenKeyboard(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('On-Screen Keyboard')
        self.setFixedSize(400, 300)

        # Entry line where text will appear
        self.input_field = QLineEdit(self)

        # Create a grid layout for the keyboard
        keyboard_layout = QGridLayout()

        # Keyboard keys (letters and numbers as an example)
        buttons = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Space', 'Backspace']
        ]

        # Populate the grid layout with buttons
        for row, keys in enumerate(buttons):
            for col, key in enumerate(keys):
                button = QPushButton(key)
                button.setFixedSize(40, 40)

                # Connect button click to handler function
                button.clicked.connect(
                    lambda checked, key=key: self.key_pressed(key))

                keyboard_layout.addWidget(button, row, col)

        # Organize everything in a vertical layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_field)
        main_layout.addLayout(keyboard_layout)

        self.setLayout(main_layout)

    def key_pressed(self, key):
        if key == 'Space':
            self.input_field.insert(' ')
        elif key == 'Backspace':
            current_text = self.input_field.text()
            self.input_field.setText(current_text[:-1])
        else:
            self.input_field.insert(key)
