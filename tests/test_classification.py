import pytest
import numpy as np
from omegaconf import OmegaConf

from matchmind.classification.color import TeamClassifier # type: ignore

@pytest.fixture
def mock_class_cfg():
    return OmegaConf.create({
        "classifier": {
            "params": {
                "kmeans_k": 2,
                "temporal_window": 3,
                "confidence_threshold": 0.6,
                "pitch_green_hsv": {
                    "lower": [35, 40, 40],
                    "upper": [85, 255, 255]
                }
            }
        }
    })

def test_dominant_color_extraction(mock_class_cfg):
    classifier = TeamClassifier(mock_class_cfg)
    
    # Create a 10x10 pure red crop
    red_crop = np.zeros((10, 10, 3), dtype=np.uint8)
    red_crop[:] = [0, 0, 255] # BGR
    
    dom_color = classifier.extract_dominant_color(red_crop)
    assert np.allclose(dom_color, [0, 0, 255])
    
def test_team_initialization(mock_class_cfg):
    classifier = TeamClassifier(mock_class_cfg)
    
    # Simulate 10 red players and 10 blue players
    for _ in range(10):
        classifier._initialization_pool.append(np.array([0, 0, 255]))
    for _ in range(10):
        classifier._initialization_pool.append(np.array([255, 0, 0]))
        
    classifier._initialize_teams()
    assert classifier.team_centroids is not None
    assert classifier.team_centroids.shape == (2, 3)

def test_temporal_smoothing(mock_class_cfg):
    classifier = TeamClassifier(mock_class_cfg)
    
    # Force centroids
    classifier.team_centroids = np.array([[0, 0, 255], [255, 0, 0]]) # A=Red, B=Blue
    
    red_crop = np.zeros((10, 10, 3), dtype=np.uint8)
    red_crop[:] = [0, 0, 255]
    
    blue_crop = np.zeros((10, 10, 3), dtype=np.uint8)
    blue_crop[:] = [255, 0, 0]
    
    # Frame 1: Red (Team 0)
    team, conf = classifier.predict_team(track_id=1, crop=red_crop)
    assert team == 0
    assert conf == 1.0
    
    # Frame 2: Red (Team 0)
    team, conf = classifier.predict_team(track_id=1, crop=red_crop)
    assert team == 0
    assert conf == 1.0
    
    # Frame 3: Noise (Blue). Smoothing should keep it Team 0 (2 votes Red, 1 vote Blue)
    team, conf = classifier.predict_team(track_id=1, crop=blue_crop)
    assert team == 0
    assert conf == 2/3 # 66% confidence
