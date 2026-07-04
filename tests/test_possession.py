import pytest
import numpy as np
from omegaconf import OmegaConf

from matchmind.possession.engine import PossessionEngine # type: ignore

@pytest.fixture
def mock_poss_cfg():
    return OmegaConf.create({
        "possession": {
            "params": {
                "max_possession_distance": 50.0,
                "temporal_window": 3
            }
        }
    })

def test_distance_calculation(mock_poss_cfg):
    engine = PossessionEngine(mock_poss_cfg)
    
    # Ball is at (50, 50), box center is (50, 50)
    ball_box = np.array([45, 45, 55, 55])
    
    # Player 1 feet are at (50, 60), dist = 10
    players = {
        1: {"box": np.array([40, 20, 60, 60]), "team_id": 0}
    }
    
    engine.update(1, ball_box, players)
    
    # The history should record team 0
    assert engine._history[-1] == 0

def test_temporal_smoothing(mock_poss_cfg):
    engine = PossessionEngine(mock_poss_cfg)
    
    ball_box = np.array([45, 45, 55, 55])
    players_a = { 1: {"box": np.array([40, 20, 60, 60]), "team_id": 0} } # Close to ball
    players_b = { 2: {"box": np.array([40, 20, 60, 60]), "team_id": 1} } # Close to ball
    
    # Frame 1: Team 0
    engine.update(1, ball_box, players_a)
    assert engine._current_possession == 0
    
    # Frame 2: Team 0
    engine.update(2, ball_box, players_a)
    assert engine._current_possession == 0
    
    # Frame 3: Team 1 (Deflection!)
    engine.update(3, ball_box, players_b)
    # The history is [0, 0, 1]. Smooth possession should still be 0!
    assert engine._current_possession == 0
    
    # Frame 4: Team 1
    engine.update(4, ball_box, players_b)
    # History [0, 1, 1]. Switch occurs!
    assert engine._current_possession == 1

def test_percentages(mock_poss_cfg):
    engine = PossessionEngine(mock_poss_cfg)
    
    # Simulate 3 frames for Team 0, 1 frame for Team 1
    engine.team_frames[0] = 3
    engine.team_frames[1] = 1
    
    pcts = engine.get_percentages()
    assert pcts[0] == 75.0
    assert pcts[1] == 25.0
