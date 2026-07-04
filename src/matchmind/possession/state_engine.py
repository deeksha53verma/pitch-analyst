import json
import numpy as np
from pathlib import Path

class PossessionStateEngine:
    """Infers granular ball states: Carrying, Receiving, Contesting, and Free."""
    def __init__(self, possession_radius=3.0, contest_radius=5.0):
        self.possession_radius = possession_radius # meters
        self.contest_radius = contest_radius
        self.current_team = -1
        self.current_player = -1
        self.state = "Free"
        self.history = []
        
    def update(self, frame_idx, player_data, ball_pitch):
        if not ball_pitch or not player_data:
            return
            
        closest_pid = -1
        closest_dist = float('inf')
        closest_team = -1
        
        opponents_near = 0
        teammates_near = 0
        
        for pid, data in player_data.items():
            dist = np.hypot(data["x"] - ball_pitch[0], data["y"] - ball_pitch[1])
            if dist < closest_dist:
                closest_dist = dist
                closest_pid = pid
                closest_team = data["team"]
                
        if closest_team != -1:
            for pid, data in player_data.items():
                if pid == closest_pid: continue
                dist = np.hypot(data["x"] - ball_pitch[0], data["y"] - ball_pitch[1])
                if dist < self.contest_radius:
                    if data["team"] == closest_team:
                        teammates_near += 1
                    else:
                        opponents_near += 1
                        
            new_state = "Free"
            if closest_dist < self.possession_radius:
                if opponents_near > 0:
                    new_state = "Contesting"
                else:
                    if self.current_player == closest_pid:
                        new_state = "Carrying"
                    else:
                        new_state = "Receiving"
            else:
                new_state = "Free"
                
            control_changed = (self.current_team != -1 and self.current_team != closest_team and new_state in ["Carrying", "Receiving"])
            
            if new_state in ["Carrying", "Receiving", "Contesting"]:
                self.current_team = closest_team
                self.current_player = closest_pid
                
            self.state = new_state
            
            # Record data every 15 frames or on key events
            if frame_idx % 15 == 0 or control_changed:
                self.history.append({
                    "frame": frame_idx,
                    "state": new_state,
                    "team": closest_team,
                    "player": int(closest_pid),
                    "control_changed": control_changed,
                    "closest_dist": float(closest_dist)
                })

    def export(self, out_dir):
        path = Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "possession_states.json", "w") as f:
            json.dump(self.history, f, indent=4)
