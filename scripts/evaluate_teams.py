import os
import sys
import numpy as np
sys.path.append(os.path.abspath("src")) # type: ignore

from matchmind.core.config import load_config # type: ignore
from matchmind.classification.color import TeamClassifier # type: ignore
from matchmind.core.logger import logger # type: ignore

def main():
    logger.info("Initializing Team Classification Evaluation...")
    cfg = load_config(config_name="main")
    
    classifier = TeamClassifier(cfg)
    
    # Simulate a pipeline processing 25 crops (20 to trigger init, 5 for inference)
    # Let's say Team A wears Red, Team B wears Blue
    red_crop = np.zeros((50, 50, 3), dtype=np.uint8)
    red_crop[:] = [0, 0, 255] # Red in BGR
    
    blue_crop = np.zeros((50, 50, 3), dtype=np.uint8)
    blue_crop[:] = [255, 0, 0] # Blue in BGR
    
    logger.info("Feeding dummy crops into the classifier initialization pool...")
    for i in range(10):
        classifier.predict_team(track_id=1, crop=red_crop)  # Player 1 (Red)
        classifier.predict_team(track_id=2, crop=blue_crop) # Player 2 (Blue)
        
    # By now (20 crops), teams are initialized.
    logger.success("Initialization triggered!")
    
    # Prime the temporal smoothing window (history length = 5)
    logger.info("Priming temporal history...")
    for _ in range(5):
        classifier.predict_team(track_id=1, crop=red_crop)
        classifier.predict_team(track_id=2, crop=blue_crop)
        
    t1, c1 = classifier.predict_team(track_id=1, crop=red_crop)
    logger.info(f"Player 1 (Red crop) -> Assigned Team {t1} with confidence {c1:.2f}")
    
    t2, c2 = classifier.predict_team(track_id=2, crop=blue_crop)
    logger.info(f"Player 2 (Blue crop) -> Assigned Team {t2} with confidence {c2:.2f}")
    
    # Test temporal smoothing: Player 1 momentarily turns blue (e.g. occlusion)
    t1_smooth, c1_smooth = classifier.predict_team(track_id=1, crop=blue_crop)
    logger.warning("Simulated 1-frame anomaly where Player 1 crop became Blue...")
    logger.info(f"Player 1 (Blue anomaly) -> Assigned Team {t1_smooth} with confidence {c1_smooth:.2f}")
    
    if t1_smooth == t1:
        logger.success("Temporal Smoothing working correctly! Ignored the anomaly.")
    else:
        logger.error("Temporal Smoothing failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
