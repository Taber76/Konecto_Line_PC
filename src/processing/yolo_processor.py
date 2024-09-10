from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

from config.config import load_config
config = load_config()

# ver donde meter esto
class_names = {
    0: "bucosan",
    1: "alerfast",
    2: "other"
}


class YOLOProcessor:
    def __init__(self, model_path="last.pt"):  # yolov8n.pt"):
        self.model = YOLO(model_path)
        self.model.predict(imgsz=(224, 320))
        # max_age quantyty of frames after detection that a track will be deleted, n_init number of consecutive detections before track creation
        self.tracker = DeepSort(max_age=config['processing']['max_age'], n_init=config['processing']
                                ['n_init'], nms_max_overlap=config['processing']['nms_max_overlap'])
        self.detection_threshold = config['processing']['detection_threshold']
        self.class_names = class_names

    def process_frame(self, frame):
        detections = []
        results = self.model(frame)
        for result in results:
            for r in result.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = r
                if score > self.detection_threshold:
                    class_name = self.class_names.get(int(class_id), "unknown")
                    detections.append(
                        ([int(x1), int(y1), int(x2)-int(x1), int(y2)-int(y1)], score, class_name))
        return detections

    def update_tracks(self, detections, frame):
        return self.tracker.update_tracks(detections, frame=frame)
