import os
import sys
import numpy as np
sys.path.append(os.path.abspath("src")) # type: ignore

from matchmind.core.config import load_config # type: ignore
from matchmind.possession.engine import PossessionEngine # type: ignore
from matchmind.core.logger import logger # type: ignore

def main():
    logger.info("Initializing Possession Engine Evaluation...")
    cfg = load_config(config_name="main")
    engine = PossessionEngine(cfg)
    
    # Simulate ball at center (50, 50)
    ball_box = np.array([45, 45, 55, 55])
    
    # Team A player is right next to the ball
    players_a = { 1: {"box": np.array([40, 20, 60, 60]), "team_id": 0} }
    # Team B player is a bit further
    players_b = { 2: {"box": np.array([140, 120, 160, 160]), "team_id": 1} }
    # Both players near the ball, but B is closer now
    players_b_close = { 
        1: {"box": np.array([10, 10, 30, 30]), "team_id": 0},
        2: {"box": np.array([40, 20, 60, 60]), "team_id": 1} 
    }
    
    logger.info("Simulating Team A possessing the ball (Frames 1-10)...")
    for f in range(1, 11):
        engine.update(f, ball_box, players_a)
        
    logger.info("Simulating a Loose Ball / Pass (Frames 11-12)...")
    for f in range(11, 13):
        # Ball box exists, but no players are within the max_possession_distance (e.g. 100px)
        engine.update(f, ball_box, players_b)
        
    logger.warning("Simulating a 1-frame deflection by Team B (Frame 13)...")
    engine.update(13, ball_box, players_b_close)
    
    logger.info("Simulating Team A regaining possession (Frames 14-20)...")
    for f in range(14, 21):
        engine.update(f, ball_box, players_a)
        
    logger.success("Checking results!")
    
    # Expected: Team 0 (Team A) should have 100% of the active possession because the 1-frame 
    # deflection and the 2-frame loose ball do not count towards active possession percentages
    # OR Team A retained possession due to smoothing!
    
    pcts = engine.get_percentages()
    if pcts.get(0, 0) == 100.0:
        logger.success("Temporal Smoothing worked! Team A retained full statistical control.")
    else:
        logger.error(f"Failed. Percentages: {pcts}")
        sys.exit(1)
        
    out_dir = "outputs/evaluation/possession"
    logger.info(f"Exporting possession timeline to {out_dir}...")
    engine.export_timeline(out_dir)

if __name__ == "__main__":
    main()
