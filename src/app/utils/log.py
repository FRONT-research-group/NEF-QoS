import logging

def get_app_logger():
    """
    Set up and return the application logger with debug support.
    """
    logger = logging.getLogger('nef_logger')
    
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)  # Allow all log levels from DEBUG and above

        # Define log format
        formatter = logging.Formatter(
            '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S'
        )

        # Console stream handler for DEBUG and above
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)  # Show debug logs in console too
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
