from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

from processing.image_processor import ImageCaptureManager


class Session_View(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('KONECTO')
        self.resize(1024, 768)

        # Main frame
        self.info_frame = QFrame(self)
        self.info_frame.setGeometry(2, 2, 1020, 100)
        self.info_frame.setStyleSheet("background-color: gray;")

        self.video_frame = QFrame(self)
        self.video_frame.setGeometry(2, 104, 1020, 600)
        self.video_frame.setStyleSheet("background-color: gray;")

        self.buttons_frame = QFrame(self)
        self.buttons_frame.setGeometry(2, 708, 1020, 58)
        self.buttons_frame.setStyleSheet("background-color: gray;")

        # Text info layout
        self.product_name = QLabel(self.info_frame)
        self.product_name.setText("PRODUCTO 1")
        self.product_name.setStyleSheet("font-weight: bold;")
        self.product_name.setAlignment(Qt.AlignCenter)
        self.product_name.setGeometry(0, 0, 500, 100)

        self.product_quantity = QLabel(self.info_frame)
        self.product_quantity.setText("CANTIDAD: 4564 UD")
        self.product_quantity.setStyleSheet("font-weight: bold;")
        self.product_quantity.setAlignment(Qt.AlignCenter)
        self.product_quantity.setGeometry(502, 0, 500, 100)

        # Video layout
        self.video_layout = QHBoxLayout(self.video_frame)
        self.video_layout.setContentsMargins(0, 0, 0, 0)
        self.video_layout.setAlignment(Qt.AlignCenter)

        # Live video
        self.video_label = QLabel(self.video_frame)
        self.video_label.setFixedSize(320, 240)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet(
            "background-color: #CCE5FF; border: 1px solid black;")
        self.video_layout.addWidget(self.video_label)

        # Last detected image
        self.image_label = QLabel(self.video_frame)
        self.image_label.setFixedSize(320, 240)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(
            "background-color: #CCE5FF; border: 1px solid black;")
        self.video_layout.addWidget(self.image_label)

        # Buttons layout
        self.button_layout = QHBoxLayout(self.buttons_frame)

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(
            "background-color: #007BFF; color: white; border-radius: 5px; padding: 10px;")
        self.button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(
            "background-color: #FF5722; color: white; border-radius: 5px; padding: 10px;")
        self.button_layout.addWidget(self.stop_button)

        # Start ImageCaptureManager
        self.image_capture_manager = ImageCaptureManager()

        # Start timer to update image on GUI
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.start(60)  # ms

        # self.start_button.clicked.connect(self.image_capture_manager.start)
        # self.stop_button.clicked.connect(self.image_capture_manager.stop)

    def update_image(self):
        q_video, q_image = self.image_capture_manager.update_images()
        if q_image is not None:
            self.image_label.setPixmap(QPixmap.fromImage(q_image))
        if q_video is not None:
            self.video_label.setPixmap(QPixmap.fromImage(q_video))

    def closeEvent(self, event):
        self.image_capture_manager.release_camera()
        super().closeEvent(event)
