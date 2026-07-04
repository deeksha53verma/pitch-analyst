import json
import numpy as np
from pathlib import Path
from collections import deque

class CounterattackEngine:
    """Module 13: Counterattack Detection"""
    def __init__(self, speed_threshold=5.0):
        self.speed_threshold = speed_threshold # m/s
        self.counterattacks = []
        
        self.active_team = None
        self.recent_x = deque(maxlen=5) # track last 5 frames of ball X
        
    def update(self, frame_id: int, team_id: int, ball_x: float, players_bev: dict, fps=30):
        if team_id == -1:
            return
            
        if self.active_team != team_id:
            self.active_team = team_id
            self.recent_x.clear()
            
        self.recent_x.append(ball_x)
        
        if len(self.recent_x) == 5:
            # Calculate speed over 5 frames (approx 1/6th of a sec at 30fps)
            dx = abs(self.recent_x[-1] - self.recent_x[0])
            dt = 5.0 / fps
            speed = dx / dt
            
            if speed > self.speed_threshold:
                # High forward speed -> Transition
                support_runners = 0
                for p_id, p_pos in players_bev.items():
                    # Simplified logic: count players of same team in attacking half
                    if p_pos["team"] == team_id and (p_pos["x"] > 52.5 if team_id == 0 else p_pos["x"] < 52.5):
                        support_runners += 1
                        
                self.counterattacks.append({
                    "frame": frame_id,
                    "team": team_id,
                    "speed_ms": float(speed),
                    "support_runners": support_runners
                })
                # Clear to avoid duplicate logging of same sprint
                self.recent_x.clear()
                
    def export(self, out_dir: str):
        path = Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "counterattacks.json", "w") as f:
            json.dump(self.counterattacks, f, indent=4)
