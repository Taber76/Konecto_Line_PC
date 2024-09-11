from PySide6.QtWidgets import QFrame, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer, QDateTime
from PySide6.QtGui import QPixmap
from sympy import Q

from processing.image_processor import ImageCaptureManager
from gui.components.info_widget import InfoWidget
from config.config import load_config
config = load_config()


class Session_View(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('KONECTO')
        self.init_ui()
        self.image_capture_manager = ImageCaptureManager()

        # Timer to update image on GUI
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)

    def init_ui(self):
        # INFO WIDGETS ------------------------------------------------------------
        # start time
        self.start_frame = InfoWidget(
            "Start time", "--:--", int(config['screen']['height'] * 0.15), 'medium')

        # quantity
        self.quantity_frame = InfoWidget(
            "Quantity", "--", int(config['screen']['height'] * 0.15), 'medium')

        # quality
        self.quality_frame = InfoWidget(
            "Quality", "--%", int(config['screen']['height'] * 0.15), 'medium')

        # IMAGE WIDGETS -----------------------------------------------------------
        # live video
        live_video_label = QLabel("Live video")
        self.live_video = QLabel("Live video")
        self.live_video.setFixedSize(480, 360)
        self.live_video.setAlignment(Qt.AlignCenter)
        self.live_video.setStyleSheet(
            "background-color: #CCE5FF; border: 1px solid black;")
        self.live_video.setScaledContents(True)
        live_video_frame = QVBoxLayout()
        live_video_frame.addWidget(live_video_label)
        live_video_frame.addWidget(self.live_video)

        # last image
        last_image_label = QLabel("Last image")
        self.last_image = QLabel("Last image")
        self.last_image.setFixedSize(480, 360)
        self.last_image.setAlignment(Qt.AlignCenter)
        self.last_image.setStyleSheet(
            "background-color: #CCE5FF; border: 1px solid black;")
        self.last_image.setScaledContents(True)
        last_image_frame = QVBoxLayout()
        last_image_frame.addWidget(last_image_label)
        last_image_frame.addWidget(self.last_image)

        # BUTTONS WIDGETS --------------------------------------------------------
        # start button
        start_button = QPushButton("Start")
        start_button.setStyleSheet(config['style']['button']['medium'])
        start_button.setFixedHeight(100)
        start_button.clicked.connect(self.start)

        # pause button
        pause_button = QPushButton("Pause")
        pause_button.setStyleSheet(config['style']['button']['medium'])
        pause_button.setFixedHeight(100)
        pause_button.clicked.connect(self.pause)

        # finish button
        stop_button = QPushButton("Finish")
        stop_button.setStyleSheet(config['style']['button']['medium'])
        stop_button.setFixedHeight(100)
        stop_button.clicked.connect(self.finish)

        # LAYOUTS --------------------------------------------------------------
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setAlignment(Qt.AlignCenter)
        info_layout.setSpacing(30)
        info_layout.addWidget(self.start_frame)
        info_layout.addWidget(self.quantity_frame)
        info_layout.addWidget(self.quality_frame)

        video_layout = QHBoxLayout()
        video_layout.setContentsMargins(0, 0, 0, 0)
        video_layout.setAlignment(Qt.AlignCenter)
        video_layout.addLayout(live_video_frame)
        video_layout.addLayout(last_image_frame)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.setSpacing(30)
        buttons_layout.addWidget(start_button)
        buttons_layout.addWidget(pause_button)
        buttons_layout.addWidget(stop_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(info_layout)
        main_layout.addLayout(video_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def start(self):
        self.image_capture_manager.start()
        self.timer.start(60)
        self.start_frame.update_value(QDateTime.currentDateTime().toString(
            "HH:mm"
        ))
        self.quality_frame.update_value("100%")

    def pause(self):
        self.image_capture_manager.stop()
        self.timer.stop()

    def finish(self):
        self.image_capture_manager.stop()
        self.timer.stop()
        self.start_frame.update_value("--:--")
        self.quantity_frame.update_value("--")
        self.quality_frame.update_value("--%")
        self.live_video.setPixmap(QPixmap())
        self.last_image.setPixmap(QPixmap())
        self.main_window.change_view('home')

    def update_image(self):
        q_video, q_image, detected_units = self.image_capture_manager.update_images()
        if q_image is not None:
            self.last_image.setPixmap(QPixmap.fromImage(q_image))
        if q_video is not None:
            self.live_video.setPixmap(QPixmap.fromImage(q_video))
        self.quantity_frame.update_value(f"{detected_units}")

    def closeEvent(self, event):
        self.image_capture_manager.release_camera()
        super().closeEvent(event)
