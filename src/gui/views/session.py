from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QFrame, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer, QDateTime, QRunnable, QThreadPool
from PySide6.QtGui import QPixmap
from sympy import Q

from processing.image_processor import ImageCaptureManager
from db.sessions.dao import session_register, session_update
from db.counts.dao import count_register
from gui.components.info_widget import InfoWidget
from config.config import load_config, load_styles
config = load_config()
style = load_styles()


class Session_View(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('KONECTO')
        self.init_ui()
        self.image_capture_manager = ImageCaptureManager()
        self.total_quantity = 0
        self.total_defects = 0
        self.session_id = None
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)

        # Timer to update image on GUI
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)

        # Timer to update session and register counts
        self.timer_db = QTimer()
        self.timer_db.timeout.connect(self.update_db)

    def init_ui(self):
        # INFO WIDGETS ------------------------------------------------------------
        # start time
        self.start_frame = InfoWidget(
            "Start time", "--:--", int(config['screen']['height'] * 0.15), 'medium')

        # quantity
        self.quantity_frame = InfoWidget(
            "Quantity", "--", int(config['screen']['height'] * 0.15), 'medium')

        # defects
        self.defects_frame = InfoWidget(
            "Defects", "--", int(config['screen']['height'] * 0.15), 'medium')

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
        start_button.setStyleSheet(style['button']['medium'])
        start_button.setFixedHeight(100)
        start_button.clicked.connect(self.start)

        # pause button
        pause_button = QPushButton("Pause")
        pause_button.setStyleSheet(style['button']['medium'])
        pause_button.setFixedHeight(100)
        pause_button.clicked.connect(self.pause)

        # finish button
        stop_button = QPushButton("Finish")
        stop_button.setStyleSheet(style['button']['medium'])
        stop_button.setFixedHeight(100)
        stop_button.clicked.connect(self.finish)

        # LAYOUTS --------------------------------------------------------------
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setAlignment(Qt.AlignCenter)
        info_layout.setSpacing(30)
        info_layout.addWidget(self.start_frame)
        info_layout.addWidget(self.quantity_frame)
        info_layout.addWidget(self.defects_frame)
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

    # for start button
    def start(self):
        self.image_capture_manager.start()
        self.timer.start(60)        # for update image
        self.timer_db.start(6000)   # for update session and register on DB
        if self.session_id is None:
            self.start_frame.update_value(QDateTime.currentDateTime().toString(
                "HH:mm"
            ))
            self.session_id = session_register(
                config['line_id'], self.main_window.batch_id, QDateTime.currentDateTime(
                ).toString("yyyy-MM-dd HH:mm:ss"),
            )
            self.quality_frame.update_value("100%")

    # for pause button
    def pause(self):
        self.image_capture_manager.stop()
        self.timer.stop()
        self.timer_db.stop()

    # for finish button
    def finish(self):
        self.image_capture_manager.stop()
        self.timer.stop()
        self.timer_db.stop()

        self.update_db()
        self.total_quantity = 0
        self.total_defects = 0
        self.session_id = None

        self.start_frame.update_value("--:--")
        self.quantity_frame.update_value("--")
        self.defects_frame.update_value("--")
        self.quality_frame.update_value("--%")
        self.live_video.setPixmap(QPixmap())
        self.last_image.setPixmap(QPixmap())

        self.main_window.change_view('home')

    # update image and data only for show in window
    def update_image(self):
        q_video, q_image, quantity, defects = self.image_capture_manager.update_images()
        if q_image is not None:
            self.last_image.setPixmap(QPixmap.fromImage(q_image))
        if q_video is not None:
            self.live_video.setPixmap(QPixmap.fromImage(q_video))
        total_detected = self.total_quantity + quantity
        total_defects = self.total_defects + defects
        if total_detected != 0:
            quality_percentage = round(
                ((total_detected - total_defects) / total_detected) * 100, 2)
            self.quantity_frame.update_value(f"{total_detected}")
            self.defects_frame.update_value(f"{total_defects}")
            self.quality_frame.update_value(f"{quality_percentage}%")

    # update database every minute: session and count tables
    def update_db(self):
        quantity, defects = self.image_capture_manager.get_counts()
        self.total_quantity += quantity
        self.total_defects += defects
        self.image_capture_manager.reset_counts()
        db_task = DatabaseTask(
            self.session_id,
            quantity,
            defects,
            self.total_quantity,
            self.total_defects
        )
        self.threadpool.start(db_task)

    def closeEvent(self, event):
        self.image_capture_manager.release_camera()
        super().closeEvent(event)


class DatabaseTask(QRunnable):
    def __init__(self, session_id, quantity, defects, total_quantity, total_defects):
        super().__init__()
        self.session_id = session_id
        self.quantity = quantity
        self.defects = defects
        self.total_quantity = total_quantity
        self.total_defects = total_defects

    def run(self):
        time_stamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

        session_update(
            self.session_id,
            end_time=time_stamp,
            quantity=self.total_quantity,
            defects=self.total_defects
        )
        count_register(
            time_stamp,
            self.session_id,
            self.quantity,
            self.defects,
            0,
            'MINUTES'
        )
