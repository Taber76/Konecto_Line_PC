from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QDateTime, QTimer

from config.config import load_config, load_styles
config = load_config()
style = load_styles()


class HeaderWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.setStyleSheet(
            f"background-color: {style['header']['background_color']};"
            f"font-family: {style['header']['font']};"
            f"font-weight: {style['header']['font-weight']};"
            f"color: {style['header']['text_color']};"
        )
        self.setFixedWidth(config['screen']['width'])
        self.setFixedHeight(int(config['screen']['height'] * 0.08))

        # First line layout
        header_layout = QHBoxLayout()
        main_layout.addLayout(header_layout)
        header_layout.setAlignment(Qt.AlignCenter)

        # Date and time
        self.date_time_label = QLabel(self)
        self.update_date_time()
        self.date_time_label.setStyleSheet(
            f"padding: {style['header']['padding']};"
            f"font-size: {int(style['header']['font-size']*1)}px;"
        )
        self.date_time_label.setFixedWidth(
            int(config['screen']['width'] * 0.15))
        self.date_time_label.setFixedHeight(
            int(config['screen']['height'] * 0.07))
        self.date_time_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.date_time_label)

        # Product name / Batch code
        self.product_label = QLabel(f"{self.main_window.product}{self.main_window.batch}")
        self.product_label.setStyleSheet(
            f"padding: {style['header']['padding']};"
            f"font-size: {int(style['header']['font-size']*1.5)}px;"
        )
        self.product_label.setFixedWidth(int(config['screen']['width'] * 0.7))
        self.product_label.setFixedHeight(int(config['screen']['height'] * 0.07))
        self.product_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.product_label)

        # Logged user
        self.logged_user = QLabel(f"{self.main_window.user['fullname']}")
        self.logged_user.setStyleSheet(
            f"padding: {style['header']['padding']};"
            f"font-size: {int(style['header']['font-size']*0.7)}px;"
        )
        self.logged_user.setFixedWidth(int(config['screen']['width'] * 0.1))
        self.logged_user.setFixedHeight(int(config['screen']['height'] * 0.05))
        self.logged_user.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.logged_user)

        # Button logout
        self.button = QPushButton("LOGOUT")
        self.button.setStyleSheet(f"{style['button']['small']}")
        self.button.clicked.connect(self.logout)
        self.button.setFixedWidth(int(config['screen']['width'] * 0.1))
        self.button.setFixedHeight(int(config['screen']['height'] * 0.05))
        header_layout.addWidget(self.button)

        # Update date and time every minute
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(60000)

    def update_date_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm")
        self.date_time_label.setText(current_time)

    def update_info(self):
        self.logged_user.setText(self.main_window.user['fullname'])
        self.product_label.setText(f"{self.main_window.product}{self.main_window.batch}")

    def logout(self):
        self.main_window.user = {"id": None, "fullname": None, "role": None}
        self.main_window.product = ""
        self.main_window.batch = ""
        self.main_window.change_view('login')
