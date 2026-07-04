import numpy as np
import json
from scipy.spatial import ConvexHull # type: ignore
from pathlib import Path
from matchmind.core.logger import logger

class CompactnessEngine:
    """Module 11: Team Compactness Analysis"""
    def __init__(self):
        self.timeline = []
        
    def calculate_frame(self, frame_id: int, team_id: int, players_bev: list):
        """players_bev is a list of [x, y] coordinates for the team."""
        if len(players_bev) < 3:
            return # Need at least 3 points for a hull
            
        pts = np.array(players_bev)
        
        width = np.max(pts[:, 1]) - np.min(pts[:, 1])
        depth = np.max(pts[:, 0]) - np.min(pts[:, 0])
        
        hull = ConvexHull(pts)
        area = hull.volume # In 2D, volume is area
        
        centroid = np.mean(pts, axis=0)
        spread = np.mean([np.linalg.norm(p - centroid) for p in pts])
        
        self.timeline.append({
            "frame": frame_id,
            "team": team_id,
            "width": float(width),
            "depth": float(depth),
            "area": float(area),
            "spread": float(spread)
        })
        
    def export(self, out_dir: str):
        path = Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "compactness.json", "w") as f:
            json.dump(self.timeline, f, indent=4)
