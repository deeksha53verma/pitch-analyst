import sys
from loguru import logger # pyrefly: ignore [missing-import]

def setup_logger(level: str = "INFO", log_file: str = None):
    """
    Configure the Loguru logger for the MatchMind project.
    
    Args:
        level (str): Logging level (e.g., 'INFO', 'DEBUG', 'WARNING').
        log_file (str, optional): Path to save the log file.
    """
    logger.remove()  # Remove default handler
    
    # Add console handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        enqueue=True
    )
    
    # Add file handler if specified
    if log_file:
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=level,
            rotation="10 MB",
            retention="1 week",
            enqueue=True
        )
    
    logger.debug("Logger initialized successfully.")
    return logger
