import logging
import os

# Determine log directory based on environment
if os.path.exists('/.dockerenv'):
    log_directory = "/tmp/logs"  # Docker
else:
    log_directory = os.path.join(os.path.dirname(__file__), 'logs')  # Lokálně

# Create log directory if it doesn't exist
os.makedirs(log_directory, exist_ok=True)

# Logger setup
logger = logging.getLogger('WeatherApp')
logger.setLevel(logging.DEBUG)  # capture all levels

# Console handler (all logs)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# File handler (all logs in one file, safe for non-root)
file_path = os.path.join(log_directory, 'weather_app.log')
f_handler = logging.FileHandler(file_path)
f_handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(formatter)
f_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(c_handler)
logger.addHandler(f_handler)

# Example logs (for testing)
#logger.debug("Debugging information: This is a detailed trace of the application's behavior.")
#logger.info("Informational message: The application has started successfully.")
#logger.warning("Warning: The application is using a deprecated method.")
#logger.error("Error: An error occurred while trying to fetch weather data.")
#logger.critical("Critical error: Unable to connect to the weather API!")