import cv2
import numpy as np
from typing import Dict, List, Tuple
from collections import deque
from omegaconf import DictConfig
from sklearn.cluster import KMeans # type: ignore
from matchmind.core.logger import logger

class TeamClassifier:
    def __init__(self, config: DictConfig):
        self.config = config.classifier.params
        self.kmeans_k = self.config.get("kmeans_k", 2)
        self.temporal_window = self.config.get("temporal_window", 5)
        self.conf_thresh = self.config.get("confidence_threshold", 0.6)
        
        lower_g = self.config.get("pitch_green_hsv", {}).get("lower", [35, 40, 40])
        upper_g = self.config.get("pitch_green_hsv", {}).get("upper", [85, 255, 255])
        self.lower_green = np.array(lower_g, dtype=np.uint8)
        self.upper_green = np.array(upper_g, dtype=np.uint8)
        
        # Tracking history: track_id -> deque of predicted Team IDs (0 or 1)
        self.history: Dict[int, deque] = {}
        
        # The true colors (BGR) for Team A (0) and Team B (1)
        self.team_centroids = None
        self._initialization_pool = []
        
    def extract_dominant_color(self, crop: np.ndarray) -> np.ndarray:
        """Extracts the dominant BGR color of the jersey, masking out the pitch."""
        if crop.size == 0:
            return np.array([0, 0, 0])
            
        # 1. Mask the pitch
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask_green = cv2.inRange(hsv, self.lower_green, self.upper_green)
        mask_not_green = cv2.bitwise_not(mask_green)
        
        # 2. Extract valid pixels
        valid_pixels = crop[mask_not_green > 0]
        
        if len(valid_pixels) < 10:
            # If the crop was basically all green or too small, fallback to center pixel
            h, w = crop.shape[:2]
            return crop[h//2, w//2]
            
        # 3. KMeans to find dominant color
        kmeans = KMeans(n_clusters=1, n_init=3, random_state=42)
        kmeans.fit(valid_pixels)
        return kmeans.cluster_centers_[0]
        
    def _initialize_teams(self):
        """Automatically assigns Team A and Team B based on initial detection pool."""
        if len(self._initialization_pool) < self.kmeans_k:
            logger.warning("Not enough players to initialize teams.")
            return
            
        data = np.array(self._initialization_pool)
        kmeans = KMeans(n_clusters=self.kmeans_k, n_init=10, random_state=42)
        kmeans.fit(data)
        
        self.team_centroids = kmeans.cluster_centers_
        logger.info(f"Initialized Team A Color: {self.team_centroids[0].astype(int)}")
        logger.info(f"Initialized Team B Color: {self.team_centroids[1].astype(int)}")
        
    def predict_team(self, track_id: int, crop: np.ndarray) -> Tuple[int, float]:
        """
        Predicts whether a player belongs to Team A (0) or Team B (1) with temporal smoothing.
        """
        color = self.extract_dominant_color(crop)
        
        if self.team_centroids is None:
            # We haven't locked in the team colors yet, store it
            self._initialization_pool.append(color)
            if len(self._initialization_pool) >= 20: # Wait for 20 detections
                self._initialize_teams()
            return -1, 0.0 # Unknown during init phase
            
        # Calculate Euclidean distance to Team A and Team B
        dist_a = np.linalg.norm(color - self.team_centroids[0])
        dist_b = np.linalg.norm(color - self.team_centroids[1])
        
        raw_team = 0 if dist_a < dist_b else 1
        raw_conf = 1.0 - (min(dist_a, dist_b) / (dist_a + dist_b + 1e-6))
        
        # Temporal Smoothing
        if track_id not in self.history:
            self.history[track_id] = deque(maxlen=self.temporal_window)
            
        self.history[track_id].append(raw_team)
        
        # Majority vote
        counts = np.bincount(self.history[track_id])
        smooth_team = int(np.argmax(counts))
        smooth_conf = float(counts[smooth_team] / len(self.history[track_id]))
        
        return smooth_team, smooth_conf
