import cv2
import numpy as np

class DetectionVisualizer:
    def __init__(self, class_names: dict):
        self.class_names = class_names
        # Color mapping (BGR)
        self.colors = {
            "player": (255, 0, 0),      # Blue
            "goalkeeper": (0, 165, 255),# Orange
            "referee": (0, 255, 255),   # Yellow
            "ball": (0, 0, 255)         # Red
        }

    def draw(self, image: np.ndarray, boxes: np.ndarray, scores: np.ndarray, class_ids: np.ndarray) -> np.ndarray:
        """
        Draws bounding boxes on the image.
        boxes: [N, 4] format (x1, y1, x2, y2) absolute coordinates.
        """
        out_img = image.copy()
        
        for box, score, cls_id in zip(boxes, scores, class_ids):
            x1, y1, x2, y2 = map(int, box)
            
            cls_name = self.class_names.get(int(cls_id), "unknown")
            color = self.colors.get(cls_name, (255, 255, 255))
            
            # Draw box
            cv2.rectangle(out_img, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{cls_name} {score:.2f}"
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(out_img, (x1, y1 - 20), (x1 + w, y1), color, -1)
            cv2.putText(out_img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            
        return out_img
