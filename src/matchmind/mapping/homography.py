import cv2
import numpy as np
from typing import Tuple, Optional
from omegaconf import DictConfig
from matchmind.core.logger import logger

class PitchMapper:
    def __init__(self, config: DictConfig):
        self.config = config.mapping.params
        
        self.length = self.config.get("pitch_length", 105.0)
        self.width = self.config.get("pitch_width", 68.0)
        self.scale = self.config.get("scale_factor", 10.0)
        
        # H matrix stores the transformation from camera space -> 2D Pitch Space
        self.H: Optional[np.ndarray] = None
        
    def compute_homography(self, src_pts: np.ndarray, dst_pts: np.ndarray):
        """
        Calculates the Homography matrix.
        src_pts: (N, 2) pixel coordinates from the video frame (e.g. pitch corners)
        dst_pts: (N, 2) physical coordinates on the 105x68 pitch
        """
        if len(src_pts) < 4 or len(dst_pts) < 4:
            logger.error("Homography requires at least 4 point pairs.")
            return
            
        # findHomography uses RANSAC to be robust to outliers
        self.H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        
    def transform_point(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        """Warps a single camera (x, y) point into the physical 2D pitch space (in meters)."""
        if self.H is None:
            return None
            
        pt = np.array([[[x, y]]], dtype=np.float32)
        transformed = cv2.perspectiveTransform(pt, self.H)
        
        out_x, out_y = transformed[0][0]
        
        # Clip to pitch bounds just in case mathematics throw them slightly out
        out_x = np.clip(out_x, 0.0, self.length)
        out_y = np.clip(out_y, 0.0, self.width)
        
        return float(out_x), float(out_y)
        
    def get_zone(self, pt: Tuple[float, float]) -> str:
        """Determines tactical thirds and channels."""
        x, y = pt
        
        # Thirds
        third = "Defensive"
        if x > self.config.thirds.defensive and x <= self.config.thirds.middle:
            third = "Middle"
        elif x > self.config.thirds.middle:
            third = "Attacking"
            
        # Channels
        channel = "Left"
        if y > self.config.channels.left and y <= self.config.channels.center:
            channel = "Center"
        elif y > self.config.channels.center:
            channel = "Right"
            
        return f"{third} Third, {channel} Channel"
