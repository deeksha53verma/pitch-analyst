import csv
from pathlib import Path
from typing import Dict, List, Any
import numpy as np
from omegaconf import DictConfig
from matchmind.core.logger import logger

class MatchTracker:
    def __init__(self, config: DictConfig):
        self.config = config.tracker.params
        
        # State storage
        # {track_id: {"history": [ [x1,y1,x2,y2], ... ], "class_id": int, "frames": [int, ...]}}
        self.tracks = {}
        self.smoothing_factor = self.config.get("smoothing_factor", 0.8)
        
    def _smooth_box(self, track_id: int, new_box: np.ndarray) -> np.ndarray:
        """Applies Exponential Moving Average (EMA) to smooth the bounding box."""
        if track_id not in self.tracks:
            return new_box
            
        history = self.tracks[track_id]["history"]
        if not history:
            return new_box
            
        last_box = history[-1]
        alpha = self.smoothing_factor
        smoothed_box = (alpha * new_box) + ((1 - alpha) * last_box)
        return smoothed_box

    def update(self, boxes: np.ndarray, track_ids: np.ndarray, class_ids: np.ndarray, frame_id: int):
        """
        Updates the tracker state with new detections for the current frame.
        Usually called after YOLO tracker parses the frame.
        """
        smoothed_boxes = []
        
        for box, t_id, cls_id in zip(boxes, track_ids, class_ids):
            t_id = int(t_id)
            
            # Apply smoothing
            smooth_b = self._smooth_box(t_id, box)
            smoothed_boxes.append(smooth_b)
            
            # Store history
            if t_id not in self.tracks:
                self.tracks[t_id] = {"history": [], "class_id": int(cls_id), "frames": []}
                
            self.tracks[t_id]["history"].append(smooth_b)
            self.tracks[t_id]["frames"].append(frame_id)
            
        return np.array(smoothed_boxes) if smoothed_boxes else np.array([])
        
    def get_trajectory(self, track_id: int) -> List[np.ndarray]:
        """Returns the full smoothed trajectory for a specific track ID."""
        if track_id in self.tracks:
            return self.tracks[track_id]["history"]
        return []

    def export_csv(self, output_path: str):
        """Exports the entire tracking history to a CSV file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        headers = ["frame_id", "track_id", "class_id", "x1", "y1", "x2", "y2"]
        
        rows = []
        for t_id, data in self.tracks.items():
            cls_id = data["class_id"]
            for frame_id, box in zip(data["frames"], data["history"]):
                row = [frame_id, t_id, cls_id, box[0], box[1], box[2], box[3]]
                rows.append(row)
                
        # Sort by frame_id then track_id
        rows.sort(key=lambda x: (x[0], x[1]))
        
        with open(path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
            
        logger.info(f"Exported tracking history ({len(rows)} rows) to {output_path}")
