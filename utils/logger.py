import logging

DEBUG = logging.DEBUG
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(threadName)s:%(module)s:[%(levelname)s]:%(message)s")
logger = logging.getLogger(__name__)
