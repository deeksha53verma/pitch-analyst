import cv2
import numpy as np

class VideoAnnotator:
    def __init__(self):
        pass
        
    def draw_player(self, frame: np.ndarray, box: list, identity_str: str, has_possession: bool) -> np.ndarray:
        """Draws bounding box, identity label, and possession indicator."""
        x1, y1, x2, y2 = [int(v) for v in box]
        
        # Team colors (Team 0 = Red, Team 1 = Blue)
        color = (0, 0, 255) if "Team_0" in identity_str else (255, 0, 0)
        if "Unknown" in identity_str:
            color = (128, 128, 128)
            
        # Draw Box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Draw Label
        cv2.putText(frame, identity_str, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw Possession Indicator (Glowing Yellow circle under feet)
        if has_possession:
            center_x = (x1 + x2) // 2
            cv2.ellipse(frame, (center_x, y2), (int((x2-x1)*0.6), 10), 0, 0, 360, (0, 255, 255), -1)
            
        return frame
        
    def draw_ball(self, frame: np.ndarray, box: list) -> np.ndarray:
        """Draws a tiny yellow box for the ball."""
        if box is not None:
            x1, y1, x2, y2 = [int(v) for v in box]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, "Ball", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        return frame
