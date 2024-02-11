import os
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging(log_directory="logs", log_file_name="latest.log", backup_count=5):
    """
    Sets up logging with TimedRotatingFileHandler.

    :param log_directory: Directory to store log files.
    :param log_file_name: Name of the log file.
    :param backup_count: Number of backup files to keep.
    """
    # Create a logger if not already created
    logger = logging.getLogger("ScriptLogger")
    if not logger.handlers:  # Check if logger has no handlers
        logger.setLevel(logging.DEBUG)  # Set the logging level

        # Define log format
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S')

        # Create log directory if it doesn't exist
        os.makedirs(log_directory, exist_ok=True)

        # Create a TimedRotatingFileHandler
        handler = TimedRotatingFileHandler(
            os.path.join(log_directory, log_file_name), 
            when="midnight", 
            interval=1, 
            backupCount=backup_count
        )
        handler.setFormatter(formatter)

        # Add handler to the logger
        logger.addHandler(handler)

    return logger
