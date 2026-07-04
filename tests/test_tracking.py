import os
import pytest
import numpy as np
from omegaconf import OmegaConf

from matchmind.tracking.bytetrack import MatchTracker # type: ignore

@pytest.fixture
def mock_tracker_cfg():
    return OmegaConf.create({
        "tracker": {
            "params": {
                "track_thresh": 0.25,
                "track_buffer": 30,
                "match_thresh": 0.8,
                "smoothing_factor": 0.5,
                "min_hits": 3
            }
        }
    })

def test_tracker_initialization(mock_tracker_cfg):
    tracker = MatchTracker(mock_tracker_cfg)
    assert tracker.smoothing_factor == 0.5
    assert len(tracker.tracks) == 0

def test_tracker_update_and_smoothing(mock_tracker_cfg):
    tracker = MatchTracker(mock_tracker_cfg)
    
    # Frame 1: Initial Detection
    boxes_f1 = np.array([[10.0, 10.0, 50.0, 50.0]])
    track_ids_f1 = np.array([1])
    class_ids_f1 = np.array([0])
    
    smoothed_f1 = tracker.update(boxes_f1, track_ids_f1, class_ids_f1, frame_id=1)
    assert np.allclose(smoothed_f1, boxes_f1), "First frame should not be smoothed"
    
    # Frame 2: Jitter Detection (moves by 10 pixels)
    # EMA with 0.5 factor -> expected = (0.5 * 20) + (0.5 * 10) = 15
    boxes_f2 = np.array([[20.0, 20.0, 60.0, 60.0]])
    
    smoothed_f2 = tracker.update(boxes_f2, track_ids_f1, class_ids_f1, frame_id=2)
    expected_box = np.array([[15.0, 15.0, 55.0, 55.0]])
    assert np.allclose(smoothed_f2, expected_box)
    
    # Check history
    traj = tracker.get_trajectory(1)
    assert len(traj) == 2

def test_csv_export(mock_tracker_cfg, tmp_path):
    tracker = MatchTracker(mock_tracker_cfg)
    
    boxes = np.array([[10.0, 10.0, 50.0, 50.0]])
    t_ids = np.array([1])
    c_ids = np.array([0])
    
    tracker.update(boxes, t_ids, c_ids, frame_id=1)
    
    export_path = tmp_path / "tracking_export.csv"
    tracker.export_csv(str(export_path))
    
    assert export_path.exists()
    with open(export_path, "r") as f:
        lines = f.readlines()
        assert len(lines) == 2 # Header + 1 data row
        assert "frame_id,track_id,class_id,x1,y1,x2,y2" in lines[0]
        assert "1,1,0,10.0,10.0,50.0,50.0" in lines[1]
