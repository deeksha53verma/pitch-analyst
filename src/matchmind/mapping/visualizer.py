import cv2
import numpy as np
from omegaconf import DictConfig

class PitchVisualizer:
    def __init__(self, config: DictConfig):
        self.config = config.mapping.params
        self.scale = self.config.get("scale_factor", 10.0)
        
        # Pixel dimensions
        self.w_px = int(self.config.get("pitch_length", 105.0) * self.scale)
        self.h_px = int(self.config.get("pitch_width", 68.0) * self.scale)
        
    def draw_pitch(self) -> np.ndarray:
        """Generates a blank 2D minimap with standard football markings."""
        # Create dark green pitch
        canvas = np.zeros((self.h_px, self.w_px, 3), dtype=np.uint8)
        canvas[:] = [34, 139, 34] # Forest Green in BGR
        
        # Colors & Line Thickness
        white = (255, 255, 255)
        thickness = 2
        
        # Outline (Sidelines and Goal lines)
        cv2.rectangle(canvas, (0, 0), (self.w_px, self.h_px), white, thickness)
        
        # Halfway Line
        mid_x = self.w_px // 2
        cv2.line(canvas, (mid_x, 0), (mid_x, self.h_px), white, thickness)
        
        # Center Circle (radius 9.15m)
        r_px = int(9.15 * self.scale)
        cv2.circle(canvas, (mid_x, self.h_px // 2), r_px, white, thickness)
        
        # Center Dot
        cv2.circle(canvas, (mid_x, self.h_px // 2), 4, white, -1)
        
        # Penalty Areas (16.5m x 40.32m)
        pa_len = int(16.5 * self.scale)
        pa_width = int(40.32 * self.scale)
        pa_y_start = (self.h_px - pa_width) // 2
        
        # Left PA
        cv2.rectangle(canvas, (0, pa_y_start), (pa_len, pa_y_start + pa_width), white, thickness)
        # Right PA
        cv2.rectangle(canvas, (self.w_px - pa_len, pa_y_start), (self.w_px, pa_y_start + pa_width), white, thickness)
        
        return canvas
        
    def plot_entities(self, canvas: np.ndarray, players: list, ball: tuple) -> np.ndarray:
        """
        Plots the transformed entities on the canvas.
        players = [(x_m, y_m, team_id), ...]
        ball = (x_m, y_m)
        """
        # Plot players
        for (x_m, y_m, team_id) in players:
            px_x = int(x_m * self.scale)
            px_y = int(y_m * self.scale)
            
            # Red for Team 0, Blue for Team 1
            color = (0, 0, 255) if team_id == 0 else (255, 0, 0)
            cv2.circle(canvas, (px_x, px_y), 6, color, -1)
            cv2.circle(canvas, (px_x, px_y), 6, (255,255,255), 1) # White border
            
        # Plot ball
        if ball is not None:
            bx, by = ball
            cv2.circle(canvas, (int(bx * self.scale), int(by * self.scale)), 4, (0, 255, 255), -1) # Yellow ball
            
        return canvas
