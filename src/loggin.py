import logging
import sys

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(f"Log/{name}.log", mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

logger = setup_custom_logger('BBP')
logger.info('This is a message!')

try:
 #Put code u wanna run here
  #run_my_stuff()
except:
    logger.exception('Got exception on main handler')
    raise
logger.error('Here is another')
logger.warning("Here is another")