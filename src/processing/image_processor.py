import cv2
import numpy as np
from PySide6.QtGui import QImage
from PySide6.QtCore import QTimer

from processing.yolo_processor import YOLOProcessor
from capture.camera import Camera

from config.config import load_config
config = load_config()


class ImageCaptureManager:

    def __init__(self):
        self.camera = Camera()
        self.processor = YOLOProcessor()
        self.checkpoint_line_x = 160
        self.detected_units = 0
        self.tracks = []
        self.previous_tracks = {}
        self.current_frame = None
        self.last_detection = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.proccess_frame)
        self.timer.start(config['processing']['interval'])

    def proccess_frame(self):  # Process current frame to detect objects
        self.current_frame = self.camera.get_frame()
        if self.current_frame is not None:
            detections = self.processor.process_frame(self.current_frame)
            self.tracks = self.processor.update_tracks(
                detections, self.current_frame)
        self.checkpoint_reach()

    def checkpoint_reach(self):  # Check if checkpoint is reached
        for track in self.tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            box = track.to_ltrb()
            if track_id in self.previous_tracks:
                previous_box = self.previous_tracks[track_id]
                if previous_box[0] < self.checkpoint_line_x and box[0] >= self.checkpoint_line_x:
                    x, y = int((box[0]+box[2])/2), int((box[1]+box[3])/2)
                    self.last_detection = self.zoom_image(
                        self.current_frame, x, y, 2.5)
                    self.detected_units += 1
            self.previous_tracks[track_id] = box

    def update_images(self):  # Update images only for show on screen
        if self.current_frame is None:
            return None, None

        # Convert frame to RGB for show on screen
        # self.current_frame = cv2.cvtColor(
        #    self.current_frame, cv2.COLOR_BGR2RGB)

        # Draw tracks
        for track in self.tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            ltrb = track.to_ltrb()
            class_name = track.det_class
            cv2.rectangle(self.current_frame, (int(ltrb[0]), int(
                ltrb[1])), (int(ltrb[2]), int(ltrb[3])), (255, 0, 0), 2)
            cv2.putText(self.current_frame, f'{class_name}', (int(
                ltrb[0]), int(ltrb[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Draw checkpoint line and number of detections
        cv2.line(self.current_frame, (self.checkpoint_line_x, 10),
                 (self.checkpoint_line_x, 230), (0, 255, 0), 2)
        cv2.putText(self.current_frame, f'Detections: {
                    self.detected_units}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        height, width, channel = self.current_frame.shape
        bytes_per_line = 3 * width
        q_video = QImage(self.current_frame.data, width, height,
                         bytes_per_line, QImage.Format_RGB888)
        q_image = self.last_detection
        if q_image is not None:
            height, width, channel = self.last_detection.shape
            bytes_per_line = 3 * width
            q_image = QImage(self.last_detection.data, width,
                             height, bytes_per_line, QImage.Format_RGB888)
        return q_video, q_image

    def zoom_image(self, frame, x_center, y_center, zoom_factor):
        frame_height, frame_width = frame.shape[:2]
        new_width = int(frame_width / zoom_factor)
        new_height = int(frame_height / zoom_factor)
        x1 = max(int(x_center - new_width // 2), 0)
        y1 = max(int(y_center - new_height // 2), 0)
        x2 = min(int(x_center + new_width // 2), frame_width)
        y2 = min(int(y_center + new_height // 2), frame_height)
        cropped_frame = frame[y1:y2, x1:x2]
        zoomed_image = cv2.resize(
            cropped_frame, (frame_width, frame_height), interpolation=cv2.INTER_LINEAR)
        return zoomed_image

    def stop(self):
        self.timer.stop()

    def release_camera(self):
        self.camera.release()
