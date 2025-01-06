"""Configures a logger for console and file logging."""
import logging


def configure_logging(logger_name: str = 'default'):
    """Sets up some basic logging for debugging and console output.

    Args:
        logger_name (str): Name for the logger

    Returns:
        Logger: Logger to use for logging
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel('DEBUG')

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('logging.log')
    c_handler.setLevel('DEBUG')
    f_handler.setLevel('DEBUG')

    # Create formatters and add it to the handlers
    c_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s: %(message)s')
    f_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s: %(name)s: %(message)s')
    c_handler.setFormatter(c_formatter)
    f_handler.setFormatter(f_formatter)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger
