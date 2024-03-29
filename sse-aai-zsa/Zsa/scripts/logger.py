import logging
import sys


def setup_custom_logger(name):
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s %(name)-40s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.FileHandler(f"logs/{name}.log", mode="w")
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger
