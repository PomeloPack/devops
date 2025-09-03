import logging
import os

# Define the base directory for logs
base_dir = os.path.dirname(os.path.abspath(__file__))  # backend/
parent_dir = os.path.dirname(base_dir)                 # project/
log_directory = os.path.join(parent_dir, 'logs')

# Create a logs directory if it doesn't exist
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Create a logger
logger = logging.getLogger('WeatherApp')
logger.setLevel(logging.DEBUG)  # Setting the minimum log level to DEBUG for comprehensive logging

# Create handlers with paths to the log files in the logs directory
c_handler = logging.StreamHandler()  # Console handler
f_handler = logging.FileHandler(os.path.join(log_directory, 'weather_app.log'))  # Main log file
w_handler = logging.FileHandler(os.path.join(log_directory, 'weather_app_warning.log'))  # Warning log file
e_handler = logging.FileHandler(os.path.join(log_directory, 'weather_app_error.log'))  # Error log file

# Set levels for handlers
c_handler.setLevel(logging.DEBUG)  # Log all levels to console
f_handler.setLevel(logging.DEBUG)  # Log all levels to the main log file
w_handler.setLevel(logging.WARNING)  # Only log warnings and above to warning log file
e_handler.setLevel(logging.ERROR)  # Only log errors and above to error log file

# Create formatters
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
w_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
e_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Assign formatters to handlers
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
w_handler.setFormatter(w_format)
e_handler.setFormatter(e_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.addHandler(w_handler)
logger.addHandler(e_handler)

# Example log messages for each level
logger.debug("Debugging information: This is a detailed trace of the application's behavior.")
logger.info("Informational message: The application has started successfully.")
logger.warning("Warning: The application is using a deprecated method.")
logger.error("Error: An error occurred while trying to fetch weather data.")
logger.critical("Critical error: Unable to connect to the weather API!")
