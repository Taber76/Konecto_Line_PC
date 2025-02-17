from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QTimer, QDateTime, QRunnable, QThreadPool
from PySide6.QtGui import QPixmap

from processing.image_processor import ImageCaptureManager
from db.batches.dao import batch_update
from db.sessions.dao import session_register, session_update
from db.counts.dao import count_register
from db.logs.dao import log_register
from gui.components.info_widget import InfoWidget
from config.config import load_config, load_styles
config = load_config()
style = load_styles()


class Session_View(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('KONECTO')
        self.start_pause_button_text = 'Start'
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

        # Timer to update batch, session and register counts
        self.timer_db = QTimer()
        self.timer_db.timeout.connect(self.update_db)
        self.last_count = 0
        self.total_last_count = 0

    def init_ui(self):

        # INFO ------------------------------------------------------------------
        self.start_frame = InfoWidget(
            "Start time", "--:--", int(config['screen']['height'] * 0.15), 'medium')
        self.quantity_frame = InfoWidget(
            "Quantity", "--", int(config['screen']['height'] * 0.15), 'medium')
        self.defects_frame = InfoWidget(
            "Defects", "--", int(config['screen']['height'] * 0.15), 'medium')
        self.quality_frame = InfoWidget(
            "Quality", "--%", int(config['screen']['height'] * 0.15), 'medium')
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setAlignment(Qt.AlignCenter)
        info_layout.setSpacing(30)
        info_layout.addWidget(self.start_frame)
        info_layout.addWidget(self.quantity_frame)
        info_layout.addWidget(self.defects_frame)
        info_layout.addWidget(self.quality_frame)

        # VIDEO -----------------------------------------------------------------
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

        video_layout = QHBoxLayout()
        video_layout.setContentsMargins(0, 0, 0, 0)
        video_layout.setAlignment(Qt.AlignCenter)
        video_layout.addLayout(live_video_frame)
        video_layout.addLayout(last_image_frame)

        # BUTTONS --------------------------------------------------------------
        self.start_button = QPushButton(self.start_pause_button_text)
        self.start_button.setStyleSheet(style['button']['medium'])
        self.start_button.setFixedHeight(100)
        self.start_button.clicked.connect(self.start)

        stop_button = QPushButton("Finish")
        stop_button.setStyleSheet(
            style['button']['medium'] + 'background-color: red;')
        stop_button.setFixedHeight(100)
        stop_button.clicked.connect(self.confirm_finish)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.setSpacing(30)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(stop_button)

        # MAIN LAYOUT ----------------------------------------------------------
        main_layout = QVBoxLayout()
        main_layout.addLayout(info_layout)
        main_layout.addLayout(video_layout)
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    # for start button
    def start(self):
        if self.start_pause_button_text == 'Start' or self.start_pause_button_text == 'Resume':
            self.image_capture_manager.start()
            self.timer.start(60)        # for update image
            self.timer_db.start(60000)  # for update session and register on DB
            self.start_pause_button_text = 'Pause'
            self.start_button.setText(self.start_pause_button_text)
            if self.session_id is None:  # first time click start button
                self.start_frame.update_value(QDateTime.currentDateTime().toString(
                    "HH:mm"
                ))
                self.session_id = session_register(
                    config['line_id'], self.main_window.batch_id, QDateTime.currentDateTime(
                    ).toString("yyyy-MM-dd HH:mm:ss"),
                )
                self.quality_frame.update_value("100%")
                log_register(
                    self.session_id,
                    self.main_window.user['id'],
                    self.main_window.user['fullname'],
                    QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss"),
                    f'Start session {self.main_window.batch}'
                )
            else:  # for resume
                log_register(
                    self.session_id,
                    self.main_window.user['id'],
                    self.main_window.user['fullname'],
                    QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss"),
                    f'Resume session {self.main_window.batch}'
                )
        else:  # for pause
            self.start_pause_button_text = 'Resume'
            self.start_button.setText(self.start_pause_button_text)
            self.image_capture_manager.stop()
            self.timer.stop()
            self.timer_db.stop()
            log_register(
                self.session_id,
                self.main_window.user['id'],
                self.main_window.user['fullname'],
                QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss"),
                f'Pause session {self.main_window.batch}'
            )

    # confirm finish session
    def confirm_finish(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Are you sure you want to finish this session?")
        msg.setWindowTitle("Finish Session")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg.exec_() == QMessageBox.Yes:
            self.finish()
        else:
            pass

    # for finish button
    def finish(self):
        log_register(
            self.session_id,
            self.main_window.user['id'],
            self.main_window.user['fullname'],
            QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss"),
            f'Finish session {self.main_window.batch}'
        )

        self.image_capture_manager.stop()
        self.timer.stop()
        self.timer_db.stop()

        self.update_db()
        self.total_quantity = 0
        self.total_defects = 0
        self.total_last_count = 0
        self.session_id = None
        self.start_pause_button_text = 'Start'
        self.start_button.setText('Start')

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
        if quantity == 0:  # No detections in the last minute
            self.last_count += 1
            self.total_last_count += 1
        else:
            db_task = DatabaseTask(
                self.main_window.batch_id,
                self.session_id,
                quantity,
                defects,
                self.total_quantity,
                self.total_defects,
                self.last_count,
                self.total_last_count
            )
            self.threadpool.start(db_task)  # start task on a separate thread
            self.last_count = 0

    def closeEvent(self, event):
        self.image_capture_manager.release_camera()
        super().closeEvent(event)


class DatabaseTask(QRunnable):
    def __init__(self, batch_id, session_id, quantity, defects, total_quantity, total_defects, time_diff, downtime_minutes):
        super().__init__()
        self.batch_id = batch_id
        self.session_id = session_id
        self.quantity = quantity
        self.defects = defects
        self.total_quantity = total_quantity
        self.total_defects = total_defects
        self.time_diff = time_diff
        self.downtime_minutes = downtime_minutes

    def run(self):
        try:
            timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

            batch_update(
                self.batch_id,
                self.quantity,
                self.defects,
                self.downtime_minutes,
                timestamp
            )
            session_update(
                self.session_id,
                end_time=timestamp,
                quantity=self.total_quantity,
                defects=self.total_defects,
                downtime_minutes=self.downtime_minutes
            )
            count_register(
                timestamp,
                self.session_id,
                self.quantity,
                self.defects,
                self.time_diff,
                'MINUTES'
            )
        except Exception as e:
            print(f"An error occurred: {e}")
