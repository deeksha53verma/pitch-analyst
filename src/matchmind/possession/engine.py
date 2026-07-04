import cv2
import csv
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import deque
from omegaconf import DictConfig
from matchmind.core.logger import logger

class PossessionEngine:
    def __init__(self, config: DictConfig):
        self.config = config.possession.params
        self.max_dist = self.config.get("max_possession_distance", 100.0)
        self.window_size = self.config.get("temporal_window", 5)
        
        # Timeline: list of dicts {"frame": int, "team": int or None, "player": int or None}
        self.timeline: List[Dict[str, Any]] = []
        
        # Sliding window for temporal smoothing (stores recent Team IDs)
        self._history = deque(maxlen=self.window_size)
        self._current_possession = None # -1 or None = Loose Ball, 0 = Team A, 1 = Team B
        
        # Statistical Tracking
        self.team_frames = {0: 0, 1: 0}
        
    def _get_center(self, box: np.ndarray) -> np.ndarray:
        """Returns the [x, y] center of a bounding box."""
        return np.array([(box[0] + box[2]) / 2, (box[1] + box[3]) / 2])
        
    def update(self, frame_id: int, ball_box: Optional[np.ndarray], players: Dict[int, Dict[str, Any]]):
        """
        Calculates distance from the ball to all players.
        players dict format: {track_id: {"box": [x1,y1,x2,y2], "team_id": int}}
        """
        if ball_box is None or not players:
            self._history.append(-1)
        else:
            ball_center = self._get_center(ball_box)
            
            min_dist = float('inf')
            nearest_player_id = None
            nearest_team_id = -1
            
            # Find nearest player to the ball
            for p_id, p_data in players.items():
                p_box = p_data["box"]
                p_team = p_data["team_id"]
                
                # Ignore players whose team is unknown (-1)
                if p_team == -1:
                    continue
                    
                # Calculate distance between ball center and player's feet (bottom center)
                p_feet = np.array([(p_box[0] + p_box[2]) / 2, p_box[3]])
                dist = np.linalg.norm(ball_center - p_feet)
                
                if dist < min_dist:
                    min_dist = float(dist)
                    nearest_player_id = p_id
                    nearest_team_id = p_team
                    
            # Check threshold
            if min_dist <= self.max_dist and nearest_player_id is not None:
                self._history.append(nearest_team_id)
            else:
                self._history.append(-1) # Loose ball
                
        # Apply Temporal Smoothing (Majority vote in the window)
        if len(self._history) > 0:
            counts = {0: 0, 1: 0, -1: 0}
            for team in self._history:
                counts[team] += 1
                
            smoothed_team = max(counts, key=counts.get) # type: ignore
            
            # If a switch occurs, log it
            if smoothed_team != self._current_possession and smoothed_team != -1:
                logger.info(f"Frame {frame_id}: Possession Switch -> Team {smoothed_team}")
                
            self._current_possession = smoothed_team
            
            if smoothed_team != -1:
                self.team_frames[smoothed_team] += 1
                
            self.timeline.append({
                "frame": frame_id,
                "team": smoothed_team,
                "nearest_player": nearest_player_id if smoothed_team != -1 else None
            })
            
    def get_percentages(self) -> Dict[int, float]:
        """Returns exact possession percentages."""
        total_controlled = self.team_frames[0] + self.team_frames[1]
        if total_controlled == 0:
            return {0: 0.0, 1: 0.0}
            
        return {
            0: round((self.team_frames[0] / total_controlled) * 100, 2),
            1: round((self.team_frames[1] / total_controlled) * 100, 2)
        }
        
    def export_timeline(self, out_dir: str):
        """Exports the full possession history to CSV."""
        path = Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        csv_path = path / "possession_timeline.csv"
        
        with open(csv_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["frame", "team_in_possession", "nearest_player_track_id"])
            for t in self.timeline:
                t_str = "Loose" if t["team"] == -1 else f"Team {t['team']}"
                p_str = t["nearest_player"] if t["nearest_player"] is not None else "None"
                writer.writerow([t["frame"], t_str, p_str])
                
        logger.info(f"Exported possession timeline to {csv_path}")
        
        # Print final summary
        pcts = self.get_percentages()
        logger.success(f"Final Possession: Team 0 ({pcts.get(0, 0)}%) - Team 1 ({pcts.get(1, 0)}%)")
