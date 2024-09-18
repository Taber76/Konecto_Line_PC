from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox
from PySide6.QtCore import Qt

from db.users.dao import authenticate
from config.config import load_config, load_styles
config = load_config()
style = load_styles()


class Login_View(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):

        # USERNAME --------------------------------------------------------------
        username_label_widget = QLabel("Username:")
        username_label_widget.setFixedWidth(
            int(config['screen']['width'] * 0.1))
        self.username_input_widget = QLineEdit()
        self.username_input_widget.setFixedWidth(
            int(config['screen']['width'] * 0.2))
        username_layout = QHBoxLayout()
        username_layout.setAlignment(Qt.AlignCenter)
        username_layout.addWidget(username_label_widget)
        username_layout.addWidget(self.username_input_widget)

        # PASSWORD --------------------------------------------------------------
        password_label_widget = QLabel("Password:")
        password_label_widget.setFixedWidth(
            int(config['screen']['width'] * 0.1))
        self.password_input_widget = QLineEdit()
        self.password_input_widget.setFixedWidth(
            int(config['screen']['width'] * 0.2))
        self.password_input_widget.setEchoMode(QLineEdit.Password)
        password_layout = QHBoxLayout()
        password_layout.setAlignment(Qt.AlignCenter)
        password_layout.addWidget(password_label_widget)
        password_layout.addWidget(self.password_input_widget)

        # LOGIN BUTTON ------------------------------------------------------------
        login_button_widget = QPushButton("LOGIN")
        login_button_widget.setStyleSheet(
            f"{style['button']['small']}")
        login_button_widget.clicked.connect(self.handle_login)
        login_button_widget.setFixedWidth(int(config['screen']['width'] * 0.1))
        login_button_widget.setFixedHeight(
            int(config['screen']['height'] * 0.05))
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(login_button_widget)

        # MAIN LAYOUT ------------------------------------------------------------
        # main vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignCenter)
        vertical_layout.addLayout(username_layout)
        vertical_layout.addLayout(password_layout)
        vertical_layout.addLayout(button_layout)

        # main horizontal layout
        main_horizontal_layout = QHBoxLayout()
        main_horizontal_layout.setAlignment(Qt.AlignCenter)
        main_horizontal_layout.addLayout(vertical_layout)
        self.setLayout(main_horizontal_layout)
        self.setStyleSheet(
            f"font-family: {style['body']['font']};"
            f"font-size: {int(style['body']['font-size']*1)}px;"
            f"font-weight: {style['body']['font-weight']};"
            f"color: {style['body']['text_color']};"
        )

    def handle_login(self):
        success, user_data = authenticate(
            self.username_input_widget.text(), self.password_input_widget.text())
        if success:
            self.username_input_widget.setText("")
            self.password_input_widget.setText("")
            self.main_window.user['fullname'] = user_data.fullname
            self.main_window.change_view("home")
        else:
            QMessageBox.warning(self, "Login Error",
                                "Incorrect username or password.")
