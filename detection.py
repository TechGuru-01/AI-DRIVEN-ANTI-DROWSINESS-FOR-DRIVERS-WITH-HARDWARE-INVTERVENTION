import numpy as np
from ultralytics import YOLO
from states import DriverStates

class LuminaDetection:
    def __init__(self, model="best.pt"):
        self.model = YOLO(model)
        self.state_timer = DriverStates()
        self.last_state = None  

    def run(self):
        try:
            stream = self.model.track(source=0, device=0, max_det=1, conf=0.15, tracker="bytetrack.yaml", stream=True, show=True)
            
            for result in stream:
                if result is None or not hasattr(result, "boxes") or result.boxes is None:
                    self.last_state = "NO_DRIVER"
                    continue

                boxes_list = []
                classes_list = []
                ids_list = []

                if len(result.boxes) > 0:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    classes = result.boxes.cls.cpu().numpy()
                    
                    if hasattr(result.boxes, "id") and result.boxes.id is not None:
                        ids = result.boxes.id.cpu().numpy()
                    else:
                        ids = np.arange(len(boxes))

                    for box, cls, tid in zip(boxes, classes, ids):
                        boxes_list.append(box)
                        classes_list.append(int(cls))
                        ids_list.append(tid)

                if len(boxes_list) == 0:
                    self.state_timer.curr_state = self.state_timer.idle_state
                    self.state_timer.awake_time = None
                    self.state_timer.drowsy_time = None
                    self.state_timer.yawn_time = None
                else:
                    if self.state_timer.curr_state == self.state_timer.idle_state:
                        self.state_timer.curr_state = self.state_timer.state_0
                        self.state_timer.awake_time = None
                        self.state_timer.drowsy_time = None
                        self.state_timer.yawn_time = None

                    if len(classes_list) > 0:
                        cls = max(set(classes_list), key=classes_list.count)
                        self.state_timer.update(cls)

                label = self.state_timer.outputs()
                self.last_state = label

        except KeyboardInterrupt:
            pass

    def get_last_state(self):
        return self.last_state