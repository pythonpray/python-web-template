import sys

from loguru import logger


def init_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time} - {level} - {file}:{line} - {function} - {message}",
        colorize=True,
        enqueue=True,  # 支持异步
        level="INFO",
    )

    logger.add(
        "app.log",
        format="{time} - {level} - {file}:{line} - {function} - {message}",
        rotation="10 MB",
        retention="7 days",
        colorize=True,
        enqueue=True,
        level="DEBUG",
    )
    return logger


app_logger = init_logger()
