import pytest # pyrefly: ignore [missing-import]
import os
from matchmind.core.logger import setup_logger, logger
from matchmind.core.config import load_config

def test_logger_initialization():
    """Test if logger initializes correctly."""
    test_logger = setup_logger(level="DEBUG")
    assert test_logger is not None
    # Log a test message
    test_logger.info("Test log message")

def test_load_config():
    """Test loading the main Hydra config."""
    # Since tests run from root or tests dir, we need to adjust path
    # Assuming tests are run from MatchMind root
    config_path = "../configs"
    try:
        cfg = load_config(config_path=config_path, config_name="main")
        assert cfg is not None
        assert "project" in cfg
        assert cfg.project.name == "MatchMind"
    except Exception as e:
        pytest.fail(f"Config loading failed with error: {e}")
