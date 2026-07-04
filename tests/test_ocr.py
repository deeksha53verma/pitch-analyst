import pytest
import numpy as np
from omegaconf import OmegaConf
from unittest.mock import patch, MagicMock

from matchmind.ocr.jersey import JerseyOCR # type: ignore

@pytest.fixture
def mock_ocr_cfg():
    return OmegaConf.create({
        "ocr": {
            "params": {
                "languages": ["en"],
                "use_gpu": False, # False for unit tests
                "confidence_threshold": 0.3,
                "temporal_window": 5,
                "torso_crop_ratio": [0.15, 0.60]
            }
        }
    })

# We patch easyocr.Reader so we don't actually download model weights during pytest
@patch("matchmind.ocr.jersey.easyocr.Reader")
def test_torso_extraction(mock_reader, mock_ocr_cfg):
    ocr = JerseyOCR(mock_ocr_cfg)
    
    # 100x100 fake crop
    crop = np.zeros((100, 100, 3), dtype=np.uint8)
    
    torso = ocr._extract_torso(crop)
    # 60 - 15 = 45 pixels height
    assert torso.shape == (45, 100, 3)

@patch("matchmind.ocr.jersey.easyocr.Reader")
def test_image_enhancement(mock_reader, mock_ocr_cfg):
    ocr = JerseyOCR(mock_ocr_cfg)
    crop = np.zeros((50, 50, 3), dtype=np.uint8)
    
    enhanced = ocr._enhance_image(crop)
    # Should be grayscale (2D)
    assert len(enhanced.shape) == 2
    assert enhanced.shape == (50, 50)

@patch("matchmind.ocr.jersey.easyocr.Reader")
def test_temporal_voting(mock_reader, mock_ocr_cfg):
    # Setup mock reader to return specific OCR hits
    mock_instance = MagicMock()
    mock_reader.return_value = mock_instance
    
    ocr = JerseyOCR(mock_ocr_cfg)
    crop = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Simulate Frame 1: Sees "10"
    mock_instance.readtext.return_value = [ (None, "10", 0.9) ]
    num, conf = ocr.predict_number(1, crop)
    assert num == "10"
    assert conf == 1.0 # 1/1
    
    # Simulate Frame 2: Sees "10"
    num, conf = ocr.predict_number(1, crop)
    assert num == "10"
    assert conf == 1.0 # 2/2
    
    # Simulate Frame 3: Sees "7" (Error!)
    mock_instance.readtext.return_value = [ (None, "7", 0.9) ]
    num, conf = ocr.predict_number(1, crop)
    
    # Voting should outvote "7" because "10" has 2 votes, "7" has 1
    assert num == "10"
    assert conf == 2/3
    
    # Simulate Frame 4: Sees nothing (None)
    mock_instance.readtext.return_value = []
    num, conf = ocr.predict_number(1, crop)
    
    # Voting ignores Nones in history length, so still 2x"10", 1x"7"
    assert num == "10"
    assert conf == 2/3
