import os
import sys
sys.path.append(os.path.abspath("src")) # type: ignore

from matchmind.core.config import load_config # type: ignore
from matchmind.data.manager import DatasetValidator # type: ignore
from matchmind.detection.yolo import YOLODetector # type: ignore
from matchmind.core.logger import logger # type: ignore

def main():
    logger.info("Initializing Safety-Locked Training Script...")
    cfg = load_config(config_name="main")
    
    # 1. Safety validation check
    logger.info("Running Dataset Validator...")
    validator = DatasetValidator(cfg)
    is_valid = validator.validate_all()
    
    if not is_valid:
        logger.error("CRITICAL: Dataset validation failed! Training is strictly locked.")
        sys.exit(1)
        
    logger.success("Validation passed! Unlocking training...")
    
    # 2. Proceed to training
    detector = YOLODetector(cfg)
    
    # Normally we would pass the actual data.yaml path for the dataset here
    target_data_yaml = cfg.datasets.football_players_detection.path + "/data.yaml"
    
    if not os.path.exists(target_data_yaml):
        logger.error(f"Cannot find data.yaml at {target_data_yaml}")
        sys.exit(1)
        
    # detector.train(target_data_yaml) 
    logger.warning("Training execution reached, but explicitly bypassed for safety in this module.")

if __name__ == "__main__":
    main()
