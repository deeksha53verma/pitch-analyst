import json
import numpy as np
from pathlib import Path

class PositionalEngine:
    """Module 12: Player Positional Analysis"""
    def __init__(self, pitch_cfg: dict):
        self.thirds = pitch_cfg.get("thirds", {"defensive": 35.0, "middle": 70.0, "attacking": 105.0})
        self.channels = pitch_cfg.get("channels", {"left": 22.6, "center": 45.3, "right": 68.0})
        self.player_positions = {}
        
    def update(self, player_id: int, team_id: int, bev_x: float, bev_y: float):
        if player_id not in self.player_positions:
            self.player_positions[player_id] = {"team": team_id, "x": [], "y": []}
            
        self.player_positions[player_id]["x"].append(bev_x)
        self.player_positions[player_id]["y"].append(bev_y)
        
    def _estimate_role(self, mean_x, mean_y):
        # Basic logical role estimation
        x_zone = "Mid"
        if mean_x <= self.thirds["defensive"]: x_zone = "Def"
        elif mean_x > self.thirds["middle"]: x_zone = "Att"
        
        y_zone = "Center"
        if mean_y <= self.channels["left"]: y_zone = "Left Wing"
        elif mean_y > self.channels["center"]: y_zone = "Right Wing"
        
        return f"{x_zone} {y_zone}"
        
    def export(self, out_dir: str):
        reports = {}
        # Sort players by number of tracked frames (descending) to find the true core players
        sorted_players = sorted(self.player_positions.items(), key=lambda item: len(item[1]["x"]), reverse=True)
        
        # Cap at 22 players max (11 per team) to eliminate any remaining mid-length ghost tracks
        for p_id, data in sorted_players[:22]:
            if len(data["x"]) < 15: # Filter out short transient ID switches
                continue
            avg_x = float(np.mean(data["x"]))
            avg_y = float(np.mean(data["y"]))
            reports[p_id] = {
                "team": data["team"],
                "avg_x": avg_x,
                "avg_y": avg_y,
                "role": self._estimate_role(avg_x, avg_y)
            }
            
        path = Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "positional.json", "w") as f:
            json.dump(reports, f, indent=4)
