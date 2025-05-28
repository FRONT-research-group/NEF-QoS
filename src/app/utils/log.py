'''
Common utils module
'''

import logging



def get_app_logger():
    """
    Set up and return the application logger with log rotation.
    """

    logger = logging.getLogger('nef_logger')
    if not logger.hasHandlers(): 
        logger.setLevel(logging.DEBUG)

        # Define log format
        formatter = logging.Formatter(
            '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S')


        # Console stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
