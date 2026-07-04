import pytest
from pathlib import Path
from omegaconf import OmegaConf
from matchmind.data.manager import DatasetValidator

@pytest.fixture
def temp_datasets(tmp_path):
    """Create a temporary dataset structure for testing."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Fake YOLO
    yolo_dir = data_dir / "yolo_data"
    (yolo_dir / "train" / "images").mkdir(parents=True)
    (yolo_dir / "train" / "labels").mkdir(parents=True)
    
    # Fake Statsbomb
    sb_dir = data_dir / "statsbomb"
    (sb_dir / "data").mkdir(parents=True)
    
    # Fake SoccerNet
    sn_dir = data_dir / "soccernet"
    (sn_dir / "tracking").mkdir(parents=True)
    
    return data_dir

def test_validator_yolo(temp_datasets):
    cfg = OmegaConf.create({
        "datasets": {
            "mock_yolo": {
                "path": str(temp_datasets / "yolo_data"),
                "format": "yolo",
                "validate": True
            }
        }
    })
    validator = DatasetValidator(cfg)
    assert validator.validate_all() == True

def test_validator_statsbomb(temp_datasets):
    cfg = OmegaConf.create({
        "datasets": {
            "mock_sb": {
                "path": str(temp_datasets / "statsbomb"),
                "format": "json_events",
                "validate": True
            }
        }
    })
    validator = DatasetValidator(cfg)
    assert validator.validate_all() == True

def test_validator_missing_dir(temp_datasets):
    cfg = OmegaConf.create({
        "datasets": {
            "missing_ds": {
                "path": str(temp_datasets / "does_not_exist"),
                "format": "yolo",
                "validate": True
            }
        }
    })
    validator = DatasetValidator(cfg)
    assert validator.validate_all() == False
