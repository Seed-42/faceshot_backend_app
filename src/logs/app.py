import logging

from config.app import APP_LOG_FORMAT, APP_LOG_PATH, APP_LOG_LEVEL

logFormatter = logging.Formatter(APP_LOG_FORMAT)
logger = logging.getLogger("faceshot_backend")
logger.setLevel(APP_LOG_LEVEL)

fileHandler = logging.FileHandler("{0}/{1}.log".format(APP_LOG_PATH, "faceshot_backend_app"))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
