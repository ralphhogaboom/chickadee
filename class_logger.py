import logging
from datetime import datetime


logging.basicConfig(filename="chickadee.log", level=logging.DEBUG)
logger = logging.getLogger('spam')

logger.info("App started: " + str(datetime.now()))

