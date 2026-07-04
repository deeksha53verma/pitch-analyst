import json
import csv
from pathlib import Path
from typing import Dict, Any, Optional
from matchmind.core.logger import logger

class IdentityEngine:
    def __init__(self):
        # Master Dictionary
        # { track_id: {"team_id": int, "jersey_number": str or None} }
        self.players: Dict[int, Dict[str, Any]] = {}
        
    def update(self, track_id: int, team_id: int, jersey_number: Optional[str]):
        """
        Dynamically updates the master database for a given track_id.
        Allows temporal voting systems to continuously overwrite data as it stabilizes.
        """
        if track_id not in self.players:
            self.players[track_id] = {"team_id": team_id, "jersey_number": jersey_number}
        else:
            # Update team if not -1 (Unknown during init)
            if team_id != -1:
                self.players[track_id]["team_id"] = team_id
                
            # Update jersey if not None
            if jersey_number is not None:
                self.players[track_id]["jersey_number"] = jersey_number
                
    def get_identity(self, track_id: int) -> str:
        """Resolves a track_id to a human readable identity string."""
        if track_id not in self.players:
            return f"Unknown_{track_id}"
            
        data = self.players[track_id]
        team_str = f"Team_{data['team_id']}" if data['team_id'] != -1 else "Team_Unknown"
        jersey_str = data['jersey_number'] if data['jersey_number'] else "Unknown"
        
        return f"{team_str}_{jersey_str}"
        
    def export_identities(self, out_dir: str):
        """Exports the master database to CSV and JSON."""
        path = Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        
        # CSV Dump
        csv_path = path / "identities.csv"
        with open(csv_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["track_id", "team_id", "jersey_number", "full_identity"])
            for t_id, data in self.players.items():
                writer.writerow([t_id, data['team_id'], data['jersey_number'], self.get_identity(t_id)])
        logger.info(f"Exported identities to {csv_path}")
                
        # JSON Dump
        json_path = path / "identities.json"
        with open(json_path, mode='w') as f:
            json.dump(self.players, f, indent=4)
        logger.info(f"Exported identities to {json_path}")
            
    def export_statistics(self, out_dir: str):
        """Calculates and exports team statistics."""
        path = Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        
        stats = {
            "total_players_tracked": len(self.players),
            "team_counts": {},
            "identified_jerseys": 0,
            "unidentified_jerseys": 0
        }
        
        for data in self.players.values():
            t_id = str(data['team_id'])
            stats["team_counts"][t_id] = stats["team_counts"].get(t_id, 0) + 1
            
            if data['jersey_number']:
                stats["identified_jerseys"] += 1
            else:
                stats["unidentified_jerseys"] += 1
                
        stats_path = path / "statistics.json"
        with open(stats_path, mode='w') as f:
            json.dump(stats, f, indent=4)
            
        logger.info(f"Exported match statistics to {stats_path}")
