import cv2

from config.config import load_config
config = load_config()


class Camera:
    def __init__(self):
        self.capture = cv2.VideoCapture('/dev/video0')#config['camera']['source'])
        if not self.capture.isOpened():
            raise ValueError("Error opening video source")
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, config['camera']['resolution'][0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config['camera']['resolution'][1])
        fourcc = cv2.VideoWriter_fourcc(*f"{config['camera']['format']}")
        self.capture.set(cv2.CAP_PROP_FOURCC, fourcc)

    def get_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return None
        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # self.current_frame = int(self.capture.get(cv2.CAP_PROP_POS_FRAMES))
        return frame  # frame_rgb

    def release(self):
        self.capture.release()
