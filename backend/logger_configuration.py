import logging
import os
import sys
from pythonjsonlogger import jsonlogger
import uuid

# ID tracking
def get_request_id():
    return str(uuid.uuid4())

# Determine environment
IS_DOCKER = os.path.exists('/.dockerenv')

# Log directory locally
log_directory = "/tmp/logs" if IS_DOCKER else os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_directory, exist_ok=True)

# Logger setup
logger = logging.getLogger('WeatherApp')
logger.setLevel(logging.DEBUG)

formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s %(request_id)s %(method)s %(path)s %(status)s')

# Console handler
c_handler = logging.StreamHandler(sys.stdout)
c_handler.setLevel(logging.DEBUG)
c_handler.setFormatter(formatter)
logger.addHandler(c_handler)

# File handler (locally)
if not IS_DOCKER:
    file_path = os.path.join(log_directory, 'weather_app.json.log')
    f_handler = logging.FileHandler(file_path)
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(formatter)
    logger.addHandler(f_handler)

# Context helper
def log_request(level, message, **kwargs):
    context = {
        "request_id": kwargs.get("request_id", get_request_id()),
        "method": kwargs.get("method", ""),
        "path": kwargs.get("path", ""),
        "status": kwargs.get("status", "")
    }
    if level.lower() == "info":
        logger.info(message, extra=context)
    elif level.lower() == "debug":
        logger.debug(message, extra=context)
    elif level.lower() == "warning":
        logger.warning(message, extra=context)
    elif level.lower() == "error":
        logger.error(message, extra=context)
    elif level.lower() == "critical":
        logger.critical(message, extra=context)