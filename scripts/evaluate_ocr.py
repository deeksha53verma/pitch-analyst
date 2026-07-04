import os
import sys
import numpy as np
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath("src")) # type: ignore

from matchmind.core.config import load_config # type: ignore
from matchmind.ocr.jersey import JerseyOCR # type: ignore
from matchmind.core.logger import logger # type: ignore

# We patch EasyOCR for the evaluation script to ensure it runs instantly without downloading gigabytes of weights
@patch("matchmind.ocr.jersey.easyocr.Reader")
def main(mock_reader):
    logger.info("Initializing Jersey OCR Evaluation...")
    cfg = load_config(config_name="main")
    
    mock_instance = MagicMock()
    mock_reader.return_value = mock_instance
    
    ocr = JerseyOCR(cfg)
    
    # 1. Simulating frames for Player 10
    logger.info("Evaluating Temporal Voting on Player Track #1...")
    
    fake_crop = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Frame 1: Perfect Read -> 10
    mock_instance.readtext.return_value = [(None, "10", 0.9)]
    num, conf = ocr.predict_number(track_id=1, crop=fake_crop)
    logger.info(f"Frame 1: Raw OCR saw '10' -> Voted: {num} (Conf: {conf:.2f})")
    
    # Frame 2: Missed Read -> None
    mock_instance.readtext.return_value = []
    num, conf = ocr.predict_number(track_id=1, crop=fake_crop)
    logger.info(f"Frame 2: Raw OCR saw NOTHING -> Voted: {num} (Conf: {conf:.2f})")
    
    # Frame 3: Motion Blur Error -> 7
    mock_instance.readtext.return_value = [(None, "7", 0.7)]
    num, conf = ocr.predict_number(track_id=1, crop=fake_crop)
    logger.warning("Simulated 1-frame anomaly where OCR misread a blurry '10' as '7'...")
    logger.info(f"Frame 3: Raw OCR saw '7' -> Voted: {num} (Conf: {conf:.2f})")
    
    if num == "10":
        logger.success("Temporal Voting successfully outvoted the anomaly!")
    else:
        logger.error("Temporal Voting failed!")
        sys.exit(1)
        
    logger.info("Outputting sample CSV format:")
    logger.info("frame_id, track_id, jersey_number, confidence")
    logger.info(f"3, 1, {num}, {conf:.2f}")

if __name__ == "__main__":
    main()
