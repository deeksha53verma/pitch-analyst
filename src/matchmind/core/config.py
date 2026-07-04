import os
from pathlib import Path
from omegaconf import DictConfig, OmegaConf # pyrefly: ignore [missing-import]
import hydra # pyrefly: ignore [missing-import]
from matchmind.core.logger import logger

def load_config(config_path: str = "../../../configs", config_name: str = "main") -> DictConfig:
    """
    Load Hydra configuration manually (useful for notebooks or non-hydra entrypoints).
    
    Args:
        config_path (str): Relative path to the configs directory.
        config_name (str): Name of the YAML config file (without extension).
        
    Returns:
        DictConfig: The loaded OmegaConf dictionary.
    """
    try:
        with hydra.initialize(version_base=None, config_path=config_path):
            cfg = hydra.compose(config_name=config_name)
            logger.info(f"Loaded configuration '{config_name}' successfully.")
            return cfg
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise

def print_config(cfg: DictConfig):
    """
    Print the configuration nicely.
    """
    yaml_cfg = OmegaConf.to_yaml(cfg)
    logger.info(f"Current Configuration:\n{yaml_cfg}")
