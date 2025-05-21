from loguru import logger
import sys

logger.remove()  # видаляємо стандартний хендлер
logger.add(sys.stdout, level="INFO", colorize=True,
           format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
logger.add("logs/runtime.log", rotation="1 week", compression="zip", level="DEBUG")