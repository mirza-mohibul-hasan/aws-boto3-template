import os
import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level=os.getenv("LOG_LEVEL", "INFO"),
)

__all__ = ["logger"]
