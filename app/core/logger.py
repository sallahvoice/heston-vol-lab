import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


log_path = Path(__file__).parent.parent / "log.log"
log_path.parent.mkdir(parents=True, exist_ok=True)

def setup_logger(name: str = __name__):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = (
        False
    )

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=4 * 1024 * 1024,
            backupCount=4,
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler) 
        logger.addHandler(stream_handler) 
        
    return logger


def get_logger(name):
    return setup_logger(name)