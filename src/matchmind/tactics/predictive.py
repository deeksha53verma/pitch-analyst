import json
import numpy as np
from pathlib import Path

class PredictiveEngine:
    """Predictive Intelligence Layer: Pass Success, Loss Risk, and Dangerous Zones."""
    def __init__(self):
        self.history = []
        
    def predict(self, frame_idx, state_engine, player_data, ball_pitch):
        if not ball_pitch or state_engine.state == "Free":
            return
            
        carrier_team = state_engine.current_team
        carrier_id = state_engine.current_player
        
        # 1. Pass Success Likelihood (Heuristic)
        teammate_dists = []
        opponent_dists = []
        
        for pid, data in player_data.items():
            if pid == carrier_id: continue
            dist = np.hypot(data["x"] - ball_pitch[0], data["y"] - ball_pitch[1])
            if data["team"] == carrier_team:
                teammate_dists.append(dist)
            else:
                opponent_dists.append(dist)
                
        # Base probability
        pass_success = 50.0 
        if len(teammate_dists) > 0 and len(opponent_dists) > 0:
            avg_tm_dist = np.mean(sorted(teammate_dists)[:3]) if len(teammate_dists) >= 3 else np.mean(teammate_dists)
            avg_opp_dist = np.mean(sorted(opponent_dists)[:3]) if len(opponent_dists) >= 3 else np.mean(opponent_dists)
            
            # If opponents are closer than teammates, pass success drops
            pressure_ratio = avg_tm_dist / (avg_opp_dist + 1e-5) 
            pass_success = 100.0 - (pressure_ratio * 30.0)
            
        pass_success = np.clip(pass_success, 15.0, 95.0)
        
        # 2. Possession Loss Risk
        loss_risk = 20.0
        if state_engine.state == "Contesting":
            loss_risk = 80.0
        elif state_engine.state == "Receiving":
            loss_risk = 45.0
        
        # Increase risk based on close opponents
        close_opps = sum(1 for d in opponent_dists if d < 4.0)
        loss_risk += close_opps * 15.0
        loss_risk = np.clip(loss_risk, 5.0, 99.0)
        
        # 3. Dangerous Phase Probability
        danger_prob = 10.0
        if ball_pitch[0] > 70.0:
            danger_prob = 40.0 + (ball_pitch[0] - 70.0) * 1.5
            if loss_risk > 60:
                danger_prob -= 30.0
                
        danger_prob = np.clip(danger_prob, 5.0, 95.0)
        
        # Sample every 15 frames
        if frame_idx % 15 == 0:
            self.history.append({
                "frame": frame_idx,
                "team": int(carrier_team),
                "pass_success": float(pass_success),
                "loss_risk": float(loss_risk),
                "danger_prob": float(danger_prob)
            })
            
    def export(self, out_dir):
        path = Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "predictive.json", "w") as f:
            json.dump(self.history, f, indent=4)
