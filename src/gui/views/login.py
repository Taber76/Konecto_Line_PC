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

        # Widgets -------------------------
        # username
        wid_username_label = QLabel("Username:")
        wid_username_label.setFixedWidth(int(config['screen']['width'] * 0.1))
        self.wid_username_input = QLineEdit()
        self.wid_username_input.setFixedWidth(
            int(config['screen']['width'] * 0.2))

        # password
        wid_password_label = QLabel("Password:")
        wid_password_label.setFixedWidth(int(config['screen']['width'] * 0.1))
        self.wid_password_input = QLineEdit()
        self.wid_password_input.setFixedWidth(
            int(config['screen']['width'] * 0.2))
        self.wid_password_input.setEchoMode(QLineEdit.Password)

        # login button
        wid_login_button = QPushButton("LOGIN")
        wid_login_button.setStyleSheet(
            f"{style['button']['small']}")
        wid_login_button.clicked.connect(self.handle_login)
        wid_login_button.setFixedWidth(int(config['screen']['width'] * 0.1))
        wid_login_button.setFixedHeight(
            int(config['screen']['height'] * 0.05))

        # Layouts -------------------------
        # username layout
        lay_username = QHBoxLayout()
        lay_username.setAlignment(Qt.AlignCenter)
        lay_username.addWidget(wid_username_label)
        lay_username.addWidget(self.wid_username_input)

        # password layout
        lay_password = QHBoxLayout()
        lay_password.setAlignment(Qt.AlignCenter)
        lay_password.addWidget(wid_password_label)
        lay_password.addWidget(self.wid_password_input)

        # button layout
        lay_button = QHBoxLayout()
        lay_button.setAlignment(Qt.AlignCenter)
        lay_button.addWidget(wid_login_button)

        # main vertical layout
        lay_vertical_layout = QVBoxLayout()
        lay_vertical_layout.setAlignment(Qt.AlignCenter)
        lay_vertical_layout.addLayout(lay_username)
        lay_vertical_layout.addLayout(lay_password)
        lay_vertical_layout.addLayout(lay_button)

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

    def handle_login(self):
        success, user_data = authenticate(
            self.wid_username_input.text(), self.wid_password_input.text())
        if success:
            self.wid_username_input.setText("")
            self.wid_password_input.setText("")
            self.main_window.user['fullname'] = user_data.fullname
            self.main_window.change_view("home")
        else:
            QMessageBox.warning(self, "Login Error",
                                "Incorrect username or password.")
