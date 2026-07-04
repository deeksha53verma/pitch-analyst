import pytest
import numpy as np
from omegaconf import OmegaConf

from matchmind.mapping.homography import PitchMapper # type: ignore

@pytest.fixture
def mock_map_cfg():
    return OmegaConf.create({
        "mapping": {
            "params": {
                "pitch_length": 105.0,
                "pitch_width": 68.0,
                "scale_factor": 10.0,
                "thirds": {
                    "defensive": 35.0,
                    "middle": 70.0,
                    "attacking": 105.0
                },
                "channels": {
                    "left": 22.6,
                    "center": 45.3,
                    "right": 68.0
                }
            }
        }
    })

def test_homography_calculation(mock_map_cfg):
    mapper = PitchMapper(mock_map_cfg)
    
    # Fake camera points forming a square
    src_pts = np.array([
        [0, 0],
        [100, 0],
        [100, 100],
        [0, 100]
    ], dtype=np.float32)
    
    # Map them directly to the 105x68 pitch
    dst_pts = np.array([
        [0, 0],
        [105, 0],
        [105, 68],
        [0, 68]
    ], dtype=np.float32)
    
    mapper.compute_homography(src_pts, dst_pts)
    assert mapper.H is not None
    assert mapper.H.shape == (3, 3)
    
    # Center of camera (50, 50) should map to center of pitch (52.5, 34)
    x, y = mapper.transform_point(50, 50)
    assert np.isclose(x, 52.5, atol=0.1)
    assert np.isclose(y, 34.0, atol=0.1)

def test_zoning(mock_map_cfg):
    mapper = PitchMapper(mock_map_cfg)
    
    # 20m x, 15m y -> Defensive, Left
    z1 = mapper.get_zone((20.0, 15.0))
    assert z1 == "Defensive Third, Left Channel"
    
    # 52.5m x, 34m y -> Middle, Center
    z2 = mapper.get_zone((52.5, 34.0))
    assert z2 == "Middle Third, Center Channel"
    
    # 90m x, 60m y -> Attacking, Right
    z3 = mapper.get_zone((90.0, 60.0))
    assert z3 == "Attacking Third, Right Channel"
