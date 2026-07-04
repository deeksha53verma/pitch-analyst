import json
import csv
from pathlib import Path
from typing import Dict, Any, List, Set
from matchmind.core.logger import logger

class BuildUpEngine:
    """Module 10: Attack Build-up Detection"""
    def __init__(self, thirds_config: dict):
        self.thirds = thirds_config
        self.sequences = []
        self.active_seq = None
        
    def _get_third(self, x: float) -> str:
        if x <= self.thirds["defensive"]: return "Defensive"
        if x <= self.thirds["middle"]: return "Middle"
        return "Attacking"
        
    def update(self, frame_id: int, team_id: int, player_id: int, ball_x: float):
        if team_id == -1:
            return
            
        if self.active_seq is None or self.active_seq["team"] != team_id:
            # Close old sequence
            if self.active_seq is not None:
                self._close_sequence()
                
            # Start new
            self.active_seq = {
                "team": team_id,
                "start_frame": frame_id,
                "end_frame": frame_id,
                "start_x": ball_x,
                "end_x": ball_x,
                "players_involved": {player_id} if player_id is not None else set()
            }
        else:
            # Update existing
            self.active_seq["end_frame"] = frame_id
            self.active_seq["end_x"] = ball_x
            if player_id is not None:
                self.active_seq["players_involved"].add(player_id)
                
    def _close_sequence(self):
        start_third = self._get_third(self.active_seq["start_x"])
        end_third = self._get_third(self.active_seq["end_x"])
        
        # Check forward progression
        progression = False
        if self.active_seq["team"] == 0:
            # Team 0 attacks left to right (0 -> 105)
            if self.active_seq["end_x"] - self.active_seq["start_x"] > 35.0:
                progression = True
        else:
            # Team 1 attacks right to left (105 -> 0)
            if self.active_seq["start_x"] - self.active_seq["end_x"] > 35.0:
                progression = True
                
        self.sequences.append({
            "team": self.active_seq["team"],
            "duration": self.active_seq["end_frame"] - self.active_seq["start_frame"],
            "players": list(self.active_seq["players_involved"]),
            "start_zone": start_third,
            "end_zone": end_third,
            "forward_progression": progression
        })
        self.active_seq = None
        
    def export(self, out_dir: str):
        if self.active_seq:
            self._close_sequence()
            
        path = Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        
        with open(path / "buildups.json", "w") as f:
            json.dump(self.sequences, f, indent=4)
